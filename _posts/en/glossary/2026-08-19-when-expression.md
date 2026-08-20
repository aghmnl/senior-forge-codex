---
layout: post
title: "when Expression"
date: 2026-08-19 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/when-expression/
---

## The Theory (The What)

The **`when` expression** in Kotlin is a powerful control-flow construct that replaces Java's `switch` statement with a more expressive and safer alternative. Unlike `switch`, `when` can match against arbitrary expressions (not just constants), supports pattern matching with `is` (enabling [smart casts]({{ "/en/glossary/smart-cast/" | relative_url }})), ranges (`in 1..10`), collections (`in listOf(...)`), and multiple conditions per branch. When used as an expression (assigned to a variable or returned), the compiler enforces exhaustiveness — all possible cases must be handled.

## The Senior Nuance

- **Exhaustive `when` + Sealed Classes**: When the subject is a [sealed class or interface]({{ "/en/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}), the compiler knows all subtypes and enforces that every branch is covered — no `else` needed. This is a compile-time safety net: if a new subtype is added later, every `when` that handles that sealed type will fail to compile until updated.
- **Expression vs. Statement**: `when` as a statement does not require exhaustiveness. `when` as an expression (e.g., `val result = when(x) { ... }`) does. Senior code prefers the expression form to get the exhaustiveness guarantee.
- **No Fall-Through**: Unlike Java's `switch`, Kotlin's `when` has no fall-through between branches. Each branch is independent, eliminating an entire class of bugs caused by missing `break` statements.
- **Performance**: The compiler optimizes `when` over enums and sealed classes into efficient `tableswitch` or `lookupswitch` bytecode instructions, making it as fast as Java's `switch`.

```kotlin
sealed interface PaymentMethod {
    data class CreditCard(val last4: String) : PaymentMethod
    data class BankTransfer(val bankName: String) : PaymentMethod
    data object Cash : PaymentMethod
}

// Exhaustive when expression — compiler enforces all branches
fun describe(method: PaymentMethod): String = when (method) {
    is PaymentMethod.CreditCard -> "Card ending in ${method.last4}"
    is PaymentMethod.BankTransfer -> "Transfer from ${method.bankName}"
    PaymentMethod.Cash -> "Cash payment"
}
```

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
