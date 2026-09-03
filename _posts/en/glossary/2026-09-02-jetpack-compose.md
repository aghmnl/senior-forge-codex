---
layout: post
title: "Jetpack Compose"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/jetpack-compose/
---

## The Theory (The What)

**Jetpack Compose** is Android's modern declarative UI toolkit. Instead of building views imperatively (create object → mutate state → invalidate), you describe *what* the screen should look like for a given state, and the framework handles rendering, diffing, and updates. Compose is a Kotlin [DSL]({{ "/en/glossary/dsl/" | relative_url }}): every `@Composable` function is a [higher-order function]({{ "/en/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) that accepts a `content` [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) with a [receiver type]({{ "/en/glossary/receiver-type/" | relative_url }}) — `ColumnScope.() -> Unit`, `RowScope.() -> Unit` — so that only the methods valid inside that layout are available.

```kotlin
// From FollowApp Suite — ConfirmationDialog.kt
@Composable
fun ConfirmationDialog(
    title: String,
    message: String,
    confirmLabel: String,
    dismissLabel: String,
    onConfirm: (dontAskAgain: Boolean) -> Unit,
    onDismiss: () -> Unit,
    dontAskAgainLabel: String? = null,
) {
    var dontAskAgain by remember { mutableStateOf(false) }
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(title) },
        text = {
            Column {
                Text(message)
                if (dontAskAgainLabel != null) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { dontAskAgain = !dontAskAgain }
                            .padding(top = 16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Checkbox(
                            checked = dontAskAgain,
                            onCheckedChange = { dontAskAgain = it }
                        )
                        Text(dontAskAgainLabel, style = MaterialTheme.typography.bodyMedium)
                    }
                }
            }
        },
        confirmButton = {
            TextButton(onClick = { onConfirm(dontAskAgain) }) { Text(confirmLabel) }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text(dismissLabel) }
        }
    )
}
```

## The Senior Nuance

- Compose is a [DSL]({{ "/en/glossary/dsl/" | relative_url }}) built on [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) with [receivers]({{ "/en/glossary/receiver-type/" | relative_url }}). The `@LayoutScopeMarker` annotation acts as a `@DslMarker` to prevent [scope]({{ "/en/glossary/scope/" | relative_url }}) leakage — you cannot call `Column`'s `Modifier.weight()` inside a `Row`. This is [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) safety that XML layouts never had.
- The Compose compiler plugin transforms `@Composable` functions at [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) level — it adds hidden `Composer` and `$changed` parameters that enable recomposition tracking. This is not standard Kotlin; the `@Composable` annotation is a compiler contract, not just metadata.
- Compose's `Modifier` chain is a fluent API whose **order matters**: `.padding(16.dp).background(Color.Red)` pads then colors, `.background(Color.Red).padding(16.dp)` colors then pads. Understanding this is a common interview differentiator.
- Unlike XML-based views, Compose does not use [inheritance]({{ "/en/glossary/inheritance/" | relative_url }}) for layout. Every UI element is a function, and composition replaces inheritance — a fundamental shift that aligns with the favor-composition-over-inheritance principle.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
