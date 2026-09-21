---
layout: post
title: "Member Function"
date: 2026-09-21 12:00:00 +0000
categories: [en, glossary]
tags: [oop, dispatch, syntax]
lang: en
permalink: /en/glossary/member-function/
---

## The Theory (The What)

A **member function** is a function declared *inside* a class body, so it is part of the type itself and participates in [virtual dispatch]({{ "/en/glossary/virtual-dispatch/" | relative_url }}): a subclass can `override` it and the call resolves by the object's runtime type. That is the decisive contrast with an [extension function]({{ "/en/glossary/extension-functions/" | relative_url }}), which is compiled to a static method and resolved by the *declared* type. When both exist with the same signature, **the member always wins** — silently.

```kotlin
// Not found in FAS — standalone example
class Text(val value: String) {
    fun shout() = value.uppercase() + "!"     // member function
}
fun Text.shout() = "never called"             // extension: shadowed by the member

Text("hi").shout()   // "HI!" — the member wins
```

## The Senior Nuance

- **A library update can shadow your extension.** If a new version adds a member with the same signature, your extension silently stops being called and the behaviour changes without a compiler error. Unique names and restricted visibility limit the blast radius.
- **Members can touch [`private`]({{ "/en/glossary/private/" | relative_url }}) state; extensions cannot.** That is often the real reason a piece of logic belongs inside the class.
- **Members are mockable, extensions are not.** A member on an interface can be faked in a test; a static extension cannot.
- See [Extension Functions]({{ "/en/01-kotlin-core/extension-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
