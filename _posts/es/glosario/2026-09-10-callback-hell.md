---
layout: post
title: "Callback Hell"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/callback-hell/
---

## The Theory (El Qué)

El **callback hell** es la forma que toma el código asíncrono cuando cada [operación async]({{ "/es/glosario/async-operations/" | relative_url }}) reporta su resultado a través de un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) y la siguiente operación tiene que arrancar *dentro* de ese callback: el anidamiento crece hacia la derecha con cada paso, el manejo de errores se duplica en cada nivel, y la cancelación hay que enhebrarla a mano.

```kotlin
// Not found in FAS — standalone example
api.getUser(id) { user ->
    api.getOrders(user.id) { orders ->
        api.getInvoice(orders.first().id) { invoice ->
            runOnUiThread { render(invoice) }   // error handling? cancellation?
        }
    }
}

// The same with suspend functions:
val invoice = api.getInvoice(api.getOrders(api.getUser(id).id).first().id)
render(invoice)
```

Las [suspend functions]({{ "/es/glosario/suspend-functions/" | relative_url }}) son el compilador haciendo el anidamiento por vos: la misma transformación de [Continuation-Passing Style]({{ "/es/glosario/continuation-passing-style/" | relative_url }}), emitida automáticamente y escondida detrás de sintaxis secuencial.

## The Senior Nuance (El Matiz Senior)

- **El problema nunca fueron los callbacks — fue la composición.** Secuenciar, ramificar, iterar y `try/finally` son triviales en código lineal y hostiles dentro de callbacks. Las coroutines devuelven el control de flujo propio del lenguaje al código async.
- **Puenteá una vez, en el borde.** [suspendCancellableCoroutine]({{ "/es/glosario/suspend-cancellable-coroutine/" | relative_url }}) convierte una API de callbacks en una suspend function en un solo lugar; todo lo que está arriba es secuencial. El Android moderno tiene poco callback hell porque Jetpack ya hizo esto.
- **`Flow` es la respuesta multi-shot.** Un listener que dispara repetidamente se convierte en `callbackFlow`, y sus consumidores obtienen operadores en lugar de handlers anidados.
- Ver [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
