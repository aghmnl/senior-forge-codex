---
layout: post
title: "repeatOnLifecycle"
date: 2026-09-25 12:00:00 +0000
categories: [en, glossary]
tags: [lifecycle, coroutines, flow]
lang: en
permalink: /en/glossary/repeat-on-lifecycle/
---

## The Theory (The What)

**`repeatOnLifecycle(state)`** is a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) on `Lifecycle` (and `LifecycleOwner`) that runs a block **every time the [lifecycle]({{ "/en/glossary/lifecycle/" | relative_url }}) reaches `state`**, and cancels it every time the lifecycle drops below it. The function itself only returns when the lifecycle is `DESTROYED`. It is the standard way to [collect]({{ "/en/glossary/collect/" | relative_url }}) flows from a View-based `Activity` or `Fragment`, and the building block behind [collectAsStateWithLifecycle]({{ "/en/glossary/collect-as-state-with-lifecycle/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
class TasksFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                // Cancelled on STOP, relaunched on START
                viewModel.uiState.collect { render(it) }
            }
        }
    }
}
```

## The Senior Nuance

- **Cancel, do not pause.** The deprecated `launchWhenStarted` *suspended* the collector in the background but kept the [upstream]({{ "/en/glossary/upstream/" | relative_url }}) subscription alive. `repeatOnLifecycle` *cancels* the block, so the upstream can really stop.
- **Code after it runs only at `DESTROYED`.** Because it suspends until the lifecycle is destroyed, anything written after the call in the same [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) is effectively dead code during the screen's life. Collecting two flows means launching two children inside the block.
- **In a `Fragment`, use `viewLifecycleOwner`.** The fragment's own lifecycle outlives its view; collecting on it keeps updating views that no longer exist.
- **The block restarts from scratch.** Each time the lifecycle returns to `STARTED` the collection begins again; on a [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) that means receiving the current value again, which is harmless for state and wrong for one-shot events.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
