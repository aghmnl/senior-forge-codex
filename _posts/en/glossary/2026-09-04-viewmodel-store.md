---
layout: post
title: "ViewModelStore"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
tags: [lifecycle, android-framework, navigation]
lang: en
permalink: /en/glossary/viewmodel-store/
---

## The Theory (The What)

**`ViewModelStore`** is the Android Jetpack class that holds ViewModel instances and ensures they survive configuration changes (screen rotations, language switches, dark mode toggles). Every `ComponentActivity`, `Fragment`, and navigation [back stack]({{ "/en/glossary/back-stack/" | relative_url }}) entry owns a `ViewModelStore`.

When you request a ViewModel via [`by viewModels()`]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}) or `ViewModelProvider(owner)`, the framework checks the owner's `ViewModelStore` first. If the ViewModel already exists, it returns the cached instance; otherwise it creates one, stores it, and returns it. On final destruction (Activity `finish()`, Fragment removal from the [back stack]({{ "/en/glossary/back-stack/" | relative_url }})), `ViewModelStore.clear()` is called, which invokes `onCleared()` on every ViewModel it holds.

The store itself is retained across configuration changes via the `NonConfigurationInstances` mechanism (Activities) or the Fragment manager's retained state (Fragments).

## The Senior Nuance

- A Senior understands that the `ViewModelStore` defines the ViewModel's **survival scope**: scoping to a Fragment's store means the ViewModel dies when the Fragment is popped; scoping to the Activity's store (`by activityViewModels()`) means it lives as long as the Activity. Choosing the wrong scope either leaks memory or causes premature state loss.
- In Compose with [Hilt]({{ "/en/glossary/hilt/" | relative_url }}), `hiltViewModel()` uses the [navigation component]({{ "/en/glossary/navigation-component/" | relative_url }})'s `NavBackStackEntry` as the `ViewModelStoreOwner`. This means each navigation destination has its own `ViewModelStore` — navigating away and returning creates a new ViewModel if the destination was popped from the [back stack]({{ "/en/glossary/back-stack/" | relative_url }}).
- `ViewModelStore` holds strong references to ViewModels. If a ViewModel holds references to large objects (bitmaps, database cursors), those objects survive configuration changes too — a potential source of [memory leaks]({{ "/en/glossary/memory-leaks/" | relative_url }}) if not properly managed in `onCleared()`.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
