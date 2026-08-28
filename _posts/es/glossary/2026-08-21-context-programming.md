---
layout: post
title: "Contexto (Programación)"
date: 2026-08-21 12:00:00 +0000
categories: [es, glossary]
lang: es
permalink: /es/glosario/context-programming/
---

## The Theory (El Qué)

En programación, un **contexto** es el estado, entorno u objeto circundante que da significado y recursos a un fragmento de código. El término se usa con diferentes acepciones según el nivel:

- **Nivel de lenguaje**: En las [scope functions]({{ "/es/01-kotlin-core/scope-functions/" | relative_url }}) de Kotlin, el "objeto de contexto" es el objeto sobre el que opera la función — disponible como `this` o `it` dentro de la lambda.
- **Nivel Android**: `android.content.Context` es la puerta de entrada del sistema a los recursos de la aplicación, servicios, bases de datos y el sistema operativo. Cada Activity, Service y Application es un Context.
- **Nivel corrutinas**: `CoroutineContext` es un conjunto de elementos (dispatcher, job, exception handler) que definen cómo y dónde se ejecuta una corrutina.

## The Senior Nuance (El Matiz Senior)

- **Jerarquía de Context en Android**: El contexto de `Application` vive durante toda la vida de la app; el contexto de `Activity` está atado a una pantalla. Usar un contexto de Activity en un singleton de larga vida causa memory leaks. Usar el contexto de Application para operaciones de UI (como inflar una vista con tema) da resultados incorrectos porque carece del tema de la Activity.
- En las scope functions, el concepto de "objeto de contexto" no tiene relación con la clase `Context` de Android — una fuente frecuente de confusión para desarrolladores nuevos en Kotlin sobre Android.
- El **contexto de corrutina** es aditivo: los contextos se pueden combinar con `+` (`Dispatchers.IO + SupervisorJob()`). Entender esta composición es esencial para la concurrencia estructurada.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
