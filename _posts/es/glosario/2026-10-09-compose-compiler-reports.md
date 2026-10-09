---
layout: post
title: "Compose Compiler Reports"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [compose, compiler, performance]
lang: es
permalink: /es/glosario/compose-compiler-reports/
---

## The Theory (El Qué)

Los **Compose compiler reports** (reportes del compilador de Compose) son archivos que el compilador de Compose puede generar en tiempo de build. Listan cada composable indicando si es **skippable** y **restartable**, y cada clase y parámetro con la [stability]({{ "/es/glosario/stability/" | relative_url }}) que infirió el compilador ([`stable`]({{ "/es/glosario/stability/" | relative_url }}), [`unstable`]({{ "/es/glosario/stability/" | relative_url }}) o `runtime`). Se activan en Gradle con las opciones `reportsDestination` y `metricsDestination` del plugin del compilador de Compose.

## The Senior Nuance (El Matiz Senior)

- **Responden "¿por qué esto no se saltea?"** Un parámetro [`unstable`]({{ "/es/glosario/stability/" | relative_url }}) en el reporte es la razón habitual.
- **Revisarlos antes de agregar [`@Immutable`]({{ "/es/glosario/immutable-annotation/" | relative_url }}) o [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}).** El reporte muestra lo que el compilador realmente infirió, así que se anota solo lo que de verdad lo necesita.
- Ver [Recomposition & Stability]({{ "/es/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
