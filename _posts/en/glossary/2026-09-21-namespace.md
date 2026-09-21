---
layout: post
title: "Namespace"
date: 2026-09-21 12:00:00 +0000
categories: [en, glossary]
tags: [scoping, design-principles]
lang: en
permalink: /en/glossary/namespace/
---

## The Theory (The What)

A **namespace** is the set of names visible at a given point in the code — in Kotlin, what a package plus its imports put within reach. [Extension Functions]({{ "/en/01-kotlin-core/extension-functions/" | relative_url }}) widen it in a particular way: a public top-level extension on `String` appears in the autocomplete of *every* `String` in every module that imports it. Keeping that set small is what "namespace pollution" is about.

```kotlin
// Not found in FAS — standalone example
// Pollutes: every String in the project now offers .toOrderId()
fun String.toOrderId(): OrderId = OrderId(this)

// Scoped: only this module sees it
internal fun String.toOrderId(): OrderId = OrderId(this)
```

## The Senior Nuance

- **Autocomplete is a shared resource.** Fifty domain-specific extensions on `String` make the IDE's suggestion list useless for everyone, which is a real cost even though nothing breaks.
- **The fix is visibility, not discipline.** [`private`]({{ "/en/glossary/private/" | relative_url }}) in the file, [`internal`]({{ "/en/glossary/internal/" | relative_url }}) in the module; reserve public top-level for genuinely universal helpers.
- **It is also a coupling signal.** If a feature's extension is visible project-wide, other features will use it, and the module boundary erodes.
- See [Extension Functions]({{ "/en/01-kotlin-core/extension-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
