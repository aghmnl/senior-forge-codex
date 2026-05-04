---
layout: page
title: Lateinit vs Lazy
lang: en
permalink: /en/01-kotlin-core/lateinit-vs-lazy/
---

## The Theory (The What)

Both `lateinit` and `lazy` provide ways to delay property initialization, but they serve different technical purposes. `lateinit` is a modifier for mutable variables (`var`) that are non-nullable and will be initialized later (often by a framework like Dagger or during a lifecycle event). `lazy` is a delegated property for read-only variables (`val`) that computes the value only upon its first access and caches the result for future use.

## The Senior Perspective (The Why)

Choosing between them is a matter of **mutability, thread safety, and ownership**.

- **Thread Safety Modes**: By default, `lazy` is thread-safe (`LazyThreadSafetyMode.SYNCHRONIZED`). A Senior knows when to use `NONE` for performance optimization if the property is accessed only from a single thread (e.g., the UI thread), or `PUBLICATION` if multiple threads can compute the value.
- **Dependency Injection**: `lateinit` is essential for field injection (Hilt/Dagger). Since these frameworks use reflection to set values after the object is constructed, `lateinit` allows for non-nullable types without boilerplate null-checks.
- **Memory Management**: `lazy` is ideal for "heavy" objects (like expensive database queries or complex ViewModels) because it defers memory allocation until strictly necessary.
- **Property State Check**: A Senior uses `.isInitialized` on `lateinit` properties to avoid `UninitializedPropertyAccessException` when the initialization flow might be non-linear or conditional.

## Code in Action

```kotlin
// Senior approach: Choosing between lazy for resources and lateinit for injection
class ProductDetailViewModel(
    private val repository: ProductRepository // Injected via constructor
) {
    // Injected by framework later
    lateinit var analyticsTracker: AnalyticsTracker

    // Computed only when accessed (e.g., when the UI requests it)
    val heavyDataDetails: List<String> by lazy(LazyThreadSafetyMode.NONE) {
        repository.getExpensiveMetadata()
    }

    fun onStart() {
        if (::analyticsTracker.isInitialized) {
            analyticsTracker.trackScreenView("ProductDetail")
        }
    }
}
```

## Interview Prep (The Hot Seat)

**Question**: What happens internally when you access a lazy property for the first time, and how does it differ from a lateinit property in terms of bytecode?

**Senior Answer**: When a lazy property is accessed, the delegated getValue() method is called. It checks an internal _value field; if it's the UNINITIALIZED_VALUE sentinel, it executes the lambda within a synchronized block (by default) to ensure thread safety, then stores and returns the result. In contrast, lateinit does not use delegation; the compiler simply generates a direct field access but adds a null-check at the bytecode level that throws an UninitializedPropertyAccessException if the backing field is null.

---

[Back to Chapters]({{ "/" | relative_url }})
