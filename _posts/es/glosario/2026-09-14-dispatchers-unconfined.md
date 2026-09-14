---
layout: post
title: "Dispatchers.Unconfined"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, threading, testing]
lang: es
permalink: /es/glosario/dispatchers-unconfined/
---

## The Theory (El Qué)

**`Dispatchers.Unconfined`** es el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) que no despacha: la coroutine arranca en el [thread]({{ "/es/glosario/thread/" | relative_url }}) del llamador y, después de cada [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}), se reanuda en el thread desde el que la función suspendible la reanudó. No confina nada, lo que lo hace rápido e impredecible.

Tiene lugar en los internos del framework y en tests (su primo de testing es `UnconfinedTestDispatcher`), no en código de aplicación.

## The Senior Nuance (El Matiz Senior)

- **La identidad del thread cambia a mitad de la función.** El código antes de un `delay` corre en el thread del llamador; el de después corre en el thread del timer que lo reanudó. Cualquier suposición sobre "el thread actual" se rompe.
- **No es una herramienta de performance.** El ahorro es un dispatch por resume; el costo es perder toda garantía que [`Main`]({{ "/es/glosario/dispatchers-main/" | relative_url }}), [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) y [`Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}) existen para dar.
- **No lo confundas con [`Main.immediate`]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }}).** `immediate` corre síncrono solo cuando ya está en el thread *correcto* y postea en otro caso; `Unconfined` no postea nunca.
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
