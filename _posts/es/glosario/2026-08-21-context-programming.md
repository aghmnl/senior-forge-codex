---
layout: post
title: "Context (Programming)"
date: 2026-08-21 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/context-programming/
---

## La Teoría (El Qué)

En programación, un **context** (contexto) es el estado, entorno u objeto circundante que provee significado y recursos a una pieza de código. El término está sobrecargado a través de diferentes niveles:

- **Nivel del lenguaje**: En las [scope functions]({{ "/es/01-kotlin-core/scope-functions/" | relative_url }}) de Kotlin, el "objeto de contexto" es el objeto sobre el cual la función opera — disponible como `this` o `it` dentro de la lambda.
- **Nivel Android**: `android.content.Context` es la puerta de acceso del sistema a recursos de la aplicación, servicios, bases de datos y el sistema operativo. Cada Activity, Service y Application es un Context.
- **Nivel de coroutines**: `CoroutineContext` es un conjunto de elementos (dispatcher, job, exception handler) que definen cómo y dónde se ejecuta una coroutine.

## El Matiz Senior

- **Jerarquía de Context en Android**: El context de `Application` vive durante todo el tiempo de vida de la app; el context de `Activity` está atado a una pantalla. Usar un context de Activity en un singleton de larga vida causa memory leaks. Usar el context de Application para operaciones de UI (como inflar una vista con tema) da resultados incorrectos porque carece del theme de la Activity.
- En las scope functions, el concepto de "objeto de contexto" no tiene relación con la clase `Context` de Android — una fuente frecuente de confusión para desarrolladores nuevos en Kotlin para Android.
- El **coroutine context** es aditivo: los contexts se pueden combinar con `+` (`Dispatchers.IO + SupervisorJob()`). Entender esta composición es esencial para la structured concurrency.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
