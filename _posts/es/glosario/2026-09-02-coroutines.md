---
layout: post
title: "Coroutines"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/coroutines/
---

## The Theory (El Qué)

Las **coroutines** son las primitivas de concurrencia liviana de Kotlin para escribir [operaciones async]({{ "/es/glosario/async-operations/" | relative_url }}) en un estilo secuencial y legible. Una coroutine no es un thread — es una computación suspendible que puede pausarse en cualquier llamada a [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) y reanudarse después, potencialmente en un thread diferente, sin bloquear el thread en el que corría. Miles de coroutines pueden correr en un pool de threads chico porque solo ocupan un thread mientras realmente ejecutan código.

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
}
```

`scope.launch` crea una coroutine en `Dispatchers.IO` que recolecta veredictos de billing indefinidamente — sin bloquear ningún thread.

## The Senior Nuance (El Matiz Senior)

- **Structured concurrency**: Las coroutines no existen aisladas — corren dentro de un `CoroutineScope` que define su lifetime. Cuando el scope se cancela, todas sus coroutines se cancelan. `viewModelScope` y `lifecycleScope` son scopes [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) que previenen trabajo leakeado. El ejemplo de FAS crea un scope custom con `SupervisorJob()` porque el repository outlives cualquier pantalla.
- **`SupervisorJob` vs `Job`**: Un `Job` regular cancela todos los siblings cuando un hijo falla. `SupervisorJob` deja que los siblings sobrevivan — esencial para operaciones independientes (recolectar billing + recolectar analytics) que no deberían cancelarse entre sí.
- **Dispatchers**: `Dispatchers.Main` para trabajo de UI, `Dispatchers.IO` para I/O bloqueante (red, disco), `Dispatchers.Default` para trabajo CPU-intensive. Los desarrolladores senior usan `withContext` para cambiar dispatchers dentro de una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) en lugar de crear nuevas coroutines.
- **Las coroutines reemplazaron a los [callbacks]({{ "/es/glosario/callbacks/" | relative_url }})** para [operaciones async]({{ "/es/glosario/async-operations/" | relative_url }}) en Android moderno. El insight clave: los [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}) invierten el flujo de control ("llamame de vuelta cuando termines"), mientras que las coroutines preservan el flujo secuencial ("suspendé acá, después continuá"). `suspendCancellableCoroutine` puentea APIs basadas en callback al mundo de coroutines.
- **Flow** es el reemplazo basado en coroutines para streams reactivos. `StateFlow` mantiene estado actual; `SharedFlow` broadcastea eventos. Ambos se integran naturalmente con recolección [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) vía `repeatOnLifecycle`.
- **Testing**: `runTest` de `kotlinx-coroutines-test` provee un `TestScope` con un scheduler de tiempo virtual. Esto permite testear lógica basada en delay instantáneamente y verificar que structured concurrency se comporta correctamente.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
