---
layout: post
title: "Layout Inspector"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [compose, performance, testing]
lang: en
permalink: /en/glossary/layout-inspector/
---

## The Theory (The What)

The **Layout Inspector** is an Android Studio tool that shows the UI hierarchy of a running app. For [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) it shows the composable tree, the parameters of each composable and, when enabled, **[recomposition]({{ "/en/glossary/recomposition/" | relative_url }}) counts**: how many times each composable was recomposed and how many times it was skipped.

## The Senior Nuance

- **It is the first tool for [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}) problems.** A count that grows on every keystroke or every frame points to the composable to investigate.
- **Combine it with the [Compose compiler reports]({{ "/en/glossary/compose-compiler-reports/" | relative_url }})**: the inspector shows that something recomposes, the reports explain why it cannot skip.
- See [Recomposition & Stability]({{ "/en/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
