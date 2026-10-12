---
layout: post
title: "SavedStateHandle"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [android-framework, state-management, lifecycle]
lang: es
permalink: /es/glosario/saved-state-handle/
---

## The Theory (El Qué)

**`SavedStateHandle`** es un mapa clave-valor que un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) recibe en su constructor y que **se escribe en el [saved instance state]({{ "/es/glosario/saved-instance-state/" | relative_url }})**. Los valores que se ponen ahí sobreviven a la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}), algo que el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) solo no logra. También expone valores como flows, y contiene los argumentos de navegación de la pantalla.

```kotlin
// Not found in FAS — standalone example
class FormViewModel(private val handle: SavedStateHandle) : ViewModel() {
    val name: StateFlow<String> = handle.getStateFlow("name", "")
    fun onNameChange(value: String) { handle["name"] = value }
}
```

## The Senior Nuance (El Matiz Senior)

- **La contraparte de [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}) para el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }})**: el mismo mecanismo, los mismos tipos de [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}), el mismo límite de tamaño.
- **Guardar la entrada, no el estado derivado.** Se guardan los valores de los campos; la validación y los datos cargados se recalculan a partir de ellos.
- Ver [remember & rememberSaveable]({{ "/es/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
