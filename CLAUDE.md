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

## Glossary (Extra Topics)

Concepts that fall outside the 100 main topics are documented as **glossary entries**. The glossary has its own search and serves as a complementary reference.

- Glossary entries live in `_posts/en/glossary/` and `_posts/es/glossary/` (bilingual, layout: `post`).
- Permalink pattern: `/en/glossary/<slug>/` and `/es/glossary/<slug>/`.
- Format: same article structure (Theory, Senior Nuance, code if applicable), with a "Back to Glossary" link.
- **Cross-linking rule:** When writing or updating a main topic article (the 100 topics), link any concept that has a glossary entry. Use the Liquid `relative_url` filter: `[Garbage Collector]({{ "/en/glossary/garbage-collector/" | relative_url }})`. This makes the Codex a connected knowledge base, not isolated pages.
- Glossary entries are not scheduled or tracked in `TOPIC_TRACKER.md` — they are added organically as needed.

## Git Workflow

- **NEVER commit until the developer explicitly says so.** Prepare changes, show them, and wait for explicit approval ("commit", "commitea", "push it"). A general instruction like "implement this" is NOT commit approval.
