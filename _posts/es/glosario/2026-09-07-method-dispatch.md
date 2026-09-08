---
layout: post
title: "Method Dispatch"
date: 2026-09-07 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/method-dispatch/
---

## The Theory (El Qué)

El **Method Dispatch** (dispatch de métodos) es cómo la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) decide *cuál* implementación de un método se ejecuta realmente en una llamada dada. Hay dos mecanismos, y la diferencia está en *cuándo* se toma la decisión:

- **[Static Dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }})** — se resuelve en [Compile Time]({{ "/es/glosario/compile-time/" | relative_url }}) a partir del tipo *declarado*. Se usa para [`final`]({{ "/es/glosario/final/" | relative_url }}), `private`, funciones top-level y [Extension Functions]({{ "/es/glosario/extension-functions/" | relative_url }}), y para el [Function Overloading]({{ "/es/glosario/function-overloading/" | relative_url }}).
- **[Virtual Dispatch]({{ "/es/glosario/virtual-dispatch/" | relative_url }})** — se resuelve en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) a partir del objeto *real*, buscando el método en la [vtable]({{ "/es/glosario/vtable/" | relative_url }}). Es lo que hace funcionar al [Polymorphism]({{ "/es/glosario/polymorphism/" | relative_url }}).

```kotlin
// From FollowApp Suite — StateChip.kt
// Virtual dispatch: la referencia ChipState se resuelve en runtime
// a Full, Outline o Partial, cada una con su propio inputColors().
sealed interface ChipState {
    @Composable fun inputColors(): SelectableChipColors
}
```

## The Senior Nuance (El Matiz Senior)

- **Las [Extension Functions]({{ "/es/glosario/extension-functions/" | relative_url }}) usan static dispatch, y es una trampa clásica de entrevista.** `fun Animal.speak() = "..."` y `fun Dog.speak() = "woof"` llamadas sobre una variable *declarada* `Animal` van a ejecutar siempre la versión de `Animal`, sin importar el objeto en runtime. Las extensions se compilan como funciones estáticas que reciben el [Receiver]({{ "/es/glosario/receiver-type/" | relative_url }}) como primer parámetro — no entran a la [vtable]({{ "/es/glosario/vtable/" | relative_url }}) y no pueden sobreescribirse.
- **La [Overload Resolution]({{ "/es/glosario/overload-resolution/" | relative_url }}) también es una decisión de compile time.** Dadas `fun log(a: Any)` y `fun log(s: String)`, llamar con una variable tipada `Any` que contiene un `String` elige la sobrecarga de `Any`. El overloading es [Polymorphism]({{ "/es/glosario/polymorphism/" | relative_url }}) *ad-hoc*; solo el overriding es dinámico.
- **El [`final`]({{ "/es/glosario/final/" | relative_url }})-por-defecto de Kotlin es una optimización de dispatch.** Los métodos no `open` son candidatos a desvirtualización por el [JIT Compiler]({{ "/es/glosario/jit-compilation/" | relative_url }}) y por [R8]({{ "/es/glosario/r8/" | relative_url }}) — el [Virtual Dispatch]({{ "/es/glosario/virtual-dispatch/" | relative_url }}) pasa a ser [Static Dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }}), y el cuerpo suele inlinearse. En [Hot Loops]({{ "/es/glosario/hot-loops/" | relative_url }}) esto es medible.
- **El dispatch de interfaces es el más lento de los tres.** La JVM usa `invokeinterface`, que no puede apoyarse en un slot fijo de la [vtable]({{ "/es/glosario/vtable/" | relative_url }}) como sí hace el [Virtual Dispatch]({{ "/es/glosario/virtual-dispatch/" | relative_url }}) de clases. Los JIT modernos lo mitigan con inline caches, así que rara vez vale diseñar alrededor de esto — pero vale saberlo cuando te lo preguntan.
- **Las [Inline Functions]({{ "/es/glosario/inline-functions/" | relative_url }}) no tienen dispatch en absoluto.** El cuerpo se copia dentro del [Call Site]({{ "/es/glosario/call-site/" | relative_url }}), que es exactamente por lo que [`reified`]({{ "/es/glosario/reified/" | relative_url }}) puede funcionar ahí.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
