---
layout: page
title: "Channel (Hot Streams)"
lang: es
permalink: /es/02-coroutines-flow/channel-hot-streams/
order: 13
---

## The Theory (El Qué)

Un [`Channel<T>`]({{ "/es/glosario/channel/" | relative_url }}) es una **cola entre [coroutines]({{ "/es/glosario/coroutines/" | relative_url }})**. Una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) mete valores con [`send`]({{ "/es/glosario/send/" | relative_url }}), otra los saca con [`receive`]({{ "/es/glosario/receive/" | relative_url }}), y **cada valor se le entrega a exactamente un receptor**. Funciona como una cola bloqueante, salvo que las dos operaciones **suspenden** en vez de bloquear un [thread]({{ "/es/glosario/thread/" | relative_url }}): [`send`]({{ "/es/glosario/send/" | relative_url }}) suspende cuando no hay lugar, y [`receive`]({{ "/es/glosario/receive/" | relative_url }}) suspende cuando no hay nada para sacar.

Un channel es un [stream hot]({{ "/es/glosario/hot-stream/" | relative_url }}). Existe independientemente de sus consumidores, y los valores que se le envían esperan ahí hasta que alguien los toma, haya o no alguien escuchando cuando se enviaron.

Su **capacidad** decide cuándo suspende [`send`]({{ "/es/glosario/send/" | relative_url }}):

- **`RENDEZVOUS`** (por defecto, [`Channel<T>()`]({{ "/es/glosario/channel/" | relative_url }})): sin buffer. [`send`]({{ "/es/glosario/send/" | relative_url }}) suspende hasta que un receptor toma el valor, así que emisor y receptor "se encuentran".
- **`BUFFERED`**: un buffer fijo (64 por defecto). [`send`]({{ "/es/glosario/send/" | relative_url }}) solo suspende cuando está lleno.
- **`UNLIMITED`**: un buffer sin límite. [`send`]({{ "/es/glosario/send/" | relative_url }}) nunca suspende.
- **[`CONFLATED`]({{ "/es/glosario/conflation/" | relative_url }})**: se queda solo con el último valor. Uno nuevo reemplaza al anterior si todavía no se tomó.

Desde código que no puede suspender, como un callback, [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) agrega un valor solo si hay lugar en ese momento, y devuelve un resultado que dice si lo logró. La diferencia entre [`send`]({{ "/es/glosario/send/" | relative_url }}) y [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) es un tema aparte.

Un channel tiene un **final**. El emisor llama a [`close()`]({{ "/es/glosario/close/" | relative_url }}) para avisar que no vienen más valores. Los receptores igual reciben todo lo que ya estaba en el buffer, y después un ciclo `for (value in channel)` termina normalmente. Enviar a un channel cerrado lanza una excepción, y también llamar a [`receive()`]({{ "/es/glosario/receive/" | relative_url }}) sobre uno cerrado y vacío.

La forma habitual de crear uno es el builder [`produce { }`]({{ "/es/glosario/produce/" | relative_url }}). Lanza una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) que envía valores, devuelve el lado que recibe, y **cierra el channel automáticamente** cuando la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) termina o se cancela. Todavía está marcado como API experimental, pero es la forma idiomática de armar un productor.

## The Senior Perspective (El Porqué)

- **Cola, no difusión: esa es toda la diferencia con [SharedFlow]({{ "/es/02-coroutines-flow/sharedflow/" | relative_url }}).** Un [SharedFlow]({{ "/es/02-coroutines-flow/sharedflow/" | relative_url }}) le da cada valor a *cada* [collector]({{ "/es/glosario/collector/" | relative_url }}). Un channel le da cada valor a *un* receptor. Con dos receptores sobre el mismo channel, los valores se reparten entre ellos ([fan-out]({{ "/es/glosario/fan-out/" | relative_url }})). Eso convierte al channel en la herramienta para repartir trabajo, y en la herramienta equivocada para avisarles a varios oyentes.
- **Un channel es un recurso que hay que cerrar.** Un receptor en `for (value in channel)` espera para siempre si nadie llama a [`close()`]({{ "/es/glosario/close/" | relative_url }}): la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) nunca termina, el scope nunca completa y lo que tenga referenciado se fuga. El código que crea channels a mano tiene que decidir quién los cierra. [`produce { }`]({{ "/es/glosario/produce/" | relative_url }}) lo resuelve atando la vida del channel a una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}): cuando el productor termina o se cancela su scope, el channel se cierra.
- **El rendezvous por defecto puede colgar el código.** Sin buffer, [`send`]({{ "/es/glosario/send/" | relative_url }}) espera a un receptor. Una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) que envía y después recibe sobre el mismo channel rendezvous, sin nadie más alrededor, queda suspendida para siempre. Elegir la capacidad es una decisión de diseño, no un detalle.
- **`UNLIMITED` mueve el problema, no lo resuelve.** Un productor más rápido que su consumidor sigue agregando a un buffer sin límite hasta que se acaba la memoria. Un buffer acotado (`BUFFERED`, o una capacidad explícita) hace esperar al productor rápido, y eso es [backpressure]({{ "/es/glosario/backpressure/" | relative_url }}). Descartar valores a propósito es [`CONFLATED`]({{ "/es/glosario/conflation/" | relative_url }}) o una política de descarte.
- **El orden se conserva, y eso es útil.** Los valores salen en el mismo orden en que entraron. Una sola [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) que procesa comandos de un channel los maneja **de a uno, en orden**, sin ningún [lock]({{ "/es/glosario/lock/" | relative_url }}). Es una forma simple de serializar trabajo que nunca debe correr en paralelo, como las escrituras a un mismo archivo.
- **Para eventos de UI, un channel con buffer es la respuesta habitual de "evento", pero no la primera.** A diferencia de un [SharedFlow]({{ "/es/02-coroutines-flow/sharedflow/" | relative_url }}) sin replay, un channel con buffer guarda un evento enviado mientras la pantalla está en background, y lo entrega cuando la UI vuelve a colectar. Igual no es infalible: un evento que ya salió del channel se pierde si el [collector]({{ "/es/glosario/collector/" | relative_url }}) se cancela antes de manejarlo. La guía de [Android]({{ "/es/glosario/android/" | relative_url }}) prefiere modelar esos eventos como estado de UI que la UI confirma, y usar un channel solo cuando algo realmente es un evento de una sola vez.
- **En el código de una app, los channels son sobre todo cañerías.** Operadores de Flow como [`buffer`]({{ "/es/glosario/buffer/" | relative_url }}), [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) y [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}) usan channels por dentro, así que la mayoría de las veces te beneficiás de ellos sin tocarlos. Recurrir a un channel crudo se justifica para pipelines productor-consumidor, reparto de trabajo y procesamiento serializado; para todo lo demás, un Flow o un [StateFlow]({{ "/es/02-coroutines-flow/stateflow/" | relative_url }}) es más simple.

## Code in Action

```kotlin
// Not found in FAS — standalone example
// produce {} crea el channel, corre el productor y lo cierra al terminar.
// El ciclo for termina solo cuando el channel se cerró y se vació.
fun CoroutineScope.pagesOf(api: TaskApi): ReceiveChannel<List<Task>> = produce {
    var page = 0
    while (true) {
        val tasks = api.fetchPage(page++)
        if (tasks.isEmpty()) break
        send(tasks)                    // suspende si el consumidor va atrasado
    }
}                                      // salir del bloque cierra el channel

suspend fun importAll(scope: CoroutineScope, api: TaskApi, dao: TaskDao) {
    for (page in scope.pagesOf(api)) {
        dao.insertAll(page)
    }
}

// Not found in FAS — standalone example
// Fan-out: tres workers comparten una cola. Cada archivo se sube exactamente
// una vez, por el worker que esté libre, y como mucho hay tres subidas a la vez.
suspend fun uploadAll(files: List<File>) = coroutineScope {
    val queue = Channel<File>(Channel.UNLIMITED)
    files.forEach { queue.send(it) }
    queue.close()                      // no hay más trabajo: los workers paran cuando se vacía

    repeat(3) {
        launch {
            for (file in queue) upload(file)
        }
    }
}

// Not found in FAS — standalone example
// Procesamiento serializado: un solo consumidor maneja los comandos de a uno,
// en orden, así dos escrituras al mismo archivo nunca se superponen. Sin lock.
class ExportWriter(scope: CoroutineScope, private val file: File) {
    private val commands = Channel<String>(Channel.BUFFERED)

    init {
        scope.launch {
            for (line in commands) file.appendText(line)
        }
    }

    suspend fun write(line: String) = commands.send(line)
}

// Not found in FAS — standalone example
// Un channel con buffer para eventos de una sola vez: un evento enviado
// mientras la pantalla está en background espera en el buffer en vez de perderse
private val _events = Channel<UiEvent>(Channel.BUFFERED)
val events: Flow<UiEvent> = _events.receiveAsFlow()
```

## The Interview (En el banquillo)

**Pregunta**: ¿Qué diferencia hay entre un [`Channel`]({{ "/es/glosario/channel/" | relative_url }}), un [`Flow`]({{ "/es/02-coroutines-flow/flow-cold-streams/" | relative_url }}) y un [`SharedFlow`]({{ "/es/02-coroutines-flow/sharedflow/" | relative_url }}), y cuándo elegirías un channel?

**Respuesta Senior**: Un [`Flow`]({{ "/es/02-coroutines-flow/flow-cold-streams/" | relative_url }}) es [cold]({{ "/es/glosario/cold-stream/" | relative_url }}): es una descripción que ejecuta su productor desde cero para cada [collector]({{ "/es/glosario/collector/" | relative_url }}), así que no se comparte nada y no pasa nada hasta que alguien colecta. Un [`SharedFlow`]({{ "/es/02-coroutines-flow/sharedflow/" | relative_url }}) y un [`Channel`]({{ "/es/glosario/channel/" | relative_url }}) son los dos [hot]({{ "/es/glosario/hot-stream/" | relative_url }}): existen independientemente de sus consumidores. La diferencia entre esos dos es cómo se entregan los valores. Un [`SharedFlow`]({{ "/es/02-coroutines-flow/sharedflow/" | relative_url }}) difunde: cada [collector]({{ "/es/glosario/collector/" | relative_url }}) recibe cada valor. Un [`Channel`]({{ "/es/glosario/channel/" | relative_url }}) es una cola: cada valor se le entrega a exactamente un receptor, así que con varios receptores los valores se reparten entre ellos. Además guarda los valores en su buffer hasta que alguien los toma, mientras que un [`SharedFlow`]({{ "/es/02-coroutines-flow/sharedflow/" | relative_url }}) sin replay descarta los valores cuando no hay nadie suscripto. Entonces recurro a un channel cuando cada ítem se tiene que manejar exactamente una vez: un pipeline productor-consumidor, un grupo de workers tomando trabajos de una misma cola, o un único consumidor que serializa comandos para que nunca corran en paralelo. Para estado uso un [`StateFlow`]({{ "/es/02-coroutines-flow/stateflow/" | relative_url }}), para avisarles a varios oyentes un [`SharedFlow`]({{ "/es/02-coroutines-flow/sharedflow/" | relative_url }}), y para eventos de UI primero intento modelarlos como estado. Uso un channel con buffer solo cuando algo realmente es un evento de una sola vez, sabiendo que un evento que ya se tomó igual se puede perder si el [collector]({{ "/es/glosario/collector/" | relative_url }}) se cancela antes de manejarlo.

**Pregunta**: Una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) recorre `for (task in channel)` para procesar trabajo, y QA nota que el scope de la pantalla nunca completa y la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) sigue corriendo después de terminar el trabajo. ¿Qué está mal y cómo lo arreglás?

**Respuesta Senior**: Un ciclo `for` sobre un channel solo termina cuando el channel está **cerrado** y su buffer vacío. Si nadie llama a [`close()`]({{ "/es/glosario/close/" | relative_url }}), el ciclo queda suspendido en el próximo [`receive`]({{ "/es/glosario/receive/" | relative_url }}) para siempre, esperando un valor que nunca va a llegar: la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) nunca termina, el scope que la lanzó nunca completa, y todo lo que referencia sigue vivo. El arreglo es que cerrarlo sea responsabilidad explícita de alguien. El productor llama a [`close()`]({{ "/es/glosario/close/" | relative_url }}) cuando envió todo, idealmente en un bloque [`finally`]({{ "/es/glosario/finally/" | relative_url }}) para que una falla también lo cierre. El mejor arreglo es no manejarlo a mano y crear el channel con [`produce { }`]({{ "/es/glosario/produce/" | relative_url }}): ata el channel a la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) productora y lo cierra automáticamente cuando esa [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) termina, falla o se cancela junto con su scope. El mismo razonamiento vale del lado del consumidor: si el consumidor deja de leer antes, tiene que cancelar el channel para que el productor no siga suspendido en [`send`]({{ "/es/glosario/send/" | relative_url }}). En general, un [`Channel()`]({{ "/es/glosario/channel/" | relative_url }}) crudo sin un dueño claro es una mala señal. Prefiero [`produce`]({{ "/es/glosario/produce/" | relative_url }}), o un [`Flow`]({{ "/es/02-coroutines-flow/flow-cold-streams/" | relative_url }}) cuando no hace falta encolar nada.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
