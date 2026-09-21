---
layout: post
title: "Downstream"
date: 2026-09-21 12:00:00 +0000
categories: [es, glosario]
tags: [flow, coroutines]
lang: es
permalink: /es/glosario/downstream/
---

## The Theory (El Qué)

**Downstream** es todo lo que viene *después* de un punto dado en una cadena de [`Flow`]({{ "/es/glosario/flow/" | relative_url }}): los operadores declarados debajo y, al final, el bloque [`collect`]({{ "/es/glosario/collect/" | relative_url }}). El código downstream siempre corre en el [contexto]({{ "/es/glosario/coroutine-context/" | relative_url }}) de quien colecta el flow — un `flowOn` puesto más arriba no lo afecta. Esa asimetría es el núcleo de [withContext vs flowOn]({{ "/es/02-coroutines-flow/with-context-vs-flow-on/" | relative_url }}): `flowOn` gobierna solo el upstream.

```kotlin
// Not found in FAS — standalone example
viewModelScope.launch {                 // contexto del colector: Main.immediate
    repository.tasks()                  // upstream: donde diga flowOn
        .map { it.toUiModel() }         // downstream: corre en Main
        .collect { _uiState.value = it } // downstream: corre en Main
}
```

## The Senior Nuance (El Matiz Senior)

- **El colector decide el contexto downstream, no el flow.** Lanzar el mismo flow desde `viewModelScope` o desde un scope de fondo cambia dónde corre cada operador downstream — la declaración del flow no dice nada al respecto.
- **Normalmente eso es lo que querés.** Actualizar un `StateFlow` o tocar estado de UI va en Main; dejar el mapeo downstream y el I/O [upstream]({{ "/es/glosario/upstream/" | relative_url }}) del `flowOn` da exactamente esa división.
- **Trabajo pesado downstream bloquea al colector.** Un `map` lento después del `flowOn` corre en Main y produce [jank]({{ "/es/glosario/jank/" | relative_url }}); movelo arriba del `flowOn`.
- Ver [withContext vs flowOn]({{ "/es/02-coroutines-flow/with-context-vs-flow-on/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
