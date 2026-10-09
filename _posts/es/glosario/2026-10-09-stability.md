---
layout: post
title: "Stability"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [compose, performance, immutability]
lang: es
permalink: /es/glosario/stability/
---

## The Theory (El Qué)

En [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}), un tipo es **stable** (estable) cuando Compose puede confiar en él durante el [skipping]({{ "/es/glosario/skipping/" | relative_url }}): [`equals`]({{ "/es/glosario/equals/" | relative_url }}) siempre da el mismo resultado para las mismas dos instancias, cualquier cambio en una propiedad pública le avisa a la [composition]({{ "/es/glosario/composition/" | relative_url }}) (está respaldada por [`MutableState`]({{ "/es/glosario/mutable-state/" | relative_url }})), y todas sus propiedades públicas también son stable. Los [primitivos]({{ "/es/glosario/primitives/" | relative_url }}), [`String`]({{ "/es/glosario/string/" | relative_url }}), las [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}), [`MutableState`]({{ "/es/glosario/mutable-state/" | relative_url }}) y las data classes de [`val`]({{ "/es/glosario/val/" | relative_url }}) de tipos stable son stable. Un tipo es **unstable** (inestable) cuando el compilador no lo puede probar: una clase con un [`var`]({{ "/es/glosario/var/" | relative_url }}), una clase de un módulo compilado sin el compilador de Compose, o las interfaces [`List`]({{ "/es/glosario/list/" | relative_url }}), [`Set`]({{ "/es/glosario/sets/" | relative_url }}) y `Map`, que pueden esconder una instancia mutable.

## The Senior Nuance (El Matiz Senior)

- **Unstable no es "roto".** Con [strong skipping]({{ "/es/glosario/strong-skipping/" | relative_url }}), los parámetros unstable se comparan por instancia, así que se siguen salteando cuando se pasa la misma instancia.
- **Los [reportes del compilador de Compose]({{ "/es/glosario/compose-compiler-reports/" | relative_url }}) dicen** qué parámetros infirió como unstable, y es lo primero que hay que revisar antes de anotar nada.
- **Soluciones, por orden de preferencia:** inmutabilidad real, colecciones inmutables, un archivo de configuración de stability, y recién después [`@Immutable`]({{ "/es/glosario/immutable-annotation/" | relative_url }}) o [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}).
- Ver [Recomposition & Stability]({{ "/es/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
