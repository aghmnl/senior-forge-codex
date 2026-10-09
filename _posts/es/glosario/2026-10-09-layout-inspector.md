---
layout: post
title: "Layout Inspector"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [compose, performance, testing]
lang: es
permalink: /es/glosario/layout-inspector/
---

## The Theory (El Qué)

El **Layout Inspector** es una herramienta de Android Studio que muestra la jerarquía de UI de una app en ejecución. Para [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) muestra el árbol de composables, los parámetros de cada uno y, si se activa, la **cantidad de recomposiciones**: cuántas veces se recompuso cada composable y cuántas veces se salteó.

## The Senior Nuance (El Matiz Senior)

- **Es la primera herramienta ante problemas de [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}).** Un contador que crece con cada tecla o con cada frame señala el composable a investigar.
- **Combinarlo con los [reportes del compilador de Compose]({{ "/es/glosario/compose-compiler-reports/" | relative_url }})**: el inspector muestra que algo se recompone, los reportes explican por qué no se puede saltear.
- Ver [Recomposition & Stability]({{ "/es/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
