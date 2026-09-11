---
layout: post
title: "Continuation-Passing Style (CPS)"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, compiler]
lang: es
permalink: /es/glosario/continuation-passing-style/
---

## The Theory (El Qué)

**Continuation-Passing Style (CPS)** es la transformación que el compilador de Kotlin aplica a toda [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}): en lugar de *devolver* un valor, la función recibe un parámetro [Continuation]({{ "/es/glosario/continuation/" | relative_url }}) y eventualmente lo *llama* con el resultado. La firma visible `suspend fun load(id: String): Task` se convierte en `fun load(id: String, cont: Continuation<Task>): Any?` en [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
// What you write:
suspend fun load(id: String): Task

// What the compiler emits (JVM signature):
fun load(id: String, cont: Continuation<Task>): Any?
```

El [return type]({{ "/es/glosario/return-type/" | relative_url }}) se amplía a `Any?` porque la función tiene dos formas de terminar: devolver el `Task` real de forma síncrona, o devolver el marcador `COROUTINE_SUSPENDED` que significa "voy a llamar `cont.resume` más tarde".

## The Senior Nuance (El Matiz Senior)

- **CPS es lo que hace de `suspend` un contrato de compile time.** Un llamador sin continuation que pasar no puede invocar la función — esa es literalmente la razón por la que las suspend functions necesitan una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}).
- **Es el patrón de [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}), automatizado.** El código con callbacks es CPS escrito a mano. Las coroutines dejan que el compilador lo escriba, y lo esconden detrás de una sintaxis secuencial — por eso eliminan el [callback hell]({{ "/es/glosario/callback-hell/" | relative_url }}) sin cambiar el modelo subyacente.
- **La interop con Java muestra la costura.** Llamar una suspend function de Kotlin desde Java expone el parámetro `Continuation` directamente; librerías como `kotlinx-coroutines-jdk8` existen para esconderlo.
- La transformación pareja es la [state machine]({{ "/es/glosario/state-machine/" | relative_url }}); ver [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
