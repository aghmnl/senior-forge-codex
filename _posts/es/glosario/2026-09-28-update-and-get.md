---
layout: post
title: "updateAndGet"
date: 2026-09-28 12:00:00 +0000
categories: [es, glosario]
tags: [concurrency, state-management, flow]
lang: es
permalink: /es/glosario/update-and-get/
---

## The Theory (El Qué)

**`updateAndGet { }`** es una variante de [update {}]({{ "/es/glosario/update/" | relative_url }}) para [MutableStateFlow]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) que aplica el cambio de forma atómica y **devuelve el valor nuevo**, el que efectivamente se guardó. Funciona exactamente igual que `update`: calcula el valor siguiente a partir del actual y lo guarda con [compareAndSet]({{ "/es/glosario/compare-and-set/" | relative_url }}), reintentando si otro escritor llegó primero.

```kotlin
// Not found in FAS — standalone example
private val _attempts = MutableStateFlow(0)

fun onRetry() {
    // El número devuelto es el que guardó esta llamada, aunque
    // otros threads estén incrementando al mismo tiempo
    val attempt = _attempts.updateAndGet { it + 1 }
    if (attempt >= MAX_ATTEMPTS) showGiveUpMessage()
}
```

## The Senior Nuance (El Matiz Senior)

- **Se usa cuando necesitás el resultado de tu propio cambio.** Leer `.value` justo después de `update` no es lo mismo: para ese momento otro escritor pudo haberlo cambiado de nuevo.
- **Valen las mismas reglas que para `update`.** El lambda puede correr más de una vez, así que tiene que ser puro y corto.
- Su hermano [getAndUpdate]({{ "/es/glosario/get-and-update/" | relative_url }}) devuelve, en cambio, el valor **antes** del cambio.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
