---
layout: post
title: "Design System"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, architecture]
lang: en
permalink: /en/glossary/design-system/
---

## The Theory (The What)

A **design system** is the shared set of visual rules and reusable components of a product: colors, typography, spacing and shapes (usually a Compose theme), plus components like buttons, chips, cards and inputs that every screen uses. In a modular Android app it often lives in its own module, such as `core:designsystem`.

## The Senior Nuance

- **Its components must be [stateless]({{ "/en/glossary/stateful-stateless/" | relative_url }}) or support [controlled]({{ "/en/glossary/controlled-uncontrolled/" | relative_url }}) mode**, because they cannot know the business rules of the screens that use them.
- **It must not depend on feature or domain code.** A component that imports a domain entity can no longer be reused; generic parameters and [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) keep it independent.
- See [State Hoisting]({{ "/en/03-jetpack-compose/state-hoisting/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
