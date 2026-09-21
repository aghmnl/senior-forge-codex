---
layout: post
title: "Namespace"
date: 2026-09-21 12:00:00 +0000
categories: [es, glosario]
tags: [scoping, design-principles]
lang: es
permalink: /es/glosario/namespace/
---

## The Theory (El Qué)

Un **namespace** (espacio de nombres) es el conjunto de nombres visibles en un punto del código — en Kotlin, lo que un paquete más sus imports ponen al alcance. Las [Extension Functions]({{ "/es/01-kotlin-core/extension-functions/" | relative_url }}) lo ensanchan de una forma particular: una extensión pública top-level sobre `String` aparece en el autocompletado de *cada* `String` de cada módulo que la importe. Mantener ese conjunto chico es de lo que trata la "contaminación del espacio de nombres".

```kotlin
// Not found in FAS — standalone example
// Contamina: todo String del proyecto ofrece ahora .toOrderId()
fun String.toOrderId(): OrderId = OrderId(this)

// Acotada: solo la ve este módulo
internal fun String.toOrderId(): OrderId = OrderId(this)
```

## The Senior Nuance (El Matiz Senior)

- **El autocompletado es un recurso compartido.** Cincuenta extensiones de dominios distintos sobre `String` vuelven inútil la lista de sugerencias del IDE para todo el mundo, y eso es un costo real aunque nada se rompa.
- **La solución es visibilidad, no disciplina.** [`private`]({{ "/es/glosario/private/" | relative_url }}) en el archivo, [`internal`]({{ "/es/glosario/internal/" | relative_url }}) en el módulo; reservá el top-level público para helpers genuinamente universales.
- **También es una señal de acoplamiento.** Si la extensión de una feature es visible en todo el proyecto, otras features la van a usar y el límite del módulo se erosiona.
- Ver [Extension Functions]({{ "/es/01-kotlin-core/extension-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
