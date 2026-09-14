---
layout: post
title: "TestDispatcher"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [testing, coroutines, threading]
lang: es
permalink: /es/glosario/test-dispatcher/
---

## The Theory (El Qué)

Un **`TestDispatcher`** (`StandardTestDispatcher`, `UnconfinedTestDispatcher`) es un [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) de `kotlinx-coroutines-test` que corre coroutines en el thread del test bajo un scheduler de tiempo virtual: `delay` completa al instante, el orden de ejecución es determinista, y `runTest` falla si una coroutine sigue corriendo al final. Reemplaza a los [thread pools]({{ "/es/glosario/thread-pool/" | relative_url }}) reales en tests unitarios.

```kotlin
// From FollowApp Suite — SettingsViewModelTest.kt
@Before
fun setup() {
    Dispatchers.setMain(testDispatcher)
}

@After
fun tearDown() {
    Dispatchers.resetMain()
}
```

`Dispatchers.setMain` reemplaza el `Main` global por el dispatcher de test, y eso es lo que hace controlable a [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) en un test de JVM. No hace nada por `Dispatchers.IO` ni `Default`.

## The Senior Nuance (El Matiz Senior)

- **Inyectá los dispatchers, o el test no puede alcanzarlos.** Un `withContext(Dispatchers.IO)` hardcodeado dentro de una clase bajo test salta a un thread real que `runTest` no controla; el test o tiene una race o duerme. Inyectá un `CoroutineDispatcher` por constructor y pasá `StandardTestDispatcher(testScheduler)` en los tests — FAS todavía no lo hace, y por eso su `BackupManager` solo es testeable con tests instrumentados.
- **`Standard` vs `Unconfined`.** `StandardTestDispatcher` encola el trabajo hasta que el test llama `advanceUntilIdle()` / `runCurrent()`, dando control explícito sobre el orden. `UnconfinedTestDispatcher` corre de forma ansiosa, lo que se parece más al `Main.immediate` de producción pero esconde bugs de orden.
- **`setMain` es global al proceso.** Emparejalo siempre con `resetMain()` en `@After`, o la próxima clase de test hereda el dispatcher.
- **Preferí `runTest` sobre [`runBlocking`]({{ "/es/glosario/run-blocking/" | relative_url }})** en tests: provee el scheduler, saltea los delays y detecta coroutines filtradas.
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
