---
layout: post
title: "Data Layer"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/data-layer/
---

## The Theory (The What)

A **data layer** is a logical tier in a layered architecture that groups classes by their distance from the data source or the user. In Android's recommended architecture, the standard layers are:

- **Data layer** — repositories, data sources (Room DAOs, Retrofit services, DataStore), and entities. Responsible for fetching, caching, and persisting data.
- **Domain layer** (optional) — use cases and domain models. Encapsulates business logic and orchestrates data layer calls.
- **UI layer** — ViewModels, UI state models, and composables/views. Consumes domain models and presents them.

Each layer has its own models, and [mapper functions]({{ "/en/glossary/mapper-function/" | relative_url }}) convert between them at the boundaries. This separation is the foundation of the [Mapper pattern]({{ "/en/glossary/mapper-pattern/" | relative_url }}): `Entity → DomainModel → UiState`.

## The Senior Nuance

- A Senior enforces that layers only depend downward: UI → Domain → Data. The data layer never imports UI classes, and the domain layer never imports framework classes (`Context`, `View`, Android SDK types). Dependency inversion (interfaces in domain, implementations in data) enables this.
- In a multi-module Android project, layers often map to Gradle modules: `:core:data`, `:core:domain`, `:feature:tasks:ui`. Module boundaries enforce layer discipline at build time — a compile error is a stronger guarantee than a code review comment.
- The data layer is the only place where [thread safety]({{ "/en/glossary/thread-safety/" | relative_url }}) concerns around I/O should live. Repositories expose `Flow` or `suspend` functions; callers don't need to know whether data comes from Room, Retrofit, or an in-memory cache. This is the single-source-of-truth principle.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
