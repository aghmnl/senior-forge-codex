---
layout: post
title: "TextField"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, state-management]
lang: en
permalink: /en/glossary/text-field/
---

## The Theory (The What)

**`TextField`** is Material's text input composable. It is [stateless]({{ "/en/glossary/stateful-stateless/" | relative_url }}): it shows the `value` it receives and calls `onValueChange` with the new text on every keystroke; the caller has to store that text and pass it back, or the field will not change. `OutlinedTextField` is the outlined variant.

```kotlin
// Not found in FAS — standalone example
var query by rememberSaveable { mutableStateOf("") }
TextField(value = query, onValueChange = { query = it })
```

## The Senior Nuance

- **Forgetting to update the state freezes the field**: typing calls `onValueChange`, but the text shown is still the old `value`.
- **Keep the text in sync without delay.** Updating it asynchronously (after a suspend call) makes the cursor jump; store it synchronously and do the slow work separately.
- See [State Hoisting]({{ "/en/03-jetpack-compose/state-hoisting/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
