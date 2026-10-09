---
layout: post
title: "One-shot Event"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [architecture, state-management, flow]
lang: es
permalink: /es/glosario/one-shot-event/
---

## The Theory (El Qué)

Un **evento one-shot** (de una sola vez) es algo que el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) quiere que la UI haga **exactamente una vez**: navegar, mostrar un snackbar, abrir un diálogo. A diferencia del estado, no es "cómo se ve la pantalla ahora" sino "algo que pasó", y procesarlo dos veces (navegar dos veces después de una rotación) o ninguna (descartarlo mientras la pantalla está en background) es un bug.

```kotlin
// Not found in FAS — standalone example
private val _events = Channel<UiEvent>(Channel.BUFFERED)
val events: Flow<UiEvent> = _events.receiveAsFlow()
```

## The Senior Nuance (El Matiz Senior)

- **No hay una primitiva perfecta.** Un [`SharedFlow`]({{ "/es/glosario/sharedflow/" | relative_url }}) sin replay descarta los eventos sin [collector]({{ "/es/glosario/collector/" | relative_url }}); con replay los repite. Un [channel]({{ "/es/glosario/channel/" | relative_url }}) con buffer y `receiveAsFlow()` entrega después y una sola vez, pero igual puede perder un evento si el [collector]({{ "/es/glosario/collector/" | relative_url }}) se cancela después de recibirlo.
- **Google prefiere modelarlo como estado**: el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) expone "navegar a X" en el estado de UI, la UI actúa y le pide al [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) que lo limpie. Eso sobrevive a la rotación y a la muerte del proceso, y es fácil de testear.
- Ver [receiveAsFlow()]({{ "/es/02-coroutines-flow/receive-as-flow/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
