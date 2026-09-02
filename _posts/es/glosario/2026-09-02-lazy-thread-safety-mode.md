---
layout: post
title: "LazyThreadSafetyMode"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/lazy-thread-safety-mode/
---

## The Theory (El Qué)

**`LazyThreadSafetyMode`** es un enum que controla cómo una propiedad `lazy` maneja el primer acceso concurrente desde múltiples threads. Tiene tres valores:

- **`SYNCHRONIZED`** (por defecto): La [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) de inicialización corre dentro de un [bloque synchronized]({{ "/es/glosario/synchronized-block/" | relative_url }}). Solo un thread ejecuta la lambda; todos los demás esperan y reciben el resultado cacheado. Seguro pero con overhead de sincronización.
- **`PUBLICATION`**: Múltiples threads pueden ejecutar la lambda de inicialización simultáneamente. El primer thread en terminar almacena su resultado; todos los demás descartan el suyo. Seguro cuando la lambda no tiene side effects y querés evitar bloqueo — al costo de computación redundante.
- **`NONE`**: Sin sincronización alguna. La lambda corre en cualquier thread que acceda primero, sin protección contra acceso concurrente. **El más rápido**, pero solo seguro cuando garantizás acceso single-threaded (ej. el thread de UI en [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }})).

```kotlin
// Standalone example — no LazyThreadSafetyMode usage found in FAS
// Propiedad solo de UI — seguro skipear sincronización
val headerConfig: HeaderConfig by lazy(LazyThreadSafetyMode.NONE) {
    repository.loadExpensiveHeaderConfig()
}

// Init segura multi-threaded — computación redundante es OK
val sharedConfig: Config by lazy(LazyThreadSafetyMode.PUBLICATION) {
    parseConfigFromDisk()
}
```

## The Senior Nuance (El Matiz Senior)

- **El default es casi siempre correcto**: `SYNCHRONIZED` es el default seguro y debería usarse a menos que el profiling muestre que la sincronización es un bottleneck. Optimización prematura con `NONE` en un path multi-threaded lleva a bugs sutiles y difíciles de reproducir.
- **`NONE` en Compose**: Las propiedades accedidas solo desde el thread principal (funciones Composable, estado del ViewModel) son candidatas seguras para `NONE`. Como Compose garantiza recomposición single-threaded en el thread principal, el overhead de sincronización es puro desperdicio.
- **Caso de uso de `PUBLICATION`**: Ideal para configuración inmutable o computaciones costosas donde el resultado es siempre el mismo sin importar qué thread lo compute. La lambda puede correr más de una vez durante la carrera, pero el valor almacenado es consistente.
- **Visibilidad con `NONE`**: Incluso con `NONE`, el delegado `Lazy` almacena el resultado en un campo `@Volatile`, así que una vez inicializado, todos los threads ven el valor. El riesgo es solo durante la carrera de inicialización en sí — dos threads podrían ejecutar la lambda y el resultado de uno se descarta silenciosamente.
- **Testing**: Si los tests corren en múltiples threads (ej. `runTest` con `UnconfinedTestDispatcher`), una propiedad `lazy(NONE)` puede exhibir comportamiento flaky. Usá `SYNCHRONIZED` en contextos de test o asegurá acceso single-threaded.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
