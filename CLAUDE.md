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
- Real code examples come from **FollowApp Suite** (`/Users/agus/Documents/Entorno/FollowApps/Android/Suite`). If a topic is not found there, mark as "Not found in FAS" and use a standalone example.
- After each topic, the learner answers the Interview Prep Q&A from memory as a daily self-evaluation.
- Weekly evaluations are cumulative and use spaced repetition (see `docs/DAILY_WORKFLOW.md`).

## Growing the Topic List

The initial 100 topics can grow. When a new concept emerges that is genuinely interview-worthy (not just a glossary term), it is added **inside the chapter section it belongs to** in `docs/TOPIC_TRACKER.md`, with a date appended at the end of the schedule. Update topic count and `Projected end date` in the summary.

- **Topic** → full article (EN + ES), planned date, evaluation, Interview Prep Q&A.
- **Glossary entry** → reference concept, no date or evaluation, cross-linked from main topics.

The distinction: if it could be asked as a standalone interview question with a "Senior Answer", it's a topic. If it's a supporting concept referenced by multiple topics, it's glossary.

## Glossary (Extra Topics)

Concepts that fall outside the 100 main topics are documented as **glossary entries**. The glossary has its own search and serves as a complementary reference.

- Glossary entries live in `_posts/en/glossary/` and `_posts/es/glossary/` (bilingual, layout: `post`).
- Permalink pattern: `/en/glossary/<slug>/` and `/es/glossary/<slug>/`.
- Format: same article structure (Theory, Senior Nuance, code if applicable), with a "Back to Glossary" link.
- **Cross-linking rule:** When writing or updating any article (topic or glossary), link any concept that already has its own article — whether it is another topic or a glossary entry. Use the Liquid `relative_url` filter: `[Garbage Collector]({{ "/en/glossary/garbage-collector/" | relative_url }})`, `[Data Objects]({{ "/en/01-kotlin-core/data-objects/" | relative_url }})`. This makes the Codex a connected knowledge base, not isolated pages.
- Glossary entries are not scheduled or tracked in `TOPIC_TRACKER.md` — they are added organically as needed.

## Git Workflow

- **NEVER commit until the developer explicitly says so.** Prepare changes, show them, and wait for explicit approval ("commit", "commitea", "push it"). A general instruction like "implement this" is NOT commit approval.
