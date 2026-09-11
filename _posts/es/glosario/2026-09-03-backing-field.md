---
layout: post
title: "Backing Field"
date: 2026-09-03 12:00:00 +0000
categories: [es, glosario]
tags: [syntax, delegation, state-management]
lang: es
permalink: /es/glosario/backing-field/
---

## The Theory (El Qué)

Un **backing field** (campo de respaldo) es el slot de almacenamiento real que una propiedad usa detrás de su getter y setter. En Kotlin, las propiedades tienen un backing field implícito generado por el compilador siempre que al menos un accessor use el identificador `field`. Se accede con la keyword `field` dentro de un `get()` o `set()` custom:

```kotlin
var name: String = "default"
    set(value) {
        field = value.trim()
    }
```

Si ningún accessor referencia `field`, no se genera un backing field — la propiedad es puramente calculada. Cuando una propiedad usa [delegated properties]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}) (`by`), el objeto delegado reemplaza al backing field por completo: el compilador genera un campo oculto que contiene la instancia del delegado, no el valor de la propiedad.

A nivel de [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}), un backing field es un campo privado de la [JVM]({{ "/es/glosario/jvm/" | relative_url }}). El modificador `lateinit` mantiene el backing field internamente nullable mientras expone un tipo no nullable a los callers — accederlo antes de la inicialización lanza `UninitializedPropertyAccessException` vía un null-check insertado por el compilador.

## The Senior Nuance (El Matiz Senior)

- Un Senior sabe que `field` solo está disponible dentro de los accessors de la propia propiedad — no es una [keyword]({{ "/es/glosario/keyword/" | relative_url }}) general y no puede usarse en otro lugar. Intentar referenciar el backing field de una propiedad desde fuera de su accessor requiere [Runtime Reflection]({{ "/es/glosario/runtime-reflection/" | relative_url }}).
- El patrón de backing property (`private var _items` + public `val items get() = _items`) es común para exponer vistas de solo lectura de estado mutable. En ViewModels [MVI]({{ "/es/glosario/mvi-pattern/" | relative_url }}), es el patrón estándar para [protected state]({{ "/es/glosario/protected-state/" | relative_url }}): `private val _uiState = MutableStateFlow(...)` con un public `val uiState: StateFlow<T> = _uiState.asStateFlow()`.
- Cuando el setter custom de una propiedad usa `field = value`, almacena el valor directamente. Cuando llama a `this.property = value` en su lugar, invoca recursivamente al setter — un error común que causa `StackOverflowError`.

**Documentación oficial:** [Backing fields](https://kotlinlang.org/docs/properties.html#backing-fields)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
