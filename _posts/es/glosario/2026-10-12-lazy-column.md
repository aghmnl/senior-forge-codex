---
layout: post
title: "LazyColumn"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [compose, performance]
lang: es
permalink: /es/glosario/lazy-column/
---

## The Theory (El Qué)

**`LazyColumn`** es la lista vertical de Compose que compone **solo los ítems visibles**, más un pequeño margen. Los ítems que salen de la pantalla al scrollear salen de la [composition]({{ "/es/glosario/composition/" | relative_url }}), y los nuevos se componen a medida que aparecen, así que una lista de miles de ítems cuesta casi lo mismo que una pantalla. `LazyRow` es la versión horizontal.

```kotlin
// Not found in FAS — standalone example
LazyColumn {
    items(tasks, key = { it.id }) { task -> TaskRow(task) }
}
```

## The Senior Nuance (El Matiz Senior)

- **Salir de la [composition]({{ "/es/glosario/composition/" | relative_url }}) olvida el estado de [`remember`]({{ "/es/glosario/remember/" | relative_url }}).** Un ítem que sale y vuelve arranca de nuevo, salvo que su estado use [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}) o viva fuera del ítem.
- **Las keys estables importan**: con `key`, Compose mantiene el estado de cada ítem pegado al ítem correcto cuando la lista cambia.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
