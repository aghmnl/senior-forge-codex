---
layout: post
title: "MutableList"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/mutable-list/
---

## The Theory (El Qué)

**`MutableList<E>`** extiende [`List`]({{ "/es/glosario/list/" | relative_url }}) con las operaciones estructurales: [`add`]({{ "/es/glosario/add/" | relative_url }}), `add(index, element)`, [`remove`]({{ "/es/glosario/remove/" | relative_url }}), `removeAt`, `set`/`[]=` y [`clear`]({{ "/es/glosario/clear/" | relative_url }}). `mutableListOf()` y [`toMutableList`]({{ "/es/glosario/to-mutable-list/" | relative_url }}) devuelven uno, respaldado por un [`ArrayList`]({{ "/es/glosario/arraylist/" | relative_url }}).

```kotlin
// De FollowApp Suite — StringListTypeConverter.kt
val list = mutableListOf<String>()
for (i in 0 until jsonArray.length()) {
    list.add(jsonArray.getString(i))
}
return list          // publicado como List<String>
```

## The Senior Nuance (El Matiz Senior)

- La regla que sobrevive a un code review: construí con un `MutableList` dentro de una función y declará el [Return Type]({{ "/es/glosario/return-type/" | relative_url }}) como [`List`]({{ "/es/glosario/list/" | relative_url }}). La [mutación]({{ "/es/glosario/mutation/" | relative_url }}) queda confinada a un [Stack Frame]({{ "/es/glosario/stack-frame/" | relative_url }}) que ningún otro thread puede observar.
- Es [invariante]({{ "/es/glosario/invariance/" | relative_url }}) — `MutableList<Task>` no es un `MutableList<Any>` — porque `E` aparece en posiciones de lectura y de escritura. Ver [Generics, Varianza y Reificación]({{ "/es/01-kotlin-core/generics-variance-reification/" | relative_url }}).
- Un `MutableList` guardado como estado compartido es un bug de [Concurrencia]({{ "/es/glosario/concurrency/" | relative_url }}) esperando ocurrir: no es [Thread-Safe]({{ "/es/glosario/thread-safety/" | relative_url }}), y modificarlo estructuralmente durante una iteración lanza `ConcurrentModificationException`. Si tiene que escapar, tomá una [Defensive Copy]({{ "/es/glosario/defensive-copy/" | relative_url }}).
- En Compose además es invisible: un `MutableList` común no es [Observable State]({{ "/es/glosario/observable-state/" | relative_url }}), así que mutarlo no recompone nada. El equivalente observable es [`mutableStateListOf`]({{ "/es/glosario/mutable-state-list-of/" | relative_url }}).

**Documentación oficial:** [`kotlin.collections.MutableList`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-mutable-list/)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
