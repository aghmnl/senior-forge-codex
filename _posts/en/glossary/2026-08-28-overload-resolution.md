---
layout: post
title: "Overload Resolution"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/overload-resolution/
---

## The Theory (The What)

**Overload resolution** is the [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) process by which the compiler determines which function to call when multiple functions share the same name but differ in parameter types, number of parameters, or receiver type. The compiler evaluates all candidates, applies type matching and [type inference]({{ "/en/glossary/type-inference/" | relative_url }}), and selects the most specific match. If no single candidate is most specific, the call is ambiguous and the build fails.

## The Senior Nuance

- Overload resolution is purely a compile-time decision. The [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) contains a direct call to the resolved function — there is no [runtime]({{ "/en/glossary/runtime/" | relative_url }}) dispatch or lookup involved (unlike virtual method dispatch, which *is* a runtime mechanism).
- [Extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}) participate in overload resolution, but member functions always win over extensions when signatures match. This is a deliberate design choice: adding an extension cannot silently override a member.
- Default parameters reduce the need for overloads in Kotlin. Where Java requires multiple constructor/method overloads for optional parameters, Kotlin uses `fun f(x: Int, y: String = "")` — one function instead of two.
- `@JvmOverloads` generates actual JVM overloads from default-parameter functions for Java interop. The compiler creates N+1 overloads (where N is the number of defaulted parameters), each calling the next.
- Operator overloading (`operator fun plus(other: T)`) follows the same resolution rules — the compiler resolves `a + b` to `a.plus(b)` at compile time based on the declared types.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
