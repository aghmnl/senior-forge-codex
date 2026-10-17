---
layout: post
title: "Touch Target"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout, design-principles]
lang: en
permalink: /en/glossary/touch-target/
---

## The Theory (The What)

The **touch target** is the area of the screen that responds to a tap. Android's accessibility guidelines ask for at least **48 x 48 dp**, even if the visible element is smaller. `Modifier.minimumInteractiveComponentSize()` enlarges the touch area to that minimum without changing how the element looks.

```kotlin
// Not found in FAS — standalone example
Icon(Icons.Default.Close, null, Modifier.minimumInteractiveComponentSize().clickable { onClose() })
```

## The Senior Nuance

- **A small icon is not a small target**: an 18 dp icon can and should have a 48 dp target.
- **Material components already do it**; custom [clickable]({{ "/en/glossary/clickable/" | relative_url }}) elements must do it themselves.
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
