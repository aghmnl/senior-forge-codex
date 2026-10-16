---
layout: post
title: "Stateful & Stateless"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, state-management]
lang: en
permalink: /en/glossary/stateful-stateless/
---

## The Theory (The What)

A **stateful** composable creates and keeps its own state with [`remember`]({{ "/en/glossary/remember/" | relative_url }}): it works on its own, but its caller cannot read or change that state. A **stateless** composable receives its state as parameters and reports changes through event [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}): it only shows what it is given. State hoisting turns the first into the second.

```kotlin
// Not found in FAS — standalone example
@Composable fun Counter() { var n by remember { mutableStateOf(0) }; Button({ n++ }) { Text("$n") } }   // stateful
@Composable fun Counter(n: Int, onIncrement: () -> Unit) { Button(onIncrement) { Text("$n") } }         // stateless
```

## The Senior Nuance

- **Stateless is reusable and testable**: it can be shown in a [Preview]({{ "/en/glossary/preview/" | relative_url }}) with any value and tested by checking the events it emits.
- **Stateful is convenient**, so libraries often offer both: a stateless version and a stateful wrapper with sensible defaults.
- See [State Hoisting]({{ "/en/03-jetpack-compose/state-hoisting/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
