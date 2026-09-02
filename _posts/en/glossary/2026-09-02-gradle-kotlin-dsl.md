---
layout: post
title: "Gradle Kotlin DSL"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/gradle-kotlin-dsl/
---

## The Theory (The What)

**Gradle Kotlin DSL** replaces Groovy-based `build.gradle` files with `build.gradle.kts` — Kotlin scripts that configure the build using a type-safe [DSL]({{ "/en/glossary/dsl/" | relative_url }}). Every block you write (`android {}`, `dependencies {}`, `plugins {}`) is a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) with a [receiver type]({{ "/en/glossary/receiver-type/" | relative_url }}): `android {}` is actually `fun android(block: ApplicationExtension.() -> Unit)`, so `this` inside the block is the `ApplicationExtension` object and the IDE can autocomplete every valid property.

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

## The Senior Nuance

- The Kotlin DSL provides [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) safety: typos in property names or wrong types fail the build immediately, while Groovy scripts fail silently or at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}). Combined with IDE autocomplete, this dramatically reduces build misconfiguration.
- Each nested block (`android {}`, `defaultConfig {}`, `dependencies {}`) is a [higher-order function]({{ "/en/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) that receives a lambda with a receiver. The nesting creates a readable, declarative structure — this is the same [DSL]({{ "/en/glossary/dsl/" | relative_url }}) mechanism that powers [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}).
- Version Catalogs (`libs.versions.toml`) work with the Kotlin DSL through type-safe accessors like `libs.plugins.kotlin.android` and `libs.androidx.activity.compose`. These accessors are generated at build time — they do not exist in source and are not a standard Kotlin feature.
- Gradle's `@DslMarker`-equivalent (`@HasImplicitReceiver`) prevents accidental access to outer [scope]({{ "/en/glossary/scope/" | relative_url }}) receivers in deeply nested build blocks — the same leakage-prevention mechanism that [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) uses with `@LayoutScopeMarker`.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
