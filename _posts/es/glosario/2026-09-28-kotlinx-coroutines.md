---
layout: post
title: "kotlinx.coroutines"
date: 2026-09-28 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, build-tools, concurrency]
lang: es
permalink: /es/glosario/kotlinx-coroutines/
---

## The Theory (El Qué)

**kotlinx.coroutines** es la **librería** oficial de JetBrains que convierte las [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) del lenguaje en algo usable. [Kotlin]({{ "/es/glosario/kotlin/" | relative_url }}) mismo aporta solo la palabra clave `suspend` y los tipos básicos detrás de ella, en su paquete [`kotlin.coroutines`]({{ "/es/glosario/coroutines/" | relative_url }}). Todo lo demás viene de esta dependencia aparte: [CoroutineScope]({{ "/es/glosario/coroutine-scope/" | relative_url }}), [launch]({{ "/es/glosario/launch/" | relative_url }}), [async]({{ "/es/glosario/async/" | relative_url }}), [Job]({{ "/es/glosario/job/" | relative_url }}), [SupervisorJob]({{ "/es/glosario/supervisor-job/" | relative_url }}), los [dispatchers]({{ "/es/glosario/dispatcher/" | relative_url }}), [withContext]({{ "/es/glosario/with-context/" | relative_url }}), [Flow]({{ "/es/glosario/flow/" | relative_url }}), [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}), [SharedFlow]({{ "/es/glosario/sharedflow/" | relative_url }}) y [Channel]({{ "/es/glosario/channel/" | relative_url }}). La `x` de `kotlinx` marca las librerías oficiales que no forman parte de la standard library, como `kotlinx.serialization` o `kotlinx.datetime`.

```kotlin
// De FollowApp Suite — libs.versions.toml
// Un módulo de Kotlin puro no recibe la librería gratis: la declara
# Flow in :core:domain repository contracts; the module has no Android dependency to inherit it from
kotlinx-coroutines-core = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version = "1.8.1" }

// De FollowApp Suite — TasksViewModel.kt
// Cada uno de estos imports es la librería, no el lenguaje
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
```

## The Senior Nuance (El Matiz Senior)

- **Lenguaje vs librería es una pregunta de entrevista real.** "¿Las coroutines son parte de Kotlin?" La respuesta honesta tiene dos mitades: la suspensión es una feature del lenguaje, implementada por el compilador; los scopes, los dispatchers, la cancelación y los streams son una librería. Por eso la librería tiene su propio número de versión, separado de la versión de Kotlin.
- **Está dividida en módulos.** `kotlinx-coroutines-core` tiene la API independiente de la plataforma; `kotlinx-coroutines-android` provee `Dispatchers.Main` sobre el looper principal de Android; `kotlinx-coroutines-test` provee `runTest` y los dispatchers de test. Sin el módulo de Android, usar `Dispatchers.Main` falla en runtime porque no hay ningún dispatcher principal disponible.
- **Los módulos Android suelen recibirla de forma transitiva.** Librerías de Jetpack como `lifecycle-viewmodel-ktx` dependen de ella, y de ahí salen `viewModelScope` y `lifecycleScope`. Un módulo de dominio en Kotlin puro no tiene esa dependencia y tiene que declarar `kotlinx-coroutines-core` explícitamente.
- **Las APIs de la librería evolucionan; la semántica del lenguaje no.** Operadores como [flatMapLatest]({{ "/es/glosario/flat-map-latest/" | relative_url }}) están marcados como experimentales en la librería y pueden cambiar entre versiones, mientras que `suspend` es estable. Leer el changelog de la librería es parte de actualizar un codebase.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
