---
layout: post
title: "Immutability"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/immutability/
---

## The Theory (El Qué)

La **immutability** (inmutabilidad) significa que una vez que un valor se crea, no puede ser modificado. En Kotlin, la inmutabilidad se expresa en múltiples niveles:

- **`val` vs `var`** — `val` declara una referencia de solo lectura (la referencia no puede ser reasignada, aunque el objeto al que apunta puede seguir siendo mutable internamente).
- **[Colecciones]({{ "/es/glosario/collections/" | relative_url }}) inmutables** — [`List`]({{ "/es/glosario/list/" | relative_url }}), [`Set`]({{ "/es/glosario/sets/" | relative_url }}), [`Map`]({{ "/es/glosario/maps/" | relative_url }}) no exponen métodos de mutación. [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}), [`MutableSet`]({{ "/es/glosario/mutable-set/" | relative_url }}), [`MutableMap`]({{ "/es/glosario/mutable-map/" | relative_url }}) los agregan.
- **[Data classes]({{ "/es/01-kotlin-core/data-classes/" | relative_url }})** — cuando todas las propiedades son `val`, la instancia es efectivamente inmutable. La función `copy()` produce una nueva instancia con campos seleccionados cambiados, preservando la original.
- **Kotlinx Immutable Collections** — `persistentListOf()`, `toImmutableList()` proveen colecciones estructuralmente inmutables que el compilador de Compose puede reconocer como [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}).

La inmutabilidad es un pilar del [estilo funcional]({{ "/es/glosario/functional-style/" | relative_url }}): las [data transformations]({{ "/es/glosario/data-transformation/" | relative_url }}) producen nuevos valores en lugar de modificar los existentes.

## The Senior Nuance (El Matiz Senior)

- Un Senior distingue entre **inmutabilidad de referencia** (`val`) e **inmutabilidad de objeto** (sin estado mutable interno). Un `val list: MutableList<Int>` es una referencia de solo lectura a un objeto mutable — una fuente común de bugs cuando la lista se expone desde un ViewModel.
- En Compose, la inmutabilidad impulsa la optimización de skip: si todos los parámetros de un composable son [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) o [primitivos]({{ "/es/glosario/primitives/" | relative_url }}), el runtime puede omitir la recomposición cuando los inputs no cambiaron. Pasar un [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}) rompe este contrato incluso si el contenido no cambió, porque Compose no puede probar estabilidad.
- La inmutabilidad simplifica la [thread safety]({{ "/es/glosario/thread-safety/" | relative_url }}): un objeto que no puede cambiar no necesita sincronización. Por esto `StateFlow` mantiene snapshots inmutables de estado, y por esto `copy()` en una [data class]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) es la forma idiomática de actualizar estado en un ViewModel.

**Documentación oficial:** [Collection types: read-only vs mutable](https://kotlinlang.org/docs/collections-overview.html#collection-types)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
