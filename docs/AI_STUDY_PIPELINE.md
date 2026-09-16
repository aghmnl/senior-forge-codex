# The Senior Forge Codex: Multi-Agent AI Study Workflow

This document outlines the synchronized workflow between Claude and Gemini Gemini Notebook processing, studying, and evaluating the 100 technical topics for Senior Android Engineering interviews. It complements the `DAILY_WORKFLOW.md` by defining the exact responsibilities of each AI agent and where the per-topic prompts live.

**Daily sequence:** Claude drafts the topic (content not shown yet) → Claude diagnostic, cold → learner reads and names extra glossary words → Claude links them and generates the notebook file → PR → Gemini creates the notebook from a single pre-filled prompt → study with the notebook → Claude final evaluation. Step-by-step in `docs/DAILY_WORKFLOW.md` (Steps 4c–4e).

## Agent Responsibilities

- **Claude:**
  - **Content Creation:** Generates the daily technical articles, glossary entries, and maintains the GitHub repository.
  - **Notebook Prompt:** Ships, with every new topic, a ready-to-paste study file under `_notebooks/` that contains everything Gemini needs — pre-researched, ordered, with no open research left to do.
  - **Baseline Diagnostic:** Administers the five diagnostic questions of that file, compares the answers against its rubric, and writes the "Nivel actual" text.
  - **Evaluation:** Conducts the final theoretical and practical technical interview simulations based on the generated content.
- **Gemini (Chat):**
  - **Notebook Setup only:** Creates the Gemini Notebook, adds the exact list of sources it is given, and pastes the "Nivel actual" text as a source. It does not scrape, search, or judge.
- \**Gemini Notebook:*Gemini Notebook
  - **Deep Study:** Utilizes native tools (Audio Overview, Mind Map, Flashcards, Quiz) to fixate terminology and architectural reasoning without consuming conversational context.

### Why the split

The first version of this pipeline asked Gemini to research and orchestrate in one pass: scrape glossary links from the article, search official documentation, extract the "Senior Perspective", judge diagnostic answers, then create the notebook. Gemini lost track of the request. The reliable part of Gemini is the mechanical part — create a notebook, add URLs, paste a text — so everything else moved to Claude and to a per-topic file prepared in advance.

## Phase 1: Content Generation + Notebook File (Claude)

As defined in `DAILY_WORKFLOW.md`, Claude drafts the daily article and publishes it to `aghmnl.github.io/senior-forge-codex/es/`. The diagnostic (Phase 2A) runs **before** the learner reads the draft; the learner then reviews it and names the extra glossary words to link; only after that does Claude create the topic's notebook file, so its glossary list is final:

```
_notebooks/<chapter-folder>/<slug>.md      e.g. _notebooks/02-coroutines-flow/suspend-functions.md
```

The folder is ignored by Jekyll (leading underscore), so it is never published. Everything in it is in Spanish. Each file has three blocks:

| Block                        | Content                                                                                                                                                                                                                                                                                                            | Who uses it                |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------- |
| **1 — Diagnóstico de nivel** | Five questions anchored in the article's "The Senior Perspective", a rubric per question (Senior / intermediate / junior answer), and the template for the "Nivel actual" text.                                                                                                                                    | Claude, with the learner   |
| **2 — Prompt para Gemini**   | Topic name, article URL, every `/es/glosario/` URL linked from the ES article (extracted from the markdown, so it never drifts), 3–12 verified official sources from `kotlinlang.org` / `developer.android.com` with a one-line purpose each, closed numbered execution steps, and a `[NIVEL ACTUAL]` placeholder. | Learner pastes into Gemini |
| **3 — Vía alternativa**      | The same diagnostic wrapped as a two-prompt flow where Gemini asks the questions and applies the rubric itself. Kept for experimentation; not the default path.                                                                                                                                                    | Optional                   |

Rules for the file:

- Diagnostic questions must differ from the article's Interview Prep Q&A and from the questions Claude will use in Phase 4. The diagnostic measures concepts; the evaluation measures design decisions and code.
- Official URLs are verified (HTTP 200) before being listed. Only `kotlinlang.org` and `developer.android.com`.
- The glossary list is regenerated whenever the article's links change.

## Phase 2: Baseline Diagnostic (Claude) and Notebook Creation (Gemini)

### Step 2A: Diagnostic with Claude — before reading the article

Claude offers it as soon as the draft is ready (or ask: _"Nivelame en <tema>"_). Claude asks the five questions from Block 1, one at a time. Answer **from memory, without having read the article** — the goal is to measure the starting point so the notebook explains what is actually missing. "No sé" is a valid answer. Claude compares the answers against the rubric and returns the "Nivel actual" text (8–12 lines: global level, what is already known, what needs in-depth explanation using the exact glossary terms, misconceptions to correct, and a one-line instruction for the Audio Overview).

Claude then records the outcome in the topic file itself, under Block 1 as a `### Resultado — YYYY-MM-DD` section: a per-question table (level + observation), the global level, and the exact "Nivel actual" text that was handed to Gemini. In the same step, Claude replaces the `[NIVEL ACTUAL]` placeholder in Block 2 with that text, so the Gemini prompt is pasted as-is. The notebook file is therefore the single record of the topic's baseline; the final evaluation result stays in `docs/TOPIC_TRACKER.md`.

### Step 2B: Notebook creation with Gemini — one prompt

Copy Block 2 of the topic file into the Gemini chat, replacing `[NIVEL ACTUAL]` with the text from Step 2A. Gemini creates the notebook, adds each listed URL, creates the "Nivel actual" text source verbatim, and replies with the notebook URL and the list of sources added. Nothing is left for Gemini to research or decide.

## Phase 3: Deep Study Tools (Gemini Notebook UI)

Once Gemini provides the notebook link, read the article, then navigate to the Gemini Notebook web interface to use the native study tools in the following sequential order. Because the "Nivel actual" text is a source, the Audio Overview will contextualize its debate based on what is already known.

1. **Audio Overview:** Listen to the generated debate based on the sources to internalize high-level concepts and architectural reasoning.
2. **Mind Map:** Generate the visualization to understand the hierarchical relationship between framework concepts and glossary definitions.
3. **Flashcards:** Use this native tool for the fixation phase (memorization of key terminology and syntax).
4. **Quiz:** Complete the quick multiple-choice evaluation provided by the interface to validate reading comprehension before the strict interview.

## Phase 4: Senior Interview Evaluation (Claude)

After completing the deep study in Gemini Notebook, return to Claude for the technical evaluation. Claude holds the context of the generated article and acts as the strict Senior Android Interviewer. These questions are not the diagnostic ones from Block 1.

### Evaluation Prompt

Copy and execute the following block in Claude's interface.

```text
**Context:**
Act as a strict Senior Android Engineering interviewer and technical mentor. I have just completed my deep study session on today's topic. We will now conduct the evaluation session in Latinamerican Spanish based strictly on the article you generated.

**Execution Steps:**
1. **Theoretical Evaluation:** Ask me exactly one advanced theoretical question about the architectural decisions discussed in the article's "The Senior Perspective" section. Wait for my answer, evaluate it strictly, and provide technical feedback.
2. **Practical Evaluation:** After the theoretical feedback, present a real-world Android/Kotlin code scenario related to the topic with a design flaw or compile error. Ask me how to fix it based on the studied concepts. Evaluate my response.

```
