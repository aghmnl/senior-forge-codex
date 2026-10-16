---
layout: post
title: "Stateful & Stateless"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, state-management]
lang: es
permalink: /es/glosario/stateful-stateless/
---

## The Theory (El Qué)

Un composable **stateful** (con estado) crea y guarda su propio estado con [`remember`]({{ "/es/glosario/remember/" | relative_url }}): funciona solo, pero quien lo llama no puede leer ni cambiar ese estado. Un composable **stateless** (sin estado) recibe su estado como parámetros e informa los cambios con [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) de eventos: solo muestra lo que le dan. El state hoisting convierte el primero en el segundo.

```kotlin
// Not found in FAS — standalone example
@Composable fun Counter() { var n by remember { mutableStateOf(0) }; Button({ n++ }) { Text("$n") } }   // stateful
@Composable fun Counter(n: Int, onIncrement: () -> Unit) { Button(onIncrement) { Text("$n") } }         // stateless
```

## The Senior Nuance (El Matiz Senior)

- **Stateless es reutilizable y testeable**: se puede mostrar en un [Preview]({{ "/es/glosario/preview/" | relative_url }}) con cualquier valor y testear revisando los eventos que emite.
- **Stateful es cómodo**, así que las librerías suelen ofrecer los dos: una versión stateless y un envoltorio stateful con valores por defecto razonables.
- Ver [State Hoisting]({{ "/es/03-jetpack-compose/state-hoisting/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
