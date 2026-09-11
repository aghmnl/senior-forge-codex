---
layout: post
title: "CancellationException"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
tags: [cancellation, coroutines, error-handling]
lang: es
permalink: /es/glosario/cancellation-exception/
---

## The Theory (El Qué)

**`CancellationException`** es la excepción que una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) lanza desde su próximo [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}) una vez que su job fue cancelado. Es el mecanismo de la [cooperative cancellation]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}): desenrolla la [state machine]({{ "/es/glosario/state-machine/" | relative_url }}) igual que lo haría cualquier excepción, así los bloques `finally` y `use { }` corren. El framework la trata de forma especial — una coroutine que termina con ella se considera *cancelada*, no *fallida*, y nunca se reporta al `CoroutineExceptionHandler`.

```kotlin
// From FollowApp Suite — DragToReorder.kt
} catch (e: CancellationException) {
    // Gesture coroutine disposed mid-drag (e.g. composition change)
    state.endDrag(cancelled = true)
    throw e
}
```

Atrapala para limpiar estado local, y después **relanzala**. Tragársela deja que la coroutine continúe más allá del punto donde se le dijo que pare.

## The Senior Nuance (El Matiz Senior)

- **`runCatching` y `catch (e: Exception)` se la tragan.** `CancellationException` extiende `IllegalStateException`. Un `runCatching { }` alrededor de una llamada suspendible convierte un ViewModel cancelado en uno que sigue escribiendo a disco. Filtrala: `catch (e: Exception) { if (e is CancellationException) throw e; ... }`, o usá `ensureActive()` después del catch.
- **Es barata a propósito.** La instancia del framework se saltea el llenado del stack trace, así que cancelar no es una operación costosa.
- **No la lances vos para señalar errores de dominio.** Un usuario cancelando un diálogo es un *resultado*, no una cancelación — el flujo de sign-in de FAS atrapa `GetCredentialCancellationException`, un tipo distinto, por esa razón.
- Ver [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
