---
layout: post
title: "Reflexión en Runtime"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/runtime-reflection/
---

## The Theory (El Qué)

La **reflexión en runtime** es la capacidad de un programa de inspeccionar y manipular su propia estructura — clases, funciones, propiedades, anotaciones — mientras se está [ejecutando]({{ "/es/glosario/runtime/" | relative_url }}). En la [JVM]({{ "/es/glosario/jvm/" | relative_url }}), esto lo provee `java.lang.reflect` y el `kotlin.reflect` de Kotlin (`KClass`, `KFunction`, `KProperty`). La reflexión evita la verificación de tipos en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}): en lugar de que el compilador resuelva una llamada a método, el programa la descubre e invoca en runtime por nombre o firma.

## The Senior Nuance (El Matiz Senior)

- La reflexión es **poderosa pero costosa**: crear instancias de `KClass`/`KFunction`, resolver métodos e invocarlos reflectivamente puede ser 10–100× más lento que una llamada directa. También evita la seguridad de compile-time — un typo en un nombre de método se convierte en un crash en runtime, no en un error de build.
- **[R8]({{ "/es/glosario/r8/" | relative_url }})/[ProGuard]({{ "/es/glosario/proguard/" | relative_url }}) y la reflexión entran en conflicto**: [R8]({{ "/es/glosario/r8/" | relative_url }}) renombra y elimina clases/métodos que parecen no usarse. Si tu código los accede solo via reflexión, [R8]({{ "/es/glosario/r8/" | relative_url }}) no ve la referencia y los elimina. Por eso las bibliotecas que usan reflexión (Gson, Retrofit con converters) requieren reglas keep de [ProGuard]({{ "/es/glosario/proguard/" | relative_url }}).
- Preferir alternativas de [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}) sobre reflexión siempre que sea posible: [procesamiento de anotaciones]({{ "/es/glosario/annotation-processing/" | relative_url }}) ([Dagger]({{ "/es/glosario/dagger/" | relative_url }})/[Hilt]({{ "/es/glosario/hilt/" | relative_url }}) genera código en lugar de reflejar), jerarquías de sealed classes (`when` exhaustivo en lugar de dispatch reflectivo), y parámetros de tipo [`reified`]({{ "/es/glosario/reified/" | relative_url }}) (sustitución de tipos en compile-time en lugar de checks de tipo en runtime).
- `::class` en Kotlin te da una referencia `KClass`. `::class.java` te da el objeto Java `Class`. Ambos son puntos de entrada a reflexión en runtime. Usos comunes: `[Room]({{ "/es/glosario/room/" | relative_url }}).inMemoryDatabaseBuilder(ctx, MyDb::class.java)`, `startActivity(Intent(this, TargetActivity::class.java))`, frameworks de serialización.
- La biblioteca `kotlin-reflect` de Kotlin agrega soporte completo de reflexión Kotlin (metadata de propiedades, nullability, etc.) pero pesa ~2.5 MB — significativo en Android. Para la mayoría de los casos de uso en Android, `java.lang.reflect` o código procesado por anotaciones es preferible.

```kotlin
// From FollowApp Suite — TaskDaoSortTest.kt
db = Room.inMemoryDatabaseBuilder(context, MyTasksDatabase::class.java)
    .allowMainThreadQueries()
    .build()
```

`::class.java` es un punto de entrada de reflexión liviano — [Room]({{ "/es/glosario/room/" | relative_url }}) usa el token `Class` para localizar la clase `_Impl` generada por [procesamiento de anotaciones]({{ "/es/glosario/annotation-processing/" | relative_url }}), no para escanear reflectivamente la clase de base de datos.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
