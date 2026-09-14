---
layout: post
title: "Lifecycle"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [lifecycle, android-framework]
lang: en
permalink: /en/glossary/lifecycle/
---

## The Theory (The What)

**Lifecycle** is the sequence of states an Android component passes through between creation and destruction — for an Activity or Fragment: `CREATED → STARTED → RESUMED → STARTED → CREATED → DESTROYED`, driven by [lifecycle events]({{ "/en/glossary/lifecycle-event/" | relative_url }}). Jetpack models it as a `Lifecycle` object owned by a `LifecycleOwner`, which is what lets [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) components observe it instead of being called from `onStart`/`onStop` by hand.

Every scope in the coroutine world is tied to some lifecycle: [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) to the ViewModel's, `lifecycleScope` to the owner's, `rememberCoroutineScope()` to the [composition]({{ "/en/glossary/composition-lifetime/" | relative_url }}).

## The Senior Nuance

- **The word means three nested things.** Process lifetime (longest), ViewModel lifetime (survives configuration changes), Activity/Fragment lifecycle (dies on rotation), composition lifetime (shortest). Choosing where state and work live is choosing which of these they should survive.
- **Cancellation follows the lifecycle, not the other way round.** A [`CoroutineScope`]({{ "/en/glossary/coroutine-scope/" | relative_url }}) bound to a lifecycle cancels its [`Job`]({{ "/en/glossary/job/" | relative_url }}) when the owner is destroyed; work that must outlive the owner needs a longer-lived scope, not a leaked one.
- **`repeatOnLifecycle(STARTED)`** is the idiom for collecting a Flow only while the UI is visible, restarting on each `ON_START`.
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
