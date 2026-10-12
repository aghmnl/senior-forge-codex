---
layout: post
title: "LazyColumn"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [compose, performance]
lang: en
permalink: /en/glossary/lazy-column/
---

## The Theory (The What)

**`LazyColumn`** is Compose's vertical list that composes **only the items that are visible**, plus a small margin. Items that scroll off screen leave the [composition]({{ "/en/glossary/composition/" | relative_url }}), and new ones are composed as they appear, so a list of thousands of items costs about the same as one screenful. `LazyRow` is the horizontal version.

```kotlin
// Not found in FAS — standalone example
LazyColumn {
    items(tasks, key = { it.id }) { task -> TaskRow(task) }
}
```

## The Senior Nuance

- **Leaving the [composition]({{ "/en/glossary/composition/" | relative_url }}) forgets [`remember`]({{ "/en/glossary/remember/" | relative_url }}) state.** An item scrolled away and back starts again, unless its state uses [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}) or lives outside the item.
- **Stable keys matter**: with `key`, Compose keeps each item's state attached to the right item when the list changes.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
