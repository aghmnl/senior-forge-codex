---
layout: post
title: "Structural Sharing"
date: 2026-09-09 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/structural-sharing/
---

## The Theory (El Qué)

El **Structural Sharing** (compartición estructural) es la técnica que hace barata a la data inmutable: una copia "modificada" reutiliza cada parte sin cambios del original en vez de duplicarla. Solo son nuevos los nodos en el camino hacia el cambio.

```kotlin
// state y next comparten activeTasks, availableLabels, form, presets... todo
// menos la única propiedad que realmente cambió. Una asignación chica, no una copia profunda.
val next = state.copy(isDrawerOpen = true)
```

## The Senior Nuance (El Matiz Senior)

- Por esto "el estado inmutable es muy lento" casi siempre es falso para estado de UI. Un [`copy`]({{ "/es/glosario/copy/" | relative_url }}) de una clase de estado con treinta campos asigna un objeto con treinta referencias — unos cientos de bytes — sin importar qué tan grandes sean las listas referenciadas.
- También es la razón por la que el estado inmutable y la comparación con [`equals`]({{ "/es/glosario/equals/" | relative_url }}) se llevan bien. Los subárboles compartidos son idénticos por referencia, así que una comparación estructural corta temprano con `===` en cada rama que no cambió. [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) saltea subárboles enteros exactamente con esa señal.
- Las [Collections]({{ "/es/glosario/collections/" | relative_url }}) nativas de Kotlin **no** comparten estructura: `list + item` copia el array de respaldo completo, así que una operación que parece `O(1)` es `O(n)`. El sharing estructural real dentro de una colección requiere [Persistent Collections]({{ "/es/glosario/persistent-collections/" | relative_url }}) (`kotlinx.collections.immutable`), cuyo `add` basado en tries reutiliza todos los nodos salvo un puñado.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
