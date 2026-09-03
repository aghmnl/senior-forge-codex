---
layout: post
title: "Lifecycle-Aware"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/lifecycle-aware/
---

## The Theory (The What)

A component is **lifecycle-aware** when it automatically adjusts its behavior based on the lifecycle state of an Android `LifecycleOwner` (Activity, Fragment, or a custom owner). Instead of manually starting and stopping work in `onCreate`/`onDestroy` pairs, lifecycle-aware components observe the lifecycle and react accordingly — starting when active, stopping when destroyed, preventing work against a dead host.

```kotlin
// From FollowApp Suite — MainActivity.kt
class MainActivity : ComponentActivity() {
    // ...
    private fun handleReferralIntent(intent: Intent?) {
        val uri = intent?.data ?: return
        if (uri.scheme == "followapp" && uri.host == "mytasks"
            && uri.path?.startsWith("/invite") == true
        ) {
            val referrerId = uri.getQueryParameter("by") ?: return
            lifecycleScope.launch { registerReferralUseCase(referrerId) }
        }
    }
}
```

`lifecycleScope` is a lifecycle-aware [CoroutineScope]({{ "/en/glossary/coroutines/" | relative_url }}): any [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) launched in it is automatically cancelled when the Activity is destroyed — no manual cleanup needed.

## The Senior Nuance

- **`lifecycleScope` and `viewModelScope`** are the two built-in lifecycle-aware scopes. `lifecycleScope` is tied to the UI component (Activity/Fragment), while `viewModelScope` survives configuration changes but is cancelled when the ViewModel is cleared. Senior developers choose the scope based on the work's natural lifetime.
- **`repeatOnLifecycle`** is the modern pattern for collecting Flows in a lifecycle-aware way: it starts collection when the lifecycle reaches a target state (usually `STARTED`) and cancels when it drops below it. This prevents processing emissions when the UI is in the background — saving resources and avoiding crashes from updating detached views.
- **[Broadcast receiver]({{ "/en/glossary/broadcast-receiver/" | relative_url }}) registration**: Lifecycle-aware registration means pairing `registerReceiver` in `onStart` with `unregisterReceiver` in `onStop`. Without this discipline, receivers leak the host Activity — a classic [memory leak]({{ "/en/glossary/memory-leaks/" | relative_url }}).
- **`DefaultLifecycleObserver`**: Components that aren't Activities or Fragments can implement `DefaultLifecycleObserver` and register themselves with a `LifecycleOwner`. This is how location managers, analytics trackers, and media players tie their work to the UI lifecycle without holding a reference to the Activity.
- **[Callbacks]({{ "/en/glossary/callbacks/" | relative_url }}) and lifecycle**: A [callback]({{ "/en/glossary/callbacks/" | relative_url }}) registered on a long-lived object (a [singleton]({{ "/en/glossary/singleton/" | relative_url }}), a system service) that captures an Activity reference leaks that Activity. The lifecycle-aware approach is to deregister in the matching lifecycle method, or use a mechanism (`repeatOnLifecycle`, `LiveData.observe`) that handles this automatically.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
