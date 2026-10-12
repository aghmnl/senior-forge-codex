---
layout: post
title: "@Immutable"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [compose, immutability]
lang: es
permalink: /es/glosario/immutable-annotation/
---

## The Theory (El Qué)

**`@Immutable`** es una anotación de Compose que promete que una clase **nunca va a cambiar** después de creada: todas sus propiedades públicas son [`val`]({{ "/es/glosario/val/" | relative_url }}) cuyos valores nunca cambian. Entonces el compilador trata la clase como [stable]({{ "/es/glosario/stability/" | relative_url }}) y la compara con [`equals`]({{ "/es/glosario/equals/" | relative_url }}) durante el [skipping]({{ "/es/glosario/skipping/" | relative_url }}). Es más fuerte que [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}), que permite cambios siempre que sean observables a través del estado de snapshot.

```kotlin
// Not found in FAS — standalone example
@Immutable
data class TaskRow(val id: String, val title: String, val tags: List<String>)
```

## The Senior Nuance (El Matiz Senior)

- **Es una promesa, no una verificación.** Nada la comprueba. Si la lista `tags` de arriba se mutara, Compose saltearía la fila y mostraría datos viejos.
- **Usarla solo cuando el compilador no puede inferir lo que es cierto**, típicamente para un [`List`]({{ "/es/glosario/list/" | relative_url }}) que se sabe que nunca se muta. La inmutabilidad real o un archivo de configuración de [stability]({{ "/es/glosario/stability/" | relative_url }}) son más seguros.
- Ver [Recomposition & Stability]({{ "/es/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
