---
layout: post
title: "getAndUpdate"
date: 2026-09-28 12:00:00 +0000
categories: [es, glosario]
tags: [concurrency, state-management, flow]
lang: es
permalink: /es/glosario/get-and-update/
---

## The Theory (El Qué)

**`getAndUpdate { }`** es una variante de [update {}]({{ "/es/glosario/update/" | relative_url }}) para [MutableStateFlow]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) que aplica el cambio de forma atómica y **devuelve el valor que tenía antes del cambio**. Funciona exactamente igual que `update`: calcula el valor siguiente a partir del actual y lo guarda con [compareAndSet]({{ "/es/glosario/compare-and-set/" | relative_url }}), reintentando si otro escritor llegó primero.

```kotlin
// Not found in FAS — standalone example
private val _pending = MutableStateFlow<List<Upload>>(emptyList())

// Tomar todas las subidas pendientes y dejar la lista vacía en un solo paso
// atómico: ninguna subida se puede agregar en el medio y perderse
fun drainPending(): List<Upload> = _pending.getAndUpdate { emptyList() }
```

## The Senior Nuance (El Matiz Senior)

- **Se usa cuando necesitás el valor viejo.** El caso típico es "tomar y resetear": leer lo que había y reemplazarlo, sin que otro escritor se meta entre la lectura y el reseteo.
- **Valen las mismas reglas que para `update`.** El lambda puede correr más de una vez, así que tiene que ser puro y corto.
- Su hermano [updateAndGet]({{ "/es/glosario/update-and-get/" | relative_url }}) devuelve, en cambio, el valor **después** del cambio.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
