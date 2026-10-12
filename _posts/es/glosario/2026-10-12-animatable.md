---
layout: post
title: "Animatable"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [compose, coroutines]
lang: es
permalink: /es/glosario/animatable/
---

## The Theory (El Qué)

**`Animatable`** guarda un valor (normalmente un `Float`) que se puede animar desde [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}): `animateTo(target)` suspende mientras anima, `snapTo(value)` salta de inmediato, y leer `.value` es observable, así que los composables se recomponen a medida que se mueve. Es la herramienta de bajo nivel para gestos y animaciones manejadas por código.

```kotlin
// Not found in FAS — standalone example
val offset = remember { Animatable(0f) }
LaunchedEffect(open) { offset.animateTo(if (open) 300f else 0f) }
```

## The Senior Nuance (El Matiz Senior)

- **Se guarda con [`remember`]({{ "/es/glosario/remember/" | relative_url }}), no con [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}).** Es estado de animación; después de una recreación tiene que arrancar de nuevo desde el estado actual de la UI.
- **Un `animateTo` nuevo cancela el que está corriendo**, lo que lo vuelve natural para gestos que interrumpen una animación.
- Ver [remember & rememberSaveable]({{ "/es/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
