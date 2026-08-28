---
layout: post
title: "Extension"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/extension/
---

## The Theory (El Qué)

Una **extension** (extensión) es cualquier mecanismo que agrega nuevas capacidades a un tipo existente sin modificar su código fuente. En Kotlin, la herramienta principal es la [extension function]({{ "/es/glosario/extension-functions/" | relative_url }}), pero el concepto también incluye extension properties, extension functions sobre companion objects, y lambdas con [receiver types]({{ "/es/glosario/receiver-type/" | relative_url }}). El principio Open/Closed ("abierto para extensión, cerrado para modificación") es la justificación de diseño detrás de todos estos mecanismos.

```kotlin
// De FollowApp Suite — BillingConnector.kt
// Extendiendo la clase Purchase de Google Play Billing sin modificarla
private fun Purchase.isOwnedProduct(): Boolean =
    productId in products && purchaseState == Purchase.PurchaseState.PURCHASED
```

```kotlin
// De FollowApp Suite — DragToReorder.kt
// Extendiendo LazyListState de Compose con lógica de scroll-anchoring personalizada
fun LazyListState.reanchorAfterMove(targetIndex: Int) {
    val visible = layoutInfo.visibleItemsInfo
    val first = visible.firstOrNull() ?: return
    if (targetIndex > first.index + 1) return
    val target = visible.firstOrNull { it.index == targetIndex } ?: return
    val newOffset = firstVisibleItemScrollOffset + first.offset - target.offset
    if (newOffset >= 0) requestScrollToItem(targetIndex, newOffset)
}
```

## The Senior Nuance (El Matiz Senior)

- Extensiones vs. [Decorator]({{ "/es/glosario/decorator/" | relative_url }}): las extensiones agregan funciones nuevas pero no pueden interceptar las existentes. Un Decorator envuelve el objeto y puede modificar *cualquier* comportamiento. Elegí extensiones para agregar utilidades; elegí Decorator para modificar u observar comportamiento existente.
- Extensiones vs. [Herencia]({{ "/es/glosario/inheritance/" | relative_url }}): las extensiones no crean una relación de subtipo. No pueden acceder a miembros privados. Se resuelven [estáticamente]({{ "/es/glosario/static-dispatch/" | relative_url }}), no a través de [polimorfismo]({{ "/es/glosario/polymorphism/" | relative_url }}). Esto las hace más seguras (sin problema de clase base frágil) pero menos poderosas (sin dispatch virtual).
- Los ejemplos FAS muestran el punto justo: agregar comportamiento específico del dominio (`isOwnedProduct`, `reanchorAfterMove`) a tipos de librería (`Purchase`, `LazyListState`) que no podés modificar. Esto mantiene la lógica de dominio cerca de donde se usa, sin contaminar la API de la librería.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
