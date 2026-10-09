---
layout: post
title: "awaitClose"
date: 2026-10-02 12:00:00 +0000
categories: [es, glosario]
tags: [flow, callbacks, cancellation]
lang: es
permalink: /es/glosario/await-close/
---

## The Theory (El Qué)

**`awaitClose { }`** es la última llamada adentro de un bloque [callbackFlow]({{ "/es/glosario/callback-flow/" | relative_url }}). **Suspende** mientras el flow se está colectando, lo que mantiene vivo el callback registrado, y cuando el collector se detiene (o el flow se [cancela]({{ "/es/glosario/cancel/" | relative_url }})) ejecuta su lambda, donde el callback se **desregistra**. Es lo que ata la vida de un listener a la vida de su colección.

```kotlin
// Not found in FAS — standalone example
fun clicks(view: View): Flow<Unit> = callbackFlow {
    view.setOnClickListener { trySend(Unit) }
    awaitClose { view.setOnClickListener(null) }   // limpieza cuando se deja de colectar
}
```

## The Senior Nuance (El Matiz Senior)

- **Es obligatorio.** Si un bloque `callbackFlow` termina sin `awaitClose`, el flow falla con una `IllegalStateException`. La regla existe porque olvidarse de la limpieza es la fuga clásica de listeners.
- **El lambda es la limpieza, y siempre corre.** Ya sea que el collector termine normalmente, se cancele o falle, el código que desregistra en `awaitClose` se ejecuta.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
