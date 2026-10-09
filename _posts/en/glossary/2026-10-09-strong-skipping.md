---
layout: post
title: "Strong Skipping"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [compose, performance, compiler]
lang: en
permalink: /en/glossary/strong-skipping/
---

## The Theory (The What)

**Strong skipping** is a Compose compiler mode, enabled by default since [Kotlin]({{ "/en/glossary/kotlin/" | relative_url }}) 2.0.20, that changes two rules. Composables with **[unstable]({{ "/en/glossary/stability/" | relative_url }})** parameters can be skipped: those parameters are compared by **instance** ([`===`]({{ "/en/glossary/referential-equality/" | relative_url }})), while [stable]({{ "/en/glossary/stability/" | relative_url }}) ones are still compared with [`equals`]({{ "/en/glossary/equals/" | relative_url }}). And [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) passed to composables are **remembered automatically**, so a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) no longer breaks [skipping]({{ "/en/glossary/skipping/" | relative_url }}) just because it is recreated.

## The Senior Nuance

- **The practical rule became identity.** Pass the same instance when nothing changed: keep unchanged lists when updating state with [`copy`]({{ "/en/glossary/copy/" | relative_url }}), and do not build collections in a composable's body without [`remember`]({{ "/en/glossary/remember/" | relative_url }}).
- **It does not make [stability]({{ "/en/glossary/stability/" | relative_url }}) irrelevant.** A [stable]({{ "/en/glossary/stability/" | relative_url }}) type can skip when its value is equal even if it is a new instance; an [unstable]({{ "/en/glossary/stability/" | relative_url }}) one needs the same instance.
- See [Recomposition & Stability]({{ "/en/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
