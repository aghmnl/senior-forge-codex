---
layout: post
title: "Layout Scopes (BoxScope, RowScope, ColumnScope)"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout, dsl]
lang: en
permalink: /en/glossary/layout-scopes/
---

## The Theory (The What)

**`BoxScope`**, **`RowScope`** and **`ColumnScope`** are the receivers of the content lambdas of [`Box`]({{ "/en/glossary/box/" | relative_url }}), [`Row`]({{ "/en/glossary/row/" | relative_url }}) and [`Column`]({{ "/en/glossary/column/" | relative_url }}). They provide [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) that only make sense inside that parent, such as `align` and [`weight`]({{ "/en/glossary/weight/" | relative_url }}), so using them anywhere else does not compile.

```kotlin
// Not found in FAS — standalone example
Box { Text("Hi", Modifier.align(Alignment.Center)) }   // align exists only in BoxScope
```

## The Senior Nuance

- **Scope-restricted [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) are a compile-time safety net**: the parent owns positioning, so only the right parent can be asked for it.
- **[`@LayoutScopeMarker`]({{ "/en/glossary/layout-scope-marker/" | relative_url }})** keeps an outer scope's [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) from leaking into nested layouts.
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
