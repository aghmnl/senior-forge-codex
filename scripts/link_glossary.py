#!/usr/bin/env python3
"""Cross-link glossary terms inside an article, and validate the result.

The linking rule of this repository is "link every occurrence of a concept that
already has its own entry" (see AGENTS.md). Doing that by hand, or with a chain
of independent substitutions, produces nested links: a rule matches text that a
previous rule already turned into a link. This script makes that impossible by
construction — every term lives in a single alternation and `re.sub` never
rescans its own replacement.

Surface forms come from two places:

  * the glossary itself — each entry's `title:` and `permalink:`, so a new entry
    is linkable the moment it exists;
  * `_data/glossary_aliases.yml` — only the forms a title cannot capture, such
    as "jerarquías selladas" for `sealed-hierarchy` or "heredar" for
    `inheritance`.

Usage:

    scripts/link_glossary.py terms --lang es
    scripts/link_glossary.py link es/02-coroutines-flow/error-handling.md \\
        --terms "Throwable,onEach,finally"
    scripts/link_glossary.py link es/.../article.md --all
    scripts/link_glossary.py check es/.../article.md en/.../article.md
    scripts/link_glossary.py check --all

`link` rewrites the file in place; `--dry-run` prints what it would do instead.
`check` runs three validations and exits non-zero on failure.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GLOSSARY_DIR = {"en": "_posts/en/glossary", "es": "_posts/es/glosario"}
URL_BASE = {"en": "/en/glossary/", "es": "/es/glosario/"}
ALIASES_FILE = "_data/glossary_aliases.yml"

# A link already present in the text. Kept verbatim so no term rule can reach
# inside it — this is what prevents nesting.
EXISTING_LINK = r"\[[^\]]*\]\(\{\{[^}]*\}\}\)"

# Lines that are never linked: front matter delimiters and fields, headings,
# and the "back to" footer.
SKIP_LINE = re.compile(r"^(---|#|\[Volver|\[Back|layout:|title:|lang:|permalink:|order:|date:|categories:|tags:)")


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #

def load_glossary(lang: str) -> dict[str, str]:
    """Return {slug: title} for every glossary entry of a language."""
    directory = os.path.join(ROOT, GLOSSARY_DIR[lang])
    entries: dict[str, str] = {}
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".md"):
            continue
        title = permalink = None
        with open(os.path.join(directory, name), encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip('"')
                elif line.startswith("permalink:"):
                    permalink = line.split(":", 1)[1].strip()
                elif line.startswith("---") and title and permalink:
                    break
        if title and permalink:
            entries[permalink.strip("/").split("/")[-1]] = title
    return entries


def load_aliases() -> dict[str, dict[str, list[str]]]:
    """Parse _data/glossary_aliases.yml.

    Deliberately a tiny parser for the one shape this file has, so the script
    stays dependency-free:

        slug:
          es: ["form", "other form"]
          en: ["form"]
    """
    path = os.path.join(ROOT, ALIASES_FILE)
    if not os.path.exists(path):
        return {}
    aliases: dict[str, dict[str, list[str]]] = {}
    slug = None
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            top = re.match(r"^([A-Za-z0-9-]+):\s*$", line)
            if top:
                slug = top.group(1)
                aliases.setdefault(slug, {})
                continue
            nested = re.match(r"^\s+(en|es):\s*\[(.*)\]\s*$", line)
            if nested and slug:
                aliases[slug][nested.group(1)] = re.findall(r'"([^"]*)"', nested.group(2))
    return aliases


# --------------------------------------------------------------------------- #
# Surface forms
# --------------------------------------------------------------------------- #

CODE_LIKE = re.compile(r"[^\w\s]")


def surface_forms(slug: str, title: str, lang: str, aliases: dict) -> list[str]:
    """Every string that should become a link to `slug`, longest first."""
    forms = {title}
    # "== (Structural Equality)" -> "=="   |   "Error (UI State)" -> "Error"
    stripped = re.sub(r"\s*\([^)]*\)\s*$", "", title).strip()
    if stripped:
        forms.add(stripped)
    forms.update(aliases.get(slug, {}).get(lang, []))
    return sorted((f for f in forms if f), key=len, reverse=True)


def form_to_regex(form: str) -> str:
    """Build the pattern for one surface form.

    A form made of word characters is matched both bare and inside a code span;
    anything containing punctuation (`as?`, `==`, `?: return`) is matched only
    inside a code span, because a bare `?:` in prose is usually not the term.

    Only the first letter is case-insensitive, so an entry titled "Coroutines"
    also matches "coroutines" at the start of a sentence — without matching an
    unrelated shout like "FLOW". The link keeps whatever casing the prose used.
    """
    escaped = re.escape(form)
    if form[:1].isalpha() and form[:1].lower() != form[:1].upper():
        first = f"[{form[0].upper()}{form[0].lower()}]"
        escaped = first + re.escape(form[1:])
    if CODE_LIKE.search(form):
        return rf"`{escaped}`"
    return rf"`{escaped}`|\b{escaped}\b"


# --------------------------------------------------------------------------- #
# Linking
# --------------------------------------------------------------------------- #

def build_linker(terms: list[tuple[str, str]], lang: str):
    """terms: [(surface form, slug)], most specific first.

    Returns a function that links one line. All terms share a single regex, so
    a replacement can never be re-matched by another term.
    """
    parts = [f"(?P<keep>{EXISTING_LINK})"]
    parts += [f"(?P<t{i}>{form_to_regex(form)})" for i, (form, _) in enumerate(terms)]
    pattern = re.compile("|".join(parts))
    base = URL_BASE[lang]

    def repl(match: re.Match) -> str:
        if match.lastgroup == "keep":
            return match.group(0)
        slug = terms[int(match.lastgroup[1:])][1]
        return f'[{match.group(0)}]({{{{ "{base}{slug}/" | relative_url }}}})'

    return lambda line: pattern.sub(repl, line)


def link_text(text: str, terms: list[tuple[str, str]], lang: str) -> tuple[str, int]:
    """Link every term outside code fences and skipped lines."""
    link_line = build_linker(terms, lang)
    out, in_code, changed = [], False, 0
    for line in text.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code or SKIP_LINE.match(line):
            out.append(line)
            continue
        linked = link_line(line)
        if linked != line:
            changed += 1
        out.append(linked)
    return "\n".join(out), changed


def collect_terms(lang: str, wanted: list[str] | None) -> list[tuple[str, str]]:
    glossary = load_glossary(lang)
    aliases = load_aliases()
    pairs: list[tuple[str, str]] = []
    unknown = list(wanted) if wanted else []
    for slug, title in glossary.items():
        forms = surface_forms(slug, title, lang, aliases)
        if wanted is not None:
            match = next((w for w in wanted if w == slug or w in forms), None)
            if match is None:
                continue
            if match in unknown:
                unknown.remove(match)
        pairs += [(form, slug) for form in forms]
    if unknown:
        sys.exit(f"unknown term(s): {', '.join(unknown)}\nRun `terms --lang {lang}` to list what is available.")
    # Longest surface form first: the alternation is leftmost-first, so
    # `as?` must be tried before `as`, `runtime-exception` before `runtime`.
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return pairs


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #

MALFORMED = [
    (re.compile(r"\[`\["), "nested link inside a code span"),
    (re.compile(r"\[\["), "double opening bracket"),
    (re.compile(r"relative_url \}\}\)\("), "link immediately followed by a stray ("),
    (re.compile(r"glossary/\[|glosario/\["), "link inside a URL"),
]


def all_articles() -> list[str]:
    """Every topic article, both languages — chapter folders only, no indexes."""
    found: list[str] = []
    for lang in ("en", "es"):
        for chapter in sorted(os.listdir(os.path.join(ROOT, lang))):
            directory = os.path.join(ROOT, lang, chapter)
            if not re.match(r"^\d\d-", chapter) or not os.path.isdir(directory):
                continue
            found += [
                f"{lang}/{chapter}/{name}"
                for name in sorted(os.listdir(directory))
                if name.endswith(".md") and name != "index.md"
            ]
    return found


def lang_of(path: str) -> str:
    return "en" if path.split(os.sep)[0] == "en" or "/en/" in path else "es"


def check_file(path: str) -> list[str]:
    problems: list[str] = []
    text = open(os.path.join(ROOT, path), encoding="utf-8").read()
    lang = lang_of(path)

    for pattern, label in MALFORMED:
        for number, line in enumerate(text.split("\n"), 1):
            if pattern.search(line):
                problems.append(f"{path}:{number}: {label}")

    directory = os.path.join(ROOT, GLOSSARY_DIR[lang])
    known = {
        name.split("-", 3)[-1][:-3]
        for name in os.listdir(directory)
        if name.endswith(".md")
    }
    for slug in sorted(set(re.findall(URL_BASE[lang] + r"([a-z0-9-]+)/", text))):
        if slug not in known:
            problems.append(f"{path}: link to unknown glossary entry '{slug}'")

    # Idempotency: linking twice must equal linking once. Comparing against the
    # original would only say "there are still unlinked terms", which is normal;
    # what must never happen is a second pass wrapping its own output, which is
    # exactly how a chained-substitution bug shows up.
    terms = collect_terms(lang, None)
    once, _ = link_text(text, terms, lang)
    twice, _ = link_text(once, terms, lang)
    if once != twice:
        first_diff = next(
            (n for n, (a, b) in enumerate(zip(once.split("\n"), twice.split("\n")), 1) if a != b),
            "?",
        )
        problems.append(f"{path}: not idempotent — a second linking pass changes line {first_diff}")
    return problems


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_terms = sub.add_parser("terms", help="list linkable surface forms")
    p_terms.add_argument("--lang", choices=["en", "es"], default="es")

    p_link = sub.add_parser("link", help="add glossary links to an article")
    p_link.add_argument("files", nargs="+")
    group = p_link.add_mutually_exclusive_group(required=True)
    group.add_argument("--terms", help="comma-separated terms or slugs to link")
    group.add_argument("--all", action="store_true", help="link every known term")
    p_link.add_argument("--dry-run", action="store_true")

    p_check = sub.add_parser("check", help="validate links in an article")
    p_check.add_argument("files", nargs="*")
    p_check.add_argument("--all", action="store_true", help="check every article in both languages")

    args = parser.parse_args()

    if args.command == "terms":
        for form, slug in collect_terms(args.lang, None):
            print(f"{form}\t{slug}")
        return 0

    if args.command == "link":
        wanted = None if args.all else [t.strip() for t in args.terms.split(",") if t.strip()]
        for path in args.files:
            lang = lang_of(path)
            full = os.path.join(ROOT, path)
            text = open(full, encoding="utf-8").read()
            linked, changed = link_text(text, collect_terms(lang, wanted), lang)
            if args.dry_run:
                print(f"{path}: would change {changed} line(s)")
                continue
            open(full, "w", encoding="utf-8").write(linked)
            counts: dict[str, int] = {}
            for slug in re.findall(URL_BASE[lang] + r"([a-z0-9-]+)/", linked):
                counts[slug] = counts.get(slug, 0) + 1
            print(f"{path}: {changed} line(s) changed, {sum(counts.values())} link(s) total")
        return 0

    files = all_articles() if args.all else args.files
    if not files:
        sys.exit("check: pass one or more files, or --all")
    problems = [p for path in files for p in check_file(path)]
    for problem in problems:
        print(problem)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
