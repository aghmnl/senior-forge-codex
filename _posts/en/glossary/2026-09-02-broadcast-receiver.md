---
layout: post
title: "Broadcast Receiver"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/broadcast-receiver/
---

## The Theory (The What)

A **BroadcastReceiver** is an Android component that listens for system-wide or app-internal broadcast messages (Intents). When a matching Intent is broadcast — battery low, connectivity change, package installed, boot completed — the system delivers it to every registered receiver. Receivers can be registered statically in `AndroidManifest.xml` (surviving process death) or dynamically via `Context.registerReceiver()` (active only while registered).

```kotlin
// Standalone example — no BroadcastReceiver usage found in FAS
class ConnectivityReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val isConnected = intent
            .getBooleanExtra(ConnectivityManager.EXTRA_NO_CONNECTIVITY, false)
            .not()
        Log.d("Connectivity", "Network available: $isConnected")
    }
}

// Dynamic registration (lifecycle-aware)
class MainActivity : ComponentActivity() {
    private val receiver = ConnectivityReceiver()

    override fun onStart() {
        super.onStart()
        registerReceiver(receiver, IntentFilter(ConnectivityManager.CONNECTIVITY_ACTION))
    }

    override fun onStop() {
        super.onStop()
        unregisterReceiver(receiver)
    }
}
```

## The Senior Nuance

- **[Memory leak]({{ "/en/glossary/memory-leaks/" | relative_url }}) risk**: A dynamically registered receiver that is never unregistered leaks the `Context` it was registered with. This is one of the classic Android leak patterns. Always pair `registerReceiver` with `unregisterReceiver` in matching lifecycle methods (`onStart`/`onStop` or `onResume`/`onPause`), or use [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) patterns.
- **Modern alternatives**: For many broadcast use cases, Android now provides dedicated APIs: `ConnectivityManager.NetworkCallback` for network state, `JobScheduler`/`WorkManager` for deferred work, `ProcessLifecycleOwner` for app foreground/background. Senior developers reach for these first and use `BroadcastReceiver` only when the broadcast is truly system-wide or from another app.
- **Implicit broadcast restrictions**: Since Android 8.0 (API 26), most implicit broadcasts can no longer be declared in the manifest — they must be registered dynamically. This was done to reduce unnecessary app wake-ups. Explicit broadcasts (targeted at a specific component) and a small allowlist of system broadcasts (boot completed, locale changed) are exempt.
- **`onReceive` runs on the main thread** and must complete within ~10 seconds. For longer work, use `goAsync()` to extend the window or delegate to a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) / `WorkManager` task. Blocking `onReceive` causes ANRs.
- **[Event wiring]({{ "/en/glossary/event-wiring/" | relative_url }})**: Broadcast receivers are the system-level form of [event wiring]({{ "/en/glossary/event-wiring/" | relative_url }}). Registering a receiver wires your component to an event source (the system or another app). This is conceptually the same as passing [event handlers]({{ "/en/glossary/event-handlers/" | relative_url }}) in Compose — just at a different abstraction layer.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
