---
layout: post
title: "@Singleton"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [di, lifecycle, architecture]
lang: es
permalink: /es/glosario/singleton-scope/
---

## The Theory (El Qué)

**`@Singleton`** es la anotación de scope de JSR-330 que le dice a [Hilt]({{ "/es/glosario/hilt/" | relative_url }})/[Dagger]({{ "/es/glosario/dagger/" | relative_url }}) que cree exactamente una instancia de un binding por componente y la reutilice en cada inyección. En Hilt pertenece a `SingletonComponent`, cuya vida es la de la `Application` — así que un objeto `@Singleton` vive tanto como el proceso.

```kotlin
// From FollowApp Suite — PremiumRepositoryImpl.kt
@Singleton
class PremiumRepositoryImpl @Inject constructor(
    private val premiumPreferences: PremiumPreferences,
    private val billingConnector: BillingConnector
) : PremiumRepository {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    // ...
}
```

Es un *scope* de DI, no el [patrón singleton]({{ "/es/glosario/singleton/" | relative_url }}) con `object` de Kotlin: la clase es común y testeable; el framework impone la regla de una única instancia.

## The Senior Nuance (El Matiz Senior)

- **La vida del proceso es la razón por la que un `@Singleton` puede ser dueño de un [`CoroutineScope`]({{ "/es/glosario/coroutine-scope/" | relative_url }}).** Nada le sobrevive para cancelarlo, así que un scope que nunca se cancela es aceptable acá — y solo acá. Todo lo de vida más corta debe usar un scope atado a un lifecycle.
- **Todo lo que un `@Singleton` retiene lo retiene para siempre.** Una referencia a un `Context` de Activity, una View o un Fragment adentro de uno es un [memory leak]({{ "/es/glosario/memory-leaks/" | relative_url }}) garantizado; inyectá `@ApplicationContext`.
- **Sin scope es el default.** Sin la anotación Hilt crea una instancia nueva por inyección. Scopeá solo lo que debe compartirse: repositorios, base de datos, cliente HTTP — no use cases sin estado.
- **El scope tiene que coincidir con el componente.** `@Singleton` en un binding de `ViewModelComponent` es un error de compilación; ahí va `@ViewModelScoped`.
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
