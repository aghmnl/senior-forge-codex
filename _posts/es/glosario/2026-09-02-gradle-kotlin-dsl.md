---
layout: post
title: "Gradle Kotlin DSL"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/gradle-kotlin-dsl/
---

## The Theory (El Qué)

**Gradle Kotlin DSL** reemplaza los archivos `build.gradle` basados en Groovy con `build.gradle.kts` — scripts de Kotlin que configuran el build usando un [DSL]({{ "/es/glosario/dsl/" | relative_url }}) type-safe. Cada bloque que escribís (`android {}`, `dependencies {}`, `plugins {}`) es una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) con un [receiver type]({{ "/es/glosario/receiver-type/" | relative_url }}): `android {}` es en realidad `fun android(block: ApplicationExtension.() -> Unit)`, así que `this` dentro del bloque es el objeto `ApplicationExtension` y el IDE puede autocompletar cada propiedad válida.

```kotlin
// From FollowApp Suite — build.gradle.kts (mysteps)
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.ksp)
    alias(libs.plugins.hilt.android)
}

android {
    namespace = "com.followapp.mysteps"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.followapp.mysteps"
        minSdk = 26
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    buildFeatures {
        compose = true
    }
}

dependencies {
    implementation(project(":core:designsystem"))
    implementation(libs.androidx.activity.compose)
    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)
}
```

## The Senior Nuance (El Matiz Senior)

- El Kotlin DSL provee seguridad en [compile-time]({{ "/es/glosario/compile-time/" | relative_url }}): errores tipográficos en nombres de propiedades o tipos incorrectos fallan el build inmediatamente, mientras que los scripts Groovy fallan silenciosamente o en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}). Combinado con el autocompletado del IDE, esto reduce drásticamente la misconfiguración del build.
- Cada bloque anidado (`android {}`, `defaultConfig {}`, `dependencies {}`) es una [función de orden superior]({{ "/es/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) que recibe una lambda con receiver. El anidamiento crea una estructura legible y declarativa — es el mismo mecanismo de [DSL]({{ "/es/glosario/dsl/" | relative_url }}) que impulsa a [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}).
- Los Version Catalogs (`libs.versions.toml`) funcionan con el Kotlin DSL a través de accessors type-safe como `libs.plugins.kotlin.android` y `libs.androidx.activity.compose`. Estos accessors se generan en build time — no existen en el código fuente y no son una feature estándar de Kotlin.
- El equivalente de `@DslMarker` en Gradle (`@HasImplicitReceiver`) previene el acceso accidental a [receivers]({{ "/es/glosario/receiver-type/" | relative_url }}) del [scope]({{ "/es/glosario/scope/" | relative_url }}) externo en bloques de build profundamente anidados — el mismo mecanismo de prevención de fugas que [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) usa con `@LayoutScopeMarker`.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
