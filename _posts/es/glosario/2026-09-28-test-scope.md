---
layout: post
title: "TestScope"
date: 2026-09-28 12:00:00 +0000
categories: [es, glosario]
tags: [testing, coroutines]
lang: es
permalink: /es/glosario/test-scope/
---

## The Theory (El Qué)

**`TestScope`** es el [CoroutineScope]({{ "/es/glosario/coroutine-scope/" | relative_url }}) que provee `kotlinx-coroutines-test` para los tests. [runTest]({{ "/es/glosario/run-test/" | relative_url }}) crea uno y ejecuta el cuerpo del test con él como receptor. Su [test dispatcher]({{ "/es/glosario/test-dispatcher/" | relative_url }}) funciona con un reloj virtual: `delay` no espera en tiempo real, avanza el tiempo virtual, así que un test que cubre un timeout de cinco minutos termina en milisegundos. Además junta las excepciones no atrapadas de sus [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) y hace fallar el test con ellas.

```kotlin
// De FollowApp Suite — AuthUseCaseTest.kt
// El cuerpo de runTest corre dentro de un TestScope: las llamadas suspend
// y first() funcionan directo, sin runBlocking y sin esperas reales
@Test
fun `signing out clears the session`() = runTest {
    saveSession(session)
    signOut()
    assertNull(getSession().first())
}
```

## The Senior Nuance (El Matiz Senior)

- **El tiempo virtual es explícito.** Con el `StandardTestDispatcher` por defecto, las coroutines lanzadas no corren hasta que el test las deja: [advanceUntilIdle()]({{ "/es/glosario/advance-until-idle/" | relative_url }}) ejecuta todo lo pendiente, `advanceTimeBy(ms)` mueve el reloj, `runCurrent()` ejecuta lo que toca ahora, y `currentTime` lee el reloj.
- **`backgroundScope` para trabajo que no termina.** Una coroutine que colecta un [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) nunca termina, y `runTest` falla si al final sigue habiendo trabajo corriendo. Lanzar esos collectors en `backgroundScope` los cancela automáticamente cuando termina el test.
- **Compartí el scheduler.** El código bajo test que crea su propio dispatcher tiene que usar el mismo `TestCoroutineScheduler`; si no, el tiempo virtual no le llega y `delay` espera de verdad. Reemplazar `Dispatchers.Main` con [Dispatchers.setMain]({{ "/es/glosario/set-main/" | relative_url }}) e inyectar los dispatchers son la forma de compartirlo.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
