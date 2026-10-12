---
layout: post
title: "Strong Skipping"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [compose, performance, compiler]
lang: es
permalink: /es/glosario/strong-skipping/
---

## The Theory (El Qué)

El **strong skipping** es un modo del compilador de Compose, activado por defecto desde [Kotlin]({{ "/es/glosario/kotlin/" | relative_url }}) 2.0.20, que cambia dos reglas. Los composables con parámetros **[unstable]({{ "/es/glosario/stability/" | relative_url }})** se pueden saltear: esos parámetros se comparan por **instancia** ([`===`]({{ "/es/glosario/referential-equality/" | relative_url }})), mientras que los [stable]({{ "/es/glosario/stability/" | relative_url }}) se siguen comparando con [`equals`]({{ "/es/glosario/equals/" | relative_url }}). Y las [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) que se pasan a los composables se **recuerdan automáticamente**, así que una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) ya no rompe el [skipping]({{ "/es/glosario/skipping/" | relative_url }}) solo porque se vuelve a crear.

## The Senior Nuance (El Matiz Senior)

- **La regla práctica pasó a ser la identidad.** Pasar la misma instancia cuando nada cambió: conservar las listas que no cambian al actualizar el estado con [`copy`]({{ "/es/glosario/copy/" | relative_url }}), y no armar colecciones en el cuerpo de un composable sin [`remember`]({{ "/es/glosario/remember/" | relative_url }}).
- **No vuelve irrelevante la [stability]({{ "/es/glosario/stability/" | relative_url }}).** Un tipo [stable]({{ "/es/glosario/stability/" | relative_url }}) se puede saltear cuando su valor es igual aunque sea una instancia nueva; uno [unstable]({{ "/es/glosario/stability/" | relative_url }}) necesita la misma instancia.
- Ver [Recomposition & Stability]({{ "/es/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
