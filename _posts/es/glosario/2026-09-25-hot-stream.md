---
layout: post
title: "Hot Stream"
date: 2026-09-25 12:00:00 +0000
categories: [es, glosario]
tags: [flow, coroutines, performance]
lang: es
permalink: /es/glosario/hot-stream/
---

## The Theory (El Qué)

Un **hot stream** (stream caliente) existe y produce (o mantiene) valores **independientemente de que alguien los esté consumiendo**. Los suscriptores se suman a un stream que ya está corriendo y ven lo que pasa desde ese momento, más, según el tipo, algunos valores pasados reproducidos. Es lo opuesto de un [cold stream]({{ "/es/glosario/cold-stream/" | relative_url }}), donde cada consumidor dispara su propia ejecución desde cero. En Kotlin los streams hot son [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}), [SharedFlow]({{ "/es/glosario/sharedflow/" | relative_url }}) y [Channel]({{ "/es/glosario/channel/" | relative_url }}); [stateIn]({{ "/es/glosario/state-in/" | relative_url }}) y `shareIn` convierten un [Flow]({{ "/es/glosario/flow/" | relative_url }}) cold en uno hot.

```kotlin
// Not found in FAS — standalone example
val hot = MutableStateFlow(0)
hot.value = 1                  // ocurre sin nadie escuchando

scope.launch { hot.collect { println(it) } }   // imprime 1: se suma al presente
hot.value = 2                                   // imprime 2
```

## The Senior Nuance (El Matiz Senior)

- **Hot significa trabajo compartido.** Un productor, muchos consumidores: tres pantallas observando un stream hot cuestan una ejecución, mientras que tres colectores de un stream cold cuestan tres.
- **Hot significa que la vida útil no es la del colector.** El stream vive en el scope que lo creó (normalmente un ViewModel). Eso es lo que le permite sobrevivir a una rotación, y también lo que convierte a un stream hot olvidado en una fuga.
- **Llegar tarde tiene consecuencias.** Un suscriptor de un stream hot puede perderse los valores emitidos antes de que llegara. Si eso está bien depende del tipo: un `StateFlow` siempre entrega su valor actual; un `SharedFlow` sin replay no.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
