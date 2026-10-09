---
layout: post
title: "Composition"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [compose, state-management]
lang: en
permalink: /en/glossary/composition/
---

## The Theory (The What)

The **Composition** is the tree [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) builds by running [`@Composable`]({{ "/en/glossary/composable/" | relative_url }}) functions. It records what each function emitted (the UI nodes), the values it remembered with [`remember`]({{ "/en/glossary/remember/" | relative_url }}), and which state it read. Compose keeps it in memory and updates it in place: [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}) changes the parts whose state changed, instead of building it again.

## The Senior Nuance

- **It is a description, not the screen.** The composition is the first of three phases (composition, layout, drawing). A change that only affects layout or drawing can skip this phase entirely.
- **Leaving the composition ends a composable's lifetime**: its remembered values are forgotten and its effects are cancelled or disposed.
- See [Recomposition & Stability]({{ "/en/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
