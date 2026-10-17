---
layout: post
title: "Compose Phases"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout, performance]
lang: en
permalink: /en/glossary/compose-phases/
---

## The Theory (The What)

Compose renders a frame in three phases: **[composition]({{ "/en/glossary/composition/" | relative_url }})** (run composables and decide what to show), **layout** (measure and place each element) and **drawing** (render pixels). State read in a phase only reruns that phase and the ones after it, which is why lambda [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) like `offset { }`, `graphicsLayer { }` and `drawBehind { }` are cheaper for values that change every frame.

## The Senior Nuance

- **Defer state reads to the latest phase that needs them**: [composition]({{ "/en/glossary/composition/" | relative_url }}) is the most expensive to rerun, drawing the cheapest.
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
