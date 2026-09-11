---
layout: post
title: "Back Stack"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
tags: [navigation, lifecycle, android-framework]
lang: en
permalink: /en/glossary/back-stack/
---

## The Theory (The What)

The **back stack** is a last-in, first-out (LIFO) stack that Android uses to track navigation history. When a user navigates forward, the current destination is pushed onto the back stack; pressing Back pops the top entry and returns to the previous destination.

Android manages several back stack layers:

- **Activity back stack** (task stack) — managed by the OS. Each task has a stack of Activities.
- **Fragment back stack** — managed by `FragmentManager`. Fragment transactions can be added to the back stack via `addToBackStack()`.
- **Navigation component back stack** — managed by `NavController`. Each `NavBackStackEntry` holds the destination, arguments, and a [ViewModelStore]({{ "/en/glossary/viewmodel-store/" | relative_url }}). This is the modern standard.

In Compose navigation, each `NavBackStackEntry` is also a `ViewModelStoreOwner` and a `LifecycleOwner`. When an entry is popped from the back stack, its ViewModels are cleared and its [lifecycle]({{ "/en/glossary/lifecycle-event/" | relative_url }}) reaches `DESTROYED`.

## The Senior Nuance

- A Senior understands that the back stack defines ViewModel [lifetime]({{ "/en/glossary/composition-lifetime/" | relative_url }}): a ViewModel obtained via `hiltViewModel()` is scoped to its `NavBackStackEntry`. If the entry is popped and the user navigates to the same destination again, a fresh ViewModel is created. If the entry remains on the back stack (navigated away but not popped), the ViewModel survives.
- Back stack operations like `popUpTo` with `inclusive = true` clear intermediate entries, destroying their ViewModels and saved state. A Senior designs navigation graphs so that critical state is not accidentally destroyed by aggressive `popUpTo` patterns.
- In multi-back-stack scenarios (bottom navigation with independent stacks), each tab maintains its own back stack. Switching tabs does not destroy the other tab's back stack entries — their ViewModels survive in their respective [ViewModelStores]({{ "/en/glossary/viewmodel-store/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
