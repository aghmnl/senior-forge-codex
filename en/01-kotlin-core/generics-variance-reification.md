---
layout: page
title: Generics, Variance & Reification
lang: en
permalink: /en/01-kotlin-core/generics-variance-reification/
order: 11
---

## The Theory (The What)

Generics allow classes and functions to work with different types while maintaining type safety. However, due to **Type Erasure**, generic type information is removed at runtime. To manage how subtyping works with generics, Kotlin uses **Variance**:
- **Covariance (`out`)**: Allows a `Box<String>` to be treated as a `Box<Any>`. The type can only be *produced* (returned).
- **Contravariance (`in`)**: Allows a `Box<Any>` to be treated as a `Box<String>`. The type can only be *consumed* (passed as argument).
- **Reification (`reified`)**: A Kotlin-specific feature that, combined with `inline` functions, allows accessing the generic type `T` at runtime.

## The Senior Perspective (The Why)

For a Senior Developer, variance is about **API flexibility** and **type-system integrity**.

- **PECS Rule**: Following the "Producer-Extends, Consumer-Super" (PECS) mnemonic from Java, Kotlin simplifies this with `out` (Producer) and `in` (Consumer). Using them correctly prevents "Type mismatch" errors in complex architectures like Repository patterns or Event Busses.
- **Bypassing Erasure**: Because the JVM erases generic types, you cannot normally do `if (T is String)`. Reification is the "Senior escape hatch" that enables type-checks and reflections without passing a `Class<T>` object manually.
- **Star-Projections**: Using `<*>` is safer than raw types, signaling that you don't care about the specific type but still want to maintain basic type safety constraints.

## Code in Action
```kotlin
// Senior approach: Variance for flexibility and Reification for type-safety
sealed interface Resource {
    data object Empty : Resource
    data class Content(val value: String) : Resource
}

// Covariant Producer: We only return T
interface Producer<out T> {
    fun produce(): T
}

// Contravariant Consumer: We only accept T
interface Consumer<in T> {
    fun consume(item: T)
}

// Using reified to avoid passing .class or KClass
inline fun <reified T> Any.isType(): Boolean {
    return this is T
}

fun example() {
    val stringProducer: Producer<String> = object : Producer<String> {
        override fun produce() = "Senior Forge"
    }
    
    // Covariance in action: Producer<String> is a subtype of Producer<Any>
    val anyProducer: Producer<Any> = stringProducer
    
    val myResource: Any = Resource.Empty
    if (myResource.isType<Resource.Empty>()) {
        println("Reified check: It is Empty")
    }
}
```

## The Interview (The Hot Seat)

**Question**: Why can't we use reified types in regular functions, and what happens to them at the bytecode level?

**Senior Answer**: Reification requires the inline keyword because the compiler needs to replace the function call with the actual code where the generic T is used. At the bytecode level, the compiler replaces every occurrence of T with the specific class used at the call site. Regular functions cannot be reified because they are compiled into a single method signature where the type is erased to Object to maintain JVM compatibility; they lack the "copy-paste" mechanism that inline provides to preserve the specific type information.

---

[Back to Chapters]({{ "/" | relative_url }})
