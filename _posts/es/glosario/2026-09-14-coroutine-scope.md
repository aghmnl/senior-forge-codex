---
layout: post
title: "CoroutineScope"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, lifecycle, cancellation]
lang: es
permalink: /es/glosario/coroutine-scope/
---

## The Theory (El Qué)

Un **`CoroutineScope`** es un objeto que sostiene un [`CoroutineContext`]({{ "/es/glosario/coroutine-context/" | relative_url }}) y actúa como receiver de `launch` y `async`. Su [`Job`]({{ "/es/glosario/job/" | relative_url }}) es la raíz de toda coroutine lanzada en él, así que cancelar el scope las cancela a todas — ese es el mecanismo detrás de [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}), `lifecycleScope` y `rememberCoroutineScope()`. Un scope custom se crea con `CoroutineScope(context)` y vive hasta que algo llame `cancel()`.

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

Un repositorio `@Singleton` sobrevive a toda pantalla, así que es dueño de un scope propio — con un [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) para que los collectors independientes no se cancelen entre sí, y `Dispatchers.IO` porque el cliente de billing bloquea.

## The Senior Nuance (El Matiz Senior)

- **Todo scope necesita un dueño que lo cancele.** Los scopes del framework los cancela su lifecycle owner. Un `CoroutineScope(...)` en un campo no lo cancela nadie salvo que lo escribas; se justifica solo para objetos que viven genuinamente tanto como el proceso, y debería decirlo en un comentario. `GlobalScope` es un scope sin dueño alguno — evitalo.
- **No pases scopes hacia abajo.** Un use case o repositorio que recibe `viewModelScope` queda acoplado al lifecycle de la UI. Exponé [suspend functions]({{ "/es/glosario/suspend-functions/" | relative_url }}) y dejá que el llamador sea dueño del scope.
- **No es lo mismo que el builder `coroutineScope { }`.** El [builder]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) es una suspend function que crea un scope hijo *temporal* y lo espera; `CoroutineScope(...)` crea uno de larga vida que tenés que manejar.
- **Un scope con `SupervisorJob` y sin [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }})** convierte cualquier excepción no capturada de un hijo en un crash del proceso. Agregá el handler cuando el scope corre trabajo fire-and-forget.
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
