---
layout: post
title: "Memory Leaks"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/memory-leaks/
---

## The Theory (The What)

A **memory leak** occurs when an object is no longer needed by the application but cannot be reclaimed by the [Garbage Collector]({{ "/en/glossary/garbage-collector/" | relative_url }}) because a strong reference chain still reaches it from a GC root. The object remains on the [heap]({{ "/en/glossary/heap/" | relative_url }}), consuming memory indefinitely. Over time, accumulated leaks exhaust the [heap]({{ "/en/glossary/heap/" | relative_url }}), leading to `OutOfMemoryError` or degraded performance as the GC works harder.

```kotlin
// Not found in FAS — standalone example
// Classic Android leak: inner class holds implicit reference to Activity
class MyActivity : AppCompatActivity() {
    private val handler = object : Handler(Looper.getMainLooper()) {
        override fun handleMessage(msg: Message) {
            // 'this' holds a reference to MyActivity
            // If a delayed message is pending when the Activity is destroyed,
            // the Activity cannot be garbage collected
        }
    }
}
```

The fix is to break the reference chain: use a `WeakReference`, cancel pending work in `onDestroy()`, or use lifecycle-aware components that automatically unregister.

## The Senior Nuance

- On Android, the most common leaks come from holding references to `Activity`, `Context`, or `View` beyond their lifecycle. A singleton that caches an `Activity` context leaks the entire view hierarchy. Always use `applicationContext` for long-lived references.
- **LeakCanary** is the standard tool for detecting leaks in debug builds. It watches destroyed Activities, Fragments, ViewModels, and Services, and reports a leak trace showing the reference chain from the GC root to the leaked object. Senior developers integrate it into every project.
- Coroutines tied to `lifecycleScope` or `viewModelScope` are automatically cancelled when the lifecycle owner is destroyed — this prevents leaks from long-running suspend functions. Using `GlobalScope` or a custom `CoroutineScope` without cancellation is a common leak source.
- [Inline functions]({{ "/en/glossary/inline-functions/" | relative_url }}) and [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) can capture outer variables, creating implicit references. A lambda passed to a long-lived callback (e.g., a listener registered on a singleton) holds a reference to its enclosing class — which may be an Activity.
- Memory leaks are not just about RAM: a leaked `Activity` holds its entire view tree, drawable caches, and potentially bitmap buffers. A single Activity leak can waste 50+ MB on a device with a 256 MB [heap]({{ "/en/glossary/heap/" | relative_url }}) cap.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
