---
layout: post
title: "Stack Trace"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/stack-trace/
---

## La Teoría (El Qué)

Un **stack trace** es la captura de la pila de llamadas en el momento en que se lanza una excepción. Lista cada llamada a función (frame) desde el punto de fallo hasta el punto de entrada, mostrando el nombre del archivo y número de línea para cada frame. En la JVM, `Throwable.stackTrace` captura esta información automáticamente.

## El Matiz Senior

- Un stack trace significativo es la diferencia entre arreglar algo en 5 minutos o una hora de adivinanzas. Por eso `?: throw IllegalStateException("order required at checkout")` es mejor que `!!` — el crash con `!!` produce una [NullPointerException]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) genérica sin contexto, mientras que el throw explícito te dice exactamente qué invariante se violó.
- Los stack traces de coroutines están fragmentados por defecto porque las funciones `suspend` se transforman en máquinas de estado. Librerías como `kotlinx-coroutines-debug` reconstruyen la cadena de llamadas lógica a través de los puntos de suspensión.
- En Android, los stack traces de builds de release están ofuscados por R8/ProGuard. Un Senior mantiene los archivos de mapping y los sube a Crashlytics para que los stack traces de producción sean legibles.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
