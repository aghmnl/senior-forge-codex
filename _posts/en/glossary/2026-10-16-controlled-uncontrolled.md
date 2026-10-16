---
layout: post
title: "Controlled & Uncontrolled"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, state-management, architecture]
lang: en
permalink: /en/glossary/controlled-uncontrolled/
---

## The Theory (The What)

A reusable component is **controlled** when its caller passes the current value and handles the change event, so the caller owns the state. It is **uncontrolled** when the component keeps its own state internally and the caller only sets an initial value. Many [design system]({{ "/en/glossary/design-system/" | relative_url }}) components support both, usually through an optional value parameter: `null` means "manage it yourself".

```kotlin
// Not found in FAS — standalone example
@Composable
fun Expandable(expanded: Boolean? = null, onExpandedChange: ((Boolean) -> Unit)? = null) {
    var internal by remember { mutableStateOf(false) }
    val isExpanded = expanded ?: internal
    // on toggle: if (expanded == null) internal = !isExpanded; onExpandedChange?.invoke(!isExpanded)
}
```

## The Senior Nuance

- **Controlled when the state must be persisted or coordinated** with other parts of the screen; uncontrolled when nobody else cares.
- **Never mix both silently.** If a value is passed, the component must not also change its internal state, or the two sources drift apart.
- See [State Hoisting]({{ "/en/03-jetpack-compose/state-hoisting/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
