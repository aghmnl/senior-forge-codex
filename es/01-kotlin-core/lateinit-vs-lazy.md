---
layout: page
title: Lateinit vs Lazy
lang: es
permalink: /es/01-kotlin-core/lateinit-vs-lazy/
---

## The Theory (El Qué)

Tanto `lateinit` como `lazy` ofrecen formas de retrasar la inicialización de propiedades, pero cumplen propósitos técnicos distintos. `lateinit` es un modificador para variables mutables (`var`) que no son nulables y se inicializarán más tarde (frecuentemente por un framework como Dagger o durante un evento del ciclo de vida). `lazy` es una propiedad delegada para variables de solo lectura (`val`) que calcula el valor solo en su primer acceso y cachea el resultado para usos futuros.

## The Senior Perspective (El Porqué)

Elegir entre ellos es una cuestión de **mutabilidad, seguridad de hilos y propiedad**.

- **Modos de Seguridad de Hilos**: Por defecto, `lazy` es thread-safe (`LazyThreadSafetyMode.SYNCHRONIZED`). Un Senior sabe cuándo usar `NONE` para optimizar el rendimiento si la propiedad se accede solo desde un hilo (ej. el hilo de UI), o `PUBLICATION` si varios hilos pueden calcular el valor simultáneamente.
- **Inyección de Dependencias**: `lateinit` es esencial para la inyección de campos (Hilt/Dagger). Dado que estos frameworks usan reflexión para asignar valores después de que el objeto es construido, `lateinit` permite tipos no nulables sin chequeos de nulos innecesarios.
- **Gestión de Memoria**: `lazy` es ideal para objetos "pesados" (como consultas costosas a base de datos o ViewModels complejos) porque difiere la asignación de memoria hasta que es estrictamente necesario.
- **Chequeo de Estado**: Un Senior utiliza `.isInitialized` en propiedades `lateinit` para evitar `UninitializedPropertyAccessException` cuando el flujo de inicialización puede ser no lineal o condicional.

## Code in Action

```kotlin
// Enfoque Senior: Elección entre lazy para recursos y lateinit para inyección
class ProductDetailViewModel(
    private val repository: ProductRepository // Inyectado vía constructor
) {
    // Inyectado por el framework más tarde
    lateinit var analyticsTracker: AnalyticsTracker

    // Calculado solo cuando se accede (ej. cuando la UI lo solicita)
    val heavyDataDetails: List<String> by lazy(LazyThreadSafetyMode.NONE) {
        repository.getExpensiveMetadata()
    }

    fun onStart() {
        if (::analyticsTracker.isInitialized) {
            analyticsTracker.trackScreenView("ProductDetail")
        }
    }
}
```

## Interview Prep (En el banquillo)

**Pregunta**: ¿Qué ocurre internamente cuando accedes a una propiedad lazy por primera vez y en qué se diferencia de una propiedad lateinit a nivel de bytecode?

**Respuesta Senior**: Cuando se accede a una propiedad lazy, se llama al método delegado getValue(). Este comprueba un campo interno _value; si es el centinela UNINITIALIZED_VALUE, ejecuta la lambda dentro de un bloque sincronizado (por defecto) para asegurar la seguridad de hilos, luego almacena y devuelve el resultado. En contraste, lateinit no utiliza delegación; el compilador simplemente genera un acceso directo al campo pero añade un chequeo de nulos a nivel de bytecode que lanza una UninitializedPropertyAccessException si el backing field es nulo.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
