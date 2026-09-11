---
layout: post
title: "Observable State"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
tags: [state-management, compose, flow]
lang: es
permalink: /es/glosario/observable-state/
---

## The Theory (El Qué)

El **observable state** (estado observable) es estado que notifica automáticamente a sus observadores cuando cambia. En desarrollo Android, el estado observable es la base de la UI reactiva: la UI se suscribe al estado, y cuando el estado cambia, la UI se actualiza sin llamadas imperativas explícitas.

Kotlin y Android proveen varios mecanismos de estado observable:

- **El [snapshot system]({{ "/es/glosario/snapshot-system/" | relative_url }}) de Compose**: `mutableStateOf()` crea estado que dispara recomposición al ser escrito. Cuando se usa con la [keyword]({{ "/es/glosario/keyword/" | relative_url }}) [`by`]({{ "/es/glosario/by-delegation/" | relative_url }}) como [propiedad delegada]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}), las lecturas y escrituras parecen variables comunes mientras el snapshot system trackea cada cambio.
- **[StateFlow]({{ "/es/glosario/stateflow/" | relative_url }})**: Un state holder observable basado en [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) que emite el valor actual a nuevos collectors y todas las actualizaciones subsiguientes. Se convierte a estado de Compose vía `collectAsStateWithLifecycle()`.
- **`Delegates.observable`**: Un [property delegate]({{ "/es/glosario/property-delegate/" | relative_url }}) de la [standard library]({{ "/es/glosario/standard-library/" | relative_url }}) que ejecuta un callback después de cada asignación de propiedad.
- **LiveData** (legacy): Un observable [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) más antiguo, en gran parte superado por [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) y el estado de Compose.

## The Senior Nuance (El Matiz Senior)

- Un Senior elige el mecanismo de estado observable correcto para la capa: `mutableStateOf()` para estado de capa UI dentro de Compose, [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) para estado de capa ViewModel que necesita sobrevivir la recomposición y puede ser colectado desde múltiples observadores.
- El estado observable en Compose usa igualdad estructural (`equals()`) para determinar si la recomposición es necesaria. Si `equals()` retorna `true`, la escritura es un no-op. Por esto las clases [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) deben garantizar comportamiento consistente de `equals()`.
- No todo el estado necesita ser observable. Variables de computación local, contadores de loops y valores intermedios deben ser `val`/`var` comunes. Hacer todo observable agrega [overhead]({{ "/es/glosario/overhead/" | relative_url }}) y oscurece qué realmente impulsa la UI.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
