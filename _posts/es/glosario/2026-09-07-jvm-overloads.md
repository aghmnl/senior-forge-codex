---
layout: post
title: "@JvmOverloads"
date: 2026-09-07 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/jvm-overloads/
---

## The Theory (El Qué)

`@JvmOverloads` le indica al compilador de Kotlin que genere, para una función con valores de parámetro por defecto, un método [JVM]({{ "/es/glosario/jvm/" | relative_url }}) adicional por cada parámetro omitido. Los argumentos por defecto de Kotlin son una característica del *lenguaje* que la JVM no conoce: sin la anotación, Kotlin emite un único método más un bridge sintético, y los callers de Java tienen que pasar todos los argumentos.

```kotlin
// Not found in FAS — standalone example
class CustomChip @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr)
```

Esa única declaración genera tres constructores en el [Bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) — `(Context)`, `(Context, AttributeSet?)` y `(Context, AttributeSet?, Int)` — que es una forma de [Polymorphism]({{ "/es/glosario/polymorphism/" | relative_url }}) ad-hoc resuelta por [Static Dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }}) en [Compile Time]({{ "/es/glosario/compile-time/" | relative_url }}).

## The Senior Nuance (El Matiz Senior)

- **Su uso clásico son las custom Views.** El layout inflater de Android busca por reflection firmas de constructor específicas, así que una `View` custom escrita en Kotlin con argumentos por defecto solo va a inflarse bien desde XML si `@JvmOverloads` los generó. Es un crash real, no una preocupación teórica — y hoy es mayormente histórico, dado que [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) reemplaza a las custom Views.
- **Es una herramienta de interop con Java, y los módulos Kotlin puros no la necesitan.** Los callers de Kotlin resuelven los argumentos por defecto en el [Call Site]({{ "/es/glosario/call-site/" | relative_url }}) sin ninguna sobrecarga generada. Ponerle la anotación a código que ningún consumidor Java toca es [Code Bloat]({{ "/es/glosario/code-bloat/" | relative_url }}) al pedo — cada método generado cuesta method count y tamaño de APK.
- **Genera una cadena lineal, no combinatoria.** Para `f(a, b = 1, c = 2)` obtenés `f(a)`, `f(a, b)` y `f(a, b, c)` — nunca `f(a, c)`. Los parámetros solo pueden descartarse desde la derecha. Si los callers de Java necesitan saltear un parámetro del medio, escribí la sobrecarga a mano.
- **Interactúa mal con agregar parámetros después.** Insertar un nuevo parámetro por defecto en el medio cambia silenciosamente qué significa cada firma generada, rompiendo callers Java ya compilados en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) en vez de en [Compile Time]({{ "/es/glosario/compile-time/" | relative_url }}). Agregá los defaults nuevos al final.
- **En un constructor la anotación va sobre el [Keyword]({{ "/es/glosario/keyword/" | relative_url }}) `constructor`**, y por eso el [Primary Constructor]({{ "/es/glosario/primary-constructor/" | relative_url }}) tiene que escribirse explícito en vez de en su forma implícita habitual.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
