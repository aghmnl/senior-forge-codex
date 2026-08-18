---
layout: page
title: Generics, Varianza y Reificación
lang: es
permalink: /es/01-kotlin-core/generics-variance-reification/
---

## The Theory (El Qué)

Los Genéricos permiten que clases y funciones trabajen con diferentes tipos manteniendo la seguridad de tipos. Sin embargo, debido al **Type Erasure** (Borrado de Tipos), la información del tipo genérico se elimina en tiempo de ejecución. Para gestionar cómo funciona la subtipificación, Kotlin utiliza la **Varianza**:
- **Covarianza (`out`)**: Permite que un `Box<String>` sea tratado como un `Box<Any>`. El tipo solo puede ser *producido* (devuelto).
- **Contravarianza (`in`)**: Permite que un `Box<Any>` sea tratado como un `Box<String>`. El tipo solo puede ser *consumido* (pasado como argumento).
- **Reificación (`reified`)**: Una característica exclusiva de Kotlin que, combinada con funciones `inline`, permite acceder al tipo genérico `T` en tiempo de ejecución.

## The Senior Perspective (El Porqué)

Para un desarrollador Senior, la varianza trata sobre la **flexibilidad de la API** y la **integridad del sistema de tipos**.

- **Regla PECS**: Siguiendo el mnemónico "Producer-Extends, Consumer-Super" (PECS) de Java, Kotlin lo simplifica con `out` (Productor) e `in` (Consumidor). Usarlos correctamente evita errores de "Type mismatch" en arquitecturas complejas como patrones Repository o Event Busses.
- **Bypassing Erasure**: Dado que la JVM borra los tipos genéricos, normalmente no puedes hacer `if (T is String)`. La reificación es la "vía de escape Senior" que permite comprobaciones de tipo y reflexión sin tener que pasar un objeto `Class<T>` manualmente.
- **Star-Projections**: Usar `<*>` es más seguro que los tipos crudos (*raw types*), señalando que no te importa el tipo específico pero quieres mantener las restricciones básicas de seguridad.

## Code in Action
```kotlin
// Enfoque Senior: Varianza para flexibilidad y Reificación para seguridad
sealed interface Resource {
    data object Empty : Resource
    data class Content(val value: String) : Resource
}

// Productor Covariante: Solo devolvemos T
interface Producer<out T> {
    fun produce(): T
}

// Consumidor Contravariante: Solo aceptamos T
interface Consumer<in T> {
    fun consume(item: T)
}

// Uso de reified para evitar pasar .class o KClass
inline fun <reified T> Any.isType(): Boolean {
    return this is T
}

fun example() {
    val stringProducer: Producer<String> = object : Producer<String> {
        override fun produce() = "Senior Forge"
    }
    
    // Covarianza en acción: Producer<String> es un subtipo de Producer<Any>
    val anyProducer: Producer<Any> = stringProducer
    
    val myResource: Any = Resource.Empty
    if (myResource.isType<Resource.Empty>()) {
        println("Check reificado: Es Empty")
    }
}
```

## Interview Prep (En el banquillo)

**Pregunta**: ¿Por qué no podemos usar tipos reified en funciones normales y qué sucede con ellos a nivel de bytecode?

**Respuesta Senior**: La reificación requiere la palabra clave inline porque el compilador necesita reemplazar la llamada a la función con el código real donde se usa el genérico T. A nivel de bytecode, el compilador reemplaza cada ocurrencia de T con la clase específica utilizada en el punto de llamada. Las funciones normales no pueden ser reificadas porque se compilan en una única firma de método donde el tipo se borra a Object para mantener la compatibilidad con la JVM; carecen del mecanismo de "copiar y pegar" que proporciona inline para preservar la información del tipo específico.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
