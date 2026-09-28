---
layout: post
title: "Coroutines"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, concurrency, lifecycle]
lang: es
permalink: /es/glosario/coroutines/
---

## The Theory (El Qué)

Las **coroutines** son las primitivas de concurrencia liviana de Kotlin para escribir [operaciones async]({{ "/es/glosario/async-operations/" | relative_url }}) en un estilo secuencial y legible. Una coroutine no es un thread — es una computación suspendible que puede pausarse en cualquier llamada a [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) y reanudarse después, potencialmente en un thread diferente, sin bloquear el thread en el que corría. Miles de coroutines pueden correr en un pool de threads chico porque solo ocupan un thread mientras realmente ejecutan código.

Las coroutines vienen en dos partes. **Kotlin mismo** aporta la palabra clave [`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) y los tipos básicos detrás de ella, en su paquete `kotlin.coroutines`, sin ninguna dependencia extra. Todo lo que se usa en el día a día ([`CoroutineScope`]({{ "/es/glosario/coroutine-scope/" | relative_url }}), [`launch`]({{ "/es/glosario/launch/" | relative_url }}), [`Job`]({{ "/es/glosario/job/" | relative_url }}), [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}), [`Dispatchers`]({{ "/es/glosario/dispatcher/" | relative_url }}), [`Flow`]({{ "/es/glosario/flow/" | relative_url }})) viene de la librería [kotlinx.coroutines]({{ "/es/glosario/kotlinx-coroutines/" | relative_url }}), una dependencia aparte.

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

[`scope.launch`]({{ "/es/glosario/launch/" | relative_url }}) crea una coroutine en [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) que recolecta veredictos de billing indefinidamente — sin bloquear ningún thread.

## The Senior Nuance (El Matiz Senior)

- **[Structured concurrency]({{ "/es/02-coroutines-flow/structured-concurrency/" | relative_url }})**: Las coroutines no existen aisladas — corren dentro de un [`CoroutineScope`]({{ "/es/glosario/coroutine-scope/" | relative_url }}) que define su lifetime. Cuando el scope se cancela, todas sus coroutines se cancelan. [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) y [`lifecycleScope`]({{ "/es/glosario/lifecycle-scope/" | relative_url }}) son scopes [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) que previenen trabajo leakeado. El ejemplo de FAS crea un scope custom con [`SupervisorJob()`]({{ "/es/glosario/supervisor-job/" | relative_url }}) porque el repository outlives cualquier pantalla.
- **[`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) vs [`Job`]({{ "/es/glosario/job/" | relative_url }})**: Un [`Job`]({{ "/es/glosario/job/" | relative_url }}) regular cancela todos los siblings cuando un hijo falla. [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) deja que los siblings sobrevivan — esencial para operaciones independientes (recolectar billing + recolectar analytics) que no deberían cancelarse entre sí.
- **[Dispatchers]({{ "/es/glosario/dispatcher/" | relative_url }})**: [`Dispatchers.Main`]({{ "/es/glosario/dispatchers-main/" | relative_url }}) para trabajo de UI, [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) para I/O bloqueante (red, disco), [`Dispatchers.Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}) para trabajo CPU-intensive. Los desarrolladores senior usan [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) para cambiar dispatchers dentro de una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) en lugar de crear nuevas coroutines.
- **Las coroutines reemplazaron a los [callbacks]({{ "/es/glosario/callbacks/" | relative_url }})** para [operaciones async]({{ "/es/glosario/async-operations/" | relative_url }}) en Android moderno. El insight clave: los [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}) invierten el flujo de control ("llamame de vuelta cuando termines"), mientras que las coroutines preservan el flujo secuencial ("suspendé acá, después continuá"). [`suspendCancellableCoroutine`]({{ "/es/glosario/suspend-cancellable-coroutine/" | relative_url }}) puentea APIs basadas en callback al mundo de coroutines.
- **[Flow]({{ "/es/glosario/flow/" | relative_url }})** es el reemplazo basado en coroutines para streams reactivos. [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}) mantiene estado actual; [`SharedFlow`]({{ "/es/glosario/sharedflow/" | relative_url }}) difunde cada emisión a todos los collectors. Ambos se integran naturalmente con recolección [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) vía [`repeatOnLifecycle`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}).
- **Testing**: [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}) de [`kotlinx-coroutines-test`]({{ "/es/glosario/kotlinx-coroutines/" | relative_url }}) provee un [`TestScope`]({{ "/es/glosario/test-scope/" | relative_url }}) con un scheduler de tiempo virtual. Esto permite testear lógica basada en delay instantáneamente y verificar que structured concurrency se comporta correctamente.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
