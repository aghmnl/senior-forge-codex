---
layout: post
title: "Collection Operators"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
tags: [collections, functional]
lang: es
permalink: /es/glosario/collection-operators/
---

## The Theory (El Qué)

Los **collection operators** (operadores de colecciones) son [extension functions]({{ "/es/glosario/extension-functions/" | relative_url }}) sobre las [colecciones]({{ "/es/glosario/collections/" | relative_url }}) de Kotlin ([`List`]({{ "/es/glosario/list/" | relative_url }}), [`Set`]({{ "/es/glosario/sets/" | relative_url }}), [`Map`]({{ "/es/glosario/maps/" | relative_url }}), `Sequence`) que expresan [data transformations]({{ "/es/glosario/data-transformation/" | relative_url }}) declarativamente. Los operadores más comunes son:

- **[`map`]({{ "/es/glosario/map-operator/" | relative_url }})** — transforma cada elemento: [`List<A> → List<B>`]({{ "/es/glosario/list/" | relative_url }}).
- **[`filter`]({{ "/es/glosario/filter/" | relative_url }})** — mantiene elementos que coinciden con un predicado.
- **`flatMap`** — mapea cada elemento a una colección y aplana los resultados.
- **[`groupBy`]({{ "/es/glosario/group-by/" | relative_url }})** — particiona elementos en un [`Map<K, List<V>>`]({{ "/es/glosario/maps/" | relative_url }}) por un key selector.
- **`fold` / `reduce`** — acumula elementos en un solo valor.
- **`associate` / `associateBy`** — construye un [`Map`]({{ "/es/glosario/maps/" | relative_url }}) desde elementos.
- **[`sortedBy`]({{ "/es/glosario/sorted/" | relative_url }}) / `sortedWith`** — produce una copia ordenada.
- **`distinct` / `distinctBy`** — elimina duplicados.

Todos estos operadores retornan [colecciones]({{ "/es/glosario/collections/" | relative_url }}) **nuevas** — no mutan la original. Esto se alinea con la preferencia de Kotlin por la [inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }}) y el [estilo funcional]({{ "/es/glosario/functional-style/" | relative_url }}).

## The Senior Nuance (El Matiz Senior)

- Un Senior encadena operadores en [pipelines]({{ "/es/glosario/pipeline/" | relative_url }}) que se leen como una especificación: `tasks.filter { !it.isDone }.sortedBy { it.dueDate }.map { it.toUiModel() }`. Cada paso es una transformación pura, trivialmente testeable de forma aislada.
- Los operadores eager (`list.map { }`) crean una nueva [`List`]({{ "/es/glosario/list/" | relative_url }}) en cada paso. Para colecciones grandes o cadenas largas, [`asSequence()`]({{ "/es/glosario/as-sequence/" | relative_url }}) evita allocations intermedias evaluando lazily. Pero las sequences tienen [overhead]({{ "/es/glosario/overhead/" | relative_url }}) por elemento, así que para colecciones pequeñas (<100 elementos), eager es más rápido.
- Los operadores de Flow ([`map`]({{ "/es/glosario/map-operator/" | relative_url }}), [`filter`]({{ "/es/glosario/filter/" | relative_url }}), `flatMapLatest`) son espejo de los operadores de colecciones pero operan sobre streams asíncronos. Un Senior reconoce la simetría conceptual: el mismo [estilo funcional]({{ "/es/glosario/functional-style/" | relative_url }}) aplica ya sea que los datos lleguen todos a la vez (colecciones) o a lo largo del tiempo (Flow).

**Documentación oficial:** [Collection operations overview](https://kotlinlang.org/docs/collection-operations.html) · [List-specific operations](https://kotlinlang.org/docs/list-operations.html)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
