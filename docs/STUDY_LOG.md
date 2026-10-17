# Senior Forge Codex: Study Log

> Single source of truth for everything about each topic's Gemini Notebook: notebook file status, notebook link, and which generated outputs have been studied.
> Articles and evaluation results live in `docs/TOPIC_TRACKER.md`.

## Rules (anti-procrastination)

1. **A notebook is not "studied" until its quiz is taken.** The quiz score is the minimum evidence of study.
2. **Eval debt** = topics with a notebook created here and no evaluation yet in `docs/TOPIC_TRACKER.md` (Last Eval). It is recalculated every time either file is updated.
3. **Daily eval quota.** Articles keep their pace; on top of the day's article, at least **1 evaluation per day** while the debt is above 0 (2 per day while it is above 10). Fridays (catch-up day) target 3. Oldest notebooks go first.
4. An evaluation is a session with Claude (cold, no notes) on the topic's Interview Prep Q&A plus follow-ups; the result (PASS / PARTIAL / FAIL) is recorded only in `docs/TOPIC_TRACKER.md` (Last Eval / Eval Result) and in the weekly file under `evals/`.

## Notebook outputs

Every notebook generates the same set, consumed in this order:

| Key | Output | Settings |
| --- | ------ | -------- |
| A | Audio overview | — |
| S | Slide deck | — |
| V | Video overview | — |
| R | Report (study guide) | — |
| I | Infographic | Detailed |
| T | Data table | — |
| F | Flashcards | Standard count, medium difficulty |
| Q | Quiz | Standard count, medium difficulty — record score |

**Notebook column:** :green_book: = the Gemini Notebook has been created — the icon links to it · :white_check_mark: = notebook file exists under `_notebooks/` (diagnostic recorded, Gemini prompt ready), not loaded into Gemini yet · :black_square_button: = article written, notebook file pending.

> The :green_book: links point to personal Gemini Notebooks: they only open for the account that owns them.

Cell values: :white_check_mark: consumed · :black_square_button: generated, not consumed yet · — not generated.

## Eval Debt

**Debt:** 32 — daily quota: 2 evals/day
**Last updated:** 2026-10-16

## Log

### I. Kotlin Core

| Topic | Notebook | A | S | V | R | I | T | F | Q (score) |
| ----- | :------: | - | - | - | - | - | - | - | --------- |
| Null Safety: Elvis & Safe Calls | [:green_book:](https://notebook.google.com/notebook/a4d54982-a2b2-44b1-bef7-0fa77012c79c) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Smart Casts | [:green_book:](https://notebook.google.com/notebook/e6c2df6a-d8ed-40fc-b513-78dcfe8b855a) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Data Classes: copy, equals, toString | [:green_book:](https://notebook.google.com/notebook/3d9b6c74-6cd1-4a6d-886f-ebf7e83b3ade) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Data Objects: Singleton & Memory Savings | [:green_book:](https://notebook.google.com/notebook/5b8f43d9-493b-405a-832c-89d353f53e2b) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Sealed Classes vs Sealed Interfaces | [:green_book:](https://notebook.google.com/notebook/5230c74e-ca25-486a-9f86-dbafaf0ea94f) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Extension Functions | [:green_book:](https://notebook.google.com/notebook/13da3244-b82b-4d7c-b756-5e837a5a735e) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Higher-Order Functions & Lambdas | [:green_book:](https://notebook.google.com/notebook/4cd330ea-14d6-4a25-a296-94ff9d1ac2e7) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Scope Functions (let, run, apply, also, with) | [:green_book:](https://notebook.google.com/notebook/d334f549-944d-4066-a9a8-f0441e200f4b) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Lateinit vs Lazy | [:green_book:](https://notebook.google.com/notebook/dce92f1a-c9c9-45cc-bcd8-f784002f7aaa) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Delegated Properties (by lazy, by viewModels) | [:green_book:](https://notebook.google.com/notebook/72a95d4f-58c3-4ab7-81af-52b030830515) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Generics: Variance & Reification (in, out, reified) | [:green_book:](https://notebook.google.com/notebook/08c6ad46-9bfb-4486-a186-7de56010e0c1) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Collections & Mutability | [:green_book:](https://notebook.google.com/notebook/751446c6-6fb6-428f-9fc7-4359b047bbc6) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Immutability & Atomic State for UI | [:green_book:](https://notebook.google.com/notebook/8b013a6e-6fe3-407a-a027-3e0c11c2fd04) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |

### II. Coroutines & Flows

| Topic | Notebook | A | S | V | R | I | T | F | Q (score) |
| ----- | :------: | - | - | - | - | - | - | - | --------- |
| Suspend functions | [:green_book:](https://notebook.google.com/notebook/b1d68038-bd5d-44bb-8913-0f48f75cc7aa) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Context & Dispatchers (Main, IO, Default) | [:green_book:](https://notebook.google.com/notebook/02868677-b56e-4a4a-8794-386fe823bcf3) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Structured Concurrency | [:green_book:](https://notebook.google.com/notebook/9ac6d52b-55e4-43b0-acb1-8d13e37b36c1) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Launch vs Async/Await | [:green_book:](https://notebook.google.com/notebook/251d9d0f-34d7-4a10-92be-b585eb0ef302) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Main-Safety | [:green_book:](https://notebook.google.com/notebook/63860824-8580-40fd-be3d-9517de84081f) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| withContext vs flowOn | [:green_book:](https://notebook.google.com/notebook/61a0d946-e393-486a-bdda-390e0eaf0595) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Flow (Cold Streams) | [:green_book:](https://notebook.google.com/notebook/24bc9c1e-03d7-4b1e-96cf-5111d5a4a7ef) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Error Handling: try-catch & .catch | [:green_book:](https://notebook.google.com/notebook/e60f0dea-401b-4602-8f4a-bf5639fc0512) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| StateFlow | [:green_book:](https://notebook.google.com/notebook/609402b0-1056-4248-9a56-e63edd1b8841) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| SharedFlow | [:green_book:](https://notebook.google.com/notebook/83279058-1006-48c8-8084-7f1796c3f692) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| shareIn & stateIn | [:green_book:](https://notebook.google.com/notebook/ee778834-1e0d-4a0e-bea9-b09b57c718f9) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| MutableStateFlow.update {} | [:green_book:](https://notebook.google.com/notebook/d4117939-f537-4e18-a8f1-05c48e9e8f22) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| Channel (Hot Streams) | [:green_book:](https://notebook.google.com/notebook/e6346671-31d0-44fe-9721-eb7c98e12d9c) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| trySend() vs send() | [:green_book:](https://notebook.google.com/notebook/4cdf8c0e-4596-4502-9069-18672c3441da) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| receiveAsFlow() | [:green_book:](https://notebook.google.com/notebook/062bc676-e604-4609-9d13-3a66a89985d4) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| callbackFlow | [:green_book:](https://notebook.google.com/notebook/2eaf4386-1ea8-470a-b1fc-fa38723f48bf) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |

### III. Jetpack Compose

| Topic | Notebook | A | S | V | R | I | T | F | Q (score) |
| ----- | :------: | - | - | - | - | - | - | - | --------- |
| Recomposition & Stability | [:green_book:](https://notebook.google.com/notebook/a29fb5a6-6591-45b3-a210-c0b34e80ed32) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| remember & rememberSaveable | [:green_book:](https://notebook.google.com/notebook/fc5ceec1-5879-4f8e-82cf-7ee05623f776) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
| State Hoisting | :white_check_mark: | — | — | — | — | — | — | — | — |
| Modifiers: Order & Alignment | :white_check_mark: | — | — | — | — | — | — | — | — |

### V. Architecture & Patterns

| Topic | Notebook | A | S | V | R | I | T | F | Q (score) |
| ----- | :------: | - | - | - | - | - | - | - | --------- |
| UI State Modeling: Sealed vs Flat Data Class | [:green_book:](https://notebook.google.com/notebook/7457b2e1-1484-4324-8c83-98202c42bbe4) | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: | :black_square_button: |
