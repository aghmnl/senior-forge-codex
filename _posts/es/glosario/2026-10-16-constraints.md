---
layout: post
title: "Constraints"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout, performance]
lang: es
permalink: /es/glosario/constraints/
---

## The Theory (El Qué)

Las **constraints** (restricciones) son el ancho y alto mínimo y máximo que un padre le permite tener a su hijo durante el layout. Bajan por la cadena de [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) y por el árbol; cada [modifier]({{ "/es/glosario/modifier/" | relative_url }}) de tamaño las acota para lo que viene después, y el hijo elige un tamaño dentro de ellas. Por eso en `Modifier.size(100.dp).size(50.dp)` gana el primer tamaño.

```kotlin
// Not found in FAS — standalone example
Box(Modifier.size(100.dp).size(50.dp))   // 100 dp
```

## The Senior Nuance (El Matiz Senior)

- **Las constraints bajan, los tamaños suben**: los padres restringen, los hijos eligen, los padres ubican.
- **Para salirse de las constraints recibidas** se usa `requiredSize`, a sabiendas: el hijo puede desbordar a su padre.
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
