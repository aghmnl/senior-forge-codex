---
layout: post
title: "SQLiteConstraintException"
date: 2026-09-23 12:00:00 +0000
categories: [en, glossary]
tags: [error-handling, persistence]
lang: en
permalink: /en/glossary/sqlite-constraint-exception/
---

## The Theory (The What)

**`SQLiteConstraintException`** is thrown when a write violates a schema constraint: a `UNIQUE` index, a `NOT NULL` column, a foreign key. In [Room]({{ "/en/glossary/room/" | relative_url }}) it surfaces from an `@Insert` or `@Update` whose data breaks a rule the database enforces — a duplicate tag name, an orphan row. It is a [`RuntimeException`]({{ "/en/glossary/runtime-exception/" | relative_url }}), so nothing forces you to handle it, and it is the textbook case of a technical exception that carries information worth preserving all the way to the UI boundary.

```kotlin
// From FollowApp Suite — ErrorMapping.kt
// Translated once, at the UI boundary: the constraint becomes a real message
fun Throwable.toUserMessage(): Int = when {
    this is SQLiteConstraintException && message.orEmpty().contains("UNIQUE") ->
        R.string.error_duplicate_tag
    else -> R.string.error_generic
}
```

## The Senior Nuance

- **Do not swallow it in the repository.** "Something went wrong" is what is left after the data layer throws away the only detail the user could act on: *this name is already taken*.
- **It is a validation signal, not always a bug.** A `UNIQUE` violation on a user-entered name is expected input, so the UI should present it as a form error rather than a crash report.
- **Matching on the message is fragile but pragmatic.** There is no typed "which constraint" API, so checking for `UNIQUE` in the message is the common workaround — worth a comment, and worth a test.
- See [Error Handling: try-catch & .catch]({{ "/en/02-coroutines-flow/error-handling/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
