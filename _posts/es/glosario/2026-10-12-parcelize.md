---
layout: post
title: "@Parcelize"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [android-framework, serialization, compiler]
lang: es
permalink: /es/glosario/parcelize/
---

## The Theory (El Qué)

**`@Parcelize`** es una anotación del plugin de Gradle `kotlin-parcelize` que **genera la implementación de [`Parcelable`]({{ "/es/glosario/parcelable/" | relative_url }})** de una clase a partir de las propiedades de su constructor primario. La clase solo tiene que implementar [`Parcelable`]({{ "/es/glosario/parcelable/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
@Parcelize
data class DateRange(val start: LocalDate, val end: LocalDate) : Parcelable
```

## The Senior Nuance (El Matiz Senior)

- **Cada propiedad tiene que ser [parcelable]({{ "/es/glosario/parcelable/" | relative_url }})** (o tener un `Parceler` propio); si no, el plugin informa un error en tiempo de compilación.
- **La forma más simple de hacer guardable un tipo propio con [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }})**, sin necesidad de un [`Saver`]({{ "/es/glosario/saver/" | relative_url }}).
- Ver [remember & rememberSaveable]({{ "/es/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
