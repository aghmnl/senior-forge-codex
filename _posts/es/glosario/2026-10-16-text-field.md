---
layout: post
title: "TextField"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, state-management]
lang: es
permalink: /es/glosario/text-field/
---

## The Theory (El Qué)

**`TextField`** es el composable de entrada de texto de Material. Es [stateless]({{ "/es/glosario/stateful-stateless/" | relative_url }}): muestra el `value` que recibe y llama a `onValueChange` con el texto nuevo en cada tecla; quien lo llama tiene que guardar ese texto y volver a pasarlo, o el campo no cambia. `OutlinedTextField` es la variante con borde.

```kotlin
// Not found in FAS — standalone example
var query by rememberSaveable { mutableStateOf("") }
TextField(value = query, onValueChange = { query = it })
```

## The Senior Nuance (El Matiz Senior)

- **Olvidarse de actualizar el estado congela el campo**: escribir llama a `onValueChange`, pero el texto que se ve sigue siendo el `value` viejo.
- **Mantener el texto sincronizado sin demora.** Actualizarlo de forma asíncrona (después de una llamada suspend) hace saltar el cursor; se guarda de forma síncrona y el trabajo lento va aparte.
- Ver [State Hoisting]({{ "/es/03-jetpack-compose/state-hoisting/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
