---
layout: page
title: "UI State Modeling: Sealed vs Flat Data Class"
lang: en
permalink: /en/05-architecture/ui-state-modeling/
order: 1
---

## The Theory (The What)

A screen's UI state is everything the UI needs to draw itself at a given moment. In a [unidirectional data flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}), the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) exposes it as a single [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}), and the UI renders whatever value it receives. There are two dominant ways to model that value:

- **[Sealed state]({{ "/en/glossary/sealed-state/" | relative_url }})**: a [`sealed interface`]({{ "/en/glossary/sealed-interface/" | relative_url }}) (or [`sealed class`]({{ "/en/glossary/sealed-class/" | relative_url }})) where each subtype is one mutually exclusive state of the screen, such as [`Loading`]({{ "/en/glossary/loading-state/" | relative_url }}), [`Success`]({{ "/en/glossary/success-state/" | relative_url }}) and [`Error`]({{ "/en/glossary/error-state/" | relative_url }}). Each subtype carries only the data that makes sense in that state, and a [`when`]({{ "/en/glossary/when-expression/" | relative_url }}) over the state must handle every subtype: if a new one is added, every [`when`]({{ "/en/glossary/when-expression/" | relative_url }}) without an `else` stops compiling until it is handled.
- **[Flat data class]({{ "/en/glossary/flat-data-class/" | relative_url }})**: a single [`data class`]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) with all the screen's properties side by side: flags like `isLoading`, nullable fields like `errorMessage`, and the data itself. Every change produces a new instance with [`copy()`]({{ "/en/glossary/copy/" | relative_url }}), usually inside [`MutableStateFlow.update { }`]({{ "/en/02-coroutines-flow/mutablestateflow-update/" | relative_url }}) so concurrent updates are not lost.

The difference is what the type allows. A [sealed state]({{ "/en/glossary/sealed-state/" | relative_url }}) can only be one of its subtypes at a time, so it **cannot represent impossible combinations**: there is no way to be [`Loading`]({{ "/en/glossary/loading-state/" | relative_url }}) and [`Error`]({{ "/en/glossary/error-state/" | relative_url }}) at once. A [flat data class]({{ "/en/glossary/flat-data-class/" | relative_url }}) can represent any combination of its fields, including ones that make no sense, such as `isLoading = true` with an error message and a list of results, and the compiler will not complain.

The two are not exclusive. A **hybrid** model uses one inside the other: a [flat data class]({{ "/en/glossary/flat-data-class/" | relative_url }}) for the parts of the screen that coexist, with a sealed (often nullable) property for a part that has mutually exclusive variants, or a sealed top-level state whose main subtype is a [flat data class]({{ "/en/glossary/flat-data-class/" | relative_url }}).

## The Senior Perspective (The Why)

- **The question is whether the states really exclude each other.** A detail screen that is either loading, showing an item or showing an error is a textbook [sealed state]({{ "/en/glossary/sealed-state/" | relative_url }}). A list screen with search, filters, selection mode, a form and a background refresh is not: the user can type a search while the list is loaded, select items while a filter is active, and see a non-blocking error while the data is still on screen. Forcing that into `Loading / Loaded / Error` means copying the shared properties into every subtype, or losing them when the state changes (the search query disappears when a refresh goes to [`Loading`]({{ "/en/glossary/loading-state/" | relative_url }})).
- **Sealed buys safety from the compiler; flat buys flexibility at the cost of discipline.** With a [flat data class]({{ "/en/glossary/flat-data-class/" | relative_url }}), nothing prevents an impossible combination, so the code has to: derived properties (`val isEmpty get() = !isLoading && items.isEmpty()`) instead of independent flags that can contradict each other, a single place that changes related fields together, and tests for the transitions. With a [sealed state]({{ "/en/glossary/sealed-state/" | relative_url }}), the transitions are explicit and the compiler checks the handling, but every shared field is duplicated or lifted out.
- **Hybrid is usually the real answer.** The parts that coexist go flat; each part with exclusive variants gets its own sealed type. A pending confirmation, for example, is either "delete" or "archive" or nothing, which is a nullable sealed property inside a flat state. That keeps the safety where states truly exclude each other, without paying for it everywhere.
- **Model one-shot UI as state, then clear it.** A confirmation dialog, or a navigation the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) requests, can be a field in the state that the UI shows and then tells the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) to clear. It survives rotation and [process death]({{ "/en/glossary/process-death/" | relative_url }}) and is easy to test, which is why it is often preferred to a [channel]({{ "/en/glossary/channel/" | relative_url }}) of [events]({{ "/en/glossary/one-shot-event/" | relative_url }}).
- **Update atomically.** A flat state is updated by copying the current value. `_state.value = _state.value.copy(...)` reads and writes in two steps, so two concurrent updates can overwrite each other. [`update { it.copy(...) }`]({{ "/en/02-coroutines-flow/mutablestateflow-update/" | relative_url }}) retries until the change is applied to the latest value.
- **The model affects Compose too.** Each [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}) compares the parameters it receives. Passing a whole flat state to every composable makes them all depend on all of it; passing only the fields each one needs, and keeping unchanged collections as the same instances when copying, lets Compose skip the rest.

### Decision Rule

| Screen | Recommended model |
|--------|-------------------|
| Simple flow (load → show → error) | [Sealed interface]({{ "/en/glossary/sealed-interface/" | relative_url }}) |
| Complex screen (search + filters + selection + forms) | [Flat data class]({{ "/en/glossary/flat-data-class/" | relative_url }}) |
| Shared parts plus a few exclusive variants | Hybrid: [flat data class]({{ "/en/glossary/flat-data-class/" | relative_url }}) with sealed properties |

## Code in Action

```kotlin
// Not found in FAS — standalone example
// Sealed state for a screen whose states truly exclude each other.
sealed interface DetailState {
    data object Loading : DetailState
    data class Success(val task: Task) : DetailState
    data class Error(val message: String) : DetailState
}

@Composable
fun DetailScreen(state: DetailState) {
    when (state) {                       // no else: a new subtype will not compile until handled
        DetailState.Loading -> Loader()
        is DetailState.Success -> TaskDetail(state.task)
        is DetailState.Error -> ErrorMessage(state.message)
    }
}

// From FollowApp Suite — TasksUiState.kt
// Flat data class for a screen whose concerns overlap: loading, search,
// selection and the form coexist. Derived properties replace flags that could
// contradict each other.
data class TasksUiState(
    val isLoading: Boolean = true,
    val activeTasks: List<Task> = emptyList(),
    @StringRes val errorMessageRes: Int? = null,
    val isFormVisible: Boolean = false,
    val searchQuery: String = "",
    val isSearchActive: Boolean = false,
    // ... 30+ properties that coexist
    val pendingCascadeAction: CascadeAction? = null,
    val selectedTaskIds: Set<String> = emptySet(),
) {
    val isSelectionMode: Boolean get() = selectedTaskIds.isNotEmpty()
}

// From FollowApp Suite — TasksUiState.kt
// The hybrid part: a confirmation is either Complete, Archive or Delete, never
// two at once, so it is a sealed type. It lives in the flat state as a nullable
// property: null means no dialog.
sealed class CascadeAction {
    abstract val taskId: String
    abstract val childCount: Int

    data class Complete(override val taskId: String, val isCompleted: Boolean, override val childCount: Int) : CascadeAction()
    data class Archive(override val taskId: String, override val childCount: Int) : CascadeAction()
    data class Delete(override val taskId: String, override val childCount: Int) : CascadeAction()
}

// From FollowApp Suite — TasksViewModel.kt
// The dialog is state: setting the property shows it, clearing it hides it.
// The when over the sealed type must handle every action.
fun onCascadeConfirmed() {
    val action = _uiState.value.pendingCascadeAction ?: return
    _uiState.update { it.copy(pendingCascadeAction = null) }
    viewModelScope.launch {
        when (action) {
            is CascadeAction.Complete -> {
                quickCompleteTaskUseCase(taskId = action.taskId, isCompleted = action.isCompleted, cascade = true)
            }
            is CascadeAction.Archive -> {
                archiveTaskUseCase(action.taskId, cascade = true)
                onFormDismissed()
            }
            is CascadeAction.Delete -> {
                moveTaskToTrashUseCase(action.taskId, cascade = true)
                onFormDismissed()
            }
        }
    }
}

fun onCascadeDismissed() {
    _uiState.update { it.copy(pendingCascadeAction = null) }
}
```

## The Interview (The Hot Seat)

**Question**: Your team is building a task management screen with search, filters, bulk selection, inline editing and a loading indicator. A colleague proposes modeling the UI state as `sealed interface TasksState { Loading, Loaded, Error }`. What is your recommendation and why?

**Senior Answer**: I would use a [flat data class]({{ "/en/glossary/flat-data-class/" | relative_url }}) for this screen, with sealed types only for the parts that are really exclusive. A [sealed state]({{ "/en/glossary/sealed-state/" | relative_url }}) assumes the screen is in exactly one state at a time, but here the concerns overlap: the user can search while the data is loaded, select tasks while a filter is active, and see a non-blocking error while the list is still visible. With `Loading / Loaded / Error`, the search query, the selection and the filters would have to be copied into every subtype, or they would be lost on every transition: a refresh that moves to [`Loading`]({{ "/en/glossary/loading-state/" | relative_url }}) would clear the search. A [flat data class]({{ "/en/glossary/flat-data-class/" | relative_url }}) lets each concern change independently with [`copy()`]({{ "/en/glossary/copy/" | relative_url }}) inside [`update { }`]({{ "/en/02-coroutines-flow/mutablestateflow-update/" | relative_url }}). The price is that the compiler no longer prevents impossible combinations, so I avoid independent flags that can contradict each other, prefer derived properties, and test the transitions. Where the screen does have exclusive variants, such as a pending confirmation that is either delete or archive, I model that part as a sealed type inside the flat state. A [sealed state]({{ "/en/glossary/sealed-state/" | relative_url }}) for the whole screen is the right choice for simpler screens with a clear load, content or error flow, like a detail page.

**Question**: The [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) needs the user to confirm a destructive action before running it. How do you model that in the UI state?

**Senior Answer**: As state, with a nullable property that holds what is pending: `pendingAction: ConfirmAction? = null`. If there are several kinds of action, `ConfirmAction` is a sealed type, because a pending confirmation is exactly one of them. When the user starts the action, the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) sets the property and the UI shows the dialog because the value is not [null]({{ "/en/glossary/null/" | relative_url }}). Confirming calls the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}), which clears the property and runs the action with a [`when`]({{ "/en/glossary/when-expression/" | relative_url }}) over the sealed type, so a new kind of action cannot be added without handling it. Dismissing just clears it. Modeling it as state instead of a one-shot [event]({{ "/en/glossary/one-shot-event/" | relative_url }}) means the dialog survives a rotation, and with [saved state]({{ "/en/glossary/saved-instance-state/" | relative_url }}) even [process death]({{ "/en/glossary/process-death/" | relative_url }}); it cannot be delivered twice or lost while the screen is in the background; and a test only has to check the state after each call. The UI stays a function of the state, which is the whole point of a single state with [unidirectional data flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}).

---

[Back to Chapters]({{ "/" | relative_url }})
