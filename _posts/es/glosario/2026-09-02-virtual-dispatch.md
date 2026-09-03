---
layout: post
title: "Virtual Dispatch"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/virtual-dispatch/
---

## The Theory (El Qué)

**Virtual dispatch** (despacho virtual, también llamado despacho dinámico) significa que la función a llamar se determina en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}), basándose en el tipo real del objeto — no en el tipo declarado de la variable. La [JVM]({{ "/es/glosario/jvm/" | relative_url }}) usa una [vtable]({{ "/es/glosario/vtable/" | relative_url }}) (tabla de métodos virtuales) para buscar el método sobreescrito correcto para la clase concreta del objeto. Este es el mecanismo detrás del [polimorfismo]({{ "/es/glosario/polymorphism/" | relative_url }}): llamar a `animal.sound()` en una instancia de `Dog` ejecuta `Dog.sound()`, incluso cuando la variable está tipada como `Animal`.

Es lo opuesto al [static dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }}), donde el compilador resuelve la llamada en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}) basándose solo en el tipo declarado.

```kotlin
// Virtual dispatch en acción
open class Animal {
    open fun sound() = "..."
}

class Dog : Animal() {
    override fun sound() = "Woof"
}

val animal: Animal = Dog()
animal.sound() // "Woof" — resuelto en runtime vía vtable
```

## The Senior Nuance (El Matiz Senior)

- En Kotlin, todas las funciones miembro no-`final` usan virtual dispatch. Dado que las clases y métodos en Kotlin son `final` por defecto (debés escribir `open`), el compilador puede frecuentemente devirtualizar llamadas — reemplazando virtual dispatch con una llamada directa cuando puede probar el tipo concreto. Es una optimización JIT que la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) realiza automáticamente.
- Las [extension functions]({{ "/es/glosario/extension-functions/" | relative_url }}) **no** usan virtual dispatch — usan [static dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }}). Esta es la diferencia de comportamiento más importante y una trampa común en entrevistas: `fun Animal.greet()` vs `fun Dog.greet()` siempre resuelve al tipo *declarado*, no al tipo en runtime.
- El costo del virtual dispatch es una indirección de puntero (el lookup en la [vtable]({{ "/es/glosario/vtable/" | relative_url }})). En la práctica, las inline caches del JIT compiler hacen esto casi gratuito para call sites monomórficos (solo un tipo concreto observado). El rendimiento solo se convierte en preocupación para sites megamórficos (muchos tipos diferentes) en bucles cerrados.
- El dispatch de interfaces es ligeramente más costoso que el de clases porque la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) usa un lookup de itable (tabla de métodos de interfaz) que involucra una búsqueda, mientras que los lookups de vtable de clase son un índice directo.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
