---
layout: post
title: "Loading (UI State)"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [state-management, sealed-types, architecture]
lang: en
permalink: /en/glossary/loading-state/
---

## The Theory (The What)

**`Loading`** is the UI state that says the screen is waiting for data. In a [sealed state]({{ "/en/glossary/sealed-state/" | relative_url }}) it is usually a [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) with no data, because there is nothing to show yet; in a [flat data class]({{ "/en/glossary/flat-data-class/" | relative_url }}) it becomes an `isLoading` flag that can coexist with data already on screen.

## The Senior Nuance

- **A sealed `Loading` replaces everything else.** Moving to it during a refresh hides the current data and drops anything stored in the previous state, such as a search query.
- **Distinguish the first load from a refresh.** A refresh over existing data is usually a flag (`isRefreshing`) next to the data, not a separate state.
- See [UI State Modeling: Sealed vs Flat Data Class]({{ "/en/05-architecture/ui-state-modeling/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
