---
layout: post
title: "Obfuscation"
date: 2026-09-13 12:00:00 +0000
categories: [es, glosario]
tags: [build-tools, reflection, error-handling]
lang: es
permalink: /es/glosario/obfuscation/
---

## The Theory (El Qué)

La **obfuscation** (ofuscación) es el renombrado de clases, métodos y campos a identificadores cortos y sin significado (`a`, `b`, `c.d()`) en un build de release. En Android es una de las tres cosas que hace [R8]({{ "/es/glosario/r8/" | relative_url }}) junto con el shrinking y la optimización, y se activa con `isMinifyEnabled = true`. Los objetivos son un `.dex` más chico y un blanco más difícil para la ingeniería inversa — no seguridad real, porque el [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) sigue siendo completamente decompilable.

```kotlin
// From FollowApp Suite — build.gradle.kts
release {
    isMinifyEnabled = true
    isShrinkResources = true
    proguardFiles(
        getDefaultProguardFile("proguard-android-optimize.txt"),
        "proguard-rules.pro"
    )
    // Crashlytics reports only from production builds. R8 mapping
    // is uploaded automatically by the Crashlytics Gradle plugin.
    manifestPlaceholders["crashlyticsCollectionEnabled"] = true
}
```

El efecto colateral es que un [stack trace]({{ "/es/glosario/stack-trace/" | relative_url }}) de producción se lee `at c.a.b(Unknown Source:12)`. R8 escribe un `mapping.txt` por cada build que mapea los nombres ofuscados a los originales; sin él, el trace es inútil.

## The Senior Nuance (El Matiz Senior)

- **Guardá el archivo de mapping, o el crash es ilegible.** `mapping.txt` se genera por build y difiere entre builds. Subilo con cada release — el plugin de Gradle de [Crashlytics]({{ "/es/glosario/crashlytics/" | relative_url }}) lo hace automáticamente, Play Console lo acepta a mano — y archivalo junto al tag.
- **Ofuscación y [reflection]({{ "/es/glosario/runtime-reflection/" | relative_url }}) entran en conflicto.** Todo lo que se busca por nombre en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) (nombres de campos en Gson, `Class.forName`, símbolos JNI, `valueOf` de enums) se rompe al renombrarse. Para eso existen las reglas `-keep` en sintaxis [ProGuard]({{ "/es/glosario/proguard/" | relative_url }}) — FAS conserva los miembros de sus enums exactamente por esto.
- **Testeá el build de release, no solo el de debug.** Los bugs de ofuscación aparecen solo con `isMinifyEnabled = true`. Un Senior corre el build minificado con regularidad, no la noche antes de publicar.
- **No es cifrado.** Strings, recursos y flujo de control sobreviven intactos. Los secretos no van en el APK, ofuscado o no.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
