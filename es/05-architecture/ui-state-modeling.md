---
layout: page
title: "Modelado de Estado de UI: Sealed vs Data Class Plano"
lang: es
permalink: /es/05-architecture/ui-state-modeling/
---

## The Theory (El Qué)

En la arquitectura de UI en Android, existen dos estrategias dominantes para modelar el estado de una pantalla:

- **Estado Sealed**: Una `sealed interface` (o `sealed class`) donde cada subtipo representa un estado de pantalla mutuamente excluyente (Loading, Success, Error). El compilador garantiza el manejo exhaustivo mediante `when`.
- **Data Class Plano**: Una única `data class` con flags booleanos y campos nullables (`isLoading`, `errorMessage`, `data`). Las transiciones de estado ocurren mediante `.copy()`.

Ambos enfoques son válidos. La elección depende de la complejidad de la pantalla y de si los estados son realmente mutuamente excluyentes.

## The Senior Perspective (El Porqué)

Este es un tema común en entrevistas Senior porque evalúa criterio arquitectónico, no solo conocimiento de sintaxis.

- **Estado Sealed** brilla cuando los estados son **mutuamente excluyentes**: una pantalla está cargando, mostrando datos, o mostrando un error — nunca dos a la vez. El sistema de tipos hace que los **estados imposibles sean irrepresentables**. Un bloque `when` sin `else` no compilará si se agrega un nuevo estado, forzando al desarrollador a manejarlo en todos los puntos.

- **Data Class Plano** brilla cuando los estados **se superponen**: una pantalla puede estar cargando *y* mostrando datos cacheados, o mostrando datos *y* un toast de error no bloqueante. Las pantallas del mundo real con búsqueda, filtros, modo selección y formularios suelen tener 20+ propiedades que coexisten. Con un enfoque sealed, las propiedades compartidas tendrían que duplicarse entre subtipos o extraerse en una base común — agregando boilerplate sin beneficio real.

- **El riesgo del Plano**: puede representar **estados imposibles** que el compilador no detectará (ej: `isLoading = true` *y* `errorMessage != null` *y* una lista no vacía). La disciplina recae en el desarrollador, no en el sistema de tipos.

- **El riesgo del Sealed**: puede llevar a **duplicación de propiedades** y transiciones incómodas cuando una pantalla tiene muchos campos compartidos entre estados.

### Regla de Decisión

| Complejidad de Pantalla | Enfoque Recomendado |
|------------------------|---------------------|
| Flujo simple (cargar → mostrar → error) | Sealed interface |
| Pantalla compleja (filtros + búsqueda + selección + formularios) | Data class plano |
| Híbrido | Sealed para estado principal + data class plano por subtipo |

## Code in Action

```kotlin
// ── Enfoque 1: Estado Sealed ──
// Ideal para estados simples y mutuamente excluyentes
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

// ── Enfoque 2: Data Class Plano ──
// Ideal para pantallas complejas con concerns superpuestos
// Ejemplo real de FollowApp Suite: TasksUiState
data class TasksUiState(
    val isLoading: Boolean = true,
    val activeTasks: List<Task> = emptyList(),
    val errorMessageRes: Int? = null,
    val searchQuery: String = "",
    val isSearchActive: Boolean = false,
    val selectedTaskIds: Set<String> = emptySet(),
    val isFormVisible: Boolean = false,
    // ... 30+ propiedades coexistiendo
) {
    val isSelectionMode: Boolean get() = selectedTaskIds.isNotEmpty()
}

// Actualización de estado con un único .copy()
fun onSearchQueryChanged(query: String) {
    _uiState.update { it.copy(searchQuery = query) }
}
```

## Preparación para Entrevistas (En el banquillo)

**Pregunta**: Tu equipo está construyendo una pantalla de gestión de tareas con búsqueda, filtros, selección masiva, edición inline y un indicador de carga. Un colega propone modelar el estado de UI como `sealed interface TasksState { Loading, Loaded, Error }`. ¿Cuál es tu recomendación y por qué?

**Respuesta Senior**: Recomendaría un `data class` plano para esta pantalla. El enfoque sealed asume estados mutuamente excluyentes, pero esta pantalla tiene concerns superpuestos: el usuario puede estar buscando *mientras* los datos están cargados, seleccionando tareas *mientras* un filtro está activo, y viendo un toast de error *mientras* la lista sigue visible. Una jerarquía sealed nos forzaría a duplicar propiedades compartidas entre subtipos (searchQuery, selectedTaskIds, filtros) o anidar un data class común dentro de cada uno — ambas opciones agregan boilerplate sin ganancias reales de seguridad. El data class plano nos permite actualizar cualquier propiedad independientemente mediante `.copy()`, lo cual escala naturalmente a medida que la pantalla crece. El enfoque sealed es más adecuado para pantallas más simples con un flujo claro de carga-a-contenido, como una página de detalle o un wizard de onboarding.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
