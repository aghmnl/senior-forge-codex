---
layout: post
title: "Collector"
date: 2026-09-15 12:00:00 +0000
categories: [es, glosario]
tags: [flow, coroutines]
lang: es
permalink: /es/glosario/collector/
---

## The Theory (El Qué)

Un **collector** es la coroutine que llama a [`collect`]({{ "/es/glosario/collect/" | relative_url }}) sobre un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) — el extremo consumidor del stream. Un `Flow` frío no hace nada hasta que llega un collector; cada collector dispara su propia ejecución del bloque productor. El collector es un nodo de coroutine común: vive en el scope que lo lanzó, suspende entre emisiones, y se detiene cuando se cancela su [`Job`]({{ "/es/glosario/job/" | relative_url }}) o el flow completa.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
subtasksJob = viewModelScope.launch {
    getSubtasksUseCase(task.id)
        .catch { error -> Log.e(TAG, "Error loading subtasks", error) }
        .collect { subtasks ->
            _uiState.update { it.copy(form = it.form.copy(subtasks = subtasks)) }
        }
}
```

## The Senior Nuance (El Matiz Senior)

- **Un collector es un hijo de vida larga.** Para una fuente infinita (Room, [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }})), `collect` nunca retorna; la coroutine del collector termina solo por cancelación. Su scope decide su vida.
- **Un collector por fuente suele ser regla.** Guardar un `Job?` y cancelar el collector anterior antes de arrancar el siguiente evita que dos collectors escriban valores en competencia en el mismo estado.
- **`.catch` es solo upstream.** Ve las excepciones del productor, no las de la lambda del collector — y nunca una [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}).
- Ver [Structured Concurrency]({{ "/es/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
