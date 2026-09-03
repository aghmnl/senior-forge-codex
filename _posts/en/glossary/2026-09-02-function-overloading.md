---
layout: post
title: "Function Overloading"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/function-overloading/
---

## The Theory (The What)

**Function overloading** (ad-hoc [polymorphism]({{ "/en/glossary/polymorphism/" | relative_url }})) is the ability to define multiple functions with the same name but different parameter lists. The compiler selects which overload to call based on the argument types and count at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) — this is [static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }}), not [virtual dispatch]({{ "/en/glossary/virtual-dispatch/" | relative_url }}). The return type alone does not differentiate overloads; the parameter signature must differ.

In Kotlin, default parameter values often eliminate the need for overloads that only vary in arity. The [`@JvmOverloads`]({{ "/en/glossary/jvm-static/" | relative_url }}) annotation generates the missing overloads in [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) for Java interop.

```kotlin
// Not found in FAS — standalone example
fun format(value: Int): String = value.toString()
fun format(value: Double, decimals: Int = 2): String =
    "%.${decimals}f".format(value)
fun format(value: String): String = "\"$value\""

format(42)          // calls format(Int)
format(3.14159, 3)  // calls format(Double, Int)
format("hello")     // calls format(String)
```

## The Senior Nuance

- The compiler resolves overloads via [overload resolution]({{ "/en/glossary/overload-resolution/" | relative_url }}) — a set of rules that ranks candidates by specificity. When two overloads are equally specific, the call is ambiguous and fails at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}). Knowing these rules is essential for designing APIs that don't surprise callers.
- Kotlin's default parameters (`fun greet(name: String, greeting: String = "Hello")`) are preferred over overloads for optional arguments. They reduce boilerplate and are self-documenting. Use true overloading only when parameter *types* differ, not just when you need optional arguments.
- [Extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}) can be overloaded by [receiver type]({{ "/en/glossary/receiver-type/" | relative_url }}): `fun Int.display()` and `fun String.display()` are valid overloads. But remember: extension function dispatch is [static]({{ "/en/glossary/static-dispatch/" | relative_url }}), so the *declared* type of the receiver determines which overload runs.
- [Operator overloading]({{ "/en/glossary/operator-overloading/" | relative_url }}) is a specialized form of function overloading where the function name maps to a Kotlin operator (`plus`, `invoke`, `contains`). The rules are the same — the compiler resolves statically based on parameter types.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
