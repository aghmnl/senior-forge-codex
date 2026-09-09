---
layout: post
title: "Stack Frame"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/stack-frame/
---

## The Theory (El Qué)

Un **Stack Frame** es el bloque que la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) apila en el call stack por cada invocación de método: sus parámetros, sus variables locales y su dirección de retorno. El frame se desapila cuando el método retorna, y toda referencia local muere con él.

```kotlin
// De FollowApp Suite — GetLabelReferenceCounts.kt
operator fun invoke(tasks: List<Task>, scaleName: String): Map<String, Int> {
    val refCounts = mutableMapOf<String, Int>()   // local a este frame
    // ...se muta libremente: ningún otro thread puede alcanzarlo...
    return refCounts                              // publicado como read-only
}
```

## The Senior Nuance (El Matiz Senior)

- Este es el mecanismo detrás de "mutá localmente, publicá [inmutable]({{ "/es/glosario/immutability/" | relative_url }})". Un [`MutableMap`]({{ "/es/glosario/mutable-map/" | relative_url }}) referenciado solo desde un frame es inalcanzable desde cualquier otro thread, así que la [mutación]({{ "/es/glosario/mutation/" | relative_url }}) es [Thread-Safe]({{ "/es/glosario/thread-safety/" | relative_url }}) por construcción — sin necesidad de [Synchronized Block]({{ "/es/glosario/synchronized-block/" | relative_url }}).
- El frame guarda la *referencia*; el objeto vive en el [Heap]({{ "/es/glosario/heap/" | relative_url }}). Por eso el confinamiento dura solo mientras ninguna otra referencia escape: devolvelo, guardalo en un campo o capturalo en una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) que sobreviva a la llamada, y la garantía desaparece.
- Los frames son además lo que imprime un [Stack Trace]({{ "/es/glosario/stack-trace/" | relative_url }}), y lo que [`inline`]({{ "/es/glosario/inline-functions/" | relative_url }}) elimina al copiar el cuerpo de la función en el [Call Site]({{ "/es/glosario/call-site/" | relative_url }}) — que es también por qué un tipo [`reified`]({{ "/es/glosario/reified/" | relative_url }}) no puede escapar de su frame inlineado.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
