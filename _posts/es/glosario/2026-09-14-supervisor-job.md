---
layout: post
title: "SupervisorJob"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, cancellation, error-handling]
lang: es
permalink: /es/glosario/supervisor-job/
---

## The Theory (El Qué)

Un **`SupervisorJob`** es un [`Job`]({{ "/es/glosario/job/" | relative_url }}) cuyos hijos fallan de forma independiente: la excepción de un hijo no cancela al padre, y por lo tanto no cancela a sus hermanos. Todo lo demás del árbol es igual — cancelar el supervisor sigue cancelando a todos los hijos. Es la raíz correcta para un [scope]({{ "/es/glosario/coroutine-scope/" | relative_url }}) que es dueño de varias coroutines de larga duración no relacionadas entre sí.

```kotlin
// From FollowApp Suite — PremiumRepositoryImpl.kt
private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

init {
    scope.launch {
        billingConnector.isOwned.filterNotNull().collect { owned ->
            premiumPreferences.setAdsRemoved(owned)
        }
    }
}
```

`viewModelScope` y `lifecycleScope` se construyen sobre un `SupervisorJob` por la misma razón: un `launch` fallido no debe derribar a todas las otras coroutines de la pantalla.

## The Senior Nuance (El Matiz Senior)

- **Cambia adónde van las excepciones no capturadas.** Con un `Job` común, la excepción de un hijo se propaga al padre, que puede manejarla. Con un `SupervisorJob` no hay propagación hacia arriba, así que la excepción va al [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}) del contexto — y si no hay ninguno, al handler de excepciones no capturadas del thread, que crashea la app. Un `SupervisorJob` sin handler es un crash esperando a que un `collect` lance una excepción.
- **Solo supervisa a los hijos *directos*.** Dentro de un hijo aplican las reglas normales: el fallo de un nieto sigue cancelando a su padre (el hijo). La supervisión no se anida automáticamente.
- **`supervisorScope { }` es la forma estructurada, como suspend function.** Usala para un fan-out acotado donde los fallos deben ser independientes; usá `SupervisorJob()` en un `CoroutineScope(...)` para scopes de larga vida.
- **No lo pongas en `launch(SupervisorJob())`.** Eso desprende la coroutine del árbol del scope por completo — el scope ya no puede cancelarla. El supervisor va en el contexto del scope, no en el call site.
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
