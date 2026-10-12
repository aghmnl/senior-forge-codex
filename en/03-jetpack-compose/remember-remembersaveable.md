---
layout: page
title: "remember & rememberSaveable"
lang: en
permalink: /en/03-jetpack-compose/remember-remembersaveable/
order: 2
---

## The Theory (The What)

A composable is a function, and Compose may call it again on every [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}). Any local variable declared in its body is created again each time. [`remember`]({{ "/en/glossary/remember/" | relative_url }}) and [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}) are the two ways to keep a value **across those calls**. The difference between them is **how long** the value lives.

**`remember { calculation }`** runs the calculation the first time the composable enters the [composition]({{ "/en/glossary/composition/" | relative_url }}), stores the result in the [composition]({{ "/en/glossary/composition/" | relative_url }}), and returns that same stored value on every [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}). With keys, `remember(key1, key2) { ... }`, it runs the calculation again whenever a key changes. The value is **forgotten when the composable leaves the [composition]({{ "/en/glossary/composition/" | relative_url }})**, and it is also lost when the [Activity]({{ "/en/glossary/activity/" | relative_url }}) is recreated: a [configuration change]({{ "/en/glossary/configuration-change/" | relative_url }}) (rotation, dark mode, a language change) or [process death]({{ "/en/glossary/process-death/" | relative_url }}).

**`rememberSaveable { calculation }`** does the same, and **also saves the value** into the [saved instance state]({{ "/en/glossary/saved-instance-state/" | relative_url }}), the same [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}) mechanism [Activities]({{ "/en/glossary/activity/" | relative_url }}) have always used. When the [Activity]({{ "/en/glossary/activity/" | relative_url }}) is recreated, after a [configuration change]({{ "/en/glossary/configuration-change/" | relative_url }}) or after the system killed the process in the background, the value is restored instead of computed again.

Because it goes into a [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}), a value saved with [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}) must be of a type the [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}) can hold: [primitives]({{ "/en/glossary/primitives/" | relative_url }}), [`String`]({{ "/en/glossary/string/" | relative_url }}), [`Parcelable`]({{ "/en/glossary/parcelable/" | relative_url }}) (usually a class annotated with [`@Parcelize`]({{ "/en/glossary/parcelize/" | relative_url }})) or [`Serializable`]({{ "/en/glossary/serializable/" | relative_url }}). For any other type you provide a **[`Saver`]({{ "/en/glossary/saver/" | relative_url }})**, which converts the value to something saveable and back. [`listSaver`]({{ "/en/glossary/list-saver/" | relative_url }}) and [`mapSaver`]({{ "/en/glossary/map-saver/" | relative_url }}) are helpers for writing one.

Neither of them is reactive on its own. To have Compose recompose when a value changes, what you [remember]({{ "/en/glossary/remember/" | relative_url }}) is a [`MutableState`]({{ "/en/glossary/mutable-state/" | relative_url }}): `var text by rememberSaveable { mutableStateOf("") }`.

## The Senior Perspective (The Why)

- **The choice is about lifetime, not importance.** [`remember`]({{ "/en/glossary/remember/" | relative_url }}) is for values that can be recreated or that are fine to lose: caches of computations, formatters, measurements, animation state, objects like [`Animatable`]({{ "/en/glossary/animatable/" | relative_url }}). [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}) is for **state the user created and would notice losing**: the text typed in a field, the selected tab, whether a section is expanded, an open dialog. The question is "if the user rotates the phone, or comes back after the system killed the app, should this still be here?".
- **Rotation is the easy case to test; [process death]({{ "/en/glossary/process-death/" | relative_url }}) is the one that bites.** Many bugs never show up during development because the process is never killed. In production, the user switches to the camera, Android reclaims memory, and when they come back the [Activity]({{ "/en/glossary/activity/" | relative_url }}) is recreated from the [saved state]({{ "/en/glossary/saved-instance-state/" | relative_url }}). Anything stored with [`remember`]({{ "/en/glossary/remember/" | relative_url }}), or only in a [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}), is gone. "Don't keep [activities]({{ "/en/glossary/activity/" | relative_url }})" in the developer options, or killing the process from adb while the app is in the background, reproduces it.
- **[`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}) is not a database.** The [saved state]({{ "/en/glossary/saved-instance-state/" | relative_url }}) travels through a [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}) that crosses process boundaries, and its total size is limited (around 1 MB for the whole transaction, shared with the rest of the app). Saving large lists or domain objects can crash with a [`TransactionTooLargeException`]({{ "/en/glossary/transaction-too-large-exception/" | relative_url }}). Save small UI values, such as an id or a query, and rebuild the rest from the real source of data.
- **Where it lives also matters.** UI element state belongs in the composable, with [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}). Screen state that comes from business logic belongs in the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}), which survives [configuration changes]({{ "/en/glossary/configuration-change/" | relative_url }}) but **not** [process death]({{ "/en/glossary/process-death/" | relative_url }}); for that, the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) uses [`SavedStateHandle`]({{ "/en/glossary/saved-state-handle/" | relative_url }}), the same mechanism exposed to the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}). Duplicating the same value in both places creates two sources of truth.
- **Keys are inputs, and forgetting one is a bug.** `remember(query) { filter(query) }` is correct. If the calculation also depends on a parameter that is not a key, the cached value goes stale when that parameter changes. Every value the calculation reads should be a key, or come from inside it.
- **Lists and navigation keep saveable state for you.** Inside a [`LazyColumn`]({{ "/en/glossary/lazy-column/" | relative_url }}), an item scrolled off screen leaves the [composition]({{ "/en/glossary/composition/" | relative_url }}) and forgets its [`remember`]({{ "/en/glossary/remember/" | relative_url }}) values, but its [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}) values are restored when it scrolls back. The same happens with screens on the Navigation back stack. That is also why [`rememberLazyListState()`]({{ "/en/glossary/remember-lazy-list-state/" | relative_url }}) restores the scroll position: it is built on [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}).

## Code in Action

```kotlin
// From FollowApp Suite — SettingsScreen.kt (TimeZonePickerDialog)
// remember used as a cache: the full zone list is computed once, and the
// filtered list is recomputed only when the query (its key) changes.
// Losing these on rotation costs nothing: they are rebuilt from scratch.
val allZones = remember {
    val device = ZoneId.systemDefault().id
    listOf(device) + ZoneId.getAvailableZoneIds().sorted().filter { it != device }
}
val filtered = remember(query) {
    if (query.isBlank()) allZones
    else allZones.filter { it.lowercase(Locale.ROOT).contains(query.trim().lowercase(Locale.ROOT)) }
}

// From FollowApp Suite — SettingsScreen.kt
// Dialog flags and the text typed in the search field use remember. The
// manifest only handles locale and layoutDirection changes itself, so a
// rotation recreates the Activity: an open dialog closes and the typed query
// is cleared. That is acceptable for a short confirmation; for text the user
// typed, rememberSaveable keeps it with no other change (Boolean and String
// are saveable).
var showClearAllConfirm by remember { mutableStateOf(false) }
var query by remember { mutableStateOf("") }

// Not found in FAS — standalone example
// The saveable versions of the same state.
var showClearAllConfirm by rememberSaveable { mutableStateOf(false) }
var query by rememberSaveable { mutableStateOf("") }

// Not found in FAS — standalone example
// A type the Bundle cannot hold needs a Saver. listSaver turns it into a
// list of saveable values and back.
data class DateRange(val start: LocalDate, val end: LocalDate)

val DateRangeSaver = listSaver<DateRange, String>(
    save = { listOf(it.start.toString(), it.end.toString()) },
    restore = { DateRange(LocalDate.parse(it[0]), LocalDate.parse(it[1])) }
)

var range by rememberSaveable(stateSaver = DateRangeSaver) {
    mutableStateOf(DateRange(LocalDate.now(), LocalDate.now().plusDays(7)))
}
```

## The Interview (The Hot Seat)

**Question**: What is the difference between [`remember`]({{ "/en/glossary/remember/" | relative_url }}) and [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}), and how do you decide which one to use?

**Senior Answer**: Both keep a value across recompositions, which a local variable cannot do because the composable function runs again each time. The difference is the lifetime. [`remember`]({{ "/en/glossary/remember/" | relative_url }}) stores the value in the [composition]({{ "/en/glossary/composition/" | relative_url }}), so it lives while the composable is in the [composition]({{ "/en/glossary/composition/" | relative_url }}): it is lost when the composable leaves, and when the [Activity]({{ "/en/glossary/activity/" | relative_url }}) is recreated, either by a [configuration change]({{ "/en/glossary/configuration-change/" | relative_url }}) like a rotation or by [process death]({{ "/en/glossary/process-death/" | relative_url }}). [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}) also writes the value into the [saved instance state]({{ "/en/glossary/saved-instance-state/" | relative_url }}), so after a recreation it is restored. Because that state is a [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}), the value has to be a primitive, a [`String`]({{ "/en/glossary/string/" | relative_url }}), a [`Parcelable`]({{ "/en/glossary/parcelable/" | relative_url }}) or a [`Serializable`]({{ "/en/glossary/serializable/" | relative_url }}), or I provide a [`Saver`]({{ "/en/glossary/saver/" | relative_url }}). My rule is about what the user would notice. Caches, formatters, measurements and animation state go in [`remember`]({{ "/en/glossary/remember/" | relative_url }}), because they can be recomputed. State the user created, like typed text, a selected tab or an expanded section, goes in [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}), because losing it after a rotation or after coming back to the app feels like a bug. And I keep it small, because the [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}) has a size limit: I save an id or a query, never a list of domain objects.

**Question**: Users report that a long form loses everything they typed when they switch to another app to copy something and come back. Rotating the device in testing does not reproduce it. What is happening, and how do you fix it?

**Senior Answer**: It sounds like [process death]({{ "/en/glossary/process-death/" | relative_url }}). While the user is in the other app, Android can kill the app's process to reclaim memory. When they come back, the [Activity]({{ "/en/glossary/activity/" | relative_url }}) is recreated from its [saved state]({{ "/en/glossary/saved-instance-state/" | relative_url }}), and only what was written there survives. If rotation works, the form state is probably in a [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}), which survives [configuration changes]({{ "/en/glossary/configuration-change/" | relative_url }}) but not [process death]({{ "/en/glossary/process-death/" | relative_url }}), or in plain [`remember`]({{ "/en/glossary/remember/" | relative_url }}). I would reproduce it first, with "Don't keep [activities]({{ "/en/glossary/activity/" | relative_url }})" or by killing the process from adb while the app is in the background. The fix depends on where the state lives. If it is UI state in the composable, [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}) instead of [`remember`]({{ "/en/glossary/remember/" | relative_url }}). If it lives in the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}), which is the usual place for a form that is validated and submitted, I store the field values in [`SavedStateHandle`]({{ "/en/glossary/saved-state-handle/" | relative_url }}), so they are written to the [saved state]({{ "/en/glossary/saved-instance-state/" | relative_url }}) and restored on recreation. In both cases I save only the small values, the text of each field and maybe a step index, and not derived data, because the [saved state]({{ "/en/glossary/saved-instance-state/" | relative_url }}) has a size limit and a large [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}) can crash with a [`TransactionTooLargeException`]({{ "/en/glossary/transaction-too-large-exception/" | relative_url }}).

---

[Back to Chapters]({{ "/" | relative_url }})
