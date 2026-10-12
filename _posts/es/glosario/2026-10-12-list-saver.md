---
layout: post
title: "listSaver"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [compose, serialization]
lang: es
permalink: /es/glosario/list-saver/
---

## The Theory (El Qué)

**`listSaver`** construye un [`Saver`]({{ "/es/glosario/saver/" | relative_url }}) que guarda un valor como una **lista** de valores guardables. `save` devuelve la lista, y `restore` la recibe y reconstruye el valor por posición.

```kotlin
// Not found in FAS — standalone example
val DateRangeSaver = listSaver<DateRange, String>(
    save = { listOf(it.start.toString(), it.end.toString()) },
    restore = { DateRange(LocalDate.parse(it[0]), LocalDate.parse(it[1])) }
)
```

## The Senior Nuance (El Matiz Senior)

- **Compacto pero posicional.** Agregar o reordenar campos obliga a actualizar `save` y `restore` juntos; [`mapSaver`]({{ "/es/glosario/map-saver/" | relative_url }}) es más claro cuando hay muchos campos.
- Ver [remember & rememberSaveable]({{ "/es/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
