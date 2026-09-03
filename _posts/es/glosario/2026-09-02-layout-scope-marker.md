---
layout: post
title: "@LayoutScopeMarker"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/layout-scope-marker/
---

## The Theory (El Qué)

**`@LayoutScopeMarker`** es la aplicación de [`@DslMarker`]({{ "/es/glosario/dsl-marker/" | relative_url }}) de [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) a los scopes de layout. Anota `ColumnScope`, `RowScope`, `BoxScope` y otras interfaces de scope de layout. El efecto: dentro de una [lambda con receptor]({{ "/es/glosario/lambda-with-receiver/" | relative_url }}) con scope de un layout, no podés accidentalmente llamar miembros del [scope]({{ "/es/glosario/scope/" | relative_url }}) de un layout externo.

```kotlin
// Not found in FAS — standalone example
Column {
    Text("Inside ColumnScope")
    Row {
        Text("Inside RowScope")
        // Modifier.weight() es solo de ColumnScope — esto NO compilaría:
        // Text(modifier = Modifier.weight(1f), text = "Wrong scope")

        // Hay que cualificar si realmente necesitás el scope externo:
        // this@Column.run { Modifier.weight(1f) }
    }
}
```

Sin `@LayoutScopeMarker`, la lambda interna del `Row` podría ver el `weight()` de `ColumnScope` a través de la resolución implícita de receivers — un bug silencioso y difícil de detectar. El marker restringe cada [receiver type]({{ "/es/glosario/receiver-type/" | relative_url }}) a su propio límite de scope.

## The Senior Nuance (El Matiz Senior)

- `@LayoutScopeMarker` se define como `@DslMarker annotation class LayoutScopeMarker` — es una anotación de una línea que hereda todo el comportamiento de la meta-anotación [`@DslMarker`]({{ "/es/glosario/dsl-marker/" | relative_url }}). Dos interfaces de scope que comparten la misma anotación `@DslMarker` no pueden combinarse implícitamente en lambdas anidadas.
- Es una restricción de [compile time]({{ "/es/glosario/compile-time/" | relative_url }}), no un chequeo de [Runtime]({{ "/es/glosario/runtime/" | relative_url }}). El compilador se rehúsa a resolver miembros de receivers externos marcados con el mismo `@DslMarker`, forzando [`this@label`]({{ "/es/glosario/this-at-label/" | relative_url }}) o una variable explícita para cruzar límites de scope.
- En la práctica, `@LayoutScopeMarker` previene uno de los errores más comunes en Compose: llamar a `Modifier.weight()` (una extensión de `ColumnScope`/`RowScope`) desde el parent equivocado. En layouts XML este tipo de desajuste era un error silencioso en runtime; en Compose es un error de compilación.
- Al escribir tu propio layout de Compose con un scope custom, aplicá `@LayoutScopeMarker` (no un nuevo `@DslMarker`) para que tu scope participe en el mismo boundary de seguridad que los layouts built-in — un `Column` dentro de tu layout custom sigue sin poder filtrar `ColumnScope` a tu scope.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
