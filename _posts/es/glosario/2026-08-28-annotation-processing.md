---
layout: post
title: "Procesamiento de Anotaciones"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/annotation-processing/
---

## The Theory (El Qué)

El **procesamiento de anotaciones** es un mecanismo de [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}) que lee las anotaciones en el [código fuente]({{ "/es/glosario/source-code/" | relative_url }}) y genera código o recursos adicionales antes de que se produzca el [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) final. En la [JVM]({{ "/es/glosario/jvm/" | relative_url }})/Android, dos herramientas principales se encargan de esto: **[kapt]({{ "/es/glosario/kapt/" | relative_url }})** (Kotlin Annotation Processing Tool), que conecta Kotlin con la API de procesamiento de anotaciones de Java, y **[KSP]({{ "/es/glosario/ksp/" | relative_url }})** (Kotlin Symbol Processing), que opera directamente sobre los símbolos del compilador de Kotlin y es significativamente más rápido.

## The Senior Nuance (El Matiz Senior)

- El procesamiento de anotaciones genera código **en tiempo de compilación**, lo que significa que los errores en el código generado se manifiestan como fallos de build — no como crashes en [tiempo de ejecución]({{ "/es/glosario/runtime/" | relative_url }}). Esto es una ventaja de seguridad importante.
- **[Dagger]({{ "/es/glosario/dagger/" | relative_url }})/[Hilt]({{ "/es/glosario/hilt/" | relative_url }})** usa procesamiento de anotaciones para construir [grafos de dependencias]({{ "/es/glosario/dependency-graph/" | relative_url }}) — cada [`@Inject`]({{ "/es/glosario/inject/" | relative_url }}), [`@Module`]({{ "/es/glosario/module-annotation/" | relative_url }}) y [`@Binds`]({{ "/es/glosario/binds/" | relative_url }}) se resuelve en tiempo de compilación, garantizando que todas las dependencias sean satisfacibles antes de que la app se ejecute.
- **[kapt]({{ "/es/glosario/kapt/" | relative_url }})** funciona generando [stubs]({{ "/es/glosario/stubs/" | relative_url }}) de Java a partir del código fuente de Kotlin y luego ejecutando la API `javax.annotation.processing` de Java. Este paso de generación de [stubs]({{ "/es/glosario/stubs/" | relative_url }}) es la razón principal por la que [kapt]({{ "/es/glosario/kapt/" | relative_url }}) es lento. **[KSP]({{ "/es/glosario/ksp/" | relative_url }})** evita los [stubs]({{ "/es/glosario/stubs/" | relative_url }}) por completo, procesando símbolos de Kotlin directamente — típicamente 2× más rápido.
- Las implementaciones de [DAOs]({{ "/es/glosario/dao/" | relative_url }}) de [Room]({{ "/es/glosario/room/" | relative_url }}), los adaptadores de [Moshi]({{ "/es/glosario/moshi/" | relative_url }})/Kotlinx.Serialization y los [Safe Args]({{ "/es/glosario/safe-args/" | relative_url }}) de [navigation]({{ "/es/glosario/navigation-component/" | relative_url }}) se generan todos mediante procesamiento de anotaciones.

```kotlin
// From FollowApp Suite — RepositoryModule.kt
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    abstract fun bindTaskRepository(
        taskRepositoryImpl: TaskRepositoryImpl
    ): TaskRepository

    @Binds
    abstract fun bindLabelRepository(
        labelRepositoryImpl: LabelRepositoryImpl
    ): LabelRepository
}
```

En este ejemplo, [`@Module`]({{ "/es/glosario/module-annotation/" | relative_url }}), [`@InstallIn`]({{ "/es/glosario/install-in/" | relative_url }}) y [`@Binds`]({{ "/es/glosario/binds/" | relative_url }}) son procesados en tiempo de compilación por el procesador de anotaciones de [Hilt]({{ "/es/glosario/hilt/" | relative_url }}), que genera el código de conexión entre interfaces y sus implementaciones.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
