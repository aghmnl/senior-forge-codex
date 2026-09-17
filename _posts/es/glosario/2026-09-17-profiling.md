---
layout: post
title: "Profiling"
date: 2026-09-17 12:00:00 +0000
categories: [es, glosario]
tags: [performance, threading]
lang: es
permalink: /es/glosario/profiling/
---

## The Theory (El Qué)

**Profiling** es medir dónde gasta realmente tiempo, memoria o energía un programa, en vez de razonarlo desde el código fuente. En Android las herramientas son el Profiler de Android Studio (CPU, memoria, energía), **Perfetto** / system traces para líneas de tiempo a nivel de frame, `Trace.beginSection()` / `trace()` para marcadores propios, y Macrobenchmark para mediciones repetibles de arranque y scroll. Para main-safety la pregunta que responde el profiling es precisa: *¿qué llamada, en qué thread, retuvo el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) cuántos milisegundos?*

```kotlin
// From FollowApp Suite — ConsentManager.kt
// MobileAds.initialize does ~700 ms of synchronous SDK bootstrap on
// the caller thread even though it exposes an async callback.
```

## The Senior Nuance (El Matiz Senior)

- **Las firmas mienten; los traces no.** Los 700 ms de arriba se encontraron midiendo, no leyendo `initialize(context, listener)`. Cualquier llamada a un [SDK]({{ "/es/glosario/sdk/" | relative_url }}) o al framework que no hayas perfilado es una suposición de main-safety.
- **Perfilá builds parecidos a release en un dispositivo lento.** Los builds de debug desactivan optimizaciones y un flagship esconde [jank]({{ "/es/glosario/jank/" | relative_url }}) que un teléfono de gama media muestra siempre.
- **Dejá los números al lado del código.** Un comentario con el costo medido convierte "¿por qué esto está en IO?" de arqueología en una respuesta de una línea.
- Ver [Main-Safety]({{ "/es/02-coroutines-flow/main-safety/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
