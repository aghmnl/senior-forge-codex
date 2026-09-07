---
layout: post
title: "by (Delegation)"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/by-delegation/
---

## The Theory (El Qué)

**`by`** es la [keyword]({{ "/es/glosario/keyword/" | relative_url }}) de Kotlin que conecta una propiedad con su [property delegate]({{ "/es/glosario/property-delegate/" | relative_url }}). Es una soft keyword — tiene significado especial solo después de una declaración de propiedad (`val`/`var`) y puede usarse como identificador regular en otros contextos.

```kotlin
val name: String by lazy { computeName() }
var count by mutableStateOf(0)
val host: String by configMap
```

Cuando el compilador encuentra `by`:

1. Evalúa la expresión de la derecha para obtener el objeto delegado.
2. Si el delegado define `provideDelegate`, lo llama primero para obtener el delegado real.
3. Genera un campo oculto para almacenar la instancia del delegado.
4. Reescribe cada acceso a la propiedad como una llamada al `operator fun getValue` del delegado (y `setValue` para `var`), pasando la instancia propietaria (`thisRef`) y un objeto de metadata [KProperty]({{ "/es/glosario/kproperty/" | relative_url }}).

`by` también se usa para delegación de clases (`class MyList<T>(inner: List<T>) : List<T> by inner`), que delega la implementación de una interfaz a otro objeto. Es un mecanismo separado pero comparte la misma [keyword]({{ "/es/glosario/keyword/" | relative_url }}).

## The Senior Nuance (El Matiz Senior)

- Un Senior reconoce que `by` se resuelve enteramente en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}): el compilador busca `operator fun getValue`/`setValue` vía convenciones de [operator overloading]({{ "/es/glosario/operator-overloading/" | relative_url }}), no mediante un chequeo de interfaz. Esto significa que un delegado no necesita implementar `ReadOnlyProperty` — solo necesita las firmas de operador correctas.
- En Compose, `by` tiene un rol dual: `by remember { mutableStateOf() }` delega al [sistema de snapshots]({{ "/es/glosario/snapshot-system/" | relative_url }}), haciendo que la variable sea legible y escribible con recomposición automática. Sin `by`, escribís `state.value` en todos lados. La keyword `by` acá convierte un wrapper `State<T>` en lo que parece una variable común.
- Entender que `by` crea un campo de delegado oculto es esencial para debugging: al inspeccionar un objeto en el debugger, las propiedades delegadas aparecen como su wrapper delegado, no como su valor desenvuelto. El valor real está dentro del campo interno del delegado.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
