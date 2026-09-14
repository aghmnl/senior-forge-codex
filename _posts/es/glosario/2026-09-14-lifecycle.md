---
layout: post
title: "Lifecycle"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [lifecycle, android-framework]
lang: es
permalink: /es/glosario/lifecycle/
---

## The Theory (El Qué)

El **lifecycle** (ciclo de vida) es la secuencia de estados por la que pasa un componente Android entre su creación y su destrucción — para una Activity o Fragment: `CREATED → STARTED → RESUMED → STARTED → CREATED → DESTROYED`, impulsada por [lifecycle events]({{ "/es/glosario/lifecycle-event/" | relative_url }}). Jetpack lo modela como un objeto `Lifecycle` cuyo dueño es un `LifecycleOwner`, y eso es lo que permite que los componentes [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) lo observen en vez de ser llamados a mano desde `onStart`/`onStop`.

Todo scope del mundo de coroutines está atado a algún lifecycle: [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) al del ViewModel, `lifecycleScope` al del owner, `rememberCoroutineScope()` a la [composición]({{ "/es/glosario/composition-lifetime/" | relative_url }}).

## The Senior Nuance (El Matiz Senior)

- **La palabra nombra tres cosas anidadas.** Vida del proceso (la más larga), vida del ViewModel (sobrevive cambios de configuración), lifecycle de Activity/Fragment (muere en la rotación), vida de la composición (la más corta). Elegir dónde vive el estado y el trabajo es elegir a cuál de estas deben sobrevivir.
- **La cancelación sigue al lifecycle, no al revés.** Un [`CoroutineScope`]({{ "/es/glosario/coroutine-scope/" | relative_url }}) atado a un lifecycle cancela su [`Job`]({{ "/es/glosario/job/" | relative_url }}) cuando el owner se destruye; el trabajo que debe sobrevivir al owner necesita un scope de vida más larga, no uno filtrado.
- **`repeatOnLifecycle(STARTED)`** es el idioma para colectar un Flow solo mientras la UI está visible, reiniciando en cada `ON_START`.
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
