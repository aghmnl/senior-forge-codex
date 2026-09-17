---
layout: post
title: "StrictMode"
date: 2026-09-17 12:00:00 +0000
categories: [es, glosario]
tags: [android-framework, threading, performance]
lang: es
permalink: /es/glosario/strict-mode/
---

## The Theory (El Qué)

**`StrictMode`** es una herramienta de desarrollo del framework Android que detecta accesos accidentales a disco y red en el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) (thread policy) y objetos filtrados como `Cursor`s sin cerrar o instancias de `Activity` (VM policy). Lo habilitás en [`Application.onCreate()`]({{ "/es/glosario/application-on-create/" | relative_url }}) para builds de debug y elegís una penalidad: log, parpadeo de pantalla, diálogo, o crash (`penaltyDeath()`). Es la forma más barata de hacer *ruidosa* una llamada no main-safe mucho antes de que se convierta en un [ANR]({{ "/es/glosario/anr/" | relative_url }}) en producción.

```kotlin
// Not found in FAS — standalone example
if (BuildConfig.DEBUG) {
    StrictMode.setThreadPolicy(
        StrictMode.ThreadPolicy.Builder()
            .detectDiskReads().detectDiskWrites().detectNetwork()
            .penaltyLog().penaltyFlashScreen()
            .build()
    )
}
```

## The Senior Nuance (El Matiz Senior)

- **Atrapa la `suspend fun` que nunca suspende.** `File(path).readText()` dentro de una coroutine en Main es invisible para el compilador y para un `TestDispatcher`; `StrictMode` lo marca la primera vez que corre en un dispositivo.
- **Solo en builds de debug.** Los chequeos cuestan unos puntos porcentuales de throughput y las penalidades son para desarrolladores, no usuarios.
- **Esperá ruido de librerías.** Algo de código del framework y de SDKs hace lecturas chicas a disco en Main por diseño; `permitDiskReads()` alrededor de una llamada conocida y benigna mantiene útil la señal.
- Ver [Main-Safety]({{ "/es/02-coroutines-flow/main-safety/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
