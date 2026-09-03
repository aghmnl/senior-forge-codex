---
layout: page
title: Lateinit vs Lazy
lang: en
permalink: /en/01-kotlin-core/lateinit-vs-lazy/
order: 9
---

## The Theory (The What)

Both `lateinit` and `lazy` provide ways to delay property initialization, but they serve different technical purposes:

- **`lateinit`** is a modifier for mutable variables (`var`) that are non-nullable and will be initialized later — often by a framework ([Hilt]({{ "/en/glossary/hilt/" | relative_url }})/[Dagger]({{ "/en/glossary/dagger/" | relative_url }}) via [injection]({{ "/en/glossary/dependency-graph/" | relative_url }})), a test setup method, or during a [lifecycle event]({{ "/en/glossary/lifecycle-event/" | relative_url }}). It cannot be used with [primitive]({{ "/en/glossary/primitives/" | relative_url }}) types (`Int`, `Boolean`, etc.) because the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) has no way to represent "uninitialized" for them.
- **`lazy`** is a delegated property for read-only variables (`val`) that computes the value only upon first access and caches the result for all future reads. Internally, it creates a `Lazy<T>` delegate object whose `getValue()` method ensures the initialization [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) (the block you pass to `lazy { ... }`) runs exactly once and caches the result.

The key distinction: `lateinit` means "I promise I will set this before using it"; `lazy` means "compute this once, on demand, then remember it forever".

## The Senior Perspective (The Why)

Choosing between them is a matter of **mutability, thread safety, and ownership**.

- **Thread Safety Modes**: By default, `lazy` is thread-safe (`LazyThreadSafetyMode.SYNCHRONIZED`) — the initialization [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) runs inside a [`synchronized` block]({{ "/en/glossary/synchronized-block/" | relative_url }}). A Senior knows when to use [`NONE`]({{ "/en/glossary/lazy-thread-safety-mode/" | relative_url }}) for performance optimization if the property is accessed only from a single thread (e.g., the UI thread in Compose), or [`PUBLICATION`]({{ "/en/glossary/lazy-thread-safety-mode/" | relative_url }}) if multiple threads can compute the value simultaneously and the first result wins.
- **Test Setup Pattern**: `lateinit` is the standard pattern for test dependencies that are wired in a [`@Before`]({{ "/en/glossary/junit-before/" | relative_url }}) method. Each test class declares its collaborators as `lateinit var`, then the setup method creates fresh instances — guaranteeing isolation between tests without nullable boilerplate. This is the most common `lateinit` usage in real Android projects.
- **Dependency Injection**: `lateinit` is essential for field injection ([Hilt]({{ "/en/glossary/hilt/" | relative_url }})/[Dagger]({{ "/en/glossary/dagger/" | relative_url }})). Since these frameworks use [Runtime Reflection]({{ "/en/glossary/runtime-reflection/" | relative_url }}) to set values after the object is [constructed]({{ "/en/glossary/constructor/" | relative_url }}), `lateinit` allows for non-nullable types without null-checks. Constructor injection is preferred architecturally, but `lateinit` is unavoidable for Android entry points (`Activity`, `Fragment`, `Service`).
- **Memory Management**: `lazy` is ideal for "heavy" objects (expensive database queries, complex configuration parsing, or icon generation) because it defers [allocation]({{ "/en/glossary/allocations/" | relative_url }}) until strictly necessary. If the property is never accessed, the object is never created.
- **Property State Check**: A Senior uses `::property.isInitialized` on `lateinit` properties to avoid `UninitializedPropertyAccessException` when the initialization flow might be non-linear or conditional.

## Code in Action

### `lateinit` in test setup — fresh dependencies per test

The standard pattern: declare test collaborators as `lateinit var`, wire them in `@Before`, and each test gets a fresh isolated instance.

```kotlin
// From FollowApp Suite — CleanUpPresetsUseCaseTest.kt
class CleanUpPresetsUseCaseTest {

    private lateinit var presetRepo: FakePresetRepository
    private lateinit var useCase: CleanUpPresetsUseCase

    @Before
    fun setup() {
        presetRepo = FakePresetRepository()
        useCase = CleanUpPresetsUseCase(presetRepo)
    }

    @Test
    fun `deleting label preserves labelFilters`() = runBlocking {
        presetRepo.addPreset(preset("p1", labelFilters = mapOf(
            "Work" to LabelFilterState.INCLUDE
        )))
        useCase.onLabelDeleted("Work")
        val updated = presetRepo.getPresets().first()
        assertTrue(updated.labelFilters.containsKey("Work"))
    }
}
```

### `lateinit` at scale — integration test with multiple collaborators

When an integration test needs a real database, a DAO, a DataStore, and an importer, `lateinit` keeps each declaration non-nullable and clean.

```kotlin
// From FollowApp Suite — LegacyDataImporterTest.kt
@RunWith(AndroidJUnit4::class)
class LegacyDataImporterTest {

    private lateinit var db: MyTasksDatabase
    private lateinit var dao: TaskDao
    private lateinit var preferences: LegacyImportPreferences
    private lateinit var importer: LegacyDataImporter
    private lateinit var dataStoreScope: CoroutineScope

    @Before
    fun setup() {
        db = Room.inMemoryDatabaseBuilder(context, MyTasksDatabase::class.java)
            .allowMainThreadQueries()
            .build()
        dao = db.taskDao()
        dataStoreScope = CoroutineScope(Dispatchers.IO + Job())
        val dataStore = PreferenceDataStoreFactory.create(scope = dataStoreScope) {
            context.preferencesDataStoreFile(dataStoreName)
        }
        preferences = LegacyImportPreferences(dataStore)
        importer = LegacyDataImporter(LegacyTaskReader(context), dao, preferences)
    }
}
```

### `lazy` with manual caching via `also`

When `by lazy` is not idiomatic (e.g., a custom property getter that must remain a computed property), the `also` [scope function]({{ "/en/01-kotlin-core/scope-functions/" | relative_url }}) can replicate lazy caching manually.

```kotlin
// From FollowApp Suite — AppIcons.kt
private var _mountainFlag: ImageVector? = null

val MountainFlag: ImageVector
    get() = _mountainFlag ?: SvgToImageVector.createImageVectorFromSvg(
        AppSvgs.MountainFlag
    ).also { _mountainFlag = it }
```

### `lazy` with thread safety mode — single-thread optimization

When a property is accessed exclusively from the UI thread, [`LazyThreadSafetyMode.NONE`]({{ "/en/glossary/lazy-thread-safety-mode/" | relative_url }}) skips the [`synchronized` block]({{ "/en/glossary/synchronized-block/" | relative_url }}) and avoids the overhead of thread-safe initialization.

```kotlin
// Standalone example — no FAS match found
class TaskDetailScreen(private val repository: TaskRepository) {

    val headerConfig: HeaderConfig by lazy(LazyThreadSafetyMode.NONE) {
        repository.loadExpensiveHeaderConfig()
    }
}
```

## The Interview (The Hot Seat)

**Question**: What happens internally when you access a `lazy` property for the first time, and how does it differ from a `lateinit` property in terms of [bytecode]({{ "/en/glossary/bytecode/" | relative_url }})?

**Senior Answer**: When a `lazy` property is accessed, the delegated `getValue()` method is called. It checks an internal `_value` field; if it's the `UNINITIALIZED_VALUE` sentinel, it executes the initialization [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) within a [`synchronized` block]({{ "/en/glossary/synchronized-block/" | relative_url }}) (by default) to ensure thread safety, stores the result, and returns it. All subsequent accesses skip the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) and return the cached value directly. In contrast, `lateinit` does not use delegation at all; the compiler generates a direct field access but adds a null-check at the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) level — if the backing field is `null`, it throws `UninitializedPropertyAccessException`. The key [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) difference: `lazy` pays for a delegate object [allocation]({{ "/en/glossary/allocations/" | relative_url }}) plus synchronization overhead, while `lateinit` has zero overhead beyond the null-check.

---

[Back to Chapters]({{ "/" | relative_url }})
