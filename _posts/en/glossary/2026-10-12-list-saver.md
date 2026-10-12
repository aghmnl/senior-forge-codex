---
layout: post
title: "listSaver"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [compose, serialization]
lang: en
permalink: /en/glossary/list-saver/
---

## The Theory (The What)

**`listSaver`** builds a [`Saver`]({{ "/en/glossary/saver/" | relative_url }}) that stores a value as a **list** of saveable values. `save` returns the list, and `restore` receives it and rebuilds the value by position.

```kotlin
// Not found in FAS — standalone example
val DateRangeSaver = listSaver<DateRange, String>(
    save = { listOf(it.start.toString(), it.end.toString()) },
    restore = { DateRange(LocalDate.parse(it[0]), LocalDate.parse(it[1])) }
)
```

## The Senior Nuance

- **Compact but positional.** Adding or reordering fields means updating `save` and `restore` together; [`mapSaver`]({{ "/en/glossary/map-saver/" | relative_url }}) is clearer when there are many fields.
- See [remember & rememberSaveable]({{ "/en/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
