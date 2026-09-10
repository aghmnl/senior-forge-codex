---
layout: post
title: "runBlocking"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/run-blocking/
---

## The Theory (El Qué)

**`runBlocking { }`** es un coroutine builder que arranca una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) y **bloquea el [thread]({{ "/es/glosario/thread/" | relative_url }}) actual** hasta que completa. Es el puente entre el mundo sin coroutines (`main()`, JUnit, `Application.onCreate`) y las [suspend functions]({{ "/es/glosario/suspend-functions/" | relative_url }}) — el único builder que convierte código suspendible de vuelta en una [llamada bloqueante]({{ "/es/glosario/blocking-call/" | relative_url }}).

```kotlin
// From FollowApp Suite — MyTasksApplication.kt
val (language, themeMode, contrastLevel) = runBlocking {
    Triple(
        languagePreferences.getLanguage().first(),
        themePreferences.getThemeMode().first(),
        themePreferences.getContrastLevel().first()
    )
}
```

FAS lo usa exactamente acá, con un comentario: el locale y el modo nocturno deben conocerse antes de que la primera Activity se infle, así que la lectura tiene que completar de forma síncrona.

## The Senior Nuance (El Matiz Senior)

- **Nunca en un ViewModel, Composable o repositorio.** Esos ya tienen un scope; `runBlocking` ahí es un bloqueo del [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) disfrazado de coroutine. Usá `launch`/`withContext`.
- **`runBlocking` en Main puede hacer deadlock.** Si el bloque espera algo que necesita `Dispatchers.Main` para correr, ambos esperan para siempre. `Dispatchers.Main.immediate` no te salva.
- **Cada uso en producción lleva un comentario y una razón.** Las razones aceptables son pocas: un valor requerido antes del primer frame; una API síncrona legacy que no podés cambiar; un entry point de CLI.
- **En tests, preferí `runTest`.** Saltea los `delay` virtualmente y falla ante coroutines filtradas; `runBlocking` no hace ninguna de las dos.
- Ver [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
