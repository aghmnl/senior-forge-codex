---
layout: post
title: "Platform Types"
date: 2026-09-13 12:00:00 +0000
categories: [es, glosario]
tags: [null-safety, interop, type-system]
lang: es
permalink: /es/glosario/platform-types/
---

## The Theory (El Qué)

Un **platform type** (tipo de plataforma) es el tipo que Kotlin asigna a un valor que viene de Java (o de cualquier código JVM) cuya nullabilidad el compilador no puede determinar. Se escribe `String!` en los mensajes de error y en los hints del IDE, y significa "o `String` o `String?` — decidilo vos". El compilador no aplica ninguno de los dos chequeos: podés llamar miembros directamente, asignarlo a una variable no-nullable o tratarlo como nullable, y acepta las tres cosas. La nullabilidad se verifica en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}), con una [NullPointerException]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) en el punto donde un `null` alcanza un tipo Kotlin no-nullable.

Los platform types existen porque el sistema de tipos de Java no tiene noción de nullabilidad. Cuando un método Java lleva una anotación de nullabilidad que el compilador reconoce — `@Nullable`/`@NonNull` de AndroidX, JetBrains, JSR-305 o `jspecify` — Kotlin la mapea a un `T?` o `T` común. Sin anotación, el platform type es la respuesta honesta.

```kotlin
// From FollowApp Suite — AboutScreen.kt
val licenseObj = firstLicenseId?.let { licensesMap.optJSONObject(it) }
License(
    licenseName = licenseObj?.optString("name")?.ifBlank { firstLicenseId }
        ?: firstLicenseId ?: "Unknown",
    licenseText = licenseObj?.optString("content").orEmpty()
)
```

`org.json` no está anotada, así que `optString` devuelve `String!` y `optJSONObject` devuelve `JSONObject!`. El código trata a ambos como nullable a propósito: [safe calls]({{ "/es/glosario/safe-call/" | relative_url }}), fallbacks con Elvis y `orEmpty()` convierten la ambigüedad en un `String` no-null explícito en el límite.

## The Senior Nuance (El Matiz Senior)

- **El peligro es el camino silencioso, no el crash.** `val name: String = javaApi.getName()` compila sin warning. Si Java devuelve `null`, el fallo es una NPE en la asignación — o peor, varios frames después, una vez que el valor fue guardado y pasado de mano en mano. Cada `!!` que el compilador *habría* exigido simplemente no está.
- **Resolvé el tipo en el límite, una sola vez.** Envolvé las llamadas Java sin anotar en una función Kotlin cuya firma diga la verdad (`fun readName(): String?`), o declará la variable receptora explícitamente (`val name: String? = javaApi.getName()`). Los platform types nunca deberían propagarse al [data layer]({{ "/es/glosario/data-layer/" | relative_url }}) ni a una [data class]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}).
- **La mayor parte del SDK de Android y de Jetpack está anotada.** `ContentResolver.openOutputStream` es `@Nullable`, y por eso FAS tiene que escribir `requireNotNull(stream) { "Cannot open destination" }` — el compilador ve `OutputStream?`, no un platform type. Los huecos son las APIs viejas del framework, `org.json` y las librerías Java de terceros; tratalas como nullable por defecto.
- **Anotá tu propio Java, o no generes ninguno.** El código Java que controlás debería llevar `@Nullable`/`@NonNull` para que los llamadores Kotlin reciban tipos reales; el código generado por annotation processing (Room, Hilt) ya lo hace. Los [raw types]({{ "/es/glosario/raw-types/" | relative_url }}) son el gemelo de este problema para los argumentos genéricos — un `List<!>` desde Java suprime tanto el chequeo de nullabilidad como el del argumento de tipo.
- **Encuadre de entrevista:** los platform types son una de las cuatro formas en que el código Kotlin todavía lanza una NPE (junto con `!!`, `lateinit` sin inicializar y `equals` roto). Ver [Null Safety: Elvis y Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
