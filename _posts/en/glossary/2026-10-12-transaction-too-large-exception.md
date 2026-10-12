---
layout: post
title: "TransactionTooLargeException"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [android-framework, error-handling, memory]
lang: en
permalink: /en/glossary/transaction-too-large-exception/
---

## The Theory (The What)

**`TransactionTooLargeException`** is thrown when data sent through Binder exceeds the transaction buffer, which is about **1 MB shared by all transactions in progress** for the process. The usual cause is a large [saved instance state]({{ "/en/glossary/saved-instance-state/" | relative_url }}) or Intent extras: big lists, bitmaps or domain objects put in a [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}).

## The Senior Nuance

- **It often crashes when the app goes to the background**, because that is when the [saved state]({{ "/en/glossary/saved-instance-state/" | relative_url }}) is sent to the system, far from the code that caused it.
- **The fix is to store less**, not to catch it: ids instead of objects, and data reloaded from a database or the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}).
- See [remember & rememberSaveable]({{ "/en/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
