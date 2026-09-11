---
layout: post
title: "Back Stack"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
tags: [navigation, lifecycle, android-framework]
lang: es
permalink: /es/glosario/back-stack/
---

## The Theory (El Qué)

El **back stack** (pila de navegación) es una pila LIFO (last-in, first-out) que Android usa para trackear el historial de navegación. Cuando un usuario navega hacia adelante, el destino actual se apila en el back stack; presionar Back desapila la entrada superior y retorna al destino anterior.

Android gestiona varias capas de back stack:

- **Back stack de Activity** (task stack) — gestionado por el OS. Cada task tiene una pila de Activities.
- **Back stack de Fragment** — gestionado por `FragmentManager`. Las transacciones de Fragment pueden agregarse al back stack vía `addToBackStack()`.
- **Back stack del navigation component** — gestionado por `NavController`. Cada `NavBackStackEntry` contiene el destino, argumentos y un [ViewModelStore]({{ "/es/glosario/viewmodel-store/" | relative_url }}). Este es el estándar moderno.

En navegación Compose, cada `NavBackStackEntry` también es un `ViewModelStoreOwner` y un `LifecycleOwner`. Cuando una entrada es sacada del back stack, sus ViewModels son limpiados y su [lifecycle]({{ "/es/glosario/lifecycle-event/" | relative_url }}) alcanza `DESTROYED`.

## The Senior Nuance (El Matiz Senior)

- Un Senior entiende que el back stack define el [lifetime]({{ "/es/glosario/composition-lifetime/" | relative_url }}) del ViewModel: un ViewModel obtenido vía `hiltViewModel()` tiene scope a su `NavBackStackEntry`. Si la entrada es sacada del stack y el usuario navega al mismo destino de nuevo, se crea un ViewModel fresco. Si la entrada permanece en el back stack (se navegó fuera pero no se sacó), el ViewModel sobrevive.
- Operaciones de back stack como `popUpTo` con `inclusive = true` limpian entradas intermedias, destruyendo sus ViewModels y estado guardado. Un Senior diseña grafos de navegación para que el estado crítico no sea accidentalmente destruido por patrones agresivos de `popUpTo`.
- En escenarios de multi-back-stack (navegación inferior con stacks independientes), cada tab mantiene su propio back stack. Cambiar de tab no destruye las entradas del back stack del otro tab — sus ViewModels sobreviven en sus respectivos [ViewModelStores]({{ "/es/glosario/viewmodel-store/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
