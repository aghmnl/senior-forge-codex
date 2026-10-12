---
layout: post
title: "Configuration Change"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [android-framework, lifecycle]
lang: es
permalink: /es/glosario/configuration-change/
---

## The Theory (El Qué)

Un **configuration change** (cambio de configuración) ocurre cuando cambia algo de lo que dependen los recursos de la app mientras corre: la rotación de pantalla, el modo oscuro, el idioma del sistema, el tamaño de fuente, el tamaño de la ventana (multiventana, plegables). Por defecto Android **destruye y recrea** la [Activity]({{ "/es/glosario/activity/" | relative_url }}) para que recargue los recursos correctos. Los ViewModels y el [saved instance state]({{ "/es/glosario/saved-instance-state/" | relative_url }}) sobreviven; los valores de un [`remember`]({{ "/es/glosario/remember/" | relative_url }}) común, no.

## The Senior Nuance (El Matiz Senior)

- **No desactivarlo para evitar el problema.** Declarar `android:configChanges` en el manifest frena la recreación, pero entonces la app tiene que manejar cada cambio sola; la solución confiable es un estado que sobreviva a la recreación.
- **La rotación es la forma fácil de probarlo**, pero la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}) es un caso más difícil que la rotación no cubre.
- Ver [remember & rememberSaveable]({{ "/es/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
