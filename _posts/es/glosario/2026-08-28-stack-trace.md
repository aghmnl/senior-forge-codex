---
layout: post
title: "Stack Trace"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
tags: [error-handling, jvm, coroutines]
lang: es
permalink: /es/glosario/stack-trace/
---

## The Theory (El Qué)

Un **stack trace** es la captura de la [pila de llamadas]({{ "/es/glosario/call-stack/" | relative_url }}) en el momento en que se lanza una excepción. Lista cada llamada a función ([frame]({{ "/es/glosario/stack-frame/" | relative_url }})) desde el punto de fallo hasta el punto de entrada, mostrando el nombre del archivo y número de línea para cada [frame]({{ "/es/glosario/stack-frame/" | relative_url }}). En la JVM, `Throwable.stackTrace` captura esta información automáticamente.

## The Senior Nuance (El Matiz Senior)

- Un stack trace significativo es la diferencia entre arreglar algo en 5 minutos o una hora de adivinanzas. Por eso `?: throw IllegalStateException("order required at checkout")` es mejor que `!!` — el crash con `!!` produce una [NullPointerException]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) genérica sin contexto, mientras que el throw explícito te dice exactamente qué [invariante]({{ "/es/glosario/invariant/" | relative_url }}) se violó.
- Los stack traces de [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) están fragmentados por defecto porque las [funciones `suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) se transforman en [máquinas de estado]({{ "/es/glosario/state-machine/" | relative_url }}). Librerías como `kotlinx-coroutines-debug` reconstruyen la cadena de llamadas lógica a través de los [puntos de suspensión]({{ "/es/glosario/suspension-point/" | relative_url }}).
- En Android, los stack traces de builds de release están [ofuscados]({{ "/es/glosario/obfuscation/" | relative_url }}) por [R8]({{ "/es/glosario/r8/" | relative_url }})/[ProGuard]({{ "/es/glosario/proguard/" | relative_url }}). Un Senior mantiene los archivos de mapping y los sube a [Crashlytics]({{ "/es/glosario/crashlytics/" | relative_url }}) para que los stack traces de producción sean legibles.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
