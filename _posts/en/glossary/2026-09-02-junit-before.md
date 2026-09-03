---
layout: post
title: "@Before"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/junit-before/
---

## The Theory (The What)

**`@Before`** is a JUnit 4 annotation (and `@BeforeEach` in JUnit 5) that marks a method to run before every test method in the class. It is the standard setup hook for test fixtures: creating fresh instances of collaborators, initializing `lateinit` properties, configuring mocks, and preparing the system under test. The method runs once per test, ensuring isolation between tests.

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
}
```

Every test gets a fresh `FakePresetRepository` and `CleanUpPresetsUseCase` — no shared mutable state between tests.

## The Senior Nuance

- **`@Before` + `lateinit` is the canonical pattern**: Test classes declare dependencies as `lateinit var` (avoiding nullable types) and initialize them in `@Before`. This keeps test code clean — no `!!` operators, no `?` checks, no `lazy` delegation — just direct property access that reads like production code.
- **`@Before` vs `@BeforeClass`/`@BeforeAll`**: `@Before` runs per test (instance-level setup); `@BeforeClass` (JUnit 4) / `@BeforeAll` (JUnit 5) runs once per class (shared setup). Senior developers use per-test setup by default and only share setup when it's expensive and provably stateless (e.g., starting an in-memory database).
- **Teardown pairing**: `@After` runs after each test and should release resources acquired in `@Before` — closing databases, cancelling [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) scopes, clearing shared state. Forgetting `@After` can cause test pollution where one test's state leaks into the next.
- **Android instrumented tests**: In `@RunWith(AndroidJUnit4::class)` tests, `@Before` often sets up Room in-memory databases, DataStores with test scopes, or Hilt test components. The FAS codebase uses this pattern extensively for integration tests.
- **Rule interaction**: JUnit 4 `@Rule` fields are initialized before `@Before` runs. This means rules like `InstantTaskExecutorRule` or `MainCoroutineRule` are already active when your setup method executes — a subtle ordering detail that matters when setup code touches LiveData or [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
