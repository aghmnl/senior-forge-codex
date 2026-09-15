---
layout: post
title: "onCleared"
date: 2026-09-15 12:00:00 +0000
categories: [es, glosario]
tags: [lifecycle, android-framework, coroutines]
lang: es
permalink: /es/glosario/on-cleared/
---

## The Theory (El Qué)

**`onCleared()`** es el callback de `ViewModel` que se invoca una sola vez, cuando se limpia el [`ViewModelStore`]({{ "/es/glosario/viewmodel-store/" | relative_url }}) que lo posee — la Activity termina de verdad, o el destino de navegación sale del [back stack]({{ "/es/glosario/back-stack/" | relative_url }}). Es el único hook de [lifecycle]({{ "/es/glosario/lifecycle/" | relative_url }}) del ViewModel, y el momento en que se cancela [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}): toda coroutine lanzada sobre él, y todo hijo de esas, recibe una [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) en su próximo [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
override fun onCleared() {
    super.onCleared()
    // viewModelScope is already being cancelled by the framework.
    // Only non-coroutine resources need explicit release here.
    listenerRegistration.remove()
}
```

## The Senior Nuance (El Matiz Senior)

- **Rara vez hace falta sobreescribirlo.** Como `viewModelScope` se cancela solo, el override es únicamente para recursos que no son coroutines: listeners, closeables, scopes propios.
- **Es la raíz del árbol de una pantalla.** La razón por la que un campo `Job?` o un collector largo en un ViewModel no es un leak es que `onCleared` lo alcanza a través de la jerarquía de [`Job`]({{ "/es/glosario/job/" | relative_url }})s — siempre que nada se haya tragado la cancelación.
- **No corre en cambios de configuración.** Una rotación conserva el ViewModel; solo un desmontaje real lo limpia.
- Ver [Structured Concurrency]({{ "/es/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
