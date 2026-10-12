---
layout: post
title: "Saved Instance State"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [android-framework, lifecycle, state-management]
lang: es
permalink: /es/glosario/saved-instance-state/
---

## The Theory (El Qué)

El **saved instance state** (estado de instancia guardado) es el [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}) en el que Android guarda pequeñas piezas de estado de UI antes de que una [Activity]({{ "/es/glosario/activity/" | relative_url }}) pueda destruirse, para restaurarlas cuando se recrea. El sistema lo pide cuando la [Activity]({{ "/es/glosario/activity/" | relative_url }}) pasa a background, y lo devuelve después de un [cambio de configuración]({{ "/es/glosario/configuration-change/" | relative_url }}) o de la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}). `onSaveInstanceState`, [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}) y [`SavedStateHandle`]({{ "/es/glosario/saved-state-handle/" | relative_url }}) escriben todos ahí.

## The Senior Nuance (El Matiz Senior)

- **Sobrevive a la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}), el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) no.** Esa es la razón principal por la que sigue importando con la arquitectura moderna.
- **No se borra al rotar, pero sí cuando el usuario cierra la pantalla**: volver atrás o deslizar la app fuera de recientes lo descarta a propósito.
- **Solo valores chicos**: comparte un límite de tamaño que impone el sistema.
- Ver [remember & rememberSaveable]({{ "/es/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
