---
layout: post
title: "@Composable"
date: 2026-09-03 12:00:00 +0000
categories: [es, glosario]
tags: [compose, compiler]
lang: es
permalink: /es/glosario/composable/
---

## The Theory (El Qué)

**`@Composable`** es la anotación que marca una función como parte del sistema de UI declarativa de [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}). Una función `@Composable` describe un fragmento de UI; no retorna una vista — en su lugar, emite nodos de UI en la slot table de Compose durante la composición.

```kotlin
@Composable
fun Greeting(name: String) {
    Text("Hello, $name!")
}
```

El plugin del compilador de Compose transforma las funciones `@Composable` en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}): inyecta un parámetro oculto `Composer` y envuelve el body en llamadas de gestión de grupos/slots. Esta transformación habilita la **recomposition** de Compose — la capacidad de re-ejecutar solo las partes del árbol de UI que necesitan actualizarse cuando el estado cambia.

Las funciones `@Composable` solo pueden llamarse desde otras funciones `@Composable`. Esta restricción es impuesta por el compilador, no el [Runtime]({{ "/es/glosario/runtime/" | relative_url }}), creando un "mundo composable" separado al que no se puede entrar desde código regular excepto a través de entry points de composición como `setContent {}`.

## The Senior Nuance (El Matiz Senior)

- Un Senior entiende que `@Composable` no es solo una anotación — el plugin del compilador le da el peso de una [keyword]({{ "/es/glosario/keyword/" | relative_url }}). Cambia la firma de [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) de la función (agregando el parámetro `Composer`), haciendo que las funciones `@Composable` sean binariamente incompatibles con sus firmas no-composable.
- Las funciones composable deben ser **idempotentes** y **libres de side effects**: dados los mismos inputs, deberían emitir la misma UI. Los side effects (llamadas de red, lecturas de base de datos, logging) pertenecen a bloques `LaunchedEffect`, `SideEffect` o `DisposableEffect`, que son wrappers lifecycle-aware que Compose gestiona.
- Al usar [delegated properties]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}) como `by remember { mutableStateOf() }` dentro de un `@Composable`, la llamada a `remember` ancla el estado a la posición del composable en la slot table. Mover el composable en el árbol (por ejemplo, rendering condicional) puede resetear este estado — una sutileza que `key()` resuelve.
- Los [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) `@Composable` — como el parámetro `content` de `Column { ... }` — llevan la misma transformación del compilador. Por esto no se puede pasar un [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) `@Composable` donde se espera un `() -> Unit` regular.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
