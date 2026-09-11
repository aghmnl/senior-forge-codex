---
layout: post
title: "Conflation"
date: 2026-09-09 12:00:00 +0000
categories: [es, glosario]
tags: [flow, state-management]
lang: es
permalink: /es/glosario/conflation/
---

## The Theory (El Qué)

La **Conflation** (conflación) es descartar valores intermedios cuando un consumidor es más lento que el productor, quedándose solo con el más reciente. [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}) es conflated por definición: guarda exactamente un valor, y un collector ocupado simplemente va a ver el último estado cuando vuelva, no la cola de estados que se perdió.

```kotlin
// Tres updates rápidos mientras la UI está recomponiendo.
// El collector puede observar solo el último — y para estado eso es correcto.
_uiState.update { it.copy(isLoading = true) }
_uiState.update { it.copy(activeTasks = tasks) }
_uiState.update { it.copy(isLoading = false) }
```

## The Senior Nuance (El Matiz Senior)

- La conflación está *bien* para estado y *mal* para eventos. "El set de filtros actual" solo necesita su último valor; "mostrar un snackbar" tiene que pasar una vez por ocurrencia. Modelar un evento one-shot como un campo de `StateFlow` es la forma de que un toast se pierda en un frame lento — o se repita tras un cambio de configuración.
- Por eso un `StateFlow` es seguro de publicar desde un hot loop: un productor emitiendo cien veces por segundo no puede atorar la UI, porque no hay buffer que llenar. Un `SharedFlow` con buffer no tiene esa propiedad.
- `StateFlow` conflaciona por [`equals`]({{ "/es/glosario/equals/" | relative_url }}), no solo por velocidad: asignarle a `value` algo igual al valor actual no emite nada. Con una clase de estado [inmutable]({{ "/es/glosario/immutability/" | relative_url }}) eso es exactamente la deduplicación que querés; con una mutable descarta cambios reales en silencio.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
