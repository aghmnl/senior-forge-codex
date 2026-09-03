---
layout: post
title: "Crossinline"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/crossinline/
---

## The Theory (El Qué)

**`crossinline`** es un modificador para parámetros [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) de [inline functions]({{ "/es/glosario/inline-functions/" | relative_url }}) que prohíbe non-local returns desde esa lambda. Cuando una función está marcada como `inline`, sus parámetros lambda se inlinean en el call site, lo que normalmente permite que la lambda use `return` para salir de la función *que la invoca* (un non-local return). `crossinline` desactiva esto cuando la lambda escapa del flujo de ejecución propio de la función inline — típicamente porque se pasa a otro contexto de ejecución como un `object` local, un `Runnable`, o un coroutine builder.

```kotlin
// Not found in FAS — standalone example
inline fun runOnUiThread(crossinline action: () -> Unit) {
    handler.post(Runnable { action() })  // action escapa a un Runnable
    // Sin crossinline, 'return' dentro de action intentaría salir
    // de la función que la invoca — pero eso es imposible desde un Runnable
}

fun loadData() {
    runOnUiThread {
        updateUI()
        // return  // ERROR: no permitido — crossinline previene non-local return
    }
}
```

## The Senior Nuance (El Matiz Senior)

- `crossinline` resuelve un problema específico: cuando una [inline function]({{ "/es/glosario/inline-functions/" | relative_url }}) pasa su lambda a un contexto donde un non-local return es estructuralmente imposible (el call stack no coincidirá). Sin `crossinline`, el compilador permitiría `return` dentro de la lambda, lo que fallaría en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}). El modificador convierte esto en un error de [compile time]({{ "/es/glosario/compile-time/" | relative_url }}).
- El caso de uso más común son inline functions que delegan lambdas a `Runnable`, `Executor.execute {}`, o coroutine builders como `launch {}`. La lambda sigue siendo inlineada (sin [allocation]({{ "/es/glosario/allocations/" | relative_url }})), pero `return` se restringe solo a `return@label` (local return).
- Contraste con [`noinline`]({{ "/es/glosario/noinline/" | relative_url }}): `crossinline` sigue inlineando el cuerpo de la lambda (cero allocation), solo bloquea non-local `return`. `noinline` previene el inlining completamente — la lambda se convierte en un objeto `Function` regular en el [heap]({{ "/es/glosario/heap/" | relative_url }}).
- En la práctica, si el compilador te dice "Can't inline 'action' here: it may contain non-local return", agregar `crossinline` es la solución. Es una herramienta de precisión — usala exactamente cuando la lambda necesita ser inlineada pero también necesita cruzar un boundary de ejecución.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
