---
layout: post
title: "Composition Lifetime"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/composition-lifetime/
---

## The Theory (El Qué)

El **composition lifetime** (tiempo de vida de la composición) se refiere a cuánto tiempo un composable — y su estado recordado — existe en el árbol de composición. Un composable entra en la composición cuando es llamado por primera vez y sale cuando su padre deja de llamarlo (por ejemplo, una rama condicional cambia, un item de lista se elimina, o la navegación se mueve a otra pantalla).

El estado creado con `remember {}` (incluyendo [propiedades delegadas]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}) como `by remember { mutableStateOf() }`) se almacena en la [slot table]({{ "/es/glosario/slot-table/" | relative_url }}) y comparte el lifetime del composable — se crea al entrar, se preserva a través de recomposiciones, y se destruye al salir.

Esto difiere de otros lifetimes de Android:

- **Lifecycle de Activity/Fragment** — atado a eventos del OS (create, start, resume, pause, stop, destroy). Puede sobrevivir cambios de configuración vía `ViewModel`.
- **Lifetime de ViewModel** — atado al owner del [ViewModelStore]({{ "/es/glosario/viewmodel-store/" | relative_url }}) (Activity, Fragment, o entry del [back stack]({{ "/es/glosario/back-stack/" | relative_url }})). Sobrevive cambios de configuración, muere en la destrucción final.
- **Lifetime de proceso** — el scope más largo; `SavedStateHandle` / `rememberSaveable` conectan estado a través de la muerte del proceso.

## The Senior Nuance (El Matiz Senior)

- Un Senior reconoce que el composition lifetime es el scope más granular: el estado de un composable se destruye en el momento en que el composable sale del árbol, incluso si la pantalla sigue visible. Por esto navegar entre tabs puede destruir estado de composición si el composable del tab se remueve — se necesita `rememberSaveable` o estado respaldado por ViewModel para persistencia.
- Los [state holders]({{ "/es/glosario/state-holder/" | relative_url }}) [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) con `by mutableStateOf()` se desacoplan del composition lifetime: su estado vive en el [heap]({{ "/es/glosario/heap/" | relative_url }}) tanto como la instancia esté referenciada. Si se pasan como parámetro, su estado sobrevive la recomposición del composable que los contiene.
- Entender el composition lifetime es esencial para la limpieza de effects: `DisposableEffect` ejecuta su `onDispose` cuando el composable sale de la composición, mientras que `LaunchedEffect` cancela su coroutine. Un mismatch entre el scope del effect y el lifetime intencionado causa ya sea recursos con leak o limpieza prematura.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
