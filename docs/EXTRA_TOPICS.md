# Extra Topics: Candidate Pool

> Topics from the 200-topic interview list that are **not already covered** by the 101 scheduled topics in `TOPIC_TRACKER.md`.
> This is a backlog — no dates, no deadlines. Topics can be promoted to the main tracker or added as glossary entries as needed.
> Last compared against TOPIC_TRACKER on: 2026-08-19.

---

## Kotlin Core & Functional

| #  | Topic | Notes |
|----|-------|-------|
| 1  | Inline Classes y Value Classes | — |
| 2  | Object Expressions vs Object Declarations | — |
| 3  | Companion Objects e instanciación | — |
| 4  | Destructuring Declarations | Related to Data Classes (#8) |
| 5  | Sequences API (Evaluación perezosa) | — |
| 6  | Visibility Modifiers (internal, protected, etc.) | — |
| 7  | Operator Overloading | — |

## Coroutines & Asynchrony

| #  | Topic | Notes |
|----|-------|-------|
| 8  | Coroutine Scopes (Global, ViewModel, Lifecycle) | Tracker has Context+Dispatchers (#14), not scopes specifically |
| 9  | Jobs y SupervisorJobs | — |
| 10 | Exception Handling en Corrutinas | Tracker #29 covers try-catch/.catch but not CoroutineExceptionHandler in depth |
| 11 | Flow Operators (Intermediate vs Terminal) | — |
| 12 | Backpressure en Flow y Buffering | — |
| 13 | Select Expression en Corrutinas | — |

## Android Components & Lifecycle

| #  | Topic | Notes |
|----|-------|-------|
| 14 | Intent Filters | Tracker #47 covers intents but not filters specifically |
| 15 | Tasks y Backstack Management | — |
| 16 | Launch Modes (Standard, SingleTop, SingleTask, SingleInstance) | — |
| 17 | SavedInstanceState y Persistence de UI | Tracker #52 is Process Death, partially related |
| 18 | FragmentManager y transacciones (add vs replace) | — |
| 19 | OnActivityResult vs Activity Result API | — |
| 20 | PendingIntents y su seguridad | — |
| 21 | Permissions (Normal vs Dangerous) | — |
| 22 | Deep Links y App Links | — |
| 23 | App Startup Library | — |

## UI Development (View System & Compose)

| #  | Topic | Notes |
|----|-------|-------|
| 24 | SideEffect (the composable function) | Tracker has LaunchedEffect (#33), DisposableEffect (#34), but not SideEffect |
| 25 | Scaffolding y Slot API | Tracker #36 covers innerPadding in Scaffold, but not Slot API pattern |
| 26 | Safe Args en navegación | Tracker #43 is Navigation Compose, but Safe Args is View-system specific |
| 27 | ConstraintLayout (Chains, Guidelines, Barriers) | — |
| 28 | RecyclerView: Internals y Pool de vistas | — |
| 29 | DiffUtil vs notifyDataSetChanged | — |
| 30 | Custom Views: OnMeasure, OnLayout, OnDraw | — |
| 31 | ViewBinding vs DataBinding | — |
| 32 | Estilos, Temas y Atributos de XML | — |
| 33 | CoordinatorLayout y Behaviors | — |
| 34 | MotionLayout para animaciones complejas | — |

## Architecture & Design Patterns

| #  | Topic | Notes |
|----|-------|-------|
| 35 | Patrón Observer | — |
| 36 | Patrón Mapper (Data Entities vs Domain Models) | — |
| 37 | Patrón Decorator y Adapter | — |
| 38 | Patrón Facade y Builder | — |
| 39 | Hexagonal Architecture (conceptos básicos) | — |
| 40 | Modularización por Features (Feature modules) | — |
| 41 | Modularización por Capas (Library modules) | — |
| 42 | Comunicación entre módulos (Interfaces/Mediator) | — |
| 43 | Estrategias de Offline-first | — |

## Dependency Injection

| #  | Topic | Notes |
|----|-------|-------|
| 44 | Qualifiers y @Named | — |
| 45 | Hilt Modules y Entry Points | — |
| 46 | Constructor Injection vs Field Injection | — |
| 47 | Koin: Service Locator vs DI | — |
| 48 | Testing con Hilt (HiltAndroidRule) | — |

## Data & Networking

| #  | Topic | Notes |
|----|-------|-------|
| 49 | GraphQL (Queries, Mutations, Subscriptions) | Tracker #68 mentions GraphQL alongside REST |
| 50 | Room Migraciones | — |
| 51 | JSON Parsing (Moshi vs Kotlin Serialization) | — |
| 52 | Paging Library 3 (RemoteMediator) | — |
| 53 | Caching Strategies (Network-bound resource) | — |
| 54 | OkHttp Timeout y Retry policies | — |

## Testing & Quality

| #  | Topic | Notes |
|----|-------|-------|
| 55 | MockK (Every, verify, coEvery) | Tracker #76 covers Fakes vs Mocks generally |
| 56 | Mockito vs MockK | — |
| 57 | Fake Objects vs Stubs vs Spies (detailed) | — |
| 58 | Integration Testing (Room/API) | — |
| 59 | Compose Testing (Semantics, findByTag) | — |
| 60 | TDD (Test Driven Development) | — |
| 61 | Robolectric | — |
| 62 | Code Coverage (Jacoco) | — |
| 63 | Assertion Libraries (Truth, AssertJ) | — |
| 64 | Hermetic Testing (Pruebas sin red/DB real) | — |

## Background Tasks & System Services

| #  | Topic | Notes |
|----|-------|-------|
| 65 | WorkManager Constraints y Expedited jobs | Tracker #48 covers Services+WorkManager broadly |
| 66 | Periodic vs OneTime Work Requests | — |
| 67 | Chaining Work (Tareas encadenadas) | — |
| 68 | AlarmManager (Alarmas exactas e inexactas) | — |
| 69 | Foreground Services y notificaciones persistentes | — |
| 70 | DownloadManager | — |
| 71 | Battery Optimization (Doze Mode, App Standby) | Related to tracker #89 (Eficiencia Energética) |
| 72 | JobScheduler | — |

## Gradle & Build System

| #  | Topic | Notes |
|----|-------|-------|
| 73 | Manifest Merger | — |
| 74 | Groovy vs KTS (Kotlin DSL) | — |
| 75 | Gradle Lifecycle (Initialization, Configuration, Execution) | — |
| 76 | Gradle Plugins (Apply plugin, Custom plugins) | — |
| 77 | Multi-module Dependency Management | — |
| 78 | Gradle Caching y Build Scan | — |
| 79 | Composite Builds | — |

## GitHub & CI/CD

| #  | Topic | Notes |
|----|-------|-------|
| 80 | Runners (GitHub-hosted vs Self-hosted) | — |
| 81 | Secrets y Environment Variables | — |
| 82 | Branch Protection Rules | — |
| 83 | CI Pipeline: Build, Test, Lint, Deploy | — |
| 84 | Fastlane: Automatización de deploys | — |
| 85 | Firebase App Distribution | — |
| 86 | Semantic Versioning (SemVer) | — |
| 87 | Git Hooks (Pre-commit linting) | — |
| 88 | GitHub Packages para librerías AAR | — |
| 89 | Artifact Management | — |
| 90 | Changelog Automation | — |

## Performance & Security

| #  | Topic | Notes |
|----|-------|-------|
| 91 | Android Profiler (CPU, Memory, Network) | — |
| 92 | Image Loading (Coil vs Glide internals) | — |
| 93 | Baseline Profiles (Optimización de arranque) | — |
| 94 | App Startup Time (Cold, Warm, Hot start) | — |
| 95 | EncryptedSharedPreferences | — |
| 96 | Proguard Keep Rules | Tracker #91 covers R8/Proguard generally |
| 97 | Play Integrity API | — |
| 98 | StrictMode para detectar leaks | — |
| 99 | Benchmarking (Macrobenchmark / Microbenchmark) | — |
| 100 | Layout Inspector y Database Inspector | — |
| 101 | WebView Security y configuraciones | — |
| 102 | Binary Compatibility (Librerías) | — |

## IA & Modern Tech

| #   | Topic | Notes |
|-----|-------|-------|
| 103 | On-device AI (Gemini Nano / AICore) | — |
| 104 | Vector Databases en mobile | — |
| 105 | Kotlin Multiplatform (KMP) | — |
| 106 | Compose Multiplatform | — |

## Soft Skills & Process (Senior Level)

| #   | Topic | Notes |
|-----|-------|-------|
| 107 | Code Review best practices | — |
| 108 | Manejo de Deuda Técnica | — |
| 109 | Estimación de tareas y refinamiento | — |
| 110 | Liderazgo técnico y Mentoría | — |
| 111 | Documentación (RFCs, ADRs) | — |

---

**Total extra topics: 111**

> To promote a topic to the main tracker, follow the rules in `CLAUDE.md` under "Growing the Topic List".
> To add it as a glossary entry instead, follow the glossary rules.
