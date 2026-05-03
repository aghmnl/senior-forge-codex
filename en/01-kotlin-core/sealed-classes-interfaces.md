---
layout: page
title: Sealed Classes & Interfaces
lang: en
---

# Sealed Classes & Interfaces

## The Theory (The What)
Sealed Classes and Interfaces represent restricted class hierarchies where all subclasses are known at compile time. This restriction provides the compiler with a complete list of all possible subtypes, enabling exhaustive `when` expressions without the need for a default `else` branch. While sealed classes can hold state through properties, sealed interfaces (introduced in Kotlin 1.5) offer enhanced flexibility, allowing a single class to implement multiple sealed hierarchies.

## The Senior Perspective (The Why)
A Senior Engineer values these structures for state robustness and long-term maintainability.

*   **Compile-time Safety**: By avoiding the `else` block in `when` statements, we force the compiler to flag errors if a new state (e.g., a specific API error) is added in the future but not handled in the UI logic.
*   **Memory Efficiency**: Using `data object` for stateless members (like `Loading` or `Idle`) is a best practice to prevent redundant object allocations while gaining built-in `equals` and `toString` support.
*   **Architectural Foundation**: They are the essential building blocks for MVI (Model-View-Intent), ensuring the UI reacts to a Single Source of Truth in a predictable manner.

## Code in Action
```kotlin
// UI State modeling following Senior principles
sealed interface UIState {
    data object Loading : UIState // Using data object for memory efficiency
    data class Success(val items: List<String>) : UIState
    data class Error(val exception: Throwable) : UIState
}

// The compiler ensures all cases are covered
fun handleState(state: UIState) {
    when (state) {
        UIState.Loading -> startShimmer()
        is UIState.Success -> display(state.items) // Automatic smart casting
        is UIState.Error -> log(state.exception.message)
    }
}
```

## Interview Prep (The Hot Seat)
**Question**: What is the primary advantage of a Sealed Interface over an Abstract Class in a restricted hierarchy?

**Senior Answer**: The primary advantage is flexibility. A class can implement multiple Sealed Interfaces, allowing it to belong to different restricted hierarchies simultaneously. Additionally, interfaces are more lightweight as they don't force a specific constructor or internal state management onto the subclasses.

---
[Back to Chapters]({{ "/" | relative_url }})
