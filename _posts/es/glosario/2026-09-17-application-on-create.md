---
layout: post
title: "Application.onCreate()"
date: 2026-09-17 12:00:00 +0000
categories: [es, glosario]
tags: [android-framework, lifecycle, performance]
lang: es
permalink: /es/glosario/application-on-create/
---

## The Theory (El Qué)

**`Application.onCreate()`** es el primer código de la app que corre cuando arranca el proceso — antes de cualquier `Activity`, `Service` o `BroadcastReceiver`, en el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}), y *dentro* de la ventana de cold start que el usuario vive como el splash. Todo lo que pongas ahí se paga en cada lanzamiento y retrasa el primer frame. Es donde se construyen los grafos de DI, donde se configura [`StrictMode`]({{ "/es/glosario/strict-mode/" | relative_url }}), y — demasiado seguido — donde se inicializan [SDK]({{ "/es/glosario/sdk/" | relative_url }})s.

```kotlin
// From FollowApp Suite — MyTasksApplication.kt
override fun onCreate() {
    super.onCreate()
    // Read the persisted appearance settings BEFORE any Activity is
    // inflated so the OS picks the right locale + night mode from the
    // very first frame. [...] All three values live in the same
    // "settings" DataStore — reading them in a single runBlocking
    // triggers exactly one cold file open.
    val (language, themeMode, contrastLevel) = runBlocking {
        Triple(
            languagePreferences.getLanguage().first(),
            themePreferences.getThemeMode().first(),
            /* ... */
        )
    }
    // ...
}
```

## The Senior Nuance (El Matiz Senior)

- **Bloquear acá a veces es un trade-off deliberado.** El ejemplo de arriba corre [`runBlocking`]({{ "/es/glosario/run-blocking/" | relative_url }}) en Main a propósito: leer tema y locale *antes* de la primera Activity evita un flash visible en cada lanzamiento. El comentario documenta el costo (una apertura fría de archivo) y la razón. Esa es la diferencia entre una decisión y un accidente.
- **Todo lo demás debería irse.** Bootstraps de SDK, analytics, crash reporters: a un dispatcher de fondo, o diferido hasta después del primer frame, o inicializado lazy con `App Startup`.
- **Corre para todo proceso, incluidos los que no tienen UI.** Un job de `WorkManager` o un push pueden arrancar el proceso; no asumas que hay un usuario mirando.
- Ver [Main-Safety]({{ "/es/02-coroutines-flow/main-safety/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
