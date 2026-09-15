---
layout: post
title: "supervisorScope"
date: 2026-09-15 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, cancellation, error-handling]
lang: es
permalink: /es/glosario/supervisor-scope/
---

## The Theory (El Qué)

**`supervisorScope { }`** es el hermano de [`coroutineScope { }`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}): una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) que crea un scope hijo, corre el bloque, y suspende hasta que toda coroutine lanzada adentro termina — pero con semántica de [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}). Un hijo que falla **no** cancela a sus hermanos ni al scope; su excepción va al [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}) del contexto (para [`launch`]({{ "/es/glosario/launch/" | relative_url }})) o queda en el [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) (para [`async`]({{ "/es/glosario/async/" | relative_url }})).

```kotlin
// Not found in FAS — standalone example
suspend fun loadDashboardLenient(): Dashboard = supervisorScope {
    val header = async { api.header() }
    val items = async { api.items() }
    Dashboard(
        header = runCatching { header.await() }.getOrNull(),
        items = runCatching { items.await() }.getOrDefault(emptyList())
    )
}
```

## The Senior Nuance (El Matiz Senior)

- **Elegilo cuando los hijos son unidades de trabajo independientes.** "Escribí las que puedas y reportá los fallos" es `supervisorScope`; "todo o nada" es `coroutineScope`.
- **Sigue esperando y sigue cancelando hacia abajo.** Solo cambia la *propagación de fallos entre hermanos*. Cancelar la coroutine que lo contiene cancela todo lo de adentro.
- **Un fallo de `launch` adentro necesita un handler.** Sin [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}) en el contexto, una excepción no capturada en un hijo `launch` crashea el proceso aunque los hermanos sobrevivan.
- Ver [Structured Concurrency]({{ "/es/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
