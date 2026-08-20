---
layout: page
title: "Data Objects: Singleton y Eficiencia de Memoria"
lang: es
permalink: /es/01-kotlin-core/data-objects/
---

## The Theory (El Qué)

Un `data object` (introducido en Kotlin 1.9) combina la garantía de singleton de `object` con los métodos `toString()`, `equals()` y `hashCode()` generados por el compilador como en una `data class`. A diferencia de un `object` simple, que produce un `toString()` por defecto como `Loading@3a71f4dd`, un `data object` genera una representación limpia y legible usando solo el nombre de la clase — por ejemplo, `Loading`. No se generan funciones `copy()` ni `componentN()`, ya que los singletons no tienen propiedades de constructor para copiar o desestructurar.

## The Senior Perspective (El Porqué)

Para un ingeniero Senior, `data object` resuelve un dolor específico en jerarquías selladas y modelado de estado.

- **Logging y Debugging Limpio**: En jerarquías de sealed class, los miembros sin estado como `Loading` o `Idle` declarados como `object` simple producen un toString inútil (`Loading@3a71f4dd`). Un `data object` garantiza una representación legible sin necesidad de sobrescribir manualmente.
- **Garantía de Singleton**: A diferencia de `data class`, un `data object` es un verdadero singleton — existe exactamente una instancia. Esto significa cero asignaciones innecesarias para estados que no llevan datos, lo cual importa en patrones de emisión de estado de alta frecuencia (ej. actualizaciones de StateFlow).
- **Igualdad Consistente**: `equals()` siempre retorna `true` cuando se compara un `data object` consigo mismo (igualdad referencial y estructural son idénticas para singletons). Esto previene bugs sutiles al mezclar verificaciones `==` y `===` en expresiones `when` u operaciones de colecciones.
- **Best Practice en Sealed Hierarchies**: La convención moderna es usar `data object` para miembros sin estado y `data class` para miembros con estado dentro de una jerarquía sellada.

## Code in Action

```kotlin
sealed interface DownloadState {
    data object Idle : DownloadState
    data object Downloading : DownloadState
    data class Progress(val percent: Int) : DownloadState
    data class Completed(val filePath: String) : DownloadState
    data class Failed(val error: Throwable) : DownloadState
}

fun logState(state: DownloadState) {
    // data object da un toString limpio: "Idle", "Downloading"
    // data class da un toString estructurado: "Progress(percent=42)"
    println("Estado actual: $state")
}

fun main() {
    val a = DownloadState.Idle
    val b = DownloadState.Idle

    println(a === b) // true — misma instancia singleton
    println(a == b)  // true — igualdad estructural
    println(a)       // "Idle" — toString limpio del data object
}
```

## Interview Prep (The Hot Seat)

**Pregunta**: ¿Por qué preferir `data object` sobre un `object` simple para miembros sin estado de una jerarquía sellada?

**Respuesta Senior**: Un `object` simple genera un `toString()` por defecto que incluye la dirección de memoria (ej. `Loading@3a71f4dd`), lo cual no sirve para logging ni debugging. Un `data object` genera un `toString()` limpio usando solo el nombre de la clase, además de implementaciones consistentes de `equals()` y `hashCode()`. Como los miembros sin estado de jerarquías selladas se loguean, comparan y emiten a través de Flows frecuentemente, el `data object` provee el comportamiento correcto y legible por defecto sin sobrescrituras manuales.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
