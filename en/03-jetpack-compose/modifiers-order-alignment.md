---
layout: page
title: "Modifiers: Order & Alignment"
lang: en
permalink: /en/03-jetpack-compose/modifiers-order-alignment/
order: 4
---

## The Theory (The What)

A [`Modifier`]({{ "/en/glossary/modifier/" | relative_url }}) decorates a composable: it can size it, pad it, draw behind it, [clip]({{ "/en/glossary/clip/" | relative_url }}) it, make it [clickable]({{ "/en/glossary/clickable/" | relative_url }}) or position it. [Modifiers]({{ "/en/glossary/modifier/" | relative_url }}) are chained, `Modifier.padding(8.dp).background(Color.Red)`, and **the chain is ordered**. Each [modifier]({{ "/en/glossary/modifier/" | relative_url }}) wraps everything that comes after it, from the outside in, so changing the order changes the result:

- `Modifier.padding(16.dp).background(Color.Red)`: the [padding]({{ "/en/glossary/padding/" | relative_url }}) is applied first, outside, so it works like a margin and the red [background]({{ "/en/glossary/background/" | relative_url }}) is drawn only inside it.
- `Modifier.background(Color.Red).padding(16.dp)`: the [background]({{ "/en/glossary/background/" | relative_url }}) covers the whole area, and the [padding]({{ "/en/glossary/padding/" | relative_url }}) is inside it, between the red edge and the content.
- `Modifier.clickable { }.padding(16.dp)` makes the [padding]({{ "/en/glossary/padding/" | relative_url }}) part of the [touch area]({{ "/en/glossary/touch-target/" | relative_url }}); `Modifier.padding(16.dp).clickable { }` does not.
- `Modifier.clip(CircleShape).background(...)` clips what comes after it, so the [background]({{ "/en/glossary/background/" | relative_url }}) and the [ripple]({{ "/en/glossary/ripple/" | relative_url }}) of a later [`clickable`]({{ "/en/glossary/clickable/" | relative_url }}) are round; [`clip`]({{ "/en/glossary/clip/" | relative_url }}) placed after them does not affect them.

**Size [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) follow [constraints]({{ "/en/glossary/constraints/" | relative_url }}).** A parent passes [constraints]({{ "/en/glossary/constraints/" | relative_url }}) down to its child, and each size [modifier]({{ "/en/glossary/modifier/" | relative_url }}) narrows them for the [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) after it. In `Modifier.size(100.dp).size(50.dp)` the first one fixes the size to 100 dp and the second cannot change it: **the first size wins**. [`fillMaxWidth()`]({{ "/en/glossary/fill-max-width/" | relative_url }}) takes all the width allowed, [`wrapContentSize()`]({{ "/en/glossary/wrap-content-size/" | relative_url }}) lets the content be smaller and positions it, and [`requiredSize()`]({{ "/en/glossary/required-size/" | relative_url }}) ignores the incoming [constraints]({{ "/en/glossary/constraints/" | relative_url }}).

**Alignment is decided by the parent layout**, and each layout offers its own tools:

- **[`Row`]({{ "/en/glossary/row/" | relative_url }})** places children horizontally. [`horizontalArrangement`]({{ "/en/glossary/arrangement/" | relative_url }}) distributes them along the **[main axis]({{ "/en/glossary/main-axis-cross-axis/" | relative_url }})** ([`Arrangement.Start`]({{ "/en/glossary/arrangement/" | relative_url }}), `SpaceBetween`, [`spacedBy(8.dp)`]({{ "/en/glossary/arrangement/" | relative_url }})), and [`verticalAlignment`]({{ "/en/glossary/alignment/" | relative_url }}) positions them on the **[cross axis]({{ "/en/glossary/main-axis-cross-axis/" | relative_url }})** ([`Alignment.CenterVertically`]({{ "/en/glossary/alignment/" | relative_url }})).
- **[`Column`]({{ "/en/glossary/column/" | relative_url }})** is the same rotated: [`verticalArrangement`]({{ "/en/glossary/arrangement/" | relative_url }}) on the [main axis]({{ "/en/glossary/main-axis-cross-axis/" | relative_url }}), [`horizontalAlignment`]({{ "/en/glossary/alignment/" | relative_url }}) on the [cross axis]({{ "/en/glossary/main-axis-cross-axis/" | relative_url }}).
- **[`Box`]({{ "/en/glossary/box/" | relative_url }})** stacks children. [`contentAlignment`]({{ "/en/glossary/alignment/" | relative_url }}) positions all of them, and [`Modifier.align(Alignment.TopStart)`]({{ "/en/glossary/layout-scopes/" | relative_url }}) positions one.

[`Modifier.align`]({{ "/en/glossary/layout-scopes/" | relative_url }}) and [`Modifier.weight`]({{ "/en/glossary/weight/" | relative_url }}) only exist inside the scope of the right parent ([`BoxScope`]({{ "/en/glossary/layout-scopes/" | relative_url }}), [`RowScope`]({{ "/en/glossary/layout-scopes/" | relative_url }}), [`ColumnScope`]({{ "/en/glossary/layout-scopes/" | relative_url }})), so using them in the wrong place does not compile.

By convention, a composable that emits UI takes a **`modifier: Modifier = Modifier`** parameter, the first optional one, and applies it to its root element.

## The Senior Perspective (The Why)

- **Read the chain as layers, from the outside in.** The first [modifier]({{ "/en/glossary/modifier/" | relative_url }}) is the outermost layer; each one after it works inside the space the previous ones left. With that model, "[padding]({{ "/en/glossary/padding/" | relative_url }}) before [background]({{ "/en/glossary/background/" | relative_url }}) is a margin" and "[clickable]({{ "/en/glossary/clickable/" | relative_url }}) before [padding]({{ "/en/glossary/padding/" | relative_url }}) enlarges the [touch area]({{ "/en/glossary/touch-target/" | relative_url }})" stop being rules to memorize and become obvious. Most layout bugs in Compose are an ordering bug.
- **Order decides what the user can tap.** A small icon with [`clickable`]({{ "/en/glossary/clickable/" | relative_url }}) applied after `size(18.dp)` has an 18 dp [touch target]({{ "/en/glossary/touch-target/" | relative_url }}), below the 48 dp accessibility minimum. Placing [`clickable`]({{ "/en/glossary/clickable/" | relative_url }}) before the [padding]({{ "/en/glossary/padding/" | relative_url }}), or using [`minimumInteractiveComponentSize()`]({{ "/en/glossary/touch-target/" | relative_url }}), makes it reachable without changing how it looks. And [`clip`]({{ "/en/glossary/clip/" | relative_url }}) must come before [`clickable`]({{ "/en/glossary/clickable/" | relative_url }}) if the [ripple]({{ "/en/glossary/ripple/" | relative_url }}) has to follow the shape.
- **Apply the caller's [modifier]({{ "/en/glossary/modifier/" | relative_url }}) first, once, at the root.** Writing `modifier.fillMaxWidth()` puts the caller's [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) outside the component's own, so a size, [padding]({{ "/en/glossary/padding/" | relative_url }}) or [`align`]({{ "/en/glossary/layout-scopes/" | relative_url }}) from the caller wins. Applying [`modifier`]({{ "/en/glossary/modifier/" | relative_url }}) to an inner child, applying it twice, or chaining your own fixed size before it, breaks the caller's expectations: their [padding]({{ "/en/glossary/padding/" | relative_url }}) ends up in the wrong place, or their size is ignored.
- **Arrangement is about the group, alignment is about each child.** [`spacedBy(8.dp)`]({{ "/en/glossary/arrangement/" | relative_url }}) is better than adding [padding]({{ "/en/glossary/padding/" | relative_url }}) to every child, because the spacing belongs to the parent, not to the items. [`weight(1f)`]({{ "/en/glossary/weight/" | relative_url }}) takes the remaining space after the unweighted children are measured, which is the clean way to push an element to the end of a [`Row`]({{ "/en/glossary/row/" | relative_url }}).
- **Scope-restricted [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) are a safety net.** Because [`align`]({{ "/en/glossary/layout-scopes/" | relative_url }}) and [`weight`]({{ "/en/glossary/weight/" | relative_url }}) only exist in their scopes, the compiler prevents asking a parent for a positioning it does not support. When a [modifier]({{ "/en/glossary/modifier/" | relative_url }}) "does not exist", the question is usually which parent should own that decision.
- **Some [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) have a deferred, [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) form for performance.** [`offset { }`]({{ "/en/glossary/modifier-offset/" | relative_url }}), [`graphicsLayer { }`]({{ "/en/glossary/graphics-layer/" | relative_url }}) and [`drawBehind { }`]({{ "/en/glossary/draw-behind/" | relative_url }}) read state in the layout or [drawing phase]({{ "/en/glossary/compose-phases/" | relative_url }}) instead of [composition]({{ "/en/glossary/composition/" | relative_url }}), so a value that changes every frame (scroll, drag, animation) does not recompose the composable. [Modifiers]({{ "/en/glossary/modifier/" | relative_url }}) that take plain values read them during [composition]({{ "/en/glossary/composition/" | relative_url }}).

## Code in Action

```kotlin
// From FollowApp Suite — StateChip.kt
// The remove button of a chip: an 18 dp circle. clip comes before clickable, so
// the ripple of the click is clipped to the circle instead of a square.
Box(
    modifier = Modifier
        .size(18.dp)
        .clip(CircleShape)
        .clickable { onRemove() },
    contentAlignment = Alignment.Center
) {
    Icon(imageVector = Icons.Default.Close, contentDescription = removeContentDescription, /* ... */)
}

// From FollowApp Suite — CollapsibleGroupCard.kt
// A header chip straddling the top border of a card. The caller's modifier is
// applied first, at the root. The card surface is pushed down by half the chip
// height with padding, and the chip is aligned to the top start of the Box, so
// it sits half in, half out of the card.
Box(modifier = modifier.fillMaxWidth()) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = chipHalfHeight),
        shape = RoundedCornerShape(12.dp),
        color = containerColor,
    ) { /* content */ }

    Box(
        modifier = Modifier
            .align(Alignment.TopStart)
            .padding(start = 16.dp)
    ) {
        headerChip()
    }
}

// From FollowApp Suite — SelectionFloatingToolbar.kt
// Arrangement on the main axis (8 dp between buttons) and alignment on the cross
// axis (vertically centered), both decided by the Row, not by each button.
Surface(
    modifier = modifier,
    shape = RoundedCornerShape(28.dp),
    color = MaterialTheme.colorScheme.surfaceContainerHigh,
    shadowElevation = 6.dp
) {
    Row(
        modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        actions.forEach { action -> IconButton(onClick = action.onClick) { /* ... */ } }
    }
}

// Not found in FAS — standalone example
// Same modifiers, different order, different result.
Text("A", Modifier.padding(16.dp).background(Color.Red))   // margin, then red
Text("B", Modifier.background(Color.Red).padding(16.dp))   // red, with padding inside
Box(Modifier.size(100.dp).size(50.dp))                     // 100 dp: the first size wins
```

## The Interview (The Hot Seat)

**Question**: Why does the order of [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) matter in Compose? Give an example where changing it changes the result.

**Senior Answer**: Because a [modifier]({{ "/en/glossary/modifier/" | relative_url }}) chain is not a set of properties, it is a sequence of wrappers: each [modifier]({{ "/en/glossary/modifier/" | relative_url }}) wraps everything that comes after it, from the outside in. So the first [modifier]({{ "/en/glossary/modifier/" | relative_url }}) is the outermost layer, and each later one works inside the space the previous ones left. The classic example is [padding]({{ "/en/glossary/padding/" | relative_url }}) and [background]({{ "/en/glossary/background/" | relative_url }}). `padding(16.dp).background(Red)` applies the [padding]({{ "/en/glossary/padding/" | relative_url }}) outside, so it behaves like a margin and the red area is smaller; `background(Red).padding(16.dp)` paints the full area red and the [padding]({{ "/en/glossary/padding/" | relative_url }}) ends up inside it. The same logic decides the [touch area]({{ "/en/glossary/touch-target/" | relative_url }}): [`clickable`]({{ "/en/glossary/clickable/" | relative_url }}) before [`padding`]({{ "/en/glossary/padding/" | relative_url }}) makes the [padding]({{ "/en/glossary/padding/" | relative_url }}) tappable, after it does not, which matters for small icons and the 48 dp minimum [touch target]({{ "/en/glossary/touch-target/" | relative_url }}). And [`clip`]({{ "/en/glossary/clip/" | relative_url }}) clips only what comes after it, so it has to go before [`background`]({{ "/en/glossary/background/" | relative_url }}) and [`clickable`]({{ "/en/glossary/clickable/" | relative_url }}) if the shape and the [ripple]({{ "/en/glossary/ripple/" | relative_url }}) must be round. Size [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) work through [constraints]({{ "/en/glossary/constraints/" | relative_url }}) that flow down the chain, so the first size wins: `size(100.dp).size(50.dp)` is 100 dp. When a layout looks wrong in Compose, the first thing I check is the order of the chain.

**Question**: You are building a reusable card component. How do you handle its [`modifier`]({{ "/en/glossary/modifier/" | relative_url }}) parameter, and how do you align its content?

**Senior Answer**: The component takes `modifier: Modifier = Modifier` as its first optional parameter and applies it once, to the root element, before its own [modifiers]({{ "/en/glossary/modifier/" | relative_url }}): `Box(modifier = modifier.fillMaxWidth())`. That puts the caller's [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) on the outside, so a [padding]({{ "/en/glossary/padding/" | relative_url }}), a size or an [`align`]({{ "/en/glossary/layout-scopes/" | relative_url }}) from the caller is respected. If I applied it to an inner child, or put my own fixed size before it, the caller's [padding]({{ "/en/glossary/padding/" | relative_url }}) would land in the wrong place or their size would be ignored, and the component would behave differently from every other composable. For the content, alignment belongs to the parent layout. In a [`Row`]({{ "/en/glossary/row/" | relative_url }}) I use [`horizontalArrangement`]({{ "/en/glossary/arrangement/" | relative_url }}), for example [`spacedBy`]({{ "/en/glossary/arrangement/" | relative_url }}), to distribute the children on the [main axis]({{ "/en/glossary/main-axis-cross-axis/" | relative_url }}), and [`verticalAlignment`]({{ "/en/glossary/alignment/" | relative_url }}) to center them on the [cross axis]({{ "/en/glossary/main-axis-cross-axis/" | relative_url }}), instead of adding [padding]({{ "/en/glossary/padding/" | relative_url }}) to each child. In a [`Box`]({{ "/en/glossary/box/" | relative_url }}) I use [`contentAlignment`]({{ "/en/glossary/alignment/" | relative_url }}) for all children or [`Modifier.align`]({{ "/en/glossary/layout-scopes/" | relative_url }}) for one, and [`weight`]({{ "/en/glossary/weight/" | relative_url }}) in a [`Row`]({{ "/en/glossary/row/" | relative_url }}) or [`Column`]({{ "/en/glossary/column/" | relative_url }}) to give the remaining space to one element. Those positioning [modifiers]({{ "/en/glossary/modifier/" | relative_url }}) only exist in their parent's scope, so the compiler stops me from using them where they make no sense.

---

[Back to Chapters]({{ "/" | relative_url }})
