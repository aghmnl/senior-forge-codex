---
layout: post
title: "Compose Compiler Reports"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [compose, compiler, performance]
lang: en
permalink: /en/glossary/compose-compiler-reports/
---

## The Theory (The What)

The **Compose compiler reports** are files the Compose compiler can generate at build time. They [list]({{ "/en/glossary/list/" | relative_url }}) every composable with whether it is **skippable** and **restartable**, and every class and parameter with the [stability]({{ "/en/glossary/stability/" | relative_url }}) the compiler inferred ([`stable`]({{ "/en/glossary/stability/" | relative_url }}), [`unstable`]({{ "/en/glossary/stability/" | relative_url }}) or `runtime`). They are enabled in Gradle through the Compose compiler plugin's `reportsDestination` and `metricsDestination` options.

## The Senior Nuance

- **They answer "why does this not skip?"** An [`unstable`]({{ "/en/glossary/stability/" | relative_url }}) parameter in the report is the usual reason.
- **Check them before adding [`@Immutable`]({{ "/en/glossary/immutable-annotation/" | relative_url }}) or [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}).** The report shows what the compiler actually inferred, so you annotate only what really needs it.
- See [Recomposition & Stability]({{ "/en/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
