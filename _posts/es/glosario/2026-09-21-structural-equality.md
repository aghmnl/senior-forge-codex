---
layout: post
title: "== (Structural Equality)"
date: 2026-09-21 12:00:00 +0000
categories: [es, glosario]
tags: [type-system, data-classes, syntax]
lang: es
permalink: /es/glosario/structural-equality/
---

## The Theory (El Qué)

**`==`** es la igualdad estructural: `a == b` compila a `a?.equals(b) ?: (b === null)`, así que le pregunta al objeto si es *equivalente*, no si es la misma instancia. `Any.equals` tiene identidad por defecto, una [Data Classes: copy, equals, toString]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) lo genera a partir de las propiedades del [constructor primario]({{ "/es/glosario/primary-constructor/" | relative_url }}), y un [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) hereda la identidad del singleton — donde la estructural y la [igualdad referencial]({{ "/es/glosario/referential-equality/" | relative_url }}) coinciden. `!=` es su negación.

```kotlin
// Not found in FAS — standalone example
data class TaskId(val value: String)
TaskId("a") == TaskId("a")     // true  — contenido equivalente
TaskId("a") === TaskId("a")    // false — dos instancias

data object Loading
val a: Any = Loading; val b: Any = Loading
a == b                          // true
a === b                         // true — una sola instancia, así que coinciden
```

## The Senior Nuance (El Matiz Senior)

- **El `==` de Kotlin es el `.equals` de Java, pero seguro.** El chequeo de null viene incorporado, así que la costumbre de `Objects.equals(a, b)` es innecesaria — y comparar [strings]({{ "/es/glosario/string/" | relative_url }}) con `==` compara contenido, no referencias.
- **`==` vale lo que valga `equals`.** En una clase común cae en identidad, y por eso los modelos escritos a mano que "parecen iguales" fallan en las aserciones; en una data class ignora las propiedades declaradas en el cuerpo.
- **Viaja junto con [`hashCode`]({{ "/es/glosario/hash-code/" | relative_url }}).** Dos objetos `==` tienen que devolver el mismo `hashCode`, o las colecciones hash se comportan mal.
- Ver [Data Classes: copy, equals, toString]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
