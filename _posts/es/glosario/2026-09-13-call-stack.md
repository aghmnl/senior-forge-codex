---
layout: post
title: "Call Stack"
date: 2026-09-13 12:00:00 +0000
categories: [es, glosario]
tags: [jvm, memory, error-handling]
lang: es
permalink: /es/glosario/call-stack/
---

## The Theory (El Qué)

La **call stack** (pila de llamadas) es la región de memoria donde un [thread]({{ "/es/glosario/thread/" | relative_url }}) registra la cadena de llamadas a función en curso. Cada llamada apila un [stack frame]({{ "/es/glosario/stack-frame/" | relative_url }}) — parámetros, locales y dirección de retorno — y cada retorno lo desapila. El frame de arriba es la función que corre ahora mismo; el de abajo es el punto de entrada (`main`, o un callback de lifecycle de Android). Un [stack trace]({{ "/es/glosario/stack-trace/" | relative_url }}) es una foto impresa de esta estructura en el momento en que se lanza una excepción.

```kotlin
// Not found in FAS — standalone example
fun main() { load("42") }                 // frame 3 (bottom)
fun load(id: String) = parse(fetch(id))   // frame 2
fun parse(raw: String): Task = TODO()     // frame 1 (top: where the exception is thrown)
```

Cada thread tiene su propia call stack (~1 MB en Android), y por eso las [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) — que guardan su estado en el [heap]({{ "/es/glosario/heap/" | relative_url }}) — pueden ser tanto más baratas que los threads.

## The Senior Nuance (El Matiz Senior)

- **La profundidad es acotada.** Una recursión sin caso base, o un setter que asigna `this.property = value` en vez de `field = value`, hace crecer la pila hasta `StackOverflowError`. El trace muestra el mismo frame repetido cientos de veces — la firma del bug.
- **Las locales mueren con el frame.** Un objeto mutable referenciado solo desde un frame es inalcanzable desde cualquier otro thread, y eso es lo que hace seguro "mutar localmente, publicar [inmutable]({{ "/es/glosario/immutability/" | relative_url }})" sin locks.
- **Las coroutines no tienen una call stack real a través de la suspensión.** Después de un [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}) la pila física se desenrolló; la cadena lógica vive en las [continuations]({{ "/es/glosario/continuation/" | relative_url }}). Por eso los stack traces de coroutines se ven fragmentados salvo que `kotlinx-coroutines-debug` los reconstruya.
- **Las [inline functions]({{ "/es/glosario/inline-functions/" | relative_url }}) no dejan frame.** Su cuerpo se copia en el llamador, así que nunca aparecen en un trace — cómodo para `let`/`apply`, ocasionalmente confuso cuando un número de línea apunta dentro del llamador.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
