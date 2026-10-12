---
layout: post
title: "SavedStateHandle"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [android-framework, state-management, lifecycle]
lang: en
permalink: /en/glossary/saved-state-handle/
---

## The Theory (The What)

**`SavedStateHandle`** is a key-value map a [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) receives in its constructor that is **written into the [saved instance state]({{ "/en/glossary/saved-instance-state/" | relative_url }})**. Values put in it survive [process death]({{ "/en/glossary/process-death/" | relative_url }}), which the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) alone does not. It also exposes values as flows, and holds the navigation arguments of the screen.

```kotlin
// Not found in FAS — standalone example
class FormViewModel(private val handle: SavedStateHandle) : ViewModel() {
    val name: StateFlow<String> = handle.getStateFlow("name", "")
    fun onNameChange(value: String) { handle["name"] = value }
}
```

## The Senior Nuance

- **The [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }})'s counterpart of [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }})**: same mechanism, same [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}) types, same size limit.
- **Save the input, not the derived state.** Store the field values; recompute validation and loaded data from them.
- See [remember & rememberSaveable]({{ "/en/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
