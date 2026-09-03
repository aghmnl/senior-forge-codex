---
layout: post
title: "Async Operations"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/async-operations/
---

## The Theory (El Qué)

Una **async operation** (operación asincrónica) es cualquier unidad de trabajo que no se completa inmediatamente y permite que el programa siga ejecutando otro trabajo mientras espera el resultado. En Android, las operaciones async comunes incluyen requests de red, queries a base de datos, I/O de archivos y comunicación entre procesos. Kotlin provee [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) como su mecanismo principal para operaciones async, reemplazando patrones viejos como threads crudos, `AsyncTask` y listeners basados en [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}).

```kotlin
// From FollowApp Suite — PremiumRepositoryImpl.kt
@Singleton
class PremiumRepositoryImpl @Inject constructor(
    private val premiumPreferences: PremiumPreferences,
    private val billingConnector: BillingConnector
) : PremiumRepository {

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    init {
        billingConnector.connect()
        scope.launch {
            billingConnector.isOwned
                .filterNotNull()
                .collect { owned ->
                    premiumPreferences.setAdsRemoved(owned)
                }
        }
    }

    override fun isPremium(): Flow<Boolean> = premiumPreferences.isAdsRemoved()
}
```

El `scope.launch` inicia una operación async que recolecta veredictos de ownership de billing en `Dispatchers.IO` sin bloquear el thread principal.

## The Senior Nuance (El Matiz Senior)

- **Coroutines vs threads**: Una coroutine es un mecanismo async liviano — miles pueden correr en un pool de threads pequeño. Un thread es un recurso a nivel de OS. Los desarrolladores senior usan coroutines para concurrencia a nivel de aplicación y solo tocan threads directamente para paralelismo CPU-bound o cuando interoperan con APIs de threading de Java.
- **`launch` vs `async`**: `launch` dispara una operación async que retorna `Job` (fire-and-forget). `async` retorna un `Deferred<T>` cuyo resultado se obtiene con `await()`. Elegí `launch` para side-effects (escribir en DB, enviar analytics), `async` cuando necesitás el valor de retorno y querés correr múltiples operaciones concurrentemente.
- **Structured concurrency** asegura que las operaciones async estén scopeadas a un lifecycle. `viewModelScope` ata el trabajo al lifecycle del ViewModel; `lifecycleScope` lo ata al lifecycle de Activity/Fragment. El ejemplo de FAS crea un `CoroutineScope` custom con `SupervisorJob()` porque el repository outlives cualquier pantalla individual — una decisión de arquitectura deliberada.
- **Las [suspend functions]({{ "/es/glosario/suspend-functions/" | relative_url }})** son la cara secuencial de las operaciones async: parecen síncronas pero suspenden en los puntos de I/O. Por eso el código pesado en [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}) se convierte naturalmente en cadenas secuenciales de [suspend functions]({{ "/es/glosario/suspend-functions/" | relative_url }}).
- **Manejo de errores**: En código async basado en callbacks, los errores se dispersan entre handlers `onFailure`. Con [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}), el `try/catch` estándar funciona porque las [suspend functions]({{ "/es/glosario/suspend-functions/" | relative_url }}) lanzan excepciones normalmente — el framework de structured concurrency las propaga por el [scope]({{ "/es/glosario/scope/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
