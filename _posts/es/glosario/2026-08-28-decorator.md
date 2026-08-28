---
layout: post
title: "Decorator"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/decorator/
---

## The Theory (El Qué)

El patrón **Decorator** agrega comportamiento a un objeto dinámicamente envolviéndolo en otro objeto que implementa la misma interfaz. El wrapper delega las llamadas al original y agrega su propia lógica antes o después. En OOP clásico, esto evita la explosión combinatoria del subclassing: en vez de crear `LoggingCachingRepository`, `LoggingRepository` y `CachingRepository` como subclases separadas, se apilan decorators.

En Kotlin, la keyword `by` hace la delegación trivial:

```kotlin
class LoggingRepository(
    private val delegate: TaskRepository
) : TaskRepository by delegate {
    override fun save(task: Task) {
        log("Saving task ${task.id}")
        delegate.save(task)
    }
}
```

## The Senior Nuance (El Matiz Senior)

- Las [extension functions]({{ "/es/glosario/extension-functions/" | relative_url }}) de Kotlin frecuentemente reemplazan el patrón Decorator para casos simples. Cuando necesitás agregar comportamiento a un tipo sin envolverlo — y no necesitás interceptar cada método — una extensión es más liviana e idiomática.
- La distinción clave: un Decorator envuelve y controla el acceso al objeto original (puede interceptar *cualquier* llamada a método). Una extension function agrega una función nueva pero no puede interceptar las existentes. Elegí Decorator cuando necesitás modificar u observar comportamiento de métodos existentes; elegí extensiones cuando estás agregando comportamiento nuevo.
- En Android, el patrón Decorator aparece naturalmente en capas de repositorio (agregando caching, logging o manejo de errores alrededor de un data source) y en cadenas de `InputStream`/`OutputStream` de la librería I/O de Java.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
