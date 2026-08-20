---
layout: page
title: "UI State Modeling: Sealed vs Flat Data Class"
lang: en
permalink: /en/05-architecture/ui-state-modeling/
---

## The Theory (The What)

In Android UI architecture, there are two dominant strategies to model the state of a screen:

- **Sealed State**: A `sealed interface` (or `sealed class`) where each subtype represents a mutually exclusive screen state (Loading, Success, Error). The compiler enforces exhaustive handling via `when`.
- **Flat Data Class**: A single `data class` with boolean flags and nullable fields (`isLoading`, `errorMessage`, `data`). State transitions happen via `.copy()`.

Both approaches are valid. The choice depends on the complexity of the screen and whether states are truly mutually exclusive.

## The Senior Perspective (The Why)

This is a common Senior interview topic because it tests architectural judgment, not just syntax knowledge.

- **Sealed State** shines when states are **mutually exclusive**: a screen is either loading, showing data, or showing an error — never two at once. The type system makes **impossible states unrepresentable**. A `when` block without an `else` will fail to compile if a new state is added, forcing the developer to handle it everywhere.

- **Flat Data Class** shines when states **overlap**: a screen can be loading *and* showing cached data, or showing data *and* a non-blocking error toast. Real-world screens with search, filters, selection mode, and forms often have 20+ properties that coexist. With a sealed approach, shared properties would need to be duplicated across subtypes or extracted into a common base — adding boilerplate without benefit.

- **The risk of Flat**: it can represent **impossible states** that the compiler won't catch (e.g., `isLoading = true` *and* `errorMessage != null` *and* a non-empty list). The discipline falls on the developer, not the type system.

- **The risk of Sealed**: it can lead to **property duplication** and awkward transitions when a screen has many shared fields across states.

### Decision Rule

| Screen Complexity | Recommended Approach |
|-------------------|---------------------|
| Simple flow (load → show → error) | Sealed interface |
| Complex screen (filters + search + selection + forms) | Flat data class |
| Hybrid | Sealed for top-level state + flat data class per subtype |

## Code in Action

```kotlin
// ── Approach 1: Sealed State ──
// Best for simple, mutually exclusive states
sealed interface ScreenState {
    data object Loading : ScreenState
    data class Success(val items: List<String>) : ScreenState
    data class Error(val message: String) : ScreenState
}

fun render(state: ScreenState) {
    when (state) {
        ScreenState.Loading -> showLoader()
        is ScreenState.Success -> showData(state.items)
        is ScreenState.Error -> showError(state.message)
    }
}

// ── Approach 2: Flat Data Class ──
// Best for complex screens with overlapping concerns
// Real example from FollowApp Suite: TasksUiState
data class TasksUiState(
    val isLoading: Boolean = true,
    val activeTasks: List<Task> = emptyList(),
    val errorMessageRes: Int? = null,
    val searchQuery: String = "",
    val isSearchActive: Boolean = false,
    val selectedTaskIds: Set<String> = emptySet(),
    val isFormVisible: Boolean = false,
    // ... 30+ properties coexisting
) {
    val isSelectionMode: Boolean get() = selectedTaskIds.isNotEmpty()
}

// State update is a single .copy() call
fun onSearchQueryChanged(query: String) {
    _uiState.update { it.copy(searchQuery = query) }
}
```

## Interview Prep (The Hot Seat)

**Question**: Your team is building a task management screen with search, filters, bulk selection, inline editing, and a loading indicator. A colleague proposes modeling the UI state as `sealed interface TasksState { Loading, Loaded, Error }`. What is your recommendation and why?

**Senior Answer**: I would recommend a flat `data class` for this screen. The sealed approach assumes mutually exclusive states, but this screen has overlapping concerns: the user can be searching *while* data is loaded, selecting tasks *while* a filter is active, and seeing a toast error *while* the list is still visible. A sealed hierarchy would force us to either duplicate shared properties across subtypes (searchQuery, selectedTaskIds, filters) or nest a common data class inside each — both add boilerplate without real safety gains. The flat data class lets us update any property independently via `.copy()`, which scales naturally as the screen grows. The sealed approach is better suited for simpler screens with a clear loading-to-content flow, like a detail page or an onboarding wizard.

---

[Back to Chapters]({{ "/" | relative_url }})
