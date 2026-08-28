---
layout: page
title: "Null Safety: Elvis y Safe Calls"
lang: es
permalink: /es/01-kotlin-core/null-safety-elvis-safe-calls/
order: 1
---

## La Teoría (El Qué)

El sistema de tipos de Kotlin distingue entre tipos nullable (`String?`) y no-nullable (`String`) en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}). Esto elimina la mayoría de los crashes por [NullPointerException]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) que afectan a las bases de código Java. Los operadores clave son:

- **[Safe call]({{ "/es/glosario/safe-call/" | relative_url }}) (`?.`)**: Accede a un miembro solo si el receptor no es null; devuelve `null` en caso contrario.
- **Operador Elvis (`?:`)**: Proporciona un valor de respaldo cuando el lado izquierdo es `null`.
- **[Assertion]({{ "/es/glosario/assertion/" | relative_url }}) de no-null (`!!`)**: Fuerza un tipo nullable a no-nullable, lanzando [NullPointerException]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) si es `null`. **No debería usarse nunca en código de producción.**
- **[Cast]({{ "/es/glosario/cast/" | relative_url }}) seguro (`as?`)**: Intenta un cast y devuelve `null` en caso de fallo en lugar de lanzar [ClassCastException]({{ "/es/glosario/class-cast-exception/" | relative_url }}).

## La Perspectiva Senior (El Por Qué)

Para un Desarrollador Senior, la null safety no es [syntax sugar]({{ "/es/glosario/syntax-sugar/" | relative_url }}) — es una herramienta de diseño que codifica invariantes del dominio en el sistema de tipos.

- **Null Significa Algo**: Un tipo de retorno `String?` es un contrato: "este valor podría estar legítimamente ausente." Un Senior usa tipos nullable para expresar opcionalidad (la URL de foto de un usuario) y tipos no-nullable para expresar garantías (el email de un usuario). Elegir la nullabilidad incorrecta filtra ambigüedad del dominio a cada consumidor.
- **`!!` No Debería Usarse Nunca**: Cada `!!` es una afirmación de que el desarrollador sabe más que el compilador — y casi siempre es incorrecto o perezoso. Produce una [NullPointerException]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) genérica sin contexto, haciendo el [stack trace]({{ "/es/glosario/stack-trace/" | relative_url }}) inútil para debugging. Siempre existe una alternativa mejor (ver estrategias abajo).
- **Platform Types**: Los valores de APIs Java llegan como "platform types" (`String!`) — ni nullable ni no-nullable. Un Senior anota los límites de interop con Java usando `@Nullable`/`@NonNull` o los envuelve en funciones Kotlin que declaran nullabilidad explícita, previniendo la propagación silenciosa de NullPointerException.
- **Early Return con Elvis**: El patrón `?: return` es la [guard clause]({{ "/es/glosario/guard-clause/" | relative_url }}) idiomática que elimina la nullabilidad del resto del [scope]({{ "/es/glosario/scope/" | relative_url }}) de la función, manteniendo el camino feliz plano y legible.

### Estrategias para eliminar `!!`

1. **Rediseñar el flujo de datos** para que el valor sea no-nullable desde el inicio — usar inyección por constructor en lugar de asignación tardía, o mover la verificación de null al llamador.
2. **Usar Elvis con una excepción explícita** (`?: throw IllegalStateException("razón")`) para que el stack trace explique qué invariante se violó.
3. **Usar [safe calls]({{ "/es/glosario/safe-call/" | relative_url }}) con `let`, `run`, o early return** (`?: return`) para manejar el caso null explícitamente en el flujo de control.

El objetivo es hacer las decisiones de nullabilidad visibles en el sistema de tipos, no esconderlas detrás de [assertions]({{ "/es/glosario/assertion/" | relative_url }}).

## Código en Acción

```kotlin
// De FollowApp Suite — BillingConnector
// Guard clause con Elvis: elimina null del resto del scope
fun launchPurchase(activity: Activity): Boolean {
    val details = productDetails ?: return false
    val params = BillingFlowParams.newBuilder()
        .setProductDetailsParamsList(
            listOf(
                BillingFlowParams.ProductDetailsParams.newBuilder()
                    .setProductDetails(details)
                    .build()
            )
        )
        .build()
    return billingClient.launchBillingFlow(activity, params)
        .responseCode == BillingClient.BillingResponseCode.OK
}

// De FollowApp Suite — AuthPreferences
// Safe call + let + Elvis: guardar cuando está presente, eliminar cuando ausente
fun saveSession(session: UserSession, prefs: MutablePreferences) {
    session.photoUrl?.let { prefs[photoUrlKey] = it }
        ?: prefs.remove(photoUrlKey)
}

// De FollowApp Suite — PresetRepositoryImpl
// Elvis para defaults: fallback seguro en producción
fun resolvePosition(existing: Preset?): Int {
    return existing?.position ?: dao.nextPosition()
}

// De FollowApp Suite — TasksViewModel
// Guard clause + smart cast en sealed hierarchy
fun onCascadeConfirmed() {
    val action = _uiState.value.pendingCascadeAction ?: return
    _uiState.update { it.copy(pendingCascadeAction = null) }
    viewModelScope.launch {
        when (action) {
            is CascadeAction.Complete -> {
                quickCompleteTaskUseCase(
                    taskId = action.taskId,
                    isCompleted = action.isCompleted,
                    cascade = true
                )
            }
            is CascadeAction.Archive -> {
                archiveTaskUseCase(action.taskId, cascade = true)
            }
            is CascadeAction.Delete -> {
                moveTaskToTrashUseCase(action.taskId, cascade = true)
            }
        }
    }
}
```

## Preparación para Entrevistas (En el banquillo)

**Pregunta**: ¿Por qué `!!` nunca debería aparecer en código de producción, y qué hace un Senior en su lugar?

**Respuesta Senior**: El operador `!!` intercambia una garantía de seguridad en tiempo de compilación por un crash en runtime sin contexto. Produce una NullPointerException genérica cuyo stack trace te dice DÓNDE fue el crash pero no POR QUÉ el valor era null. En todos los casos, un Senior elimina el `!!` a través de tres estrategias: (1) rediseñar el flujo de datos para que el valor sea no-nullable desde el inicio — por ejemplo, usando inyección por constructor en lugar de asignación tardía; (2) usar el operador Elvis con una excepción explícita (`?: throw IllegalStateException("razón")`) para que el stack trace explique la invariante que se violó; o (3) usar safe calls con `let`, `run`, o early return (`?: return`) para manejar el caso null explícitamente. El objetivo es hacer las decisiones de nullabilidad visibles en el sistema de tipos, no esconderlas detrás de assertions.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
