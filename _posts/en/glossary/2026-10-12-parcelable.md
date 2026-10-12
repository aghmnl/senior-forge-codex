---
layout: post
title: "Parcelable"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [android-framework, serialization]
lang: en
permalink: /en/glossary/parcelable/
---

## The Theory (The What)

**`Parcelable`** is Android's interface for flattening an object into a `Parcel`, the format used to send data through Binder between components and processes. It is how custom objects go into a [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}), an Intent or the [saved instance state]({{ "/en/glossary/saved-instance-state/" | relative_url }}). Writing it by hand is verbose; [`@Parcelize`]({{ "/en/glossary/parcelize/" | relative_url }}) generates it.

## The Senior Nuance

- **Faster than [`Serializable`]({{ "/en/glossary/serializable/" | relative_url }})** on Android, because it writes fields explicitly instead of using reflection.
- **Being parcelable does not make an object small.** It still counts against the size limit of the transaction.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
