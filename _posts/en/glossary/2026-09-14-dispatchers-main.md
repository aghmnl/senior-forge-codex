---
layout: post
title: "Dispatchers.Main"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, threading, android-framework]
lang: en
permalink: /en/glossary/dispatchers-main/
---

## The Theory (The What)

**`Dispatchers.Main`** is the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) bound to the Android [main thread]({{ "/en/glossary/main-thread/" | relative_url }}). It is implemented as a `Handler` on the main [`Looper`]({{ "/en/glossary/looper/" | relative_url }}): resuming a coroutine here posts its [continuation]({{ "/en/glossary/continuation/" | relative_url }}) to the message queue, so it runs after whatever the UI thread is currently doing. It is the only dispatcher where touching Views, `LiveData.setValue` and most Compose state writes are legal.

`Dispatchers.Main` is provided by `kotlinx-coroutines-android`; without that artifact on the classpath it throws at first use.

## The Senior Nuance

- **Suspending on Main is free; blocking on Main is the bug.** A coroutine parked at a [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) releases the thread to render; a [blocking call]({{ "/en/glossary/blocking-call/" | relative_url }}) does not.
- **It always posts, even when already on Main.** That costs a trip through the queue. [`Main.immediate`]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }}) skips it when possible, which is why the lifecycle scopes use the latter.
- **In JVM unit tests it does not exist** until [`Dispatchers.setMain`]({{ "/en/glossary/set-main/" | relative_url }}) installs a [`TestDispatcher`]({{ "/en/glossary/test-dispatcher/" | relative_url }}).
- **A repository should never switch to Main.** Return the value; let the UI-layer caller — already on Main — decide where it lands.
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
