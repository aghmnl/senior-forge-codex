---
layout: post
title: "lifecycleScope"
date: 2026-09-28 12:00:00 +0000
categories: [en, glossary]
tags: [lifecycle, coroutines, android-framework]
lang: en
permalink: /en/glossary/lifecycle-scope/
---

## The Theory (The What)

**`lifecycleScope`** is a [CoroutineScope]({{ "/en/glossary/coroutine-scope/" | relative_url }}) tied to a `LifecycleOwner` (an `Activity`, a `Fragment` or its `viewLifecycleOwner`), provided by `androidx.lifecycle:lifecycle-runtime-ktx`. Every [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) launched in it is cancelled when the owner's [lifecycle]({{ "/en/glossary/lifecycle/" | relative_url }}) reaches `DESTROYED`. It runs on [Dispatchers.Main.immediate]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }}) and uses a [SupervisorJob]({{ "/en/glossary/supervisor-job/" | relative_url }}), so one failing child does not cancel the others. It is the UI-side counterpart of [viewModelScope]({{ "/en/glossary/viewmodel-scope/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
class TasksFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        viewLifecycleOwner.lifecycleScope.launch {
            // Cancelled when the VIEW is destroyed, not only the fragment
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect { render(it) }
            }
        }
    }
}
```

## The Senior Nuance

- **Destroyed is late.** The scope only cancels at `DESTROYED`, so a plain `lifecycleScope.launch { flow.collect { } }` keeps collecting while the app is in the background. Collection belongs inside [repeatOnLifecycle]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}), which cancels at `STOP` and restarts at `START`.
- **It dies on rotation.** A configuration change destroys the `Activity`, and its `lifecycleScope` with it. Work that must survive a rotation (a network request, a save) belongs in [viewModelScope]({{ "/en/glossary/viewmodel-scope/" | relative_url }}).
- **In a `Fragment`, use `viewLifecycleOwner.lifecycleScope`.** The fragment outlives its view on the back stack; the fragment's own scope keeps touching views that no longer exist.
- In Compose it is rarely needed: [LaunchedEffect]({{ "/en/glossary/launched-effect/" | relative_url }}) and `rememberCoroutineScope` tie coroutines to the composition instead.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
