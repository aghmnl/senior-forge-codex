# Glossary Tags

Closed vocabulary of thematic tags for glossary entries. Tags are internal identifiers — English, kebab-case, never rendered as visible text — and each entry carries the **same list in the same order** in its EN and ES versions.

They feed two mechanisms:

- `_includes/related-posts.html` scores +1 per shared tag when picking related entries.
- `assets/js/data/search.json` indexes them, so the search box finds entries by concept.

## Rules

- Every entry has **2 to 4 tags**. The first is the primary axis; the rest are secondary.
- Only tags from the table below are valid. If an entry does not fit, extend the vocabulary here first and explain why in the PR.
- No tag should apply to more than ~40% of entries — a tag that matches everything discriminates nothing.
- Front matter format, on the line right after `categories:`: `tags: [state-management, concurrency, flow]`
- Tag by reading the entry, not its title.

## Vocabulary (43 tags)

| Tag | Meaning | Entries | Example entries |
|-----|---------|:-------:|-----------------|
| `android-framework` | platform components and services: Context, BroadcastReceiver, ViewModelStore, main thread | 11 | [Broadcast Receiver](../_posts/en/glossary/2026-09-02-broadcast-receiver.md), [Context](../_posts/en/glossary/2026-08-21-context-programming.md), [Hilt](../_posts/en/glossary/2026-09-02-hilt.md), [Lifecycle-Aware](../_posts/en/glossary/2026-09-02-lifecycle-aware.md) |
| `architecture` | layers, patterns for app structure (UDF, MVI, mapper, repository), SOLID at system level | 18 | [Unidirectional Data Flow](../_posts/en/glossary/2026-08-28-unidirectional-data-flow.md), [MVI Pattern](../_posts/en/glossary/2026-08-30-mvi-pattern.md), [Data Layer](../_posts/en/glossary/2026-09-04-data-layer.md), [Mapper Function](../_posts/en/glossary/2026-09-04-mapper-function.md) |
| `build-tools` | Gradle, kapt/KSP, R8/ProGuard, stubs | 9 | [Gradle Kotlin DSL](../_posts/en/glossary/2026-09-02-gradle-kotlin-dsl.md), [kapt](../_posts/en/glossary/2026-09-02-kapt.md), [KSP](../_posts/en/glossary/2026-09-02-ksp.md), [ProGuard](../_posts/en/glossary/2026-09-02-proguard.md) |
| `callbacks` | callback-style APIs, event handlers, event wiring | 7 | [Callbacks](../_posts/en/glossary/2026-09-02-callbacks.md), [Event Handlers](../_posts/en/glossary/2026-09-02-event-handlers.md), [Event Wiring](../_posts/en/glossary/2026-09-02-event-wiring.md), [Callback Hell](../_posts/en/glossary/2026-09-10-callback-hell.md) |
| `cancellation` | cooperative cancellation, CancellationException, scope teardown | 6 | [CancellationException](../_posts/en/glossary/2026-09-10-cancellation-exception.md), [Cooperative Cancellation](../_posts/en/glossary/2026-09-10-cooperative-cancellation.md), [coroutineScope (builder)](../_posts/en/glossary/2026-09-10-coroutine-scope-builder.md), [suspendCancellableCoroutine](../_posts/en/glossary/2026-09-10-suspend-cancellable-coroutine.md) |
| `collections` | List/Set/Map, their operators, builders and conversions | 43 | [Collections](../_posts/en/glossary/2026-08-28-collections.md), [Maps](../_posts/en/glossary/2026-08-28-maps.md), [Sets](../_posts/en/glossary/2026-08-28-sets.md), [Standard Library](../_posts/en/glossary/2026-09-03-standard-library.md) |
| `compiler` | what kotlinc/plugins do at compile time: transformations, generated code, checks | 30 | [Compile Time](../_posts/en/glossary/2026-08-19-compile-time.md), [Annotation Processing](../_posts/en/glossary/2026-08-28-annotation-processing.md), [Source Code](../_posts/en/glossary/2026-08-28-source-code.md), [Call Site](../_posts/en/glossary/2026-09-07-call-site.md) |
| `compose` | Jetpack Compose runtime: recomposition, snapshot system, stability, scopes | 22 | [Jetpack Compose](../_posts/en/glossary/2026-09-02-jetpack-compose.md), [@LayoutScopeMarker](../_posts/en/glossary/2026-09-02-layout-scope-marker.md), [@Composable](../_posts/en/glossary/2026-09-03-composable.md), [@Stable](../_posts/en/glossary/2026-09-03-stable.md) |
| `concurrency` | shared state across coroutines/threads, races, atomicity, thread safety | 20 | [Thread Safety](../_posts/en/glossary/2026-09-04-thread-safety.md), [Concurrency](../_posts/en/glossary/2026-09-08-concurrency.md), [Atomicity](../_posts/en/glossary/2026-09-09-atomicity.md), [Compare-and-Set (CAS)](../_posts/en/glossary/2026-09-09-compare-and-set.md) |
| `coroutines` | suspend functions, scopes, builders, continuations, dispatchers | 26 | [Async Operations](../_posts/en/glossary/2026-09-02-async-operations.md), [Coroutines](../_posts/en/glossary/2026-09-02-coroutines.md), [Suspend Functions](../_posts/en/glossary/2026-09-02-suspend-functions.md), [Continuation-Passing Style (CPS)](../_posts/en/glossary/2026-09-10-continuation-passing-style.md) |
| `data-classes` | data class machinery: equals/hashCode, copy, componentN, primary constructor | 11 | [Multiple Return Patterns](../_posts/en/glossary/2026-08-28-multiple-return-patterns.md), [Primary Constructor](../_posts/en/glossary/2026-08-28-primary-constructor.md), [equals](../_posts/en/glossary/2026-09-08-equals.md), [copy](../_posts/en/glossary/2026-09-09-copy.md) |
| `delegation` | `by`, property delegates, lazy, KProperty | 6 | [by (Delegation)](../_posts/en/glossary/2026-09-04-by-delegation.md), [KProperty](../_posts/en/glossary/2026-09-04-kproperty.md), [Property Delegate](../_posts/en/glossary/2026-09-04-property-delegate.md), [Decorator](../_posts/en/glossary/2026-08-28-decorator.md) |
| `design-patterns` | classic GoF-style patterns: singleton, decorator, DAO, mapper | 5 | [Decorator](../_posts/en/glossary/2026-08-28-decorator.md), [Singleton](../_posts/en/glossary/2026-08-28-singleton.md), [Companion Object](../_posts/en/glossary/2026-09-02-companion-object.md), [DAO](../_posts/en/glossary/2026-09-02-dao.md) |
| `design-principles` | code-level guidance: SRP, intent signaling, guard clauses, composition over inheritance | 9 | [Intent Signaling](../_posts/en/glossary/2026-08-21-intent-signaling.md), [Guard Clause](../_posts/en/glossary/2026-08-28-guard-clause.md), [Single Responsibility Principle](../_posts/en/glossary/2026-09-02-single-responsibility-principle.md), [Assertion](../_posts/en/glossary/2026-08-28-assertion.md) |
| `di` | Dagger/Hilt annotations, modules, components, dependency graph | 8 | [Dependency Graph](../_posts/en/glossary/2026-08-28-dependency-graph.md), [@Binds](../_posts/en/glossary/2026-09-02-binds.md), [Dagger](../_posts/en/glossary/2026-09-02-dagger.md), [Hilt](../_posts/en/glossary/2026-09-02-hilt.md) |
| `dispatch` | how a call is resolved: static vs virtual dispatch, vtable, overloading | 13 | [Overload Resolution](../_posts/en/glossary/2026-08-28-overload-resolution.md), [Static Dispatch](../_posts/en/glossary/2026-08-28-static-dispatch.md), [Function Overloading](../_posts/en/glossary/2026-09-02-function-overloading.md), [Virtual Dispatch](../_posts/en/glossary/2026-09-02-virtual-dispatch.md) |
| `dsl` | type-safe builders, lambdas with receiver, DSL markers | 10 | [DSL](../_posts/en/glossary/2026-08-28-dsl.md), [@DslMarker](../_posts/en/glossary/2026-09-02-dsl-marker.md), [Ktor Routing](../_posts/en/glossary/2026-09-02-ktor-routing.md), [Receiver Type](../_posts/en/glossary/2026-08-28-receiver-type.md) |
| `error-handling` | exceptions, assertions, stack traces | 6 | [Assertion](../_posts/en/glossary/2026-08-28-assertion.md), [ClassCastException](../_posts/en/glossary/2026-08-28-class-cast-exception.md), [Stack Trace](../_posts/en/glossary/2026-08-28-stack-trace.md), [Cast](../_posts/en/glossary/2026-08-28-cast.md) |
| `flow` | StateFlow/SharedFlow and Flow operators | 7 | [StateFlow](../_posts/en/glossary/2026-08-30-stateflow.md), [asStateFlow](../_posts/en/glossary/2026-09-09-as-state-flow.md), [Conflation](../_posts/en/glossary/2026-09-09-conflation.md), [distinctUntilChanged](../_posts/en/glossary/2026-09-09-distinct-until-changed.md) |
| `functional` | lambdas-as-values, pure transformations, pipelines, operator chains | 17 | [Data Transformation](../_posts/en/glossary/2026-08-21-data-transformation.md), [Functional Style](../_posts/en/glossary/2026-09-04-functional-style.md), [Pipeline](../_posts/en/glossary/2026-09-04-pipeline.md), [Extension Functions](../_posts/en/glossary/2026-08-28-extension-functions.md) |
| `generics` | type parameters, variance, erasure, projections, bounds | 18 | [Generic Type Parameters](../_posts/en/glossary/2026-08-28-generic-type-parameters.md), [Reified](../_posts/en/glossary/2026-08-28-reified.md), [Type Erasure](../_posts/en/glossary/2026-09-02-type-erasure.md), [Contravariance](../_posts/en/glossary/2026-09-07-contravariance.md) |
| `immutability` | read-only vs mutable, value vs reference, defensive copies, persistent structures | 30 | [Mutation](../_posts/en/glossary/2026-08-28-mutation.md), [Immutability](../_posts/en/glossary/2026-09-04-immutability.md), [Defensive Copy](../_posts/en/glossary/2026-09-08-defensive-copy.md), [Structural Sharing](../_posts/en/glossary/2026-09-09-structural-sharing.md) |
| `inlining` | inline/noinline/crossinline, reified, call-site copying, code bloat | 8 | [Inline Functions](../_posts/en/glossary/2026-08-28-inline-functions.md), [Code Bloat](../_posts/en/glossary/2026-09-02-code-bloat.md), [Crossinline](../_posts/en/glossary/2026-09-02-crossinline.md), [Noinline](../_posts/en/glossary/2026-09-02-noinline.md) |
| `interop` | Kotlin/Java boundary: @Jvm* annotations, platform types, raw types | 6 | [@JvmStatic](../_posts/en/glossary/2026-09-02-jvm-static.md), [@JvmOverloads](../_posts/en/glossary/2026-09-07-jvm-overloads.md), [NullPointerException](../_posts/en/glossary/2026-08-28-null-pointer-exception.md), [Companion Object](../_posts/en/glossary/2026-09-02-companion-object.md) |
| `jvm` | JVM-level facts: bytecode, heap/stack, erasure, static methods | 19 | [Bytecode](../_posts/en/glossary/2026-08-28-bytecode.md), [JVM](../_posts/en/glossary/2026-08-28-jvm.md), [Primitives](../_posts/en/glossary/2026-08-28-primitives.md), [Stack Frame](../_posts/en/glossary/2026-09-08-stack-frame.md) |
| `lambdas` | lambda expressions, higher-order functions, receivers | 12 | [Lambdas](../_posts/en/glossary/2026-08-28-lambdas.md), [Receiver Type](../_posts/en/glossary/2026-08-28-receiver-type.md), [Lambda with Receiver](../_posts/en/glossary/2026-09-02-lambda-with-receiver.md), [DSL](../_posts/en/glossary/2026-08-28-dsl.md) |
| `lifecycle` | Android lifecycles and the scopes tied to them (ViewModel, back stack, composition) | 12 | [Lifecycle-Aware](../_posts/en/glossary/2026-09-02-lifecycle-aware.md), [Lifecycle Event](../_posts/en/glossary/2026-09-02-lifecycle-event.md), [ViewModelStore](../_posts/en/glossary/2026-09-04-viewmodel-store.md), [Scope](../_posts/en/glossary/2026-08-21-scope.md) |
| `memory` | allocations, heap, GC, leaks, boxing | 20 | [Garbage Collector (GC)](../_posts/en/glossary/2026-05-04-garbage-collector.md), [Allocations](../_posts/en/glossary/2026-08-30-allocations.md), [Autoboxing](../_posts/en/glossary/2026-09-02-autoboxing.md), [Heap](../_posts/en/glossary/2026-09-02-heap.md) |
| `navigation` | Navigation Component, back stack, Safe Args | 4 | [Navigation Component](../_posts/en/glossary/2026-09-02-navigation-component.md), [Safe Args](../_posts/en/glossary/2026-09-02-safe-args.md), [Back Stack](../_posts/en/glossary/2026-09-04-back-stack.md), [ViewModelStore](../_posts/en/glossary/2026-09-04-viewmodel-store.md) |
| `null-safety` | nullable types, safe call, Elvis, NPE avoidance | 5 | [NullPointerException](../_posts/en/glossary/2026-08-28-null-pointer-exception.md), [Safe Call](../_posts/en/glossary/2026-08-28-safe-call.md), [Assertion](../_posts/en/glossary/2026-08-28-assertion.md), [Guard Clause](../_posts/en/glossary/2026-08-28-guard-clause.md) |
| `oop` | classes, inheritance, abstraction, polymorphism, visibility | 15 | [Polymorphism](../_posts/en/glossary/2026-08-19-polymorphism.md), [Inheritance](../_posts/en/glossary/2026-08-28-inheritance.md), [Abstract Class](../_posts/en/glossary/2026-08-30-abstract-class.md), [Constructor](../_posts/en/glossary/2026-08-30-constructor.md) |
| `performance` | cost, overhead, hot paths, complexity | 33 | [Hot Loops](../_posts/en/glossary/2026-09-02-hot-loops.md), [Round-Trip](../_posts/en/glossary/2026-09-02-round-trip.md), [Overhead](../_posts/en/glossary/2026-09-04-overhead.md), [Garbage Collector (GC)](../_posts/en/glossary/2026-05-04-garbage-collector.md) |
| `persistence` | Room, DAOs, DataStore and data-layer storage | 4 | [DAO](../_posts/en/glossary/2026-09-02-dao.md), [Room](../_posts/en/glossary/2026-09-02-room.md), [Round-Trip](../_posts/en/glossary/2026-09-02-round-trip.md), [Data Layer](../_posts/en/glossary/2026-09-04-data-layer.md) |
| `reflection` | KClass/KProperty, runtime reflection, keep rules | 5 | [Runtime Reflection](../_posts/en/glossary/2026-08-28-runtime-reflection.md), [Moshi](../_posts/en/glossary/2026-09-02-moshi.md), [ProGuard](../_posts/en/glossary/2026-09-02-proguard.md), [R8](../_posts/en/glossary/2026-09-02-r8.md) |
| `runtime` | ART/JVM execution: JIT, AOT, PGO, reflection at run time | 7 | [Runtime](../_posts/en/glossary/2026-08-19-runtime.md), [AOT Compilation](../_posts/en/glossary/2026-08-28-aot-compilation.md), [JIT Compilation](../_posts/en/glossary/2026-08-28-jit-compilation.md), [Profile-Guided Optimization (PGO)](../_posts/en/glossary/2026-08-28-pgo.md) |
| `scoping` | visibility and receiver scope: scope, this@label, DslMarker, nested receivers | 9 | [Context](../_posts/en/glossary/2026-08-21-context-programming.md), [Scope](../_posts/en/glossary/2026-08-21-scope.md), [this@label](../_posts/en/glossary/2026-09-02-this-at-label.md), [Receiver Type](../_posts/en/glossary/2026-08-28-receiver-type.md) |
| `sealed-types` | sealed hierarchies, ADTs, exhaustiveness, `when` over closed sets | 9 | [Sealed Hierarchy](../_posts/en/glossary/2026-08-28-sealed-hierarchy.md), [Algebraic Data Types (ADTs)](../_posts/en/glossary/2026-08-30-algebraic-data-types.md), [Exhaustiveness](../_posts/en/glossary/2026-09-02-exhaustiveness.md), [when Expression](../_posts/en/glossary/2026-08-19-when-expression.md) |
| `serialization` | JSON/argument (de)serialization: Moshi, kotlinx.serialization, Safe Args | 2 | [Moshi](../_posts/en/glossary/2026-09-02-moshi.md), [Safe Args](../_posts/en/glossary/2026-09-02-safe-args.md) |
| `state-management` | UI state holders, state transitions, emission, derived state | 31 | [State Transitions](../_posts/en/glossary/2026-08-28-state-transitions.md), [State Emission Patterns](../_posts/en/glossary/2026-08-30-state-emission-patterns.md), [Observable State](../_posts/en/glossary/2026-09-04-observable-state.md), [State Holder](../_posts/en/glossary/2026-09-04-state-holder.md) |
| `syntax` | language constructs and sugar: keywords, operators, `when`, destructuring | 23 | [when Expression](../_posts/en/glossary/2026-08-19-when-expression.md), [Destructuring](../_posts/en/glossary/2026-08-28-destructuring.md), [Extension Functions](../_posts/en/glossary/2026-08-28-extension-functions.md), [Extension](../_posts/en/glossary/2026-08-28-extension.md) |
| `testing` | JUnit, fakes, test dispatchers, mockability | 4 | [@Before](../_posts/en/glossary/2026-09-02-junit-before.md), [@Inject](../_posts/en/glossary/2026-09-02-inject.md), [Single Responsibility Principle](../_posts/en/glossary/2026-09-02-single-responsibility-principle.md), [runBlocking](../_posts/en/glossary/2026-09-10-run-blocking.md) |
| `threading` | OS threads, main thread, pools, blocking calls, locks | 11 | [LazyThreadSafetyMode](../_posts/en/glossary/2026-09-02-lazy-thread-safety-mode.md), [Synchronized Block](../_posts/en/glossary/2026-09-02-synchronized-block.md), [Blocking Call](../_posts/en/glossary/2026-09-10-blocking-call.md), [Main Thread](../_posts/en/glossary/2026-09-10-main-thread.md) |
| `type-system` | static typing, inference, casts, type safety, return types | 16 | [Cast](../_posts/en/glossary/2026-08-28-cast.md), [Type Inference](../_posts/en/glossary/2026-08-28-type-inference.md), [Type Safety](../_posts/en/glossary/2026-09-02-type-safety.md), [Return Type](../_posts/en/glossary/2026-09-07-return-type.md) |

## Notes on scope boundaries

- `concurrency` is the *problem* (shared state, races, atomicity); `threading` is the OS-level *mechanism* (threads, pools, blocking, locks); `coroutines` is the Kotlin *abstraction*. An entry can carry two of them when it bridges levels (e.g. `blocking-call`).
- `cancellation` was split out of `coroutines` because cancellation semantics (cooperative checks, `CancellationException`, scope teardown) form a coherent cluster that related-posts should surface together.
- `architecture` covers app-level structure (layers, UDF, MVI); `design-patterns` covers named object-level patterns (Singleton, Decorator, DAO); `design-principles` covers code-level guidance (SRP, guard clauses, intent signaling).
- `compiler` is what kotlinc and its plugins *do* (transformations, generated code, checks); `build-tools` is the toolchain around it (Gradle, kapt/KSP, R8); `jvm` is the platform model the output targets; `runtime` is execution-time behaviour (ART, JIT, AOT, reflection).
- `sealed-types` is deliberately broader than sealed classes: it also holds ADTs, exhaustiveness and `when` over closed sets, because those entries always link to each other.
- `serialization` was added beyond the initial axis list because Moshi and Safe Args did not fit any existing tag without stretching it; it will also hold future kotlinx.serialization / Parcelable entries.

## Full assignment

| Entry | Tags |
|-------|------|
| [@Before](../_posts/en/glossary/2026-09-02-junit-before.md) | `testing`, `lifecycle` |
| [@Binds](../_posts/en/glossary/2026-09-02-binds.md) | `di`, `compiler` |
| [@Composable](../_posts/en/glossary/2026-09-03-composable.md) | `compose`, `compiler` |
| [@DslMarker](../_posts/en/glossary/2026-09-02-dsl-marker.md) | `dsl`, `scoping`, `compose` |
| [@Inject](../_posts/en/glossary/2026-09-02-inject.md) | `di`, `testing` |
| [@InstallIn](../_posts/en/glossary/2026-09-02-install-in.md) | `di`, `scoping` |
| [@JvmOverloads](../_posts/en/glossary/2026-09-07-jvm-overloads.md) | `interop`, `dispatch`, `android-framework` |
| [@JvmStatic](../_posts/en/glossary/2026-09-02-jvm-static.md) | `interop`, `jvm`, `dispatch` |
| [@LayoutScopeMarker](../_posts/en/glossary/2026-09-02-layout-scope-marker.md) | `compose`, `dsl`, `scoping` |
| [@Module](../_posts/en/glossary/2026-09-02-module-annotation.md) | `di`, `architecture` |
| [@Stable](../_posts/en/glossary/2026-09-03-stable.md) | `compose`, `immutability`, `performance` |
| [Abstract Class](../_posts/en/glossary/2026-08-30-abstract-class.md) | `oop`, `sealed-types` |
| [add](../_posts/en/glossary/2026-09-08-add.md) | `collections`, `performance` |
| [Algebraic Data Types (ADTs)](../_posts/en/glossary/2026-08-30-algebraic-data-types.md) | `sealed-types`, `type-system`, `state-management` |
| [Allocations](../_posts/en/glossary/2026-08-30-allocations.md) | `memory`, `performance`, `jvm` |
| [Android Runtime (ART)](../_posts/en/glossary/2026-09-02-android-runtime.md) | `runtime`, `memory`, `performance` |
| [Annotation Processing](../_posts/en/glossary/2026-08-28-annotation-processing.md) | `compiler`, `build-tools`, `di` |
| [AOT Compilation](../_posts/en/glossary/2026-08-28-aot-compilation.md) | `runtime`, `performance`, `compiler` |
| [ArrayList](../_posts/en/glossary/2026-09-08-arraylist.md) | `collections`, `performance`, `memory` |
| [asSequence](../_posts/en/glossary/2026-09-08-as-sequence.md) | `collections`, `functional`, `performance` |
| [Assertion](../_posts/en/glossary/2026-08-28-assertion.md) | `error-handling`, `null-safety`, `design-principles` |
| [asStateFlow](../_posts/en/glossary/2026-09-09-as-state-flow.md) | `flow`, `state-management`, `architecture` |
| [Async Operations](../_posts/en/glossary/2026-09-02-async-operations.md) | `coroutines`, `concurrency`, `callbacks` |
| [Atomicity](../_posts/en/glossary/2026-09-09-atomicity.md) | `concurrency`, `state-management`, `immutability` |
| [Autoboxing](../_posts/en/glossary/2026-09-02-autoboxing.md) | `memory`, `jvm`, `performance` |
| [Back Stack](../_posts/en/glossary/2026-09-04-back-stack.md) | `navigation`, `lifecycle`, `android-framework` |
| [Backing Field](../_posts/en/glossary/2026-09-03-backing-field.md) | `syntax`, `delegation`, `state-management` |
| [Blocking Call](../_posts/en/glossary/2026-09-10-blocking-call.md) | `threading`, `coroutines`, `performance` |
| [Broadcast Receiver](../_posts/en/glossary/2026-09-02-broadcast-receiver.md) | `android-framework`, `callbacks`, `lifecycle` |
| [Builder Functions](../_posts/en/glossary/2026-09-08-builder-functions.md) | `collections`, `immutability`, `lambdas` |
| [buildList](../_posts/en/glossary/2026-09-08-build-list.md) | `collections`, `immutability`, `inlining` |
| [buildMap](../_posts/en/glossary/2026-09-08-build-map.md) | `collections`, `immutability` |
| [by (Delegation)](../_posts/en/glossary/2026-09-04-by-delegation.md) | `delegation`, `syntax`, `compose` |
| [Bytecode](../_posts/en/glossary/2026-08-28-bytecode.md) | `jvm`, `compiler` |
| [Call Site](../_posts/en/glossary/2026-09-07-call-site.md) | `compiler`, `inlining`, `generics` |
| [Callback Hell](../_posts/en/glossary/2026-09-10-callback-hell.md) | `callbacks`, `coroutines` |
| [Callbacks](../_posts/en/glossary/2026-09-02-callbacks.md) | `callbacks`, `lambdas`, `coroutines` |
| [CancellationException](../_posts/en/glossary/2026-09-10-cancellation-exception.md) | `cancellation`, `coroutines`, `error-handling` |
| [Cast](../_posts/en/glossary/2026-08-28-cast.md) | `type-system`, `syntax`, `error-handling` |
| [ClassCastException](../_posts/en/glossary/2026-08-28-class-cast-exception.md) | `error-handling`, `type-system`, `generics` |
| [clear](../_posts/en/glossary/2026-09-08-clear.md) | `collections`, `state-management`, `concurrency` |
| [Code Bloat](../_posts/en/glossary/2026-09-02-code-bloat.md) | `inlining`, `performance`, `build-tools` |
| [Collection Operators](../_posts/en/glossary/2026-09-04-collection-operators.md) | `collections`, `functional` |
| [Collections](../_posts/en/glossary/2026-08-28-collections.md) | `collections`, `immutability` |
| [Companion Object](../_posts/en/glossary/2026-09-02-companion-object.md) | `syntax`, `interop`, `design-patterns` |
| [Compare-and-Set (CAS)](../_posts/en/glossary/2026-09-09-compare-and-set.md) | `concurrency`, `threading`, `state-management` |
| [Compile Time](../_posts/en/glossary/2026-08-19-compile-time.md) | `compiler`, `type-system` |
| [Composition Lifetime](../_posts/en/glossary/2026-09-04-composition-lifetime.md) | `compose`, `lifecycle`, `state-management` |
| [Concurrency](../_posts/en/glossary/2026-09-08-concurrency.md) | `concurrency`, `immutability`, `coroutines` |
| [Conflation](../_posts/en/glossary/2026-09-09-conflation.md) | `flow`, `state-management` |
| [Constructor](../_posts/en/glossary/2026-08-30-constructor.md) | `oop`, `data-classes`, `syntax` |
| [contains](../_posts/en/glossary/2026-09-08-contains.md) | `collections`, `performance` |
| [Context](../_posts/en/glossary/2026-08-21-context-programming.md) | `scoping`, `android-framework`, `coroutines` |
| [Continuation](../_posts/en/glossary/2026-09-10-continuation.md) | `coroutines`, `compiler`, `memory` |
| [Continuation-Passing Style (CPS)](../_posts/en/glossary/2026-09-10-continuation-passing-style.md) | `coroutines`, `compiler` |
| [Contravariance](../_posts/en/glossary/2026-09-07-contravariance.md) | `generics`, `type-system` |
| [Cooperative Cancellation](../_posts/en/glossary/2026-09-10-cooperative-cancellation.md) | `cancellation`, `coroutines` |
| [copy](../_posts/en/glossary/2026-09-09-copy.md) | `data-classes`, `immutability`, `state-management` |
| [Coroutines](../_posts/en/glossary/2026-09-02-coroutines.md) | `coroutines`, `concurrency`, `lifecycle` |
| [coroutineScope (builder)](../_posts/en/glossary/2026-09-10-coroutine-scope-builder.md) | `coroutines`, `concurrency`, `cancellation` |
| [Covariance](../_posts/en/glossary/2026-09-07-covariance.md) | `generics`, `type-system`, `immutability` |
| [Crossinline](../_posts/en/glossary/2026-09-02-crossinline.md) | `inlining`, `lambdas` |
| [Dagger](../_posts/en/glossary/2026-09-02-dagger.md) | `di`, `compiler`, `architecture` |
| [DAO](../_posts/en/glossary/2026-09-02-dao.md) | `persistence`, `design-patterns`, `coroutines` |
| [Data Layer](../_posts/en/glossary/2026-09-04-data-layer.md) | `architecture`, `persistence` |
| [Data Transformation](../_posts/en/glossary/2026-08-21-data-transformation.md) | `functional`, `architecture`, `collections` |
| [Decorator](../_posts/en/glossary/2026-08-28-decorator.md) | `design-patterns`, `oop`, `delegation` |
| [Defensive Copy](../_posts/en/glossary/2026-09-08-defensive-copy.md) | `immutability`, `collections`, `concurrency` |
| [Dependency Graph](../_posts/en/glossary/2026-08-28-dependency-graph.md) | `di`, `architecture`, `compiler` |
| [Derived State](../_posts/en/glossary/2026-09-09-derived-state.md) | `state-management`, `data-classes`, `compose` |
| [Destructuring](../_posts/en/glossary/2026-08-28-destructuring.md) | `syntax`, `data-classes` |
| [Dispatcher](../_posts/en/glossary/2026-09-10-dispatcher.md) | `coroutines`, `threading` |
| [distinctUntilChanged](../_posts/en/glossary/2026-09-09-distinct-until-changed.md) | `flow`, `state-management`, `immutability` |
| [DSL](../_posts/en/glossary/2026-08-28-dsl.md) | `dsl`, `lambdas`, `syntax` |
| [equals](../_posts/en/glossary/2026-09-08-equals.md) | `data-classes`, `collections`, `compose` |
| [Event Handlers](../_posts/en/glossary/2026-09-02-event-handlers.md) | `callbacks`, `compose`, `state-management` |
| [Event Wiring](../_posts/en/glossary/2026-09-02-event-wiring.md) | `callbacks`, `compose`, `architecture` |
| [Exhaustiveness](../_posts/en/glossary/2026-09-02-exhaustiveness.md) | `sealed-types`, `compiler`, `state-management` |
| [Extension](../_posts/en/glossary/2026-08-28-extension.md) | `syntax`, `oop`, `design-principles` |
| [Extension Functions](../_posts/en/glossary/2026-08-28-extension-functions.md) | `syntax`, `dispatch`, `functional` |
| [filter](../_posts/en/glossary/2026-09-08-filter.md) | `collections`, `functional`, `performance` |
| [Final](../_posts/en/glossary/2026-09-02-final.md) | `oop`, `dispatch`, `performance` |
| [Function Overloading](../_posts/en/glossary/2026-09-02-function-overloading.md) | `dispatch`, `syntax`, `interop` |
| [Functional Style](../_posts/en/glossary/2026-09-04-functional-style.md) | `functional`, `immutability`, `collections` |
| [Garbage Collector (GC)](../_posts/en/glossary/2026-05-04-garbage-collector.md) | `memory`, `jvm`, `performance` |
| [Generic Type Parameters](../_posts/en/glossary/2026-08-28-generic-type-parameters.md) | `generics`, `type-system`, `jvm` |
| [Gradle Kotlin DSL](../_posts/en/glossary/2026-09-02-gradle-kotlin-dsl.md) | `build-tools`, `dsl`, `lambdas` |
| [groupBy](../_posts/en/glossary/2026-09-08-group-by.md) | `collections`, `functional`, `performance` |
| [Guard Clause](../_posts/en/glossary/2026-08-28-guard-clause.md) | `design-principles`, `null-safety`, `syntax` |
| [Heap](../_posts/en/glossary/2026-09-02-heap.md) | `memory`, `jvm` |
| [Hilt](../_posts/en/glossary/2026-09-02-hilt.md) | `di`, `android-framework`, `compiler` |
| [Hot Loops](../_posts/en/glossary/2026-09-02-hot-loops.md) | `performance`, `memory`, `compose` |
| [Immutability](../_posts/en/glossary/2026-09-04-immutability.md) | `immutability`, `functional`, `concurrency` |
| [Inheritance](../_posts/en/glossary/2026-08-28-inheritance.md) | `oop`, `design-principles` |
| [Inline Functions](../_posts/en/glossary/2026-08-28-inline-functions.md) | `inlining`, `lambdas`, `performance` |
| [IntArray](../_posts/en/glossary/2026-09-02-intarray.md) | `memory`, `performance`, `collections` |
| [Intent Signaling](../_posts/en/glossary/2026-08-21-intent-signaling.md) | `design-principles`, `syntax` |
| [Invariance](../_posts/en/glossary/2026-09-07-invariance.md) | `generics`, `type-system` |
| [Jetpack Compose](../_posts/en/glossary/2026-09-02-jetpack-compose.md) | `compose`, `dsl`, `lambdas` |
| [JIT Compilation](../_posts/en/glossary/2026-08-28-jit-compilation.md) | `runtime`, `performance`, `jvm` |
| [JVM](../_posts/en/glossary/2026-08-28-jvm.md) | `jvm`, `runtime` |
| [kapt](../_posts/en/glossary/2026-09-02-kapt.md) | `build-tools`, `compiler` |
| [Keyword](../_posts/en/glossary/2026-09-03-keyword.md) | `syntax`, `compiler` |
| [KProperty](../_posts/en/glossary/2026-09-04-kproperty.md) | `delegation`, `reflection` |
| [KSP](../_posts/en/glossary/2026-09-02-ksp.md) | `build-tools`, `compiler` |
| [Ktor Routing](../_posts/en/glossary/2026-09-02-ktor-routing.md) | `dsl`, `lambdas`, `coroutines` |
| [Lambda with Receiver](../_posts/en/glossary/2026-09-02-lambda-with-receiver.md) | `lambdas`, `dsl`, `scoping` |
| [Lambdas](../_posts/en/glossary/2026-08-28-lambdas.md) | `lambdas`, `functional`, `memory` |
| [LazyThreadSafetyMode](../_posts/en/glossary/2026-09-02-lazy-thread-safety-mode.md) | `threading`, `delegation`, `concurrency` |
| [Lifecycle Event](../_posts/en/glossary/2026-09-02-lifecycle-event.md) | `lifecycle`, `android-framework` |
| [Lifecycle-Aware](../_posts/en/glossary/2026-09-02-lifecycle-aware.md) | `lifecycle`, `android-framework`, `coroutines` |
| [List](../_posts/en/glossary/2026-09-08-list.md) | `collections`, `immutability`, `generics` |
| [listOf](../_posts/en/glossary/2026-09-08-list-of.md) | `collections`, `immutability` |
| [Main Thread](../_posts/en/glossary/2026-09-10-main-thread.md) | `threading`, `android-framework`, `performance` |
| [map (Operator)](../_posts/en/glossary/2026-09-08-map-operator.md) | `collections`, `functional`, `architecture` |
| [mapOf](../_posts/en/glossary/2026-09-08-map-of.md) | `collections`, `generics` |
| [Mapper Function](../_posts/en/glossary/2026-09-04-mapper-function.md) | `architecture`, `functional` |
| [Mapper Pattern](../_posts/en/glossary/2026-09-04-mapper-pattern.md) | `architecture`, `design-patterns`, `functional` |
| [Maps](../_posts/en/glossary/2026-08-28-maps.md) | `collections`, `data-classes` |
| [Memory Leaks](../_posts/en/glossary/2026-09-02-memory-leaks.md) | `memory`, `lifecycle`, `android-framework` |
| [Method Dispatch](../_posts/en/glossary/2026-09-07-method-dispatch.md) | `dispatch`, `oop`, `jvm` |
| [Moshi](../_posts/en/glossary/2026-09-02-moshi.md) | `serialization`, `compiler`, `reflection` |
| [Multiple Return Patterns](../_posts/en/glossary/2026-08-28-multiple-return-patterns.md) | `data-classes`, `syntax`, `design-principles` |
| [MutableList](../_posts/en/glossary/2026-09-08-mutable-list.md) | `collections`, `immutability`, `concurrency` |
| [MutableMap](../_posts/en/glossary/2026-09-08-mutable-map.md) | `collections`, `generics` |
| [MutableSet](../_posts/en/glossary/2026-09-08-mutable-set.md) | `collections`, `immutability` |
| [mutableStateListOf](../_posts/en/glossary/2026-09-08-mutable-state-list-of.md) | `compose`, `collections`, `state-management` |
| [Mutation](../_posts/en/glossary/2026-08-28-mutation.md) | `immutability`, `collections`, `state-management` |
| [MVI Pattern](../_posts/en/glossary/2026-08-30-mvi-pattern.md) | `architecture`, `state-management`, `sealed-types` |
| [Navigation Component](../_posts/en/glossary/2026-09-02-navigation-component.md) | `navigation`, `android-framework`, `lifecycle` |
| [Noinline](../_posts/en/glossary/2026-09-02-noinline.md) | `inlining`, `lambdas`, `memory` |
| [NullPointerException](../_posts/en/glossary/2026-08-28-null-pointer-exception.md) | `null-safety`, `error-handling`, `interop` |
| [Object-Oriented Programming](../_posts/en/glossary/2026-09-07-object-oriented-programming.md) | `oop`, `design-principles` |
| [Observable State](../_posts/en/glossary/2026-09-04-observable-state.md) | `state-management`, `compose`, `flow` |
| [Operator Overloading](../_posts/en/glossary/2026-09-02-operator-overloading.md) | `syntax`, `dsl`, `dispatch` |
| [Overhead](../_posts/en/glossary/2026-09-04-overhead.md) | `performance`, `memory` |
| [Overload Resolution](../_posts/en/glossary/2026-08-28-overload-resolution.md) | `dispatch`, `compiler`, `type-system` |
| [Persistent Collections](../_posts/en/glossary/2026-09-08-persistent-collections.md) | `collections`, `immutability`, `compose` |
| [Pipeline](../_posts/en/glossary/2026-09-04-pipeline.md) | `functional`, `architecture`, `collections` |
| [Polymorphism](../_posts/en/glossary/2026-08-19-polymorphism.md) | `oop`, `dispatch`, `generics` |
| [Primary Constructor](../_posts/en/glossary/2026-08-28-primary-constructor.md) | `data-classes`, `oop`, `syntax` |
| [Primitives](../_posts/en/glossary/2026-08-28-primitives.md) | `jvm`, `memory`, `performance` |
| [Profile-Guided Optimization (PGO)](../_posts/en/glossary/2026-08-28-pgo.md) | `runtime`, `performance`, `build-tools` |
| [ProGuard](../_posts/en/glossary/2026-09-02-proguard.md) | `build-tools`, `reflection` |
| [Property Delegate](../_posts/en/glossary/2026-09-04-property-delegate.md) | `delegation`, `syntax`, `memory` |
| [Protected State](../_posts/en/glossary/2026-08-30-protected-state.md) | `oop`, `sealed-types`, `scoping` |
| [put](../_posts/en/glossary/2026-09-08-put.md) | `collections`, `immutability` |
| [R8](../_posts/en/glossary/2026-09-02-r8.md) | `build-tools`, `reflection`, `performance` |
| [Race Condition](../_posts/en/glossary/2026-09-09-race-condition.md) | `concurrency`, `state-management`, `coroutines` |
| [Raw Types](../_posts/en/glossary/2026-09-07-raw-types.md) | `generics`, `interop`, `type-system` |
| [Read-Only View](../_posts/en/glossary/2026-09-08-read-only-view.md) | `collections`, `immutability`, `generics` |
| [Receiver Type](../_posts/en/glossary/2026-08-28-receiver-type.md) | `lambdas`, `dsl`, `scoping` |
| [Recomposition](../_posts/en/glossary/2026-09-09-recomposition.md) | `compose`, `state-management`, `immutability` |
| [Reified](../_posts/en/glossary/2026-08-28-reified.md) | `generics`, `inlining`, `compiler` |
| [remove](../_posts/en/glossary/2026-09-08-remove.md) | `collections`, `data-classes` |
| [Return Type](../_posts/en/glossary/2026-09-07-return-type.md) | `type-system`, `generics`, `syntax` |
| [Room](../_posts/en/glossary/2026-09-02-room.md) | `persistence`, `compiler`, `coroutines` |
| [Round-Trip](../_posts/en/glossary/2026-09-02-round-trip.md) | `performance`, `architecture`, `persistence` |
| [runBlocking](../_posts/en/glossary/2026-09-10-run-blocking.md) | `coroutines`, `threading`, `testing` |
| [Runtime](../_posts/en/glossary/2026-08-19-runtime.md) | `runtime`, `jvm`, `compiler` |
| [Runtime Reflection](../_posts/en/glossary/2026-08-28-runtime-reflection.md) | `reflection`, `runtime`, `performance` |
| [Safe Args](../_posts/en/glossary/2026-09-02-safe-args.md) | `navigation`, `serialization`, `compiler` |
| [Safe Call](../_posts/en/glossary/2026-08-28-safe-call.md) | `null-safety`, `syntax` |
| [Scope](../_posts/en/glossary/2026-08-21-scope.md) | `scoping`, `syntax`, `lifecycle` |
| [Sealed Hierarchy](../_posts/en/glossary/2026-08-28-sealed-hierarchy.md) | `sealed-types`, `oop`, `state-management` |
| [Sequences](../_posts/en/glossary/2026-09-08-sequences.md) | `collections`, `functional`, `performance` |
| [setOf](../_posts/en/glossary/2026-09-08-set-of.md) | `collections`, `immutability`, `compose` |
| [Sets](../_posts/en/glossary/2026-08-28-sets.md) | `collections`, `data-classes` |
| [Single Responsibility Principle](../_posts/en/glossary/2026-09-02-single-responsibility-principle.md) | `design-principles`, `architecture`, `testing` |
| [Single Source of Truth](../_posts/en/glossary/2026-09-09-single-source-of-truth.md) | `state-management`, `architecture`, `design-principles` |
| [Singleton](../_posts/en/glossary/2026-08-28-singleton.md) | `design-patterns`, `oop`, `memory` |
| [Slot Table](../_posts/en/glossary/2026-09-04-slot-table.md) | `compose`, `state-management`, `memory` |
| [Snapshot State List](../_posts/en/glossary/2026-09-08-snapshot-state-list.md) | `compose`, `collections`, `state-management` |
| [Snapshot System](../_posts/en/glossary/2026-09-04-snapshot-system.md) | `compose`, `state-management`, `concurrency` |
| [sorted](../_posts/en/glossary/2026-09-08-sorted.md) | `collections`, `performance`, `functional` |
| [Source Code](../_posts/en/glossary/2026-08-28-source-code.md) | `compiler`, `jvm` |
| [Stack Frame](../_posts/en/glossary/2026-09-08-stack-frame.md) | `jvm`, `memory`, `concurrency` |
| [Stack Trace](../_posts/en/glossary/2026-08-28-stack-trace.md) | `error-handling`, `jvm`, `coroutines` |
| [Standard Library](../_posts/en/glossary/2026-09-03-standard-library.md) | `collections`, `functional`, `inlining` |
| [Star Projection](../_posts/en/glossary/2026-09-07-star-projection.md) | `generics`, `type-system` |
| [State Emission Patterns](../_posts/en/glossary/2026-08-30-state-emission-patterns.md) | `state-management`, `flow`, `concurrency` |
| [State Holder](../_posts/en/glossary/2026-09-04-state-holder.md) | `state-management`, `compose`, `architecture` |
| [State Machine (Coroutines)](../_posts/en/glossary/2026-09-10-state-machine.md) | `coroutines`, `compiler`, `jvm` |
| [State Transitions](../_posts/en/glossary/2026-08-28-state-transitions.md) | `state-management`, `sealed-types`, `architecture` |
| [StateFlow](../_posts/en/glossary/2026-08-30-stateflow.md) | `flow`, `state-management`, `compose` |
| [Static Dispatch](../_posts/en/glossary/2026-08-28-static-dispatch.md) | `dispatch`, `compiler`, `performance` |
| [Structural Sharing](../_posts/en/glossary/2026-09-09-structural-sharing.md) | `immutability`, `memory`, `collections` |
| [Stubs](../_posts/en/glossary/2026-09-02-stubs.md) | `build-tools`, `compiler` |
| [Subclass](../_posts/en/glossary/2026-09-07-subclass.md) | `oop`, `dispatch` |
| [Suspend Functions](../_posts/en/glossary/2026-09-02-suspend-functions.md) | `coroutines`, `concurrency`, `compiler` |
| [suspendCancellableCoroutine](../_posts/en/glossary/2026-09-10-suspend-cancellable-coroutine.md) | `coroutines`, `callbacks`, `cancellation` |
| [Suspension Point](../_posts/en/glossary/2026-09-10-suspension-point.md) | `coroutines`, `cancellation`, `threading` |
| [Synchronized Block](../_posts/en/glossary/2026-09-02-synchronized-block.md) | `threading`, `concurrency`, `performance` |
| [Syntax Sugar](../_posts/en/glossary/2026-08-28-syntax-sugar.md) | `syntax`, `compiler` |
| [Terminal Operations](../_posts/en/glossary/2026-09-08-terminal-operations.md) | `collections`, `functional`, `performance` |
| [this@label](../_posts/en/glossary/2026-09-02-this-at-label.md) | `scoping`, `dsl`, `syntax` |
| [Thread](../_posts/en/glossary/2026-09-10-thread.md) | `threading`, `concurrency`, `memory` |
| [Thread Pool](../_posts/en/glossary/2026-09-10-thread-pool.md) | `threading`, `coroutines` |
| [Thread Safety](../_posts/en/glossary/2026-09-04-thread-safety.md) | `concurrency`, `immutability`, `threading` |
| [toList](../_posts/en/glossary/2026-09-08-to-list.md) | `collections`, `immutability` |
| [toMutableList](../_posts/en/glossary/2026-09-08-to-mutable-list.md) | `collections`, `immutability` |
| [toSet](../_posts/en/glossary/2026-09-08-to-set.md) | `collections`, `performance` |
| [Type Erasure](../_posts/en/glossary/2026-09-02-type-erasure.md) | `generics`, `jvm`, `compiler` |
| [Type Inference](../_posts/en/glossary/2026-08-28-type-inference.md) | `type-system`, `compiler` |
| [Type Safety](../_posts/en/glossary/2026-09-02-type-safety.md) | `type-system`, `null-safety`, `sealed-types` |
| [Unidirectional Data Flow](../_posts/en/glossary/2026-08-28-unidirectional-data-flow.md) | `architecture`, `state-management`, `immutability` |
| [update](../_posts/en/glossary/2026-09-09-update.md) | `flow`, `concurrency`, `state-management` |
| [Upper Bound](../_posts/en/glossary/2026-09-07-upper-bound.md) | `generics`, `type-system` |
| [Value Semantics](../_posts/en/glossary/2026-09-09-value-semantics.md) | `data-classes`, `immutability`, `state-management` |
| [Variance](../_posts/en/glossary/2026-09-07-variance.md) | `generics`, `type-system`, `immutability` |
| [viewModelScope](../_posts/en/glossary/2026-09-10-viewmodel-scope.md) | `coroutines`, `lifecycle`, `cancellation` |
| [ViewModelStore](../_posts/en/glossary/2026-09-04-viewmodel-store.md) | `lifecycle`, `android-framework`, `navigation` |
| [Virtual Dispatch](../_posts/en/glossary/2026-09-02-virtual-dispatch.md) | `dispatch`, `oop`, `jvm` |
| [Vtable](../_posts/en/glossary/2026-09-02-vtable.md) | `dispatch`, `jvm`, `performance` |
| [when Expression](../_posts/en/glossary/2026-08-19-when-expression.md) | `syntax`, `sealed-types` |
