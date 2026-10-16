---
layout: page
title: "State Hoisting"
lang: en
permalink: /en/03-jetpack-compose/state-hoisting/
order: 3
---

## The Theory (The What)

A composable that creates and keeps its own state with [`remember`]({{ "/en/glossary/remember/" | relative_url }}) is **[stateful]({{ "/en/glossary/stateful-stateless/" | relative_url }})**: it works on its own, but whoever calls it cannot read that state or change it. A composable that receives its state as parameters is **[stateless]({{ "/en/glossary/stateful-stateless/" | relative_url }})**: it only shows what it is given and reports what the user does.

**State hoisting** is the pattern of turning a [stateful]({{ "/en/glossary/stateful-stateless/" | relative_url }}) composable into a [stateless]({{ "/en/glossary/stateful-stateless/" | relative_url }}) one by moving its state up to the caller. The state is replaced by two parameters:

- **`value: T`**, the current value to display, and
- **`onValueChange: (T) -> Unit`**, an event the composable calls when the user wants to change it.

The composable no longer decides anything: it shows `value` and calls `onValueChange`. The caller owns the state, decides what to do with each event, and passes the new value back down. This is **[unidirectional data flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }})** at the scale of a single component: **state flows down, events flow up**. Material's own components follow it: [`TextField(value, onValueChange)`]({{ "/en/glossary/text-field/" | relative_url }}), [`Checkbox(checked, onCheckedChange)`]({{ "/en/glossary/checkbox/" | relative_url }}), [`Switch(checked, onCheckedChange)`]({{ "/en/glossary/switch/" | relative_url }}).

How high to hoist is a decision. The rule from the Compose guidance is to hoist state **at least to the lowest common ancestor of every composable that reads it**, and **as high as the lowest one that writes it**, but no higher than needed. The three usual destinations are:

- **The composable itself**, with [`remember`]({{ "/en/glossary/remember/" | relative_url }}), when nobody else needs the state (simple UI element state).
- **A plain [state holder]({{ "/en/glossary/state-holder/" | relative_url }}) class**, created with a `rememberXState()` function, when the UI logic is complex enough to deserve its own class, like [`LazyListState`]({{ "/en/glossary/lazy-list-state/" | relative_url }}).
- **The [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }})**, when the state comes from business logic, has to survive [configuration changes]({{ "/en/glossary/configuration-change/" | relative_url }}), or is read by distant parts of the screen.

## The Senior Perspective (The Why)

- **Hoisting buys [single source of truth]({{ "/en/glossary/single-source-of-truth/" | relative_url }}).** If two composables keep their own copy of the same value, they drift apart. Hoisted to their common ancestor, there is one owner and everyone reads the same value. That also makes the state shareable: a search query hoisted out of the search bar can drive both the bar and the list.
- **[Stateless]({{ "/en/glossary/stateful-stateless/" | relative_url }}) composables are the reusable, testable ones.** A [stateless]({{ "/en/glossary/stateful-stateless/" | relative_url }}) component can be used in any screen, shown in a [Preview]({{ "/en/glossary/preview/" | relative_url }}) with any value, and tested by passing values and checking which events it emits, with no [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) and no fake repositories.
- **Do not hoist by reflex.** Hoisting everything to the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) turns UI details (whether a dropdown is open, the scroll position, an animation) into business state, makes the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) huge, and recomposes more than necessary. UI element state that nobody else reads belongs close to where it is used. The question is "who needs to read or change this?", not "should everything go to the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }})?".
- **Offer both modes in reusable components.** A [design system]({{ "/en/glossary/design-system/" | relative_url }}) component often supports being **[uncontrolled]({{ "/en/glossary/controlled-uncontrolled/" | relative_url }})**, managing its own state with sensible defaults, and **[controlled]({{ "/en/glossary/controlled-uncontrolled/" | relative_url }})**, when the caller passes the value and the event because it needs to persist or coordinate it. The usual shape is an optional `value` parameter: when it is null, the component uses its internal [`remember`]({{ "/en/glossary/remember/" | relative_url }}); when it is not, the caller is in charge.
- **Pass values and [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}), not ViewModels or [`MutableState`]({{ "/en/glossary/mutable-state/" | relative_url }}).** A child that receives the whole [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) can call anything on it, cannot be previewed, and depends on a class it does not need. A child that receives a [`MutableState`]({{ "/en/glossary/mutable-state/" | relative_url }}) can write it directly, which creates a second writer and breaks the "events up" rule. Passing a plain value and a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) keeps the child honest about what it reads and what it can trigger.
- **Name events by what happened, not by what to do.** [`onQueryChange`]({{ "/en/glossary/event-handlers/" | relative_url }}), [`onExpandedChange`]({{ "/en/glossary/event-handlers/" | relative_url }}) and [`onDeleteClick`]({{ "/en/glossary/event-handlers/" | relative_url }}) describe user intent; the owner decides the effect. It keeps the component agnostic of the business rules, and lets the same component trigger different behavior in different screens.
- **Hoisting can also reduce [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}).** The composable that reads a state is the one that recomposes. Hoisting a value only as high as it is needed, and passing it down only to the children that use it, keeps a frequent change from recomposing a whole screen.

## Code in Action

```kotlin
// From FollowApp Suite — AnimatedSearchBar.kt
// Fully stateless: the query and whether search is active come from the
// caller, and typing or closing are reported as events. The bar never decides
// what the query is; the screen's state does.
@Composable
fun AnimatedSearchBar(
    isSearchActive: Boolean,
    searchQuery: String,
    onQueryChange: (String) -> Unit,
    onClose: () -> Unit,
    focusRequester: FocusRequester,
    // ...
)

// From FollowApp Suite — CollapsibleGroupCard.kt
// Both modes in one component. With expanded == null it is uncontrolled and
// keeps its own remember; with a value it is controlled and only reports the
// toggle, because the caller needs to persist the state.
@Composable
fun CollapsibleGroupCard(
    headerChip: @Composable () -> Unit,
    modifier: Modifier = Modifier,
    collapsible: Boolean = true,
    initiallyExpanded: Boolean = true,
    expanded: Boolean? = null,
    onExpandedChange: ((Boolean) -> Unit)? = null,
    // ...
) {
    var internalExpanded by remember { mutableStateOf(initiallyExpanded) }
    val effectiveExpandedRaw = expanded ?: internalExpanded
    // ...
    IconButton(
        onClick = {
            val next = !effectiveExpandedRaw
            if (expanded == null) internalExpanded = next
            onExpandedChange?.invoke(next)
        },
    ) { /* ... */ }
}

// From FollowApp Suite — TasksViewModel.kt
// Where the controlled mode leads: the collapsed groups are hoisted all the way
// to the ViewModel, because they are persisted per filter preset. The card only
// reports the toggle; the ViewModel owns the state.
fun onGroupCollapseToggle(groupKey: String) {
    val state = _uiState.value
    val bucket = state.activePresetId
        ?: com.followapp.mytasks.data.local.preferences.TasksViewPreferences.UNSAVED_PRESET_KEY
    val current = state.collapsedGroupsByPreset[bucket] ?: emptySet()
    val next = if (groupKey in current) current - groupKey else current + groupKey
    val newMap = if (next.isEmpty()) {
        state.collapsedGroupsByPreset - bucket
    } else {
        state.collapsedGroupsByPreset + (bucket to next)
    }
    _uiState.update { it.copy(collapsedGroupsByPreset = newMap) }
}

// Not found in FAS — standalone example
// The same component before and after hoisting.
@Composable
fun RatingBarStateful() {
    var rating by remember { mutableStateOf(0) }                 // nobody outside can read it
    Stars(selected = rating, onSelect = { rating = it })
}

@Composable
fun RatingBar(rating: Int, onRatingChange: (Int) -> Unit) {     // state down, events up
    Stars(selected = rating, onSelect = onRatingChange)
}
```

## The Interview (The Hot Seat)

**Question**: What is state hoisting in Compose, and how do you decide how high to hoist a piece of state?

**Senior Answer**: State hoisting is moving a composable's state out of it and up to its caller, replacing it with a value parameter and an event callback, like [`TextField(value, onValueChange)`]({{ "/en/glossary/text-field/" | relative_url }}). The composable becomes [stateless]({{ "/en/glossary/stateful-stateless/" | relative_url }}): it shows what it receives and reports what the user does, and the caller owns the state. It is [unidirectional data flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}) at component level: state goes down, events go up. The benefits are a [single source of truth]({{ "/en/glossary/single-source-of-truth/" | relative_url }}), because only one place owns the value; reusability, because the component works in any screen; and testability and [previews]({{ "/en/glossary/preview/" | relative_url }}), because I can render it with any value and assert the events it emits. For the height, I hoist to the lowest common ancestor of everything that reads or writes the state, and no higher. If only that composable cares, like whether a dropdown is open, it stays local with [`remember`]({{ "/en/glossary/remember/" | relative_url }}). If the UI logic gets complex, I put it in a plain [state holder]({{ "/en/glossary/state-holder/" | relative_url }}) class with a [`remember`]({{ "/en/glossary/remember/" | relative_url }}) function, the way [`LazyListState`]({{ "/en/glossary/lazy-list-state/" | relative_url }}) works. And if the state comes from business logic, has to survive [configuration changes]({{ "/en/glossary/configuration-change/" | relative_url }}) or is persisted, it goes to the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}). What I avoid is hoisting everything to the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) by default, because it mixes UI details with business state and recomposes more than it should.

**Question**: A teammate passes the whole [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}), or a [`MutableState`]({{ "/en/glossary/mutable-state/" | relative_url }}), into a child composable so it can update the state directly. What is wrong with that, and what would you do instead?

**Senior Answer**: Both break the direction of the data flow. With the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}), the child depends on a class it does not need, can call anything on it, cannot be shown in a [Preview]({{ "/en/glossary/preview/" | relative_url }}) without building a [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}), and is tied to that one screen. With a [`MutableState`]({{ "/en/glossary/mutable-state/" | relative_url }}), the child becomes a second writer of state it does not own: the owner no longer decides what happens on each change, so validation, side effects or persistence can be skipped, and when something goes wrong there are two places to look. Instead, I pass the child exactly what it reads, as plain values, and what it can trigger, as [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) named after the user's intent, like [`onQueryChange`]({{ "/en/glossary/event-handlers/" | relative_url }}) or [`onDeleteClick`]({{ "/en/glossary/event-handlers/" | relative_url }}). The owner, usually the screen-level composable that talks to the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}), connects those [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) to the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }})'s functions. The child stays [stateless]({{ "/en/glossary/stateful-stateless/" | relative_url }}), previewable and reusable, and every change to the state goes through a single owner. If the component should also work on its own, I give it an optional value parameter so it can be either [controlled]({{ "/en/glossary/controlled-uncontrolled/" | relative_url }}) by the caller or keep its own state.

---

[Back to Chapters]({{ "/" | relative_url }})
