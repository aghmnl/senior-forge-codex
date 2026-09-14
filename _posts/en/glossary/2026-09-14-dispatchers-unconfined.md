---
layout: post
title: "Dispatchers.Unconfined"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, threading, testing]
lang: en
permalink: /en/glossary/dispatchers-unconfined/
---

## The Theory (The What)

**`Dispatchers.Unconfined`** is the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) that does not dispatch: the coroutine starts on the caller's [thread]({{ "/en/glossary/thread/" | relative_url }}) and, after each [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}), resumes on whatever thread the suspending function resumed it from. It confines nothing, which makes it fast and unpredictable.

It belongs in framework internals and in tests (its testing cousin is `UnconfinedTestDispatcher`), not in application code.

## The Senior Nuance

- **Thread identity changes mid-function.** Code before a `delay` runs on the caller's thread; code after runs on the timer thread that resumed it. Any assumption about "the current thread" is broken.
- **Not a performance tool.** The saving is one dispatch per resume; the cost is losing every guarantee [`Main`]({{ "/en/glossary/dispatchers-main/" | relative_url }}), [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) and [`Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}) exist to provide.
- **Do not confuse it with [`Main.immediate`]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }}).** `immediate` runs synchronously only when already on the *right* thread and posts otherwise; `Unconfined` never posts at all.
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
