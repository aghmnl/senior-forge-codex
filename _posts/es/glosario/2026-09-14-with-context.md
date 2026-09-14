---
layout: post
title: "withContext"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, threading]
lang: es
permalink: /es/glosario/with-context/
---

## The Theory (El Qué)

**`withContext(context) { }`** corre un bloque con un [`CoroutineContext`]({{ "/es/glosario/coroutine-context/" | relative_url }}) modificado — casi siempre otro [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) — y devuelve el valor del bloque. Es una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}): el llamador suspende, la [continuation]({{ "/es/glosario/continuation/" | relative_url }}) del bloque se agenda en el dispatcher destino, y cuando el bloque completa el llamador se reanuda en su dispatcher *original*. No se crea ninguna coroutine nueva; el bloque corre en el mismo [`Job`]({{ "/es/glosario/job/" | relative_url }}), así que la cancelación fluye directo a través.

```kotlin
// From FollowApp Suite — LegacyDataImporter.kt
val legacyTasks = withContext(Dispatchers.IO) { reader.readLegacyTasks() }
if (legacyTasks.isNotEmpty()) {
    taskDao.insertTasks(legacyTasks.mapIndexed { index, task -> task.toTaskEntity(index, now) })
}
```

Solo se envuelve la llamada genuinamente [bloqueante]({{ "/es/glosario/blocking-call/" | relative_url }}); el insert de Room que sigue ya es main-safe y se queda en el dispatcher del llamador.

## The Senior Nuance (El Matiz Senior)

- **Es lo que hace main-safe a una suspend function.** Ponelo *adentro* de la función que bloquea, así todo llamador — un ViewModel en Main, un test, un worker — obtiene el comportamiento correcto sin saberlo. Envolver en el call site significa que el próximo llamador se olvida.
- **`withContext` es secuencial; `launch`/`async` son concurrentes.** Devuelve el resultado del bloque y no sigue hasta que el bloque termina. Si necesitás el valor, es la herramienta correcta; si necesitás disparar y seguir, es la equivocada.
- **Barato cuando el dispatcher no cambia realmente.** `IO` y `Default` comparten pool, y el [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) se saltea el salto de thread cuando el dispatcher destino ya es el actual. Un `withContext(IO)` anidado dentro de otro `withContext(IO)` cuesta casi nada.
- **No lo uses para llegar a `Dispatchers.Main` desde un repositorio.** Una clase del data layer que cambia a Main tiene una dependencia de UI; devolvé el valor y dejá que el llamador decida dónde aterriza.
- **`withContext(NonCancellable)`** es la vía de escape para cleanup que debe terminar incluso después de la cancelación — dentro de un `finally`, y en ningún otro lado.
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
