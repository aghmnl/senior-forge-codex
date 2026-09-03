---
layout: post
title: "Navigation Component"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/navigation-component/
---

## The Theory (El Qué)

El **Navigation Component** es una biblioteca de Jetpack que maneja la navegación in-app — moverse entre pantallas, gestionar el back stack, pasar argumentos y deep linking. Provee un `NavController` que orquesta las acciones de navegación, un `NavHost` que hostea el destino actual, y un grafo de navegación que declara todas las rutas posibles. En [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}), la navegación se declara vía `NavHost { composable("route") { ... } }`.

## The Senior Nuance (El Matiz Senior)

- **Argumentos type-safe**: [Safe Args]({{ "/es/glosario/safe-args/" | relative_url }}) genera clases type-safe para pasar datos entre destinos. Esto mueve el parsing de argumentos de matching de strings en [runtime]({{ "/es/glosario/runtime/" | relative_url }}) a código chequeado en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}) — no más crashes por `getStringExtra("key")`.
- **Arquitectura Single Activity**: Navigation Component está diseñado para apps de una sola Activity donde todas las pantallas son Fragments o destinos Compose. La Activity hostea el `NavHost`; el `NavController` maneja el back stack.
- **Deep linking**: El grafo de navegación puede declarar URIs de deep link. Cuando el sistema resuelve una URI que matchea, Navigation Component abre el destino correcto con los argumentos correctos — sin parsing manual de intents.
- **Compose Navigation**: En Compose, las rutas son string-based por defecto (`"profile/{userId}"`). Navegación type-safe con Kotlin serialization es el approach recomendado en versiones más nuevas, eliminando el sistema de rutas basado en strings.
- **Manejo del back stack**: `NavController.popBackStack()`, `navigate(route) { popUpTo(...) }`, y `launchSingleTop = true` controlan el comportamiento del back stack. Manejarlos mal lleva a destinos duplicados o estado perdido.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
