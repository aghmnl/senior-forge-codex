---
layout: post
title: "Stability"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [compose, performance, immutability]
lang: en
permalink: /en/glossary/stability/
---

## The Theory (The What)

In [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}), a type is **stable** when Compose can trust it during [skipping]({{ "/en/glossary/skipping/" | relative_url }}): [`equals`]({{ "/en/glossary/equals/" | relative_url }}) always gives the same result for the same two instances, any change to a public property notifies the [composition]({{ "/en/glossary/composition/" | relative_url }}) (it is backed by [`MutableState`]({{ "/en/glossary/mutable-state/" | relative_url }})), and all its public properties are stable too. [Primitives]({{ "/en/glossary/primitives/" | relative_url }}), [`String`]({{ "/en/glossary/string/" | relative_url }}), [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}), [`MutableState`]({{ "/en/glossary/mutable-state/" | relative_url }}) and data classes of [`val`]({{ "/en/glossary/val/" | relative_url }})s of stable types are stable. A type is **unstable** when the compiler cannot prove it: a class with a [`var`]({{ "/en/glossary/var/" | relative_url }}), a class from a module compiled without the Compose compiler, or the [`List`]({{ "/en/glossary/list/" | relative_url }}), [`Set`]({{ "/en/glossary/sets/" | relative_url }}) and `Map` interfaces, which may hide a mutable instance.

## The Senior Nuance

- **Unstable is not "broken".** With [strong skipping]({{ "/en/glossary/strong-skipping/" | relative_url }}), unstable parameters are compared by instance, so they still skip when the same instance is passed.
- **The [Compose compiler reports]({{ "/en/glossary/compose-compiler-reports/" | relative_url }}) tell you** which parameters the compiler inferred as unstable, which is the first thing to check before annotating anything.
- **Fixes, in order of preference:** real immutability, immutable collections, a stability configuration file, and only then [`@Immutable`]({{ "/en/glossary/immutable-annotation/" | relative_url }}) or [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}).
- See [Recomposition & Stability]({{ "/en/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
