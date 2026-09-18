---
layout: post
title: "!! (Non-Null Assertion)"
date: 2026-09-18 12:00:00 +0000
categories: [es, glosario]
tags: [null-safety, error-handling]
lang: es
permalink: /es/glosario/non-null-assertion/
---

## The Theory (El Qué)

**`!!`** es el operador de [assertion]({{ "/es/glosario/assertion/" | relative_url }}) de no-null: `x!!` convierte un `T?` en `T` lanzando [`NullPointerException`]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) si `x` es [`null`]({{ "/es/glosario/null/" | relative_url }}). Es el único lugar donde Kotlin te deja salir de la null safety, y la posición del artículo [Null Safety: Elvis & Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) es que nunca debería aparecer en código de producción: cambia una garantía de [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}) por un crash en [runtime]({{ "/es/glosario/runtime/" | relative_url }}) cuyo [stack trace]({{ "/es/glosario/stack-trace/" | relative_url }}) dice *dónde* pero nunca *por qué*.

```kotlin
// Not found in FAS — standalone example
val details = productDetails!!          // NPE sin mensaje si es null

// Cada alternativa dice *por qué* el valor tiene que existir
val details = productDetails ?: return false                            // guard clause
val details = checkNotNull(productDetails) { "connect() no fue llamado" } // invariante con nombre
val details = requireNotNull(productDetails) { "details es obligatorio" } // precondición con nombre
```

## The Senior Nuance (El Matiz Senior)

- **`!!` es una afirmación de que sabés más que el compilador.** A veces es cierto — pero entonces codificá ese conocimiento: rediseñá para que el tipo sea no-nulo, o usá [`checkNotNull`]({{ "/es/glosario/check-not-null/" | relative_url }}) / [`requireNotNull`]({{ "/es/glosario/require-not-null/" | relative_url }}) con mensaje. Mismo crash, diagnóstico útil.
- **Los usos que parecen legítimos suelen ser olores de diseño.** `_binding!!` en Fragments, `intent.extras!!`, `map[key]!!`: cada uno esconde una suposición de ciclo de vida o de datos que un [`?: return`]({{ "/es/glosario/elvis-return/" | relative_url }}) o un default con [Elvis]({{ "/es/glosario/elvis-operator/" | relative_url }}) harían explícita.
- **Los tests son la excepción.** En un test, `!!` sobre un valor que el propio test acaba de armar es aceptable: una falla ahí es un bug del test, y la NPE lo señala directo.
- Ver [Null Safety: Elvis & Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
