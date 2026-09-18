---
layout: post
title: "@Nullable"
date: 2026-09-18 12:00:00 +0000
categories: [es, glosario]
tags: [interop, null-safety]
lang: es
permalink: /es/glosario/nullable-annotation/
---

## The Theory (El Qué)

**`@Nullable`** es una anotación Java (de `androidx.annotation`, JetBrains, JSpecify o JSR-305) que le dice al compilador de Kotlin que un parámetro, campo o valor de retorno Java puede ser [`null`]({{ "/es/glosario/null/" | relative_url }}). Sin ella, los valores que cruzan desde Java llegan como [platform types]({{ "/es/glosario/platform-types/" | relative_url }}) (`String!`) y Kotlin no puede garantizar nada; con ella, el valor se ve como `String?` y cada uso tiene que manejar el null. Su contraparte es [`@NonNull`]({{ "/es/glosario/non-null-annotation/" | relative_url }}). Anotar el lado Java es la primera herramienta del artículo [Null Safety: Elvis & Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) para cerrar el límite de interop.

```kotlin
// Lado Java (librería o módulo legacy)
public class LegacyUserStore {
    public @Nullable String getPhotoUrl() { ... }   // Kotlin ve String?
    public @NonNull  String getEmail()    { ... }   // Kotlin ve String
}

// Lado Kotlin: el compilador ahora obliga a manejar el null
val url: String? = store.photoUrl
val length = url?.length ?: 0
```

## The Senior Nuance (El Matiz Senior)

- **Una anotación es una promesa que Kotlin le exige al llamador, no al cuerpo Java.** Si un método `@NonNull` devuelve null igual, Kotlin crashea de todos modos — pero en el punto de llamada, con un mensaje estilo `IllegalStateException` que nombra el parámetro, mucho mejor que una NPE lejana.
- **Cuando no podés editar el código Java, envolvelo.** Una función Kotlin de una línea que devuelve `String?` documenta el límite y deja el platform type fuera del resto del código.
- **Preferí las anotaciones de AndroidX en Android.** `androidx.annotation.Nullable`/`NonNull` son las que Lint, el IDE y el compilador de Kotlin entienden por igual.
- Ver [Null Safety: Elvis & Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
