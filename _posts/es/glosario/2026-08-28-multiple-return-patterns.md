---
layout: post
title: "Multiple Return Patterns"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/multiple-return-patterns/
---

## The Theory (El Qué)

Las funciones Kotlin retornan un solo valor, pero los **multiple return patterns** (patrones de retorno múltiple) permiten agrupar varios valores juntos. Los enfoques más comunes son `Pair<A, B>`, `Triple<A, B, C>` y tipos `data class` personalizados. Los tres soportan [destructuring]({{ "/es/glosario/destructuring/" | relative_url }}), por lo que los llamadores pueden desempaquetar los valores directamente.

```kotlin
// De FollowApp Suite — PremiumUseCaseTest.kt
private fun useCase(
    installedDaysAgo: Int,
    skipFreeTrial: Boolean = false
): Pair<GetPremiumStatusUseCase, FakeLedgerRepository> {
    val ledgerRepo = FakeLedgerRepository(
        System.currentTimeMillis() - installedDaysAgo * dayMs, skipFreeTrial
    )
    return GetPremiumStatusUseCase(ledgerRepo, authRepo) to ledgerRepo
}

// Uso — destructuring del Pair
val (getStatus, _) = useCase(installedDaysAgo = 10)
```

## The Senior Nuance (El Matiz Senior)

- `Pair` y `Triple` son convenientes pero sus nombres de componentes (`first`, `second`, `third`) no llevan significado semántico. Para APIs públicas o cuando los valores de retorno no son obvios por contexto, preferí una `data class` con nombre — documenta la intención y sobrevive refactoring.
- La función infix `to` crea un `Pair`, que es por lo que `mapOf("a" to 1)` funciona. Pero `to` asigna un objeto `Pair` cada vez — en código crítico de performance construyendo [maps]({{ "/es/glosario/maps/" | relative_url }}) grandes, preferí `buildMap { put("a", 1) }`.
- El [destructuring]({{ "/es/glosario/destructuring/" | relative_url }}) es lo que hace los patrones de retorno múltiple ergonómicos: `val (status, repo) = useCase(10)` se lee casi como una multi-asignación. Sin destructuring, necesitarías `result.first` y `result.second`, que es ruidoso y frágil.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
