---
layout: post
title: "@Parcelize"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [android-framework, serialization, compiler]
lang: en
permalink: /en/glossary/parcelize/
---

## The Theory (The What)

**`@Parcelize`** is an annotation from the `kotlin-parcelize` Gradle plugin that **generates the [`Parcelable`]({{ "/en/glossary/parcelable/" | relative_url }}) implementation** of a class from its primary constructor properties. The class only has to implement [`Parcelable`]({{ "/en/glossary/parcelable/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
@Parcelize
data class DateRange(val start: LocalDate, val end: LocalDate) : Parcelable
```

## The Senior Nuance

- **Every property must be [parcelable]({{ "/en/glossary/parcelable/" | relative_url }})** (or have a custom `Parceler`); the plugin reports an error at compile time otherwise.
- **The simplest way to make your own type saveable with [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }})**, with no [`Saver`]({{ "/en/glossary/saver/" | relative_url }}) needed.
- See [remember & rememberSaveable]({{ "/en/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
