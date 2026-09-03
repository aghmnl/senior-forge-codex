---
layout: post
title: "Single Responsibility Principle"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/single-responsibility-principle/
---

## The Theory (The What)

The **Single Responsibility Principle (SRP)** states that a class (or module, or function) should have only one reason to change — meaning it should encapsulate exactly one responsibility. It is the "S" in the SOLID principles. In practice, SRP means that a class that handles both data persistence and UI formatting is doing too much: changes to the database schema shouldn't force changes to the UI layer, and vice versa.

In Kotlin and Android, SRP manifests at every layer: ViewModels handle state management (not data fetching), Repositories handle data access (not business logic), and Use Cases encapsulate single business operations.

## The Senior Nuance

- **SRP is about cohesion, not size**: A class with 500 lines that all serve one purpose follows SRP better than a 50-line class that mixes two unrelated concerns. The question is "what would cause this to change?" — if the answer is two different stakeholders or two different reasons, the class has two responsibilities.
- **In Android architecture**: The Repository pattern exists because of SRP — data access logic (Room, Retrofit) is separated from business logic (Use Cases) and presentation logic (ViewModels). [Hilt]({{ "/en/glossary/hilt/" | relative_url }}) and [dependency graphs]({{ "/en/glossary/dependency-graph/" | relative_url }}) make this layering practical by wiring the pieces together.
- **At function level**: Kotlin's scope functions enforce a micro-level SRP — `also` handles side effects (logging, caching) separately from the main transformation chain, keeping each step focused on one task. This is why senior developers prefer `also` for side effects rather than mixing them into `apply` or `let` blocks.
- **Over-application warning**: Splitting responsibilities too aggressively leads to "ravioli code" — dozens of tiny classes that individually do one thing but collectively obscure the flow. Senior engineers balance SRP against readability: if two responsibilities always change together, they might belong in the same class.
- **Testing signal**: If a class is hard to test because it requires many mocks from unrelated domains (a database mock AND a network mock AND a UI framework mock), that's a sign it violates SRP. Well-separated responsibilities lead to focused, easy-to-write tests.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
