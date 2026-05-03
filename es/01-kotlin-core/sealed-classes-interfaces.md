---
layout: page
title: Sealed Classes & Interfaces
lang: es
permalink: /es/01-kotlin-core/sealed-classes-interfaces/
---

# Sealed Classes & Interfaces

## The Theory (El Qué)
Las Sealed Classes e Interfaces permiten representar jerarquías de clases restringidas. A diferencia de una interfaz o clase abstracta común, todos los subtipos de un elemento sealed deben conocerse en tiempo de compilación. Esto significa que el compilador tiene un control total sobre quién puede extender estas clases, lo que permite el uso de expresiones `when` exhaustivas. Mientras que las clases selladas pueden mantener un estado (mediante propiedades), las interfaces selladas (introducidas en Kotlin 1.5) permiten una mayor flexibilidad al permitir que una clase implemente múltiples jerarquías selladas.

## The Senior Perspective (El Porqué)
Para un Senior, el valor no está solo en la restricción, sino en la mantenibilidad y la robustez del estado.

*   **Seguridad en el tiempo**: Al evitar el uso del bloque `else` en un `when`, obligamos al compilador a alertarnos si en el futuro alguien agrega un nuevo estado (ej. un nuevo error de red) y no lo manejamos en la UI.
*   **Optimización de Memoria**: Es una práctica recomendada usar `data object` para estados que no requieren parámetros (como `Loading` o `Empty`), ya que evitamos la creación innecesaria de múltiples instancias y obtenemos implementaciones automáticas de `equals` y `toString`.
*   **Modelado Atómico**: Son la piedra angular del patrón MVI, permitiendo que la UI reaccione a un único "Estado de Verdad" de forma predecible.

## Code in Action
```kotlin
// Modelado de estados de UI siguiendo principios Senior
sealed interface UIState {
    data object Loading : UIState // Uso de data object para eficiencia
    data class Success(val data: List<String>) : UIState
    data class Error(val message: String) : UIState
}

// El compilador garantiza que manejamos todos los casos
fun render(state: UIState) {
    when (state) {
        UIState.Loading -> showLoader()
        is UIState.Success -> showData(state.data) // Smart cast automático
        is UIState.Error -> showError(state.message)
    }
}
```

## Interview Prep (The Hot Seat)
**Pregunta**: ¿Cuándo elegirías una Sealed Interface sobre una Sealed Class?

**Respuesta Senior**: Elegiría una Sealed Interface cuando necesite que una clase implemente múltiples jerarquías selladas (herencia múltiple de comportamiento) o cuando no necesite almacenar un estado protegido o constructores específicos que solo una clase abstracta puede proveer. Las interfaces selladas son más ligeras y flexibles para arquitecturas modulares.

---
[Volver a Capítulos]({{ "/es/" | relative_url }})
