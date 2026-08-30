# Senior Forge Codex: Daily Learning Workflow

> Living document that defines the daily study routine and evaluation system.
> This workflow will be refined as we iterate on the process.

## Goal

Master all 100 topics at a Senior Android Developer level by **March 2027**. Each topic must be:
1. Understood deeply enough to explain in an interview.
2. Connected to real code in the FollowApp Suite project.
3. Documented as a bilingual article in the Codex.
4. Validated through periodic evaluations.

---

## Daily Routine (1 topic/day)

### Step 1: Select the Topic
- Follow the order in `docs/TOPIC_TRACKER.md` unless there's a reason to jump (e.g., a topic became relevant in FollowApp Suite development).

### Step 2: Find Real Usage in FollowApp Suite
- Search the FollowApp Suite codebase (`/Users/agus/Documents/Entorno/FollowApps/Android/Suite`) for real examples of the concept.
- If the concept is **not found** in FollowApp Suite, mark it as "Not found in FAS" in the tracker and continue with the topic using a realistic standalone example. FollowApp Suite evolves rapidly — unfound topics can be revisited later when they appear in the codebase.

### Step 3: Study Together
- Explain the theory and the "Senior Perspective" (why it matters in production, what interviewers look for).
- Walk through the real FollowApp Suite example (or the standalone example if not found).
- Discuss edge cases, common mistakes, and interview follow-up questions.

### Step 4: Write the Article (EN + ES)
- Follow the format established in `CODEX_GUIDE.md`:
  - **The Theory (The What)** — core concept explanation.
  - **The Senior Perspective (The Why)** — production relevance and architectural impact.
  - **Code in Action** — working code example (ideally from FollowApp Suite).
  - **Interview Prep (The Hot Seat)** — one strong Q&A for interview practice. This Q&A is the basis for the daily self-evaluation.
- Create both language versions.
- Update both chapter `index.md` files.

### Step 4b: Cross-link Glossary Entries
- If the article references a concept that has a glossary entry (e.g., Garbage Collector, JVM), add a link to it using `{{ "/en/glossary/<slug>/" | relative_url }}`.
- If the concept doesn't have a glossary entry yet but is worth explaining, create one in `_posts/en/glossary/` and `_posts/es/glossary/`.
- Glossary entries are extra topics outside the 100 — they are not scheduled or tracked, but they enrich the knowledge base.

### Step 5: Daily Self-Evaluation
- After studying the topic, the learner must answer the **Interview Prep (The Hot Seat)** question from memory, without reading the article.
- This tests whether the topic was truly understood, not just read.
- Result is logged in `docs/TOPIC_TRACKER.md`.

### Step 6: Review, Commit & PR
- Review the article for technical correctness.
- Commit and create a PR.
- Update `docs/TOPIC_TRACKER.md`: mark as done, record the date.

---

## Weekly Evaluation System

Every week (suggested: Friday or weekend), a structured evaluation session covers the accumulated topics. Each evaluation is documented as a markdown file in the `evals/` folder.

### How It Works

Claude asks interview-style questions. The learner answers **in writing, in the chat, without consulting the articles**. After each answer, Claude grades it with brief feedback. At the end, a summary table is generated and saved to `evals/`.

### What Gets Evaluated
1. **All topics learned that week** (the 5-7 new ones).
2. **Flagged topics from prior weeks** — any topic previously marked as not-passed.
3. **Random review topics** — a small random sample (1-3) of previously passed topics, to ensure long-term retention.

### Question Categories

Each topic is evaluated with a mix of these three question types:

| Category | What it tests | Example |
|----------|--------------|---------|
| **Conceptual** | Deep understanding of the concept and its production relevance | "Explain what X is and why it matters in production" |
| **Code** | Practical application — read, write, or debug a snippet | "What does this code do? What problem does it have?" |
| **Tradeoff/Design** | Senior-level judgment and architectural reasoning | "Why would you choose X over Y in this scenario?" |

### Number of Questions Per Topic

| Evaluation type | Questions per topic |
|----------------|-------------------|
| **New topics** | 2-3 (mix of all categories) |
| **Re-evaluation (PARTIAL/FAIL)** | 1-2 (focused on what failed) |
| **Random retention check** | 1 (quick) |

### Scoring (Per Question, 1–5)

| Score | Meaning |
|-------|---------|
| **5** | Senior answer: precise, complete, mentions tradeoffs and edge cases |
| **4** | Correct and solid, but missing some Senior-level nuance or detail |
| **3** | Understands the concept but explanation is incomplete or imprecise |
| **2** | General idea is right but significant errors |
| **1** | Cannot explain it or fundamental errors |

### Topic Result (Average of Question Scores)

| Average | Result | Action |
|---------|--------|--------|
| **4.0+** | **PASS** | Topic moves to the long-term retention pool |
| **3.0–3.9** | **PARTIAL** | Re-evaluated next week alongside new topics |
| **< 3.0** | **FAIL** | Re-evaluated next week with priority; review the article before eval |

### After the Evaluation
- Create an eval record in `evals/` (e.g., `evals/2026-W34.md`).
- Update `docs/TOPIC_TRACKER.md` with the eval date, result, and any notes.
- Topics that scored PARTIAL or FAIL stay in the active review queue.
- Topics that scored PASS enter the long-term retention pool (re-evaluated randomly, roughly once every 4-6 weeks).

---

## Evaluation Record Format (`evals/YYYY-WNN.md`)

Each weekly evaluation is saved as a markdown file:

```markdown
# Weekly Evaluation — YYYY-WNN

**Date:** YYYY-MM-DD

## New Topics
| # | Topic | Q1 | Q2 | Q3 | Avg | Result | Notes |
|---|-------|----|----|----|-----|--------|-------|

## Review (Flagged from Prior Weeks)
| # | Topic | Previous Result | Q1 | Q2 | Avg | Result | Notes |
|---|-------|----------------|----|----|-----|--------|-------|

## Random Re-evaluation
| # | Topic | Q1 | Avg | Result | Notes |
|---|-------|----|-----|--------|-------|

## Summary
- Topics passed: X
- Topics flagged for next week: Y
- Cumulative mastered: Z / 100
```

---

## Spaced Repetition Logic

The system uses a simplified spaced repetition approach:

| Topic Status | Re-evaluation Frequency |
|-------------|------------------------|
| Never evaluated | Evaluated the week it's learned |
| FAIL | Every week until PASS |
| PARTIAL | Every week until PASS |
| PASS (1st time) | Random re-eval in ~3-4 weeks |
| PASS (2nd time) | Random re-eval in ~6-8 weeks |
| PASS (3rd+ time) | Random re-eval in ~10-12 weeks |

A topic is considered **mastered** after 3 consecutive PASS results across spaced intervals.

---

## Pace & Timeline

- **100 topics** at 1/day, Monday through Thursday only.
- Fridays are reserved for catch-up (if a day was missed) and weekly evaluation.
- Start date: 19-ago-2026 (topic #1).
- Projected end date: recalculated as topics are added (see `docs/TOPIC_TRACKER.md`).
- New interview-worthy topics are appended beyond #100 with dates at the end of the schedule.
- Glossary entries (supporting concepts) are added without dates or evaluation pressure.

---

## Files & Locations

| Path | Purpose |
|------|---------|
| `docs/TOPIC_TRACKER.md` | Master checklist with dates, links, and eval results |
| `docs/DAILY_WORKFLOW.md` | This document — the process definition |
| `evals/YYYY-WNN.md` | Weekly evaluation records |
| `CODEX_GUIDE.md` | Article format and engineering standards |
| FollowApp Suite | Source of real-world code examples |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-08-18 | Initial workflow definition |
| 2026-08-18 | Added: daily Q&A self-eval, evals/ folder, FollowApp "not found" handling, docs reorganization |
| 2026-08-28 | Detailed evaluation criteria: 1-5 scoring scale, question categories (Conceptual/Code/Tradeoff), pass threshold (4.0+), questions-per-topic counts, updated eval record format with per-question scores |
