---
layout: post
title: "State Holder"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/state-holder/
---

## The Theory (El Qué)

Un **state holder** (contenedor de estado) es una clase responsable de poseer, producir y gestionar el estado de UI. En la arquitectura Android, los state holders centralizan la lógica de estado que de otra forma estaría dispersa entre composables o fragments, haciendo el estado testeable y capaz de sobrevivir cambios de configuración.

Hay dos categorías principales:

- **State holders basados en ViewModel** — subclasean `ViewModel`, scoped a un [ViewModelStore]({{ "/es/glosario/viewmodel-store/" | relative_url }}), sobreviven cambios de configuración. Contienen lógica de negocio y estado de dominio. Se inyectan vía [`by viewModels()`]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}) en Fragments o `hiltViewModel()` en Compose.
- **State holders de clase plana** — clases regulares (frecuentemente anotadas [`@Stable`]({{ "/es/glosario/stable/" | relative_url }})) que contienen estado específico de UI: posiciones de scroll, estado de animación, flags de expandido/colapsado. Creados vía `remember { MyStateHolder() }` o `rememberSaveable`. No sobreviven la muerte del proceso a menos que se guarden explícitamente.

Un state holder típicamente expone [estado observable]({{ "/es/glosario/observable-state/" | relative_url }}) — ya sea [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) para holders basados en ViewModel o `mutableStateOf()` para holders de nivel Compose — y funciones que modifican el estado en respuesta a eventos.

## The Senior Nuance (El Matiz Senior)

- Un Senior separa **state holders de negocio** (ViewModels: carga de datos, acciones de usuario, eventos de navegación) de **state holders de UI** (estado de scroll, estado de drag, input de formulario). Mezclar ambos lleva a ViewModels que conocen posiciones de píxeles y clases planas que llaman a repositorios.
- Los state holders [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) de Compose con [`by mutableStateOf()`]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}) participan en el [snapshot system]({{ "/es/glosario/snapshot-system/" | relative_url }}) directamente. Su [lifetime]({{ "/es/glosario/composition-lifetime/" | relative_url }}) está atado a la instancia de la clase, no a una posición en la [slot table]({{ "/es/glosario/slot-table/" | relative_url }}) — haciéndolos compartibles entre múltiples composables sin `remember`.
- La guía oficial de arquitectura de Google (Now in Android, architecture samples) recomienda elevar los state holders al ancestro común más bajo. Un state holder con scope demasiado alto desperdicia memoria; con scope demasiado bajo, se recrea en cada recomposición o navegación.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
