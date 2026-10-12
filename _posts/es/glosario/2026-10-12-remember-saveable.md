---
layout: post
title: "rememberSaveable"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [compose, state-management, lifecycle]
lang: es
permalink: /es/glosario/remember-saveable/
---

## The Theory (El Qué)

**`rememberSaveable { }`** funciona como [`remember`]({{ "/es/glosario/remember/" | relative_url }}), conservando un valor entre recomposiciones, y además lo escribe en el [saved instance state]({{ "/es/glosario/saved-instance-state/" | relative_url }}). Cuando la [Activity]({{ "/es/glosario/activity/" | relative_url }}) se recrea, después de un [cambio de configuración]({{ "/es/glosario/configuration-change/" | relative_url }}) o de la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}), el valor se restaura en lugar de calcularse de nuevo. El valor tiene que ser de un tipo que un [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}) pueda contener ([primitivos]({{ "/es/glosario/primitives/" | relative_url }}), [`String`]({{ "/es/glosario/string/" | relative_url }}), [`Parcelable`]({{ "/es/glosario/parcelable/" | relative_url }}), [`Serializable`]({{ "/es/glosario/serializable/" | relative_url }})) o venir con un [`Saver`]({{ "/es/glosario/saver/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
var query by rememberSaveable { mutableStateOf("") }
```

## The Senior Nuance (El Matiz Senior)

- **Para el estado que creó el usuario**: texto escrito, una pestaña elegida, una sección expandida. Los caches y las mediciones van en [`remember`]({{ "/es/glosario/remember/" | relative_url }}).
- **Mantenerlo chico.** El [estado guardado]({{ "/es/glosario/saved-instance-state/" | relative_url }}) tiene un límite de tamaño; se guarda un id, no una lista.
- **También restaura estado en listas lazy y en el back stack de navegación**, donde los ítems y las pantallas salen de la [composition]({{ "/es/glosario/composition/" | relative_url }}) y vuelven.
- Ver [remember & rememberSaveable]({{ "/es/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
