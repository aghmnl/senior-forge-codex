---
layout: post
title: "Event Handlers"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/event-handlers/
---

## The Theory (El Qué)

Un **event handler** (manejador de eventos) es un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) que responde a una interacción específica del usuario o evento del sistema — un tap en un botón, un cambio de texto, una transición de lifecycle, un gesto. En [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}), los event handlers son parámetros [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) (`onClick`, `onValueChange`, `onDismissRequest`) pasados a funciones composable. En el sistema de Views, son interfaces de listener (`OnClickListener`, `OnScrollListener`) seteadas en widgets.

```kotlin
// From FollowApp Suite — ConfirmationDialog.kt
@Composable
fun ConfirmationDialog(
    title: String,
    message: String,
    confirmLabel: String,
    dismissLabel: String,
    onConfirm: (dontAskAgain: Boolean) -> Unit,
    onDismiss: () -> Unit,
    dontAskAgainLabel: String? = null,
) {
    // ...
    confirmButton = {
        TextButton(onClick = { onConfirm(dontAskAgain) }) { Text(confirmLabel) }
    }
    dismissButton = {
        TextButton(onClick = onDismiss) { Text(dismissLabel) }
    }
}
```

Cada event handler tiene una firma [type-safe]({{ "/es/glosario/type-safety/" | relative_url }}): `onConfirm` recibe un `Boolean` (la flag de "no preguntar de nuevo"), mientras que `onDismiss` no toma argumentos.

## The Senior Nuance (El Matiz Senior)

- **Flujo de eventos en Compose**: Los eventos fluyen **hacia arriba** (hijo → padre) mientras el estado fluye **hacia abajo** (padre → hijo). Este es el patrón de [unidirectional data flow]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}). Los event handlers son el canal ascendente — notifican al padre (a menudo un ViewModel) que algo pasó, y el padre actualiza el estado.
- **Consolidación vía clases de callback**: Cuando un composable necesita muchos event handlers, agruparlos en una clase dedicada (como `TaskFormCallbacks`) evita la explosión de listas de parámetros y hace la API más fácil de evolucionar. Ver [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}).
- **No hagas trabajo pesado dentro de event handlers**: Un `onClick` corre en el thread principal. Si necesitás trabajo async, lanzá una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) desde el handler o despachá un intent/evento al ViewModel. En [MVI]({{ "/es/glosario/mvi-pattern/" | relative_url }}), los event handlers simplemente emiten user intents.
- **Estabilidad y recomposición**: En Compose, un event handler lambda captura su estado envolvente. Si esas capturas son inestables (referencian un objeto mutable que no es `State`), el composable se considera inestable y no puede ser salteado durante la recomposición. Los desarrolladores senior usan `remember`, referencias estables o mueven el handler a un holder estable para evitar esto.
- **Legado del sistema de Views**: En el sistema de Views, olvidarse de remover un event handler (ej., un `OnClickListener` en una view retenida por un adapter de larga vida) es un vector de [memory leak]({{ "/es/glosario/memory-leaks/" | relative_url }}). El modelo declarativo de Compose elimina esto — los handlers existen solo mientras el composable está en la composición.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
