---
layout: post
title: "Lifecycle Event"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/lifecycle-event/
---

## The Theory (The What)

A **lifecycle event** is a signal emitted by the Android system when an Activity, Fragment, or other `LifecycleOwner` transitions between states: `ON_CREATE`, `ON_START`, `ON_RESUME`, `ON_PAUSE`, `ON_STOP`, and `ON_DESTROY`. These events drive the paired lifecycle callbacks (`onCreate()`, `onStart()`, etc.) and are the foundation of [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) programming in Android.

```kotlin
// From FollowApp Suite — MainActivity.kt
class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // ...
    }

    override fun onResume() {
        super.onResume()
        inAppUpdateManager.onResume(this, updateLauncher)
    }
}
```

Each callback corresponds to a lifecycle event: `onCreate` → `ON_CREATE`, `onResume` → `ON_RESUME`. The system guarantees their ordering — `ON_START` always follows `ON_CREATE`, `ON_STOP` always follows `ON_PAUSE`.

## The Senior Nuance

- **`lateinit` and lifecycle events**: `lateinit` properties are often initialized during a lifecycle event — typically `onCreate` for Activities or `onViewCreated` for Fragments. The contract is that the property will be set before it's used, and the lifecycle event provides the timing guarantee.
- **Paired callbacks**: Resources acquired in one lifecycle event must be released in its mirror: `onStart`/`onStop`, `onResume`/`onPause`. Registering a [broadcast receiver]({{ "/en/glossary/broadcast-receiver/" | relative_url }}) in `onStart` and unregistering in `onStop` is the classic example. Mismatched pairs cause [memory leaks]({{ "/en/glossary/memory-leaks/" | relative_url }}).
- **`repeatOnLifecycle`**: Modern Android code uses `repeatOnLifecycle(Lifecycle.State.STARTED)` to tie [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) collection to lifecycle events — the block starts on `ON_START` and cancels on `ON_STOP`, then restarts on the next `ON_START`. This replaces manual `onStart`/`onStop` pairing for Flow collection.
- **Configuration changes**: `ON_DESTROY` followed by `ON_CREATE` happens during configuration changes (rotation, locale change). Senior developers use `ViewModel` to survive this — the ViewModel's `viewModelScope` outlives the Activity's lifecycle events but is cancelled on final destruction.
- **Process death**: After process death, the system delivers `ON_CREATE` with a non-null `savedInstanceState` bundle. Senior developers handle this edge case explicitly — a `lateinit` property initialized from an Intent extra will crash if the Intent is lost after process death.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
