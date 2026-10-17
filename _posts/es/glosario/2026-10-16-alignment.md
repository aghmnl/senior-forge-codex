---
layout: post
title: "Alignment"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout]
lang: es
permalink: /es/glosario/alignment/
---

## The Theory (El Qué)

**`Alignment`** posiciona a los hijos adentro del espacio que reciben. En un [`Box`]({{ "/es/glosario/box/" | relative_url }}) funciona en los dos ejes (`TopStart`, `Center`, `BottomEnd`); en un [`Row`]({{ "/es/glosario/row/" | relative_url }}) es solo vertical (`Top`, `CenterVertically`, `Bottom`) y en un [`Column`]({{ "/es/glosario/column/" | relative_url }}) solo horizontal, porque se aplica sobre el **[eje transversal]({{ "/es/glosario/main-axis-cross-axis/" | relative_url }})**.

```kotlin
// Not found in FAS — standalone example
Box(contentAlignment = Alignment.BottomEnd) { /* ... */ }
```

## The Senior Nuance (El Matiz Senior)

- **La alineación posiciona a cada hijo; el [arrangement]({{ "/es/glosario/arrangement/" | relative_url }}) distribuye al grupo.** Confundirlos es una fuente habitual de "¿por qué no se centra?".
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
