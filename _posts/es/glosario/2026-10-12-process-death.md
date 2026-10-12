---
layout: post
title: "Process Death"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [android-framework, lifecycle, memory]
lang: es
permalink: /es/glosario/process-death/
---

## The Theory (El Qué)

La **process death** (muerte del proceso) es cuando Android mata el proceso de una app mientras está en background, para recuperar memoria. El usuario no lo ve: cuando vuelve, Android arranca un proceso nuevo y recrea la [Activity]({{ "/es/glosario/activity/" | relative_url }}) desde su [saved instance state]({{ "/es/glosario/saved-instance-state/" | relative_url }}), así que la app parece no haberse ido nunca. Todo lo que vivía solo en memoria (ViewModels, [singletons]({{ "/es/glosario/singleton/" | relative_url }}), valores de [`remember`]({{ "/es/glosario/remember/" | relative_url }})) desapareció; solo sobreviven el [saved instance state]({{ "/es/glosario/saved-instance-state/" | relative_url }}) y el almacenamiento persistente.

## The Senior Nuance (El Matiz Senior)

- **Los desarrolladores casi nunca la ven, los usuarios la sufren todo el tiempo** (pasar a la cámara, una llamada larga). Se prueba con "No mantener actividades" o matando el proceso con adb mientras la app está en background.
- **Es el caso para el que existen [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}) y [`SavedStateHandle`]({{ "/es/glosario/saved-state-handle/" | relative_url }}).**
- Ver [remember & rememberSaveable]({{ "/es/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
