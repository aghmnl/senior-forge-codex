---
layout: post
title: "clickable"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout, callbacks]
lang: en
permalink: /en/glossary/clickable/
---

## The Theory (The What)

**`Modifier.clickable { }`** makes an element respond to taps, shows the press indication (the [ripple]({{ "/en/glossary/ripple/" | relative_url }})), and exposes it to accessibility services as a button. Its [touch area]({{ "/en/glossary/touch-target/" | relative_url }}) is the space it wraps, so its position in the chain decides how much of the element can be tapped.

```kotlin
// Not found in FAS — standalone example
Icon(Icons.Default.Close, null, Modifier.clickable { onClose() }.padding(12.dp))   // padding is tappable
```

## The Senior Nuance

- **Before a padding, the padding is tappable; after it, it is not.**
- **Put [`clip`]({{ "/en/glossary/clip/" | relative_url }}) before it** so the [ripple]({{ "/en/glossary/ripple/" | relative_url }}) follows the shape.
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
