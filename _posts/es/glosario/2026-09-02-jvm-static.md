---
layout: post
title: "@JvmStatic"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/jvm-static/
---

## The Theory (El Qué)

**`@JvmStatic`** es una anotación de Kotlin que instruye al compilador a generar un verdadero método `static` de JVM en la clase que lo contiene, además del método de instancia regular en el [companion object]({{ "/es/glosario/companion-object/" | relative_url }}). Sin ella, una función del companion `MyClass.Companion.doSomething()` existe como un método de instancia en la clase `Companion` — los callers de Java deben escribir `MyClass.Companion.doSomething()` en lugar de `MyClass.doSomething()`.

`@JvmStatic` se puede aplicar a funciones y accessors de propiedades dentro de un `companion object` o un `object` con nombre.

```kotlin
// Not found in FAS — standalone example
class AppConfig {
    companion object {
        @JvmStatic
        fun defaultTimeout(): Long = 30_000L

        @JvmStatic
        val version: String = "2.1.0"
    }
}

// Kotlin: AppConfig.defaultTimeout() — funciona con o sin @JvmStatic
// Java:   AppConfig.defaultTimeout() — funciona SOLO con @JvmStatic
// Java sin @JvmStatic: AppConfig.Companion.defaultTimeout()
```

## The Senior Nuance (El Matiz Senior)

- **Interop con Java**: `@JvmStatic` es esencial cuando tu código Kotlin es consumido por callers de Java. Sin ella, el código Java debe pasar por el singleton `.Companion`, lo cual es incómodo y rompe el contrato de API que pretendías. En un codebase mixto Kotlin/Java, toda función pública de [companion object]({{ "/es/glosario/companion-object/" | relative_url }}) que Java llame debería tener `@JvmStatic`.
- **Reflexión de frameworks**: Algunos frameworks de Android (especialmente los más antiguos) usan reflexión para encontrar métodos estáticos — `@JvmStatic` asegura que el método aparezca a nivel de clase en el [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}), satisfaciendo esos lookups. Aplica a métodos `@BeforeClass`/`@AfterClass` de JUnit y métodos `@Provides` en algunas configuraciones de Dagger.
- **[Static dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }})**: Tanto las funciones anotadas como las no anotadas del companion usan [static dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }}) desde la perspectiva de Kotlin — el compilador resuelve la llamada en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}). La diferencia está a nivel de [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}): `@JvmStatic` genera un verdadero método `static` (una indirección menos), mientras que el default genera un método de instancia en la clase `Companion`.
- **`const val` no lo necesita**: Las propiedades declaradas como `const val` en un companion object ya compilan a campos `static final` de JVM directamente en la clase contenedora — `@JvmStatic` es redundante y de hecho es un error de compilación en `const val`.
- **Objetos con nombre también**: `@JvmStatic` también funciona en declaraciones de `object` con nombre ([singletons]({{ "/es/glosario/singleton/" | relative_url }})), lo cual es útil para objetos utilitarios que el código Java necesita llamar sin `.INSTANCE`.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
