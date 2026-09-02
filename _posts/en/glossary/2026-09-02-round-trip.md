---
layout: post
title: "Round-Trip"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/round-trip/
---

## The Theory (The What)

A **round-trip** is a complete request-response cycle between two system boundaries — typically between the UI layer and a data source (database, network API, or file system). The request travels "out" to the data source and the response travels "back," hence "round-trip." The time this takes is the **round-trip time (RTT)**, and it is often the dominant factor in perceived UI latency.

```
UI ──request──▶ Repository ──query──▶ Database
UI ◀──response── Repository ◀──result── Database
         └───────── round-trip ─────────┘
```

In Android, minimizing round-trips is a core performance strategy: every database query, network call, or IPC (inter-process communication) adds latency that can cause frame drops or loading spinners.

## The Senior Nuance

- **Optimistic updates** eliminate the perceived round-trip by updating the UI immediately with the expected result, then confirming with the data source in the background. If the data source disagrees, the UI rolls back. This pattern — used in FAS's `updateSelectedTasksOptimistically` — makes the app feel instant even with slow backends.
- **Batching** reduces round-trips by combining multiple operations into a single request. Instead of N individual database inserts, use a single transaction. Instead of N API calls, use a batch endpoint. The savings are proportional to the number of avoided trips.
- In offline-first architectures (Room + WorkManager), the "round-trip" to the local database is milliseconds, while the network round-trip may be seconds or infinite (offline). Separating these two round-trips — fast local read, eventual network sync — is the foundation of responsive Android apps.
- **Caching** is round-trip avoidance: if the data is already in memory or in a local database, the round-trip to the network is eliminated entirely. Kotlin's `StateFlow` acts as an in-memory cache — downstream collectors read the cached value instantly, with zero round-trip.
- In Compose, unnecessary recomposition is a kind of "internal round-trip" — the UI re-renders without any data actually changing. Stable types and `remember {}` avoid this wasted work.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
