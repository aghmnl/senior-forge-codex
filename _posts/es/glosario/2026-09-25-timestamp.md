---
layout: post
title: "Timestamp"
date: 2026-09-25 12:00:00 +0000
categories: [es, glosario]
tags: [jvm, state-management]
lang: es
permalink: /es/glosario/timestamp/
---

## The Theory (El Qué)

Un **timestamp** (marca de tiempo) es un número que identifica un momento. En la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) y en Android el más común es `System.currentTimeMillis()`: milisegundos desde la época Unix (1970-01-01 UTC), según el **reloj de pared** del dispositivo. Android también ofrece relojes monotónicos que solo avanzan, `SystemClock.elapsedRealtime()` y `System.nanoTime()`, que miden tiempo transcurrido pero no corresponden a una fecha de calendario.

```kotlin
// De FollowApp Suite — TasksViewModel.kt
// Un timestamp usado como trigger de "disparar de nuevo": cada apertura del
// formulario escribe un valor nuevo, así el StateFlow no lo descarta por igual
_formOpenTrigger.value = System.currentTimeMillis()
```

## The Senior Nuance (El Matiz Senior)

- **El reloj de pared puede saltar.** El usuario puede cambiar la hora, y la sincronización horaria por red puede moverla hacia atrás. Medir una duración como la diferencia entre dos `currentTimeMillis()` puede dar resultados negativos o absurdos; las duraciones van con `elapsedRealtime()` o `nanoTime()`.
- **Como trigger, un timestamp es solo "probablemente distinto".** Dos escrituras en el mismo milisegundo producen el mismo valor, y un [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) descarta la segunda. Un contador que se incrementa garantiza que sea distinto.
- **Inyectar el "ahora" hace el código testeable.** El código que llama a `System.currentTimeMillis()` en lo profundo es difícil de testear; pasar `now` como parámetro, o inyectar un reloj, hace que el tiempo sea controlable.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
