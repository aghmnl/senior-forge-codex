---
layout: post
title: "ViewModelStore"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
tags: [lifecycle, android-framework, navigation]
lang: es
permalink: /es/glosario/viewmodel-store/
---

## The Theory (El Qué)

**`ViewModelStore`** es la clase de Android Jetpack que contiene instancias de ViewModel y asegura que sobrevivan cambios de configuración (rotaciones de pantalla, cambios de idioma, toggles de modo oscuro). Cada `ComponentActivity`, `Fragment` y entry del [back stack]({{ "/es/glosario/back-stack/" | relative_url }}) de navegación posee un `ViewModelStore`.

Cuando solicitás un ViewModel vía [`by viewModels()`]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}) o `ViewModelProvider(owner)`, el framework chequea primero el `ViewModelStore` del owner. Si el ViewModel ya existe, retorna la instancia cacheada; de lo contrario la crea, la almacena y la retorna. En la destrucción final (`finish()` de Activity, remoción del Fragment del [back stack]({{ "/es/glosario/back-stack/" | relative_url }})), se llama a `ViewModelStore.clear()`, que invoca `onCleared()` en cada ViewModel que contiene.

El store en sí es retenido a través de cambios de configuración vía el mecanismo de `NonConfigurationInstances` (Activities) o el estado retenido del Fragment manager (Fragments).

## The Senior Nuance (El Matiz Senior)

- Un Senior entiende que el `ViewModelStore` define el **scope de supervivencia** del ViewModel: scopear al store de un Fragment significa que el ViewModel muere cuando el Fragment es sacado del stack; scopear al store de la Activity (`by activityViewModels()`) significa que vive tanto como la Activity. Elegir el scope incorrecto o genera memory leaks o causa pérdida prematura de estado.
- En Compose con [Hilt]({{ "/es/glosario/hilt/" | relative_url }}), `hiltViewModel()` usa el `NavBackStackEntry` del [navigation component]({{ "/es/glosario/navigation-component/" | relative_url }}) como `ViewModelStoreOwner`. Esto significa que cada destino de navegación tiene su propio `ViewModelStore` — navegar fuera y volver crea un nuevo ViewModel si el destino fue sacado del [back stack]({{ "/es/glosario/back-stack/" | relative_url }}).
- `ViewModelStore` mantiene referencias fuertes a los ViewModels. Si un ViewModel tiene referencias a objetos grandes (bitmaps, cursores de base de datos), esos objetos sobreviven cambios de configuración también — una fuente potencial de [memory leaks]({{ "/es/glosario/memory-leaks/" | relative_url }}) si no se gestionan correctamente en `onCleared()`.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
