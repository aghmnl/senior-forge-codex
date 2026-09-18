---
layout: post
title: "IllegalStateException"
date: 2026-09-18 12:00:00 +0000
categories: [es, glosario]
tags: [error-handling, design-principles]
lang: es
permalink: /es/glosario/illegal-state-exception/
---

## The Theory (El Qué)

**`IllegalStateException`** es la excepción de la JVM que significa "este objeto está en un estado en el que nunca debería estar": se llamó un método antes de inicializar, después de destruir, o con una [invariante]({{ "/es/glosario/invariant/" | relative_url }}) interna rota. Los [`check`]({{ "/es/glosario/check/" | relative_url }}), [`checkNotNull`]({{ "/es/glosario/check-not-null/" | relative_url }}) y `error()` de Kotlin la lanzan ([throw]({{ "/es/glosario/throw/" | relative_url }})). En [Null Safety: Elvis & Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) es el reemplazo recomendado para `!!`: `value ?: throw IllegalStateException("motivo")` crashea con el mismo input pero deja un [stack trace]({{ "/es/glosario/stack-trace/" | relative_url }}) que nombra la regla violada en vez de una [`NullPointerException`]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) anónima.

```kotlin
// Not found in FAS — standalone example
fun launchPurchase(activity: Activity) {
    val details = productDetails
        ?: throw IllegalStateException("launchPurchase llamado antes de queryProductDetails()")
    billingClient.launchBillingFlow(activity, params(details))
}

// Lo mismo, más corto
val details = checkNotNull(productDetails) { "launchPurchase llamado antes de queryProductDetails()" }
```

## The Senior Nuance (El Matiz Senior)

- **Estado vs. argumento.** `IllegalStateException` culpa al objeto; `IllegalArgumentException` (de [`require`]({{ "/es/glosario/require/" | relative_url }})) culpa al llamador. Elegir bien es lo primero que revisa quien lee el reporte del crash.
- **El mensaje es el valor.** Una `IllegalStateException` sin mensaje es apenas mejor que una NPE. Nombrá el método que debería haberse llamado antes, o el campo que debería estar seteado.
- **No la atrapes.** Señala un error de programación, no una condición recuperable; atraparla esconde el bug. Dejá que crashee en debug y llegue a Crashlytics en release.
- Ver [Null Safety: Elvis & Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
