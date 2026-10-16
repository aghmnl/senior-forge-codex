---
layout: post
title: "Design System"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, architecture]
lang: es
permalink: /es/glosario/design-system/
---

## The Theory (El Qué)

Un **design system** (sistema de diseño) es el conjunto compartido de reglas visuales y componentes reutilizables de un producto: colores, tipografía, espaciados y formas (normalmente un tema de Compose), más componentes como botones, chips, tarjetas e inputs que usan todas las pantallas. En una app Android modular suele vivir en su propio módulo, como `core:designsystem`.

## The Senior Nuance (El Matiz Senior)

- **Sus componentes tienen que ser [stateless]({{ "/es/glosario/stateful-stateless/" | relative_url }}) o admitir el modo [controlado]({{ "/es/glosario/controlled-uncontrolled/" | relative_url }})**, porque no pueden conocer las reglas de negocio de las pantallas que los usan.
- **No tiene que depender del código de features ni de dominio.** Un componente que importa una entidad de dominio ya no se puede reutilizar; los parámetros genéricos y las [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) lo mantienen independiente.
- Ver [State Hoisting]({{ "/es/03-jetpack-compose/state-hoisting/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
