# Senior Forge Codex — Project Rules

## Language

- All interaction with the user is in **Spanish** (castellano). Do not switch to English in conversation.
- Articles are written in **both English and Spanish** (bilingual).
- Documentation files (`docs/`, `evals/`, `CODEX_GUIDE.md`) are written in **English**.

## Key Documents

- `docs/TOPIC_TRACKER.md` — Master checklist of 100 topics with progress, dates, article links, and evaluation results.
- `docs/DAILY_WORKFLOW.md` — Defines the daily learning routine, weekly evaluation system, and spaced repetition logic.
- `evals/` — Weekly evaluation records (one markdown per week, named `YYYY-WNN.md`).
- `CODEX_GUIDE.md` — Article format, engineering standards, and content creation checklist.

## Workflow Reference

- Follow the daily routine defined in `docs/DAILY_WORKFLOW.md`.
- **ALWAYS use real code examples from FollowApp Suite** (`/Users/agus/Documents/Entorno/FollowApps/Android/Suite`). When writing or updating any article, search FAS for relevant usages FIRST — do not use generic/invented examples unless no match exists in FAS. If a topic is not found there, mark as "Not found in FAS" and use a standalone example. Each code snippet must include a `// From FollowApp Suite — FileName.kt` comment identifying its origin.
- After each topic, the learner answers the Interview Prep Q&A from memory as a daily self-evaluation.
- Weekly evaluations are cumulative and use spaced repetition (see `docs/DAILY_WORKFLOW.md`).

## Growing the Topic List

The initial 100 topics can grow. When a new concept emerges that is genuinely interview-worthy (not just a glossary term), it is added **inside the chapter section it belongs to** in `docs/TOPIC_TRACKER.md`, with a date appended at the end of the schedule. Update topic count and `Projected end date` in the summary.

- **Topic** → full article (EN + ES), planned date, evaluation, Interview Prep Q&A.
- **Glossary entry** → reference concept, no date or evaluation, cross-linked from main topics.

The distinction: if it could be asked as a standalone interview question with a "Senior Answer", it's a topic. If it's a supporting concept referenced by multiple topics, it's glossary.

## Glossary (Extra Topics)

Concepts that fall outside the 100 main topics are documented as **glossary entries**. The glossary has its own search and serves as a complementary reference.

- Glossary entries live in `_posts/en/glossary/` and `_posts/es/glosario/` (bilingual, layout: `post`).
- Permalink pattern: `/en/glossary/<slug>/` and `/es/glosario/<slug>/`.
- See `docs/GLOSSARY_INDEX.md` for the full inventory of entries with links and FAS coverage status.
- Format: same article structure (Theory, Senior Nuance, code if applicable), with a "Back to Glossary" link.
- **Cross-linking rule:** When writing or updating any article (topic or glossary), link **every occurrence** of a concept that already has its own article — whether it is another topic or a glossary entry. Do not link only the first mention; every time the term appears in the text, it must be a link. Use the Liquid `relative_url` filter: `[Garbage Collector]({{ "/en/glossary/garbage-collector/" | relative_url }})`, `[Data Objects]({{ "/en/01-kotlin-core/data-objects/" | relative_url }})`. This makes the Codex a connected knowledge base, not isolated pages.
- **Section headings — canonical set:**
  - **English topic articles:** `## The Theory (The What)` · `## The Senior Perspective (The Why)` · `## Code in Action` · `## The Interview (The Hot Seat)`
  - **Spanish topic articles:** `## The Theory (El Qué)` · `## The Senior Perspective (El Porqué)` · `## Code in Action` · `## The Interview (En el banquillo)`
  - **English glossary entries:** `## The Theory (The What)` · `## The Senior Nuance`
  - **Spanish glossary entries:** `## The Theory (El Qué)` · `## The Senior Nuance (El Matiz Senior)`
  - These are the only valid section headings. Always use them exactly as listed — no variations, no translations beyond what is shown.
- **Glossary naming rule:** Glossary entries are listed by their **English name only** in `docs/GLOSSARY_INDEX.md` and `docs/TOPIC_TRACKER.md`. No Spanish translations in entry names. The glossary index is sorted **alphabetically** by English name. No numbering column.
- **Topic naming rule:** All topic names in `docs/TOPIC_TRACKER.md` must be in **English only**. No Spanish titles.
- **Terminology in Spanish articles:** Always use the **English technical term** (Runtime, Scope, Cast, Flow, etc.) since it is the industry standard. On first mention in an article, optionally clarify in parentheses: "el Runtime (tiempo de ejecución)". After that, always use the English term. This keeps articles aligned with how terms are used in interviews and codebases.
- Glossary entries are not scheduled or tracked in `TOPIC_TRACKER.md` — they are added organically as needed.

## Git Workflow

- **NEVER commit until the developer explicitly says so.** Prepare changes, show them, and wait for explicit approval ("commit", "commitea", "push it"). A general instruction like "implement this" is NOT commit approval.
