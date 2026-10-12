---
layout: post
title: "rememberSaveable"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [compose, state-management, lifecycle]
lang: en
permalink: /en/glossary/remember-saveable/
---

## The Theory (The What)

**`rememberSaveable { }`** works like [`remember`]({{ "/en/glossary/remember/" | relative_url }}), keeping a value across recompositions, and also writes it into the [saved instance state]({{ "/en/glossary/saved-instance-state/" | relative_url }}). When the [Activity]({{ "/en/glossary/activity/" | relative_url }}) is recreated, after a [configuration change]({{ "/en/glossary/configuration-change/" | relative_url }}) or after [process death]({{ "/en/glossary/process-death/" | relative_url }}), the value is restored instead of computed again. The value must be a type a [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}) can hold ([primitives]({{ "/en/glossary/primitives/" | relative_url }}), [`String`]({{ "/en/glossary/string/" | relative_url }}), [`Parcelable`]({{ "/en/glossary/parcelable/" | relative_url }}), [`Serializable`]({{ "/en/glossary/serializable/" | relative_url }})) or come with a [`Saver`]({{ "/en/glossary/saver/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
var query by rememberSaveable { mutableStateOf("") }
```

## The Senior Nuance

- **For state the user created**: typed text, a selected tab, an expanded section. Caches and measurements belong in [`remember`]({{ "/en/glossary/remember/" | relative_url }}).
- **Keep it small.** The [saved state]({{ "/en/glossary/saved-instance-state/" | relative_url }}) has a size limit; store an id, not a list.
- **It also restores state in lazy lists and on the navigation back stack**, where items and screens leave the [composition]({{ "/en/glossary/composition/" | relative_url }}) and come back.
- See [remember & rememberSaveable]({{ "/en/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
