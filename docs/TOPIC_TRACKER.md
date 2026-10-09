# Senior Forge Codex: Topic Tracker

> Master checklist of topics for Senior Android Developer mastery.
> The list starts at 100 and grows as new interview-worthy topics emerge.
> Target: all topics learned and documented by **March 2027**.

## Status Legend

| Symbol                | Meaning                       |
| --------------------- | ----------------------------- |
| :white_check_mark:    | Article written and published |
| :hourglass:           | In progress                   |
| :black_square_button: | Not started                   |

**FAS column:** Full = uses real FollowApp Suite code · None = standalone examples · — = article not written yet.

**Notebook column:** :green_book: = the Gemini Notebook has been created — the icon links to it · :white_check_mark: = study file exists under `_notebooks/` (diagnostic recorded, Gemini prompt ready), not loaded into Gemini yet · :black_square_button: = article written, notebook file pending · — = article not written yet.

> The :green_book: links point to personal Gemini Notebooks: they only open for the account that owns them.

## Progress Summary

**Completed:** 0 / 101 (studied & evaluated)
**Articles written:** 31 / 101
**Last updated:** 2026-10-09
**Projected end date:** 10-feb-2027

---

## I. Kotlin Core (0/13)

| Topic                                                | Article                                                                                                                                                                                                   | Planned | Status                | Article Date | FAS  | Notebook           | Last Eval | Eval Result |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | --------------------- | ------------ | :--: | :----------------: | --------- | ----------- |
| Null Safety: Elvis & Safe Calls                      | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/null-safety-elvis-safe-calls/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/null-safety-elvis-safe-calls/)     | 19-ago  | :black_square_button: | 2026-08-28   | Full | [:green_book:](https://notebook.google.com/notebook/a4d54982-a2b2-44b1-bef7-0fa77012c79c) | —         | —           |
| Smart Casts                                          | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/smart-casts/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/smart-casts/)                                       | 20-ago  | :black_square_button: | 2026-08-19   | Full | [:green_book:](https://notebook.google.com/notebook/e6c2df6a-d8ed-40fc-b513-78dcfe8b855a) | —         | —           |
| Data Classes: copy, equals, toString                 | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/data-classes/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/data-classes/)                                     | 24-ago  | :black_square_button: | 2026-08-19   | Full | [:green_book:](https://notebook.google.com/notebook/3d9b6c74-6cd1-4a6d-886f-ebf7e83b3ade) | —         | —           |
| Data Objects: Singleton & Memory Savings             | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/data-objects/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/data-objects/)                                     | 25-ago  | :black_square_button: | 2026-08-19   | Full | [:green_book:](https://notebook.google.com/notebook/5b8f43d9-493b-405a-832c-89d353f53e2b) | —         | —           |
| Sealed Classes vs Sealed Interfaces                  | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/sealed-classes-interfaces/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/sealed-classes-interfaces/)           | 26-ago  | :black_square_button: | 2026-08-30   | Full | [:green_book:](https://notebook.google.com/notebook/5230c74e-ca25-486a-9f86-dbafaf0ea94f) | —         | —           |
| Extension Functions                                  | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/extension-functions/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/extension-functions/)                       | 27-ago  | :black_square_button: | 2026-05-03   | None | [:green_book:](https://notebook.google.com/notebook/13da3244-b82b-4d7c-b756-5e837a5a735e) | —         | —           |
| Higher-Order Functions & Lambdas                     | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/higher-order-functions-lambdas/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/higher-order-functions-lambdas/) | 31-ago  | :black_square_button: | 2026-09-02   | Full | :black_square_button: | —         | —           |
| Scope Functions (let, run, apply, also, with)        | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/scope-functions/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/scope-functions/)                               | 01-sep  | :black_square_button: | 2026-09-02   | Full | :black_square_button: | —         | —           |
| Lateinit vs Lazy                                     | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/lateinit-vs-lazy/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/lateinit-vs-lazy/)                             | 02-sep  | :black_square_button: | 2026-09-02   | Full | :black_square_button: | —         | —           |
| Delegated Properties (by lazy, by viewModels)        | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/delegated-properties/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/delegated-properties/)                     | 03-sep  | :black_square_button: | 2026-09-03   | Full | :black_square_button: | —         | —           |
| Generics: Variance & Reification (in, out, reified) | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/generics-variance-reification/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/generics-variance-reification/)   | 07-sep  | :black_square_button: | 2026-09-07   | Full | :black_square_button: | —         | —           |
| Collections & Mutability                             | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/collections-mutability/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/collections-mutability/)                 | 08-sep  | :black_square_button: | 2026-09-08   | Full | :black_square_button: | —         | —           |
| Immutability & Atomic State for UI                   | [EN](https://aghmnl.github.io/senior-forge-codex/en/01-kotlin-core/immutability-atomic-state/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/immutability-atomic-state/)           | 09-sep  | :black_square_button: | 2026-09-09   | Full | :black_square_button: | —         | —           |

## II. Coroutines & Flows (0/16)

| Topic                                     | Article | Planned | Status                | Article Date | FAS  | Notebook           | Last Eval | Eval Result |
| ----------------------------------------- | ------- | ------- | --------------------- | ------------ | :--: | :----------------: | --------- | ----------- |
| Suspend functions                         | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/suspend-functions/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/suspend-functions/) | 10-sep  | :black_square_button: | 2026-09-10   | Full | [:green_book:](https://notebook.google.com/notebook/b1d68038-bd5d-44bb-8913-0f48f75cc7aa) | —         | —           |
| Context & Dispatchers (Main, IO, Default) | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/context-dispatchers/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/context-dispatchers/) | 14-sep  | :black_square_button: | 2026-09-14   | Full | [:green_book:](https://notebook.google.com/notebook/02868677-b56e-4a4a-8794-386fe823bcf3) | —         | —           |
| Structured Concurrency                    | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/structured-concurrency/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/structured-concurrency/) | 15-sep  | :black_square_button: | 2026-09-15   | Full | [:green_book:](https://notebook.google.com/notebook/9ac6d52b-55e4-43b0-acb1-8d13e37b36c1) | —         | —           |
| Launch vs Async/Await                     | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/launch-vs-async-await/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/launch-vs-async-await/) | 16-sep  | :black_square_button: | 2026-09-16   | Full | [:green_book:](https://notebook.google.com/notebook/251d9d0f-34d7-4a10-92be-b585eb0ef302) | —         | —           |
| Main-Safety                               | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/main-safety/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/main-safety/) | 17-sep  | :black_square_button: | 2026-09-17   | Full | [:green_book:](https://notebook.google.com/notebook/63860824-8580-40fd-be3d-9517de84081f) | —         | —           |
| withContext vs flowOn                     | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/with-context-vs-flow-on/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/with-context-vs-flow-on/) | 21-sep  | :black_square_button: | 2026-09-21   | Full | [:green_book:](https://notebook.google.com/notebook/61a0d946-e393-486a-bdda-390e0eaf0595) | —         | —           |
| Flow (Cold Streams)                       | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/flow-cold-streams/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/flow-cold-streams/) | 22-sep  | :black_square_button: | 2026-09-23   | Full | [:green_book:](https://notebook.google.com/notebook/24bc9c1e-03d7-4b1e-96cf-5111d5a4a7ef) | —         | —           |
| Error Handling: try-catch & .catch        | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/error-handling/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/error-handling/) | 23-sep  | :black_square_button: | 2026-09-23   | Full | [:green_book:](https://notebook.google.com/notebook/e60f0dea-401b-4602-8f4a-bf5639fc0512) | —         | —           |
| StateFlow                                 | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/stateflow/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/stateflow/) | 24-sep  | :black_square_button: | 2026-09-25   | Full | [:green_book:](https://notebook.google.com/notebook/609402b0-1056-4248-9a56-e63edd1b8841) | —         | —           |
| SharedFlow                                | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/sharedflow/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/sharedflow/) | 28-sep  | :black_square_button: | 2026-09-25   | Full | [:green_book:](https://notebook.google.com/notebook/83279058-1006-48c8-8084-7f1796c3f692) | —         | —           |
| shareIn & stateIn                         | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/sharein-statein/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/sharein-statein/) | 29-sep  | :black_square_button: | 2026-09-28   | Full | [:green_book:](https://notebook.google.com/notebook/ee778834-1e0d-4a0e-bea9-b09b57c718f9) | —         | —           |
| MutableStateFlow.update {}                | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/mutablestateflow-update/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/mutablestateflow-update/) | 30-sep  | :black_square_button: | 2026-09-28   | Full | [:green_book:](https://notebook.google.com/notebook/d4117939-f537-4e18-a8f1-05c48e9e8f22) | —         | —           |
| Channel (Hot Streams)                     | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/channel-hot-streams/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/channel-hot-streams/) | 01-oct  | :black_square_button: | 2026-09-28   | None | [:green_book:](https://notebook.google.com/notebook/e6346671-31d0-44fe-9721-eb7c98e12d9c) | —         | —           |
| trySend() vs send()                       | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/trysend-vs-send/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/trysend-vs-send/) | 05-oct  | :black_square_button: | 2026-10-02   | Full | [:green_book:](https://notebook.google.com/notebook/4cdf8c0e-4596-4502-9069-18672c3441da) | —         | —           |
| receiveAsFlow()                           | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/receive-as-flow/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/receive-as-flow/) | 06-oct  | :black_square_button: | 2026-10-09   | None | [:green_book:](https://notebook.google.com/notebook/062bc676-e604-4609-9d13-3a66a89985d4) | —         | —           |
| callbackFlow                              | [EN](https://aghmnl.github.io/senior-forge-codex/en/02-coroutines-flow/callback-flow/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/callback-flow/) | 07-oct  | :black_square_button: | 2026-10-09   | Full | [:green_book:](https://notebook.google.com/notebook/2eaf4386-1ea8-470a-b1fc-fa38723f48bf) | —         | —           |

## III. Jetpack Compose (0/14)

| Topic                                           | Article | Planned | Status                | Article Date | FAS  | Notebook           | Last Eval | Eval Result |
| ----------------------------------------------- | ------- | ------- | --------------------- | ------------ | :--: | :----------------: | --------- | ----------- |
| Recomposition & Stability                       | [EN](https://aghmnl.github.io/senior-forge-codex/en/03-jetpack-compose/recomposition-stability/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/03-jetpack-compose/recomposition-stability/) | 08-oct  | :black_square_button: | 2026-10-09   | Full | :white_check_mark: | —         | —           |
| remember & rememberSaveable                     | —       | 12-oct  | :black_square_button: | —            | —    | —                  | —         | —           |
| State Hoisting                                  | —       | 13-oct  | :black_square_button: | —            | —    | —                  | —         | —           |
| Modifiers: Order & Alignment                    | —       | 14-oct  | :black_square_button: | —            | —    | —                  | —         | —           |
| Lazy Lists (LazyColumn, LazyRow)                | —       | 15-oct  | :black_square_button: | —            | —    | —                  | —         | —           |
| innerPadding in Scaffold                        | —       | 19-oct  | :black_square_button: | —            | —    | —                  | —         | —           |
| LaunchedEffect(Unit)                            | —       | 20-oct  | :black_square_button: | —            | —    | —                  | —         | —           |
| DisposableEffect                                | —       | 21-oct  | :black_square_button: | —            | —    | —                  | —         | —           |
| collectAsStateWithLifecycle                     | —       | 22-oct  | :black_square_button: | —            | —    | —                  | —         | —           |
| DerivedStateOf                                  | —       | 26-oct  | :black_square_button: | —            | —    | —                  | —         | —           |
| CompositionLocal                                | —       | 27-oct  | :black_square_button: | —            | —    | —                  | —         | —           |
| LocalContext.current                            | —       | 28-oct  | :black_square_button: | —            | —    | —                  | —         | —           |
| Navigation Compose                              | —       | 29-oct  | :black_square_button: | —            | —    | —                  | —         | —           |
| Accessibility: Semantics & Content Descriptions | —       | 02-nov  | :black_square_button: | —            | —    | —                  | —         | —           |

## IV. Android Framework & Lifecycle (0/9)

| Topic                                   | Article | Planned | Status                | Article Date | FAS  | Notebook           | Last Eval | Eval Result |
| --------------------------------------- | ------- | ------- | --------------------- | ------------ | :--: | :----------------: | --------- | ----------- |
| Activity vs Fragment                    | —       | 03-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Fragment Lifecycle                      | —       | 04-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Config Changes                          | —       | 05-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Process Death                           | —       | 09-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Context Hierarchy                       | —       | 10-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Manifest                                | —       | 11-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Explicit & Implicit Intents             | —       | 12-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Services & WorkManager                  | —       | 16-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Broadcast Receivers & Content Providers | —       | 17-nov  | :black_square_button: | —            | —    | —                  | —         | —           |

## V. Architecture & Patterns (0/11)

| Topic                                        | Article | Planned | Status                | Article Date | FAS  | Notebook           | Last Eval | Eval Result |
| -------------------------------------------- | ------- | ------- | --------------------- | ------------ | :--: | :----------------: | --------- | ----------- |
| SOLID in Android                             | —       | 18-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Clean Architecture                           | —       | 19-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Dependency Inversion                         | —       | 23-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Repository Pattern                           | —       | 24-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Use Cases (Interactors)                      | —       | 25-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| Single Source of Truth (SSoT)                | —       | 26-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| MVVM vs MVI                                  | —       | 30-nov  | :black_square_button: | —            | —    | —                  | —         | —           |
| MVI (Unidirectional Data Flow)               | —       | 01-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| UI State Modeling: Sealed vs Flat Data Class | [EN](https://aghmnl.github.io/senior-forge-codex/en/05-architecture/ui-state-modeling/) · [ES](https://aghmnl.github.io/senior-forge-codex/es/05-architecture/ui-state-modeling/) | 02-dic  | :black_square_button: | 2026-08-19   | Full | :black_square_button: | —         | —           |
| Singleton & Factory                          | —       | 03-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| MVP (Legacy)                                 | —       | 10-feb  | :black_square_button: | —            | —    | —                  | —         | —           |

## VI. Dependency Injection (0/5)

| Topic                                      | Article | Planned | Status                | Article Date | FAS  | Notebook           | Last Eval | Eval Result |
| ------------------------------------------ | ------- | ------- | --------------------- | ------------ | :--: | :----------------: | --------- | ----------- |
| DI Concepts                                | —       | 07-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| Hilt: @HiltAndroidApp & @AndroidEntryPoint | —       | 08-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| @Binds vs @Provides                        | —       | 09-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| Hilt Scopes                                | —       | 10-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| Dagger 2 vs Hilt                           | —       | 14-dic  | :black_square_button: | —            | —    | —                  | —         | —           |

## VII. Data & Networking (0/7)

| Topic                               | Article | Planned | Status                | Article Date | FAS  | Notebook           | Last Eval | Eval Result |
| ----------------------------------- | ------- | ------- | --------------------- | ------------ | :--: | :----------------: | --------- | ----------- |
| REST API & GraphQL                  | —       | 15-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| OkHttp & Interceptors               | —       | 16-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| Retrofit                            | —       | 17-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| Room & SQL                          | —       | 21-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| Complex Queries: @Query & JOINs     | —       | 22-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| SharedPreferences & DataStore       | —       | 23-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| WireMock                            | —       | 24-dic  | :black_square_button: | —            | —    | —                  | —         | —           |

## VIII. Testing & Quality (0/5)

| Topic                                    | Article | Planned | Status                | Article Date | FAS  | Notebook           | Last Eval | Eval Result |
| ---------------------------------------- | ------- | ------- | --------------------- | ------------ | :--: | :----------------: | --------- | ----------- |
| Unit Tests (JUnit)                       | —       | 28-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| Test Fakes vs Mocks                      | —       | 29-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| Coroutine Testing                        | —       | 30-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| Espresso                                 | —       | 31-dic  | :black_square_button: | —            | —    | —                  | —         | —           |
| Static Analysis (Ktlint, Detekt, Lint)   | —       | 04-ene  | :black_square_button: | —            | —    | —                  | —         | —           |

## IX. GitHub & CI/CD (0/4)

| Topic                                | Article | Planned | Status                | Article Date | FAS  | Notebook           | Last Eval | Eval Result |
| ------------------------------------ | ------- | ------- | --------------------- | ------------ | :--: | :----------------: | --------- | ----------- |
| Merge vs Rebase vs Squash            | —       | 05-ene  | :black_square_button: | —            | —    | —                  | —         | —           |
| GitFlow & Trunk-based                | —       | 06-ene  | :black_square_button: | —            | —    | —                  | —         | —           |
| Pull Request Templates & Code Owners | —       | 07-ene  | :black_square_button: | —            | —    | —                  | —         | —           |
| GitHub Actions                       | —       | 11-ene  | :black_square_button: | —            | —    | —                  | —         | —           |

## X. Gradle & Build System (0/3)

| Topic                                | Article | Planned | Status                | Article Date | FAS  | Notebook           | Last Eval | Eval Result |
| ------------------------------------ | ------- | ------- | --------------------- | ------------ | :--: | :----------------: | --------- | ----------- |
| Build Variants                       | —       | 12-ene  | :black_square_button: | —            | —    | —                  | —         | —           |
| Source Sets                          | —       | 13-ene  | :black_square_button: | —            | —    | —                  | —         | —           |
| Version Catalog (libs.versions.toml) | —       | 14-ene  | :black_square_button: | —            | —    | —                  | —         | —           |

## XI. Performance & Security (0/6)

| Topic                     | Article | Planned | Status                | Article Date | FAS  | Notebook           | Last Eval | Eval Result |
| ------------------------- | ------- | ------- | --------------------- | ------------ | :--: | :----------------: | --------- | ----------- |
| Memory Leaks (LeakCanary) | —       | 18-ene  | :black_square_button: | —            | —    | —                  | —         | —           |
| ANR                       | —       | 19-ene  | :black_square_button: | —            | —    | —                  | —         | —           |
| R8/Proguard               | —       | 20-ene  | :black_square_button: | —            | —    | —                  | —         | —           |
| Energy Efficiency         | —       | 21-ene  | :black_square_button: | —            | —    | —                  | —         | —           |
| Android Keystore          | —       | 25-ene  | :black_square_button: | —            | —    | —                  | —         | —           |
| SSL Pinning               | —       | 26-ene  | :black_square_button: | —            | —    | —                  | —         | —           |

## XII. Artificial Intelligence (0/8)

| Topic                                          | Article | Planned | Status                | Article Date | FAS  | Notebook           | Last Eval | Eval Result |
| ---------------------------------------------- | ------- | ------- | --------------------- | ------------ | :--: | :----------------: | --------- | ----------- |
| Cloud vs Edge Models                           | —       | 27-ene  | :black_square_button: | —            | —    | —                  | —         | —           |
| Tokens & Context Window                        | —       | 28-ene  | :black_square_button: | —            | —    | —                  | —         | —           |
| Generation Parameters (Temp, Top-P, Top-K)     | —       | 01-feb  | :black_square_button: | —            | —    | —                  | —         | —           |
| Prompting (System vs User)                     | —       | 02-feb  | :black_square_button: | —            | —    | —                  | —         | —           |
| Skills / Tool Use (Function Calling)           | —       | 03-feb  | :black_square_button: | —            | —    | —                  | —         | —           |
| RAG (Retrieval-Augmented Generation)           | —       | 04-feb  | :black_square_button: | —            | —    | —                  | —         | —           |
| Agents & Agentic AI                            | —       | 08-feb  | :black_square_button: | —            | —    | —                  | —         | —           |
| Model Context Protocol (MCP)                   | —       | 09-feb  | :black_square_button: | —            | —    | —                  | —         | —           |

---

## Evaluation History

> Weekly evaluations are logged here. Each entry records the date, topics evaluated,
> results, and any topics flagged for re-evaluation.

| Date | Topics Evaluated | Result | Flagged for Review |
| ---- | ---------------- | ------ | ------------------ |
| —    | —                | —      | —                  |

---

## Notes

- All chapters reordered pedagogically (2026-08-28): topics within each chapter follow dependency chains, from fundamentals to advanced. Original dates reassigned to match new order.
- Articles use `order` field in frontmatter for sidebar display order within each chapter.
- Schedule: Mon-Thu for new topics, Fri reserved for catch-up and weekly evaluation.
- Topics may be updated as Android ecosystem evolves.
- New interview-worthy topics are inserted into their corresponding chapter section, with dates appended at the end of the schedule. Update topic count and `Projected end date` in the summary.
