---
layout: post
title: "Event Wiring"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/event-wiring/
---

## The Theory (El Qué)

**Event wiring** (cableado de eventos) es la práctica de conectar componentes de UI con la lógica que maneja sus interacciones — enchufar [event handlers]({{ "/es/glosario/event-handlers/" | relative_url }}) en los composables, views o componentes de framework que producen eventos. En [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}), event wiring significa pasar [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) de [callback]({{ "/es/glosario/callbacks/" | relative_url }}) desde un composable a nivel de pantalla (que tiene la referencia al ViewModel) hacia abajo a los composables hoja. En el sistema de Views, significa llamar a `setOnClickListener`, `addTextChangedListener` o registrar interfaces observer.

```kotlin
// From FollowApp Suite — TasksCallbacks.kt
class TaskFormCallbacks(
    val onFormTitleChange: (String) -> Unit,
    val onFormDescriptionChange: (String) -> Unit,
    val onFormCompletedChange: (Boolean) -> Unit,
    val onFormDueDateChange: (Long?) -> Unit,
    val onFormConfirmed: () -> Unit,
    val onFormDismissed: () -> Unit,
    val onFormRecurrenceChange: (RecurrenceRule?) -> Unit,
    val onAddSubtask: (String) -> Unit,
)
```

Esta clase es el contrato de wiring: el composable de pantalla crea una instancia (cada [callback]({{ "/es/glosario/callbacks/" | relative_url }}) llamando al método correspondiente del ViewModel) y la pasa al composable del formulario, que invoca el handler correcto en cada interacción del usuario.

## The Senior Nuance (El Matiz Senior)

- **Compose hace el wiring explícito**: Cada camino de eventos es visible en la firma de la función — sin cadenas ocultas de `findViewById` + `setListener`. Esto facilita trazar qué pasa cuando un usuario tappea, tipea o swipea, porque el [callback]({{ "/es/glosario/callbacks/" | relative_url }}) está ahí mismo en la lista de parámetros.
- **La consolidación de callbacks es un patrón de wiring**: Cuando un formulario tiene 10+ eventos, pasarlos individualmente crea firmas ruidosas y call sites frágiles. Agruparlos en una clase (como `TaskFormCallbacks`) es una estrategia de wiring que mantiene la conexión limpia y [type-safe]({{ "/es/glosario/type-safety/" | relative_url }}).
- **En [MVI]({{ "/es/glosario/mvi-pattern/" | relative_url }})**, el event wiring rutea eventos de UI a una sola función `onEvent(UiEvent)` en el ViewModel. El wiring se convierte en un mapeo de acción de usuario → variante de sealed class, manteniendo la capa composable delgada y el ruteo de eventos centralizado.
- **Pitfalls del wiring en el sistema de Views**: Olvidarse de deswirear (desregistrar un listener) cuando una view se recicla (RecyclerView) o un fragment se destruye es una fuente clásica de [memory leak]({{ "/es/glosario/memory-leaks/" | relative_url }}). El modelo declarativo de Compose elimina este problema — el wiring existe solo mientras el composable está en el árbol de composición.
- **Los [broadcast receivers]({{ "/es/glosario/broadcast-receiver/" | relative_url }})** representan event wiring a nivel de sistema: registrar un receiver wirea tu componente a eventos de sistema o app (cambios de conectividad, batería baja). Los desarrolladores senior prefieren registro [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) para evitar leakear receivers.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
