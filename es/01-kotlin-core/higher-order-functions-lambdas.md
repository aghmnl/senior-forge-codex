---
layout: page
title: Higher-Order Functions y Lambdas
lang: es
permalink: /es/01-kotlin-core/higher-order-functions-lambdas/
---

## The Theory (El Qué)

Las funciones de orden superior (HOFs) son funciones que reciben otras funciones como parámetros o las devuelven como resultado. En Kotlin, las funciones son "ciudadanos de primer nivel", lo que significa que pueden tratarse como cualquier otro valor: almacenarse en variables, pasarse a otras funciones o devolverse. Las lambdas son "literales de función": bloques de código que no se declaran como funciones tradicionales, sino que se pasan inmediatamente como expresiones.

## The Senior Perspective (El Porqué)

Un Ingeniero Senior evalúa las funciones de orden superior bajo la lente de la **abstracción frente al rendimiento en tiempo de ejecución**.

- **Sobrecarga de Memoria**: Cada vez que se pasa una lambda sin ser "inlineada", el compilador crea una nueva instancia de una clase `Function` (ej. `Function0`, `Function1`). En operaciones de alta frecuencia, esto aumenta la presión sobre el Garbage Collector.
- **El poder de `inline`**: Usar la palabra clave `inline` ordena al compilador reemplazar la llamada a la función con el código real de la lambda. Esto elimina la creación de objetos y permite características como los "non-local returns" (usar `return` dentro de una lambda para salir de la función que la llama).
- **Control sobre el Inlining**: `crossinline` se utiliza cuando una lambda se pasa a otro contexto de ejecución (como un objeto local o un hilo diferente) donde los retornos no locales están prohibidos. `noinline` se usa si necesitas mantener una lambda específica como un objeto para almacenarla o pasarla a otro lugar.
- **DSLs Declarativos**: Las HOFs combinadas con "Function types con receptores" son la base del desarrollo moderno en Android, permitiendo la sintaxis declarativa que vemos en Jetpack Compose o en las configuraciones de Hilt.

## Code in Action

```kotlin
// Enfoque Senior: Uso de inline para optimizar el manejo funcional de errores
sealed interface RepositoryResult {
    data object Loading : RepositoryResult
    data class Success(val data: String) : RepositoryResult
    data class Error(val code: Int) : RepositoryResult
}

// HOF inline para procesar resultados con cero coste de asignación
inline fun RepositoryResult.onSuccess(action: (String) -> Unit): RepositoryResult {
    if (this is RepositoryResult.Success) {
        action(data)
    }
    return this
}

fun fetchAndDisplay() {
    val result = RepositoryResult.Success("Contenido de la Forja")

    // El código dentro de esta lambda es "pegado" aquí por el compilador
    result.onSuccess { data ->
        println("Mostrando: $data")
    }
}
```

## Interview Prep (En el banquillo)

**Pregunta**: ¿Por qué evitarías usar la palabra clave inline para absolutamente todas las funciones de orden superior en un proyecto grande?

**Respuesta Senior**: Aunque inline evita la creación de objetos, provoca que el compilador copie el bytecode de la función en cada lugar donde se llama. Si la función es grande y se llama en muchos sitios, esto produce un "code bloat", aumentando significativamente el tamaño del binario final (APK/AAB). Además, las funciones inline no pueden acceder a miembros privados de la clase en la que se encuentran, lo que puede limitar las decisiones de arquitectura. Solo aplico inline en funciones que reciben lambdas y son lo suficientemente pequeñas como para justificar el compromiso.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
