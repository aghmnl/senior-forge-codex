---
layout: post
title: "@DslMarker"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/dsl-marker/
---

## The Theory (El Qué)

**`@DslMarker`** es una meta-anotación de Kotlin que previene el acceso implícito a [receivers]({{ "/es/glosario/receiver-type/" | relative_url }}) exteriores cuando las [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) con receivers están anidadas dentro de un [DSL]({{ "/es/glosario/dsl/" | relative_url }}). Sin ella, el código dentro de una lambda interna puede accidentalmente llamar métodos de receivers exteriores — el compilador resuelve silenciosamente al match más externo. `@DslMarker` convierte esto en un error de [compile-time]({{ "/es/glosario/compile-time/" | relative_url }}): si realmente necesitás el receiver externo, debés escribir [`this@label`]({{ "/es/glosario/this-at-label/" | relative_url }}) explícitamente.

Se crea un `@DslMarker` anotando tu propia anotación con `@DslMarker`, luego aplicando esa anotación a cada [receiver type]({{ "/es/glosario/receiver-type/" | relative_url }}) en tu DSL. Todos los tipos anotados con el mismo marker forman un "grupo de scope" — dentro de una lambda anidada, solo el miembro más interno del grupo es implícitamente accesible.

```kotlin
// Not found in FAS — standalone example
@DslMarker
annotation class HtmlDsl

@HtmlDsl
class HtmlBuilder {
    fun body(block: BodyBuilder.() -> Unit) { /* ... */ }
}

@HtmlDsl
class BodyBuilder {
    fun p(text: String) { /* ... */ }
    fun div(block: DivBuilder.() -> Unit) { /* ... */ }
}

@HtmlDsl
class DivBuilder {
    fun span(text: String) { /* ... */ }
}

fun html(block: HtmlBuilder.() -> Unit): String { /* ... */ }

// Uso — @DslMarker previene la fuga de scope:
html {
    body {
        div {
            span("Hello")
            // p("World")  // ERROR: p() es de BodyBuilder, no de DivBuilder
            // this@body.p("World")  // OK: cualificación explícita
        }
    }
}
```

## The Senior Nuance (El Matiz Senior)

- **`@LayoutScopeMarker` de Compose**: [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) usa `@LayoutScopeMarker` (un `@DslMarker`) en `ColumnScope`, `RowScope`, `BoxScope`, etc. Por eso `Modifier.weight()` está disponible dentro de `Column {}` pero no dentro de un `Row {}` anidado — el marker restringe cada [scope]({{ "/es/glosario/scope/" | relative_url }}) a los métodos de su propio receiver.
- **[Gradle Kotlin DSL]({{ "/es/glosario/gradle-kotlin-dsl/" | relative_url }})**: Gradle aplica un mecanismo similar (`@HasImplicitReceiver`) para prevenir que los bloques del build script accedan accidentalmente a [scopes]({{ "/es/glosario/scope/" | relative_url }}) exteriores. El bloque `android {}` no puede llamar directamente a métodos de `dependencies {}`, aunque ambos estén anidados en el mismo archivo.
- **Cuándo aplicarlo**: Cada vez que diseñés un [DSL]({{ "/es/glosario/dsl/" | relative_url }}) con más de un nivel de anidamiento. Sin `@DslMarker`, los usuarios de tu DSL escribirán código que compila pero hace algo inesperado — llamando a un método en el receiver equivocado. Es una de las fuentes más comunes de bugs en DSLs personalizados de Kotlin.
- **Relación con `this@label`**: `@DslMarker` no bloquea los receivers exteriores por completo — bloquea el acceso *implícito*. [`this@label`]({{ "/es/glosario/this-at-label/" | relative_url }}) explícito sigue funcionando, lo que significa que el desarrollador debe optar conscientemente por llamadas cross-scope. Es diseño de "pit of success": el camino seguro es el default.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
