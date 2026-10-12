---
layout: post
title: "Sealed State"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [state-management, sealed-types, architecture]
lang: es
permalink: /es/glosario/sealed-state/
---

## The Theory (El Qué)

Un **sealed state** modela el UI state de una pantalla como una [`sealed interface`]({{ "/es/glosario/sealed-interface/" | relative_url }}) (o [`sealed class`]({{ "/es/glosario/sealed-class/" | relative_url }})) cuyos subtipos son estados mutuamente excluyentes, como `Loading`, [`Success`]({{ "/es/glosario/success-state/" | relative_url }}) y [`Error`]({{ "/es/glosario/error-state/" | relative_url }}). La pantalla siempre está en exactamente uno de ellos, cada subtipo lleva solo sus propios datos, y un `when` sin `else` tiene que manejar todos los subtipos.

```kotlin
// Not found in FAS — standalone example
sealed interface DetailState {
    data object Loading : DetailState
    data class Success(val task: Task) : DetailState
    data class Error(val message: String) : DetailState
}
```

## The Senior Nuance (El Matiz Senior)

- **No puede representar combinaciones imposibles**: no hay un valor que esté cargando y fallado al mismo tiempo.
- **Le cuesta cuando las preocupaciones se superponen.** Los datos compartidos por varios estados (una búsqueda, una selección) se tienen que duplicar en cada subtipo o se pierden en cada transición.
- Ver [UI State Modeling: Sealed vs Flat Data Class]({{ "/es/05-architecture/ui-state-modeling/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
