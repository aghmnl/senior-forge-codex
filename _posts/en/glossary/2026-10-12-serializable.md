---
layout: post
title: "Serializable"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [jvm, serialization]
lang: en
permalink: /en/glossary/serializable/
---

## The Theory (The What)

**`java.io.Serializable`** is the Java marker interface that lets an object be converted to bytes by Java serialization. A [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}) accepts `Serializable` values, so it is an alternative to [`Parcelable`]({{ "/en/glossary/parcelable/" | relative_url }}) for passing objects.

## The Senior Nuance

- **Slower and heavier than [`Parcelable`]({{ "/en/glossary/parcelable/" | relative_url }})** on Android, because it uses reflection and writes class metadata. Prefer [`@Parcelize`]({{ "/en/glossary/parcelize/" | relative_url }}).
- **Not to be confused with kotlinx.serialization's `@Serializable`**, which generates serializers for formats like JSON and has nothing to do with [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
