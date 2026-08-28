---
layout: post
title: "Extension"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/extension/
---

## The Theory (The What)

An **extension** is any mechanism that adds new capabilities to an existing type without modifying its source code. In Kotlin, the primary tool is the [extension function]({{ "/en/glossary/extension-functions/" | relative_url }}), but the concept also includes extension properties, extension functions on companion objects, and lambda with [receiver types]({{ "/en/glossary/receiver-type/" | relative_url }}). The Open/Closed Principle ("open for extension, closed for modification") is the design rationale behind all of these.

```kotlin
// From FollowApp Suite — BillingConnector.kt
// Extending Google Play Billing's Purchase class without modifying it
private fun Purchase.isOwnedProduct(): Boolean =
    productId in products && purchaseState == Purchase.PurchaseState.PURCHASED
```

```kotlin
// From FollowApp Suite — DragToReorder.kt
// Extending Compose's LazyListState with custom scroll-anchoring logic
fun LazyListState.reanchorAfterMove(targetIndex: Int) {
    val visible = layoutInfo.visibleItemsInfo
    val first = visible.firstOrNull() ?: return
    if (targetIndex > first.index + 1) return
    val target = visible.firstOrNull { it.index == targetIndex } ?: return
    val newOffset = firstVisibleItemScrollOffset + first.offset - target.offset
    if (newOffset >= 0) requestScrollToItem(targetIndex, newOffset)
}
```

## The Senior Nuance

- Extensions vs. [Decorator]({{ "/en/glossary/decorator/" | relative_url }}): extensions add new functions but cannot intercept existing ones. A Decorator wraps the object and can modify *any* behavior. Choose extensions for adding utilities; choose Decorator for modifying or observing existing behavior.
- Extensions vs. [Inheritance]({{ "/en/glossary/inheritance/" | relative_url }}): extensions do not create a subtype relationship. They cannot access private members. They are resolved [statically]({{ "/en/glossary/static-dispatch/" | relative_url }}), not through [polymorphism]({{ "/en/glossary/polymorphism/" | relative_url }}). This makes them safer (no fragile base class problem) but less powerful (no virtual dispatch).
- The FAS examples show the sweet spot: adding domain-specific behavior (`isOwnedProduct`, `reanchorAfterMove`) to library types (`Purchase`, `LazyListState`) that you cannot modify. This keeps domain logic close to where it's used, without polluting the library's API.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
