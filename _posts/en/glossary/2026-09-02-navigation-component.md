---
layout: post
title: "Navigation Component"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/navigation-component/
---

## The Theory (The What)

The **Navigation Component** is a Jetpack library that manages in-app navigation — moving between screens, handling the back stack, passing arguments, and deep linking. It provides a `NavController` that orchestrates navigation actions, a `NavHost` that hosts the current destination, and a navigation graph that declares all possible routes. In [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}), navigation is declared via `NavHost { composable("route") { ... } }`.

## The Senior Nuance

- **Type-safe arguments**: [Safe Args]({{ "/en/glossary/safe-args/" | relative_url }}) generates type-safe classes for passing data between destinations. This moves argument parsing from [runtime]({{ "/en/glossary/runtime/" | relative_url }}) string matching to [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) checked code — no more `getStringExtra("key")` crashes.
- **Single Activity architecture**: Navigation Component is designed for single-Activity apps where all screens are Fragments or Compose destinations. The Activity hosts the `NavHost`; the `NavController` manages the back stack.
- **Deep linking**: The navigation graph can declare deep link URIs. When the system resolves a matching URI, Navigation Component opens the correct destination with the right arguments — no manual intent parsing.
- **Compose Navigation**: In Compose, routes are string-based by default (`"profile/{userId}"`). Type-safe navigation with Kotlin serialization is the recommended approach in newer versions, eliminating the string-based route system.
- **Back stack management**: `NavController.popBackStack()`, `navigate(route) { popUpTo(...) }`, and `launchSingleTop = true` control back stack behavior. Mismanaging these leads to duplicate destinations or lost state.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
