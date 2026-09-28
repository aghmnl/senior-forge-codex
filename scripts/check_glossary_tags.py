#!/usr/bin/env python3
"""Validate glossary tags against the vocabulary in docs/GLOSSARY_TAGS.md.

The tag rules live in `docs/GLOSSARY_TAGS.md`; this script enforces them so the
vocabulary table cannot silently drift from the entries it describes.

Checks:

  * every EN entry has 2 to 4 tags, all from the vocabulary, without repeats;
  * its ES counterpart carries the same list in the same order;
  * the "Entries" column matches the real per-tag count, and the
    "Vocabulary (N tags)" heading matches the number of rows;
  * no tag applies to more than 40% of the entries;
  * every "Example entries" link exists and carries that tag;
  * every vocabulary tag has labels in `_data/glossary_tags.yml` and a page in
    `en/tags/` and `es/etiquetas/`, and nothing there is left over;
  * the "Tags" column of `docs/GLOSSARY_INDEX.md` matches the front matter.

Usage:

    scripts/check_glossary_tags.py            # validate, exit non-zero on failure
    scripts/check_glossary_tags.py --write    # rewrite the Entries column first

`--write` only refreshes the counts; every other problem still has to be fixed
by hand.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GLOSSARY_DIR = {"en": "_posts/en/glossary", "es": "_posts/es/glosario"}
TAG_PAGES_DIR = {"en": "en/tags", "es": "es/etiquetas"}
TAGS_DOC = "docs/GLOSSARY_TAGS.md"
INDEX_DOC = "docs/GLOSSARY_INDEX.md"
LABELS_FILE = "_data/glossary_tags.yml"

MIN_TAGS, MAX_TAGS = 2, 4
MAX_SHARE = 0.40

# | `tag` | meaning | 12 | [Name](../_posts/...), ... |
TABLE_ROW = re.compile(r"^\| `([a-z0-9-]+)` \|([^|]*)\|\s*(\d+)\s*\|(.*)\|\s*$")
VOCAB_HEADING = re.compile(r"^## Vocabulary \((\d+) tags\)$", re.M)
EXAMPLE_LINK = re.compile(r"\[([^\]]+)\]\(\.\./(_posts/[^)]+)\)")
INDEX_ROW = re.compile(r"/en/glossary/([a-z0-9-]+)/\).*\|([^|]*)\|\s*$")


def read(path: str) -> str:
    return open(os.path.join(ROOT, path), encoding="utf-8").read()


def front_matter(path: str) -> str:
    parts = read(path).split("---", 2)
    return parts[1] if len(parts) == 3 else ""


def parse_tags(path: str) -> list[str] | None:
    match = re.search(r"^tags:\s*\[(.*)\]\s*$", front_matter(path), re.M)
    if not match:
        return None
    return [t.strip() for t in match.group(1).split(",") if t.strip()]


def parse_slug(path: str) -> str | None:
    match = re.search(r"^permalink:\s*/en/glossary/([a-z0-9-]+)/", front_matter(path), re.M)
    return match.group(1) if match else None


def entries(lang: str) -> list[str]:
    directory = os.path.join(ROOT, GLOSSARY_DIR[lang])
    return sorted(os.path.join(GLOSSARY_DIR[lang], f) for f in os.listdir(directory) if f.endswith(".md"))


def load_vocabulary() -> dict[str, tuple[int, list[tuple[str, str]]]]:
    """Return {tag: (stated count, [(example name, example path)])} from the table."""
    vocab = {}
    for line in read(TAGS_DOC).splitlines():
        match = TABLE_ROW.match(line)
        if match:
            vocab[match.group(1)] = (int(match.group(3)), EXAMPLE_LINK.findall(match.group(4)))
    return vocab


def load_label_keys() -> set[str]:
    return set(re.findall(r"^([a-z0-9-]+):\s*$", read(LABELS_FILE), re.M))


def count_tags() -> tuple[Counter, dict[str, list[str]], list[str]]:
    """Validate every entry's tags; return (counts, {slug: tags}, problems)."""
    counts: Counter = Counter()
    by_slug: dict[str, list[str]] = {}
    problems: list[str] = []
    vocab = load_vocabulary()

    en_files = entries("en")
    es_names = {os.path.basename(p) for p in entries("es")}
    for name in sorted(es_names - {os.path.basename(p) for p in en_files}):
        problems.append(f"{GLOSSARY_DIR['es']}/{name}: no EN counterpart")

    for path in en_files:
        tags = parse_tags(path)
        if tags is None:
            problems.append(f"{path}: missing `tags: [...]` line")
            continue
        counts.update(tags)
        slug = parse_slug(path)
        if slug:
            by_slug[slug] = tags
        if not MIN_TAGS <= len(tags) <= MAX_TAGS:
            problems.append(f"{path}: {len(tags)} tags, expected {MIN_TAGS}-{MAX_TAGS}")
        if len(set(tags)) != len(tags):
            problems.append(f"{path}: repeated tag in {tags}")
        for tag in tags:
            if tag not in vocab:
                problems.append(f"{path}: `{tag}` is not in the vocabulary")

        es_path = os.path.join(GLOSSARY_DIR["es"], os.path.basename(path))
        if not os.path.exists(os.path.join(ROOT, es_path)):
            problems.append(f"{path}: no ES counterpart")
        elif parse_tags(es_path) != tags:
            problems.append(f"{es_path}: tags {parse_tags(es_path)} differ from EN {tags}")

    return counts, by_slug, problems


def check_table(counts: Counter, total: int) -> list[str]:
    problems = []
    vocab = load_vocabulary()
    heading = VOCAB_HEADING.search(read(TAGS_DOC))
    if not heading or int(heading.group(1)) != len(vocab):
        stated = heading.group(1) if heading else "missing"
        problems.append(f"{TAGS_DOC}: heading says {stated} tags, table has {len(vocab)}")

    for tag, (stated, examples) in vocab.items():
        if stated != counts[tag]:
            problems.append(f"{TAGS_DOC}: `{tag}` Entries is {stated}, actual {counts[tag]}")
        if total and counts[tag] / total > MAX_SHARE:
            problems.append(f"`{tag}` is on {counts[tag]}/{total} entries (> {MAX_SHARE:.0%})")
        for name, path in examples:
            if not os.path.exists(os.path.join(ROOT, path)):
                problems.append(f"{TAGS_DOC}: `{tag}` example {name} -> {path} does not exist")
            elif tag not in (parse_tags(path) or []):
                problems.append(f"{TAGS_DOC}: `{tag}` example {name} does not carry that tag")
    return problems


def check_labels_and_pages() -> list[str]:
    problems = []
    vocab = set(load_vocabulary())
    labels = load_label_keys()
    for tag in sorted(vocab - labels):
        problems.append(f"{LABELS_FILE}: no labels for `{tag}`")
    for tag in sorted(labels - vocab):
        problems.append(f"{LABELS_FILE}: `{tag}` is not in the vocabulary")
    for lang, directory in TAG_PAGES_DIR.items():
        pages = {}
        for name in os.listdir(os.path.join(ROOT, directory)):
            match = re.search(r"^tag:\s*(\S+)\s*$", front_matter(os.path.join(directory, name)), re.M)
            if match:
                pages[match.group(1)] = name
        for tag in sorted(vocab - set(pages)):
            problems.append(f"{directory}/: no page for `{tag}`")
        for tag in sorted(set(pages) - vocab):
            problems.append(f"{directory}/{pages[tag]}: `{tag}` is not in the vocabulary")
    return problems


def check_index(by_slug: dict[str, list[str]]) -> list[str]:
    problems = []
    seen = set()
    for line in read(INDEX_DOC).splitlines():
        match = INDEX_ROW.search(line)
        if not match:
            continue
        slug, cell = match.groups()
        seen.add(slug)
        listed = re.findall(r"`([a-z0-9-]+)`", cell)
        if slug in by_slug and listed != by_slug[slug]:
            problems.append(f"{INDEX_DOC}: `{slug}` lists {listed}, front matter has {by_slug[slug]}")
    for slug in sorted(set(by_slug) - seen):
        problems.append(f"{INDEX_DOC}: no row for `{slug}`")
    return problems


def write_counts(counts: Counter) -> int:
    """Rewrite the Entries column in place; return the number of rows changed."""
    changed = 0
    lines = read(TAGS_DOC).split("\n")
    for i, line in enumerate(lines):
        match = TABLE_ROW.match(line)
        if match and int(match.group(3)) != counts[match.group(1)]:
            start, end = match.span(3)
            lines[i] = line[:start] + str(counts[match.group(1)]) + line[end:]
            changed += 1
    with open(os.path.join(ROOT, TAGS_DOC), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true", help="refresh the Entries column before checking")
    args = parser.parse_args()

    counts, by_slug, problems = count_tags()
    if args.write:
        print(f"{TAGS_DOC}: {write_counts(counts)} count(s) updated")

    total = len(entries("en"))
    problems += check_table(counts, total)
    problems += check_labels_and_pages()
    problems += check_index(by_slug)
    for problem in problems:
        print(problem)
    print(f"OK ({total} entries, {len(load_vocabulary())} tags)" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
