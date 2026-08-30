---
layout: post
title: "Protected State"
date: 2026-08-30 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/protected-state/
---

## The Theory (El Qué)

El **protected state** (estado protegido) se refiere a propiedades o campos declarados con el modificador de visibilidad `protected`, haciéndolos accesibles solo dentro de la clase misma y sus subclases. En Kotlin, los miembros `protected` son invisibles para código fuera de la cadena de [herencia]({{ "/es/glosario/inheritance/" | relative_url }}) — a diferencia de Java, donde `protected` también otorga acceso a nivel de paquete. El estado protegido es un diferenciador clave entre `sealed class` y `sealed interface`: una sealed class puede contener propiedades protegidas y bloques `init` que las subclases heredan, mientras que una sealed interface no puede contener estado de ningún tipo.

```kotlin
// sealed class CON estado protegido — los subtipos heredan campos compartidos
sealed class NetworkResult {
    protected val timestamp: Long = System.currentTimeMillis()

    data class Success(val data: String) : NetworkResult()
    data class Error(val code: Int) : NetworkResult()
}

// sealed interface — SIN estado protegido posible.
// Cada implementación es estructuralmente independiente
sealed interface UIEvent
```

## The Senior Nuance (El Matiz Senior)

- La presencia o ausencia de estado protegido es el criterio de decisión para elegir entre `sealed class` y `sealed interface`. Si los subtipos necesitan estado interno compartido (propiedades, bloques `init`, métodos helper), usá una [sealed class]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}). Si no, preferí una sealed interface por su flexibilidad de [herencia]({{ "/es/glosario/inheritance/" | relative_url }}) múltiple.
- En arquitectura Android, el estado protegido en ViewModels o clases base es un code smell: crea acoplamiento implícito entre padre e hijo, haciendo el comportamiento más difícil de rastrear. Preferí composición (inyectar dependencias) sobre estado protegido en la mayoría de los casos.
- El `protected` de Kotlin es más estricto que el de Java: no otorga acceso a nivel de paquete. Una propiedad `protected` en una clase Kotlin es verdaderamente visible solo para subclases, haciéndolo un límite de encapsulamiento más ajustado.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
