---
layout: post
title: "Star Projection"
date: 2026-09-07 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/star-projection/
---

## The Theory (El Qué)

Una **Star Projection** — escrita `Foo<*>` — dice "esto es un `Foo` de *algún* tipo concreto, y no sé cuál". Es el reemplazo [type-safe]({{ "/es/glosario/type-safety/" | relative_url }}) de Kotlin para los [Raw Types]({{ "/es/glosario/raw-types/" | relative_url }}) de Java.

El compilador sigue rastreando que existe un type argument real, e impone una asimetría:

- Las **lecturas** están permitidas, ampliadas al [Upper Bound]({{ "/es/glosario/upper-bound/" | relative_url }}).
- Las **escrituras** están prohibidas, porque no se puede probar que ningún valor coincida con el tipo desconocido.

```kotlin
// Not found in FAS — standalone example
fun logDragActivity(state: ReorderState<*>) {
    // Lectura: K? se amplía al upper bound, Any?
    val key: Any? = state.draggingKey
    println("dragging: $key")

    // state.isDragging(someKey)   // no compila: K es desconocido para escribir
}
```

La star projection es además el único chequeo genérico que sobrevive al [Type Erasure]({{ "/es/glosario/type-erasure/" | relative_url }}): `list is List<*>` compila, `list is List<String>` no.

## The Senior Nuance (El Matiz Senior)

- **`<*>` no es un [Raw Type]({{ "/es/glosario/raw-types/" | relative_url }}).** Un `List` raw de Java te deja leer y escribir sin chequeo, difiriendo la falla a una [`ClassCastException`]({{ "/es/glosario/class-cast-exception/" | relative_url }}). `List<*>` rechaza la escritura en [Compile Time]({{ "/es/glosario/compile-time/" | relative_url }}). La diferencia es dónde aflora el bug.
- **Es por parámetro.** Para `Map<K, V>`, `Map<*, *>` proyecta ambos, pero `Map<String, *>` proyecta solo el tipo del valor — útil cuando conocés una mitad de la firma.
- **El tipo de lectura es el [Upper Bound]({{ "/es/glosario/upper-bound/" | relative_url }}), no `Any?` por defecto.** `ReorderState<*>.draggingKey` se lee como `Any?` porque el bound es `Any` y la property es nullable; un `Foo<T : CharSequence>` star-projected se leería como `CharSequence`. Bounds más ajustados vuelven la star projection genuinamente usable.
- **Buscá esto antes que [`reified`]({{ "/es/glosario/reified/" | relative_url }}).** Mucho código que "necesita el tipo en [Runtime]({{ "/es/glosario/runtime/" | relative_url }})" en realidad solo necesita *que no le importe*. Loguear, contar y limpiar un contenedor genérico son todos trabajos de star projection, y no cargan nada del [Code Bloat]({{ "/es/glosario/code-bloat/" | relative_url }}) que sí trae la reificación con [Inline Functions]({{ "/es/glosario/inline-functions/" | relative_url }}).
- **`<*>` es distinto de `<Any?>`.** `MutableList<Any?>` es una lista que genuinamente acepta cualquier cosa, así que las escrituras son legales. `MutableList<*>` es una lista de un tipo específico desconocido, así que no lo son. Confundir ambas es una fuente común de "por qué no compila esto" en review.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
