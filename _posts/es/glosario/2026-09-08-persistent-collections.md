---
layout: post
title: "Persistent Collections"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/persistent-collections/
---

## The Theory (El Qué)

Las **Persistent Collections** (`kotlinx.collections.immutable`: `PersistentList`, `PersistentSet`, `PersistentMap`) son [Collections]({{ "/es/glosario/collections/" | relative_url }}) genuinamente [inmutables]({{ "/es/glosario/immutability/" | relative_url }}). Cada "modificación" devuelve una colección *nueva* que comparte la mayor parte de su estructura interna con la anterior, así que [`add`]({{ "/es/glosario/add/" | relative_url }}) no es una copia `O(n)`.

```kotlin
// No encontrado en FAS — ejemplo standalone
val selected: PersistentSet<String> = persistentSetOf("a", "b")
val next = selected.add("c")   // valor nuevo; `selected` no cambia
```

## The Senior Nuance (El Matiz Senior)

- Cierran la brecha que deja abierta la jerarquía propia de Kotlin: [`List`]({{ "/es/glosario/list/" | relative_url }}) es apenas una [Read-Only View]({{ "/es/glosario/read-only-view/" | relative_url }}), mientras que `PersistentList` es un valor que nadie puede mutar — no hace falta [Defensive Copy]({{ "/es/glosario/defensive-copy/" | relative_url }}) en ningún límite.
- Compose es la razón práctica más fuerte para adoptarlas. `ImmutableList` está anotada como [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}), así que un composable que la recibe es skippable; un parámetro [`List<T>`]({{ "/es/glosario/list/" | relative_url }}) común se trata como inestable, lo que desactiva en silencio el salteo de recomposición para ese composable.
- El costo es una dependencia y una lectura de un solo elemento algo más lenta que [`ArrayList`]({{ "/es/glosario/arraylist/" | relative_url }}) (recorrido de árbol en vez de indexación de array). Para estado de UI — muchas lecturas, actualizaciones estructurales ocasionales, compartido entre threads — el canje casi siempre vale la pena.

**Documentación oficial:** [kotlinx.collections.immutable](https://github.com/Kotlin/kotlinx.collections.immutable)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
