---
layout: post
title: "advanceUntilIdle"
date: 2026-09-15 12:00:00 +0000
categories: [es, glosario]
tags: [testing, coroutines]
lang: es
permalink: /es/glosario/advance-until-idle/
---

## The Theory (El Qué)

**`advanceUntilIdle()`** es la llamada de [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}) / `TestScope` que corre el scheduler de tiempo virtual hasta que ninguna coroutine del [`TestDispatcher`]({{ "/es/glosario/test-dispatcher/" | relative_url }}) tiene trabajo pendiente. Adelanta cada `delay`, drena cada tarea encolada, y retorna — así la aserción que sigue ve el estado que "eventualmente" hubiera aparecido.

```kotlin
// From FollowApp Suite — SettingsViewModelTest.kt
@Test
fun `init loads language from use case`() = runTest {
    languageFlow.value = "es"
    val vm = createViewModel()
    advanceUntilIdle()

    assertEquals("es", vm.uiState.value.currentLanguage)
}
```

## The Senior Nuance (El Matiz Senior)

- **Solo drena lo que posee el test dispatcher.** Una coroutine en `Dispatchers.IO` real o en `GlobalScope` es invisible para él: el test corre una carrera o se cuelga. Ese es el síntoma de un scope no estructurado.
- **`StandardTestDispatcher` lo necesita; `UnconfinedTestDispatcher` casi nunca.** Con el dispatcher estándar nada corre hasta que avanzás; con unconfined, las coroutines corren ansiosamente hasta su primera suspensión.
- **Es la vista desde el test de "el padre espera a sus hijos".** `runTest` en sí falla si un hijo sigue activo cuando termina el bloque; `advanceUntilIdle` es cómo llegás ahí de forma determinista.
- Ver [Structured Concurrency]({{ "/es/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
