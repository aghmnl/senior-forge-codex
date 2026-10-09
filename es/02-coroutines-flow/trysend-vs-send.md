---
layout: page
title: "trySend() vs send()"
lang: es
permalink: /es/02-coroutines-flow/trysend-vs-send/
order: 14
---

## The Theory (El Qué)

Hay dos formas de meter un valor en un [`Channel`]({{ "/es/02-coroutines-flow/channel-hot-streams/" | relative_url }}), y la diferencia es qué pasa cuando el channel no tiene lugar.

- **[`send(value)`]({{ "/es/glosario/send/" | relative_url }})** es una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}). Si hay lugar, agrega el valor. Si no lo hay (el buffer está lleno, o es un channel [rendezvous]({{ "/es/glosario/channel-capacity/" | relative_url }}) y nadie está recibiendo), **suspende** hasta que un [receptor]({{ "/es/glosario/receive/" | relative_url }}) hace lugar. Nunca pierde un valor: espera. Como suspende, solo se puede llamar desde una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}).
- **[`trySend(value)`]({{ "/es/glosario/try-send/" | relative_url }})** es una función común. **Nunca espera**: si hay lugar en ese momento agrega el valor, y si no, desiste de inmediato. Devuelve un [`ChannelResult`]({{ "/es/glosario/channel-result/" | relative_url }}) que dice qué pasó: [`isSuccess`]({{ "/es/glosario/channel-result/" | relative_url }}) cuando el valor se agregó, [`isFailure`]({{ "/es/glosario/channel-result/" | relative_url }}) cuando no, e [`isClosed`]({{ "/es/glosario/channel-result/" | relative_url }}) cuando falló porque el channel está cerrado. Como no suspende, se puede llamar desde cualquier lado, incluido código que no es una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}).

También se diferencian cuando el channel está **cerrado**. [`send`]({{ "/es/glosario/send/" | relative_url }}) lanza una excepción. [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) no lanza: devuelve un resultado de cerrado.

Hay una tercera opción para código que corre en un [thread]({{ "/es/glosario/thread/" | relative_url }}) de background fuera de las [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}): **[`trySendBlocking(value)`]({{ "/es/glosario/try-send-blocking/" | relative_url }})** bloquea ese [thread]({{ "/es/glosario/thread/" | relative_url }}) hasta que haya lugar. Nunca debe correr en el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}).

[`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) reemplazó al viejo [`offer()`]({{ "/es/glosario/offer/" | relative_url }}), que lanzaba una excepción sobre un channel cerrado y hoy está deprecado.

## The Senior Perspective (El Porqué)

- **La pregunta real es "¿este código puede suspender?".** Adentro de una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}), [`send`]({{ "/es/glosario/send/" | relative_url }}) es la opción por defecto correcta: aplica [backpressure]({{ "/es/glosario/backpressure/" | relative_url }}) (un [productor]({{ "/es/glosario/producer-consumer/" | relative_url }}) rápido espera a un [consumidor]({{ "/es/glosario/producer-consumer/" | relative_url }}) lento) y nunca pierde un valor. [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) existe para el código que **no puede** suspender: un [listener]({{ "/es/glosario/listener/" | relative_url }}) de clicks, un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) de un [SDK]({{ "/es/glosario/sdk/" | relative_url }}), un broadcast del sistema. No es un "[`send`]({{ "/es/glosario/send/" | relative_url }}) más rápido"; es [`send`]({{ "/es/glosario/send/" | relative_url }}) para los lugares donde esperar es imposible.
- **[`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) puede fallar, y por defecto la falla es silenciosa.** Llamar a `trySend(event)` e ignorar el resultado significa que, cuando el buffer está lleno o el channel cerrado, el evento simplemente desaparece, sin error y sin log. Cada [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) tiene que responder la pregunta "¿qué pasa cuando esto falla?". O se revisa y se maneja el resultado (loguearlo, contarlo, tener un plan B), o se configura el channel para que la falla sea imposible salvo cuando está cerrado.
- **La capacidad decide si [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) puede fallar.** En un channel [rendezvous]({{ "/es/glosario/channel-capacity/" | relative_url }}) sin ningún [receptor]({{ "/es/glosario/receive/" | relative_url }}) suspendido en ese momento, [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) falla. En un [`BUFFERED`]({{ "/es/glosario/channel-capacity/" | relative_url }}) lleno, falla. En [`UNLIMITED`]({{ "/es/glosario/channel-capacity/" | relative_url }}), [`CONFLATED`]({{ "/es/glosario/channel-capacity/" | relative_url }}), o un buffer con política de descarte, solo falla cuando el channel está cerrado. Entonces elegir [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) y elegir la capacidad son una sola decisión: si perder valores no es aceptable, el channel necesita lugar para ellos, o el [productor]({{ "/es/glosario/producer-consumer/" | relative_url }}) tiene que poder esperar.
- **"Descartar" puede ser correcto, pero tiene que ser deliberado.** Para actualizaciones de ubicación o un sensor solo importa el último valor, y perder los intermedios es el comportamiento correcto: un channel [`CONFLATED`]({{ "/es/glosario/channel-capacity/" | relative_url }}) más [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) dice exactamente eso. Para la confirmación de un pago, perder un valor es un bug. El código tiene que dejar claro cuál de los dos casos es.
- **[`trySendBlocking`]({{ "/es/glosario/try-send-blocking/" | relative_url }}) mueve la espera a un [thread]({{ "/es/glosario/thread/" | relative_url }}).** Sirve cuando un [thread]({{ "/es/glosario/thread/" | relative_url }}) de background que no es una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) (el lector de un socket, una librería vieja) produce valores y tiene que respetar el [backpressure]({{ "/es/glosario/backpressure/" | relative_url }}). En el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) congela la UI y puede terminar en un [ANR]({{ "/es/glosario/anr/" | relative_url }}), así que ahí no va.
- **A veces la respuesta correcta no es un channel.** Cuando un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) solo necesita publicar "el último valor" (un estado de conexión, el veredicto de una compra), asignar [`MutableStateFlow.value`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) es más simple: nunca suspende, nunca falla y conserva el último valor para quien colecte. Un channel con [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) tiene sentido cuando cada valor importa por sí mismo y se tiene que procesar una vez.

## Code in Action

```kotlin
// Not found in FAS — standalone example
// Adentro de una coroutine: send espera lugar y nunca pierde un valor
suspend fun enqueueUploads(queue: SendChannel<File>, files: List<File>) {
    files.forEach { queue.send(it) }      // suspende mientras los workers están ocupados
}

// Not found in FAS — standalone example
// Desde un callback: trySend no puede esperar, así que la falla se maneja explícitamente
private val scans = Channel<Barcode>(capacity = 16)

private val listener = BarcodeListener { barcode ->
    val result = scans.trySend(barcode)
    when {
        result.isClosed -> Log.w(TAG, "Escaneo descartado: el escáner se detuvo")
        result.isFailure -> Log.w(TAG, "Escaneo descartado: la cola está llena")
    }
}

// Not found in FAS — standalone example
// Cuando solo importa el último valor, CONFLATED hace que trySend no pueda fallar
// (salvo con el channel cerrado): el valor nuevo reemplaza al pendiente
private val positions = Channel<Location>(Channel.CONFLATED)

private val locationListener = LocationListener { location ->
    positions.trySend(location)
}

// De FollowApp Suite — BillingConnector.kt
// La misma situación, un callback de Play Billing que no puede suspender,
// resuelta sin channel: el resultado es estado, así que alcanza con asignar value.
// Nunca suspende, nunca falla y conserva el último veredicto.
billingClient.queryPurchasesAsync(params) { result, purchases ->
    if (result.responseCode == BillingClient.BillingResponseCode.OK) {
        handlePurchases(purchases)
        if (purchases.none { it.isOwnedProduct() }) {
            _isOwned.value = false
        }
    }
}
```

## The Interview (En el banquillo)

**Pregunta**: ¿Qué diferencia hay entre [`send`]({{ "/es/glosario/send/" | relative_url }}) y [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) en un [`Channel`]({{ "/es/02-coroutines-flow/channel-hot-streams/" | relative_url }}), y cómo decidís cuál usar?

**Respuesta Senior**: Los dos meten un valor en un channel; la diferencia es qué pasa cuando no hay lugar. [`send`]({{ "/es/glosario/send/" | relative_url }}) es una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}): espera hasta que un [receptor]({{ "/es/glosario/receive/" | relative_url }}) hace lugar, así que nunca pierde un valor y te da [backpressure]({{ "/es/glosario/backpressure/" | relative_url }}) gratis, porque un [consumidor]({{ "/es/glosario/producer-consumer/" | relative_url }}) lento frena a un [productor]({{ "/es/glosario/producer-consumer/" | relative_url }}) rápido. Sobre un channel cerrado lanza una excepción. [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) es una función común que nunca espera: o agrega el valor de inmediato o desiste, y devuelve un [`ChannelResult`]({{ "/es/glosario/channel-result/" | relative_url }}) que te dice si tuvo éxito, si falló o si encontró el channel cerrado. Nunca lanza. Entonces la decisión depende en realidad de dónde corre el código. Adentro de una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) uso [`send`]({{ "/es/glosario/send/" | relative_url }}). Desde código que no puede suspender, como un [listener]({{ "/es/glosario/listener/" | relative_url }}) o el [callback]({{ "/es/glosario/callbacks/" | relative_url }}) de un [SDK]({{ "/es/glosario/sdk/" | relative_url }}), uso [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}), y ahí tengo que decidir qué significa una falla: o reviso el resultado y lo manejo, o elijo una capacidad donde la falla sea aceptable o imposible, como [`CONFLATED`]({{ "/es/glosario/channel-capacity/" | relative_url }}) cuando solo importa el último valor. Lo que evito es tratar a [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) como un [`send`]({{ "/es/glosario/send/" | relative_url }}) más rápido, porque ignorar su resultado convierte un buffer lleno en datos perdidos en silencio.

**Pregunta**: Un [listener]({{ "/es/glosario/listener/" | relative_url }}) llama a `channel.trySend(event)` e ignora el resultado. En producción, algunos eventos nunca llegan. ¿Qué puede estar pasando y cómo lo arreglás?

**Respuesta Senior**: [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) solo agrega el valor si hay lugar en ese momento exacto, y el código está tirando el resultado que dice si lo logró. Hay tres causas típicas. El channel es [rendezvous]({{ "/es/glosario/channel-capacity/" | relative_url }}), el de por defecto, y no había ningún [receptor]({{ "/es/glosario/receive/" | relative_url }}) esperando en ese momento, así que cada evento enviado mientras el [consumidor]({{ "/es/glosario/producer-consumer/" | relative_url }}) está ocupado falla. O tiene buffer y estaba lleno porque el [consumidor]({{ "/es/glosario/producer-consumer/" | relative_url }}) es más lento que el [productor]({{ "/es/glosario/producer-consumer/" | relative_url }}). O el channel ya estaba cerrado, por ejemplo porque la pantalla que lo consumía ya no existía. El arreglo empieza por hacer visible la falla: revisar el resultado, como mínimo loguearlo, para saber cuál de los casos es. Después hay que decidir qué son los eventos. Si cada evento importa, el channel necesita lugar para ellos, un buffer más grande o [`UNLIMITED`]({{ "/es/glosario/channel-capacity/" | relative_url }}) cuando el volumen está acotado, o el [productor]({{ "/es/glosario/producer-consumer/" | relative_url }}) tiene que pasar a una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) y usar [`send`]({{ "/es/glosario/send/" | relative_url }}) para poder esperar. Si solo importa el último, [`CONFLATED`]({{ "/es/glosario/channel-capacity/" | relative_url }}) hace que la pérdida sea intencional en vez de accidental. Y si el channel estaba cerrado, el bug está en el ciclo de vida: el [listener]({{ "/es/glosario/listener/" | relative_url }}) se tiene que desregistrar cuando el [consumidor]({{ "/es/glosario/producer-consumer/" | relative_url }}) desaparece, que es exactamente lo que hace [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}) con [`awaitClose`]({{ "/es/glosario/await-close/" | relative_url }}).

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
