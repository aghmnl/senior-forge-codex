---
layout: post
title: "Assertion"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/assertion/
---

## La Teoría (El Qué)

Una **assertion** (aserción) es una declaración que afirma una condición que el desarrollador cree verdadera en un punto dado. Si la condición es falsa, el programa falla inmediatamente. En Kotlin, las assertions incluyen `require` (valida argumentos de función, lanza `IllegalArgumentException`), `check` (valida estado del objeto, lanza `IllegalStateException`), `assert` (assertion de la JVM, deshabilitada por defecto), y la aserción de no-null `!!` (lanza [NullPointerException]({{ "/es/glosario/null-pointer-exception/" | relative_url }})).

## El Matiz Senior

- `require` y `check` son las funciones de assertion preferidas en Kotlin porque producen mensajes de excepción significativos: `require(age >= 0) { "Age must be non-negative: $age" }`. Documentan el contrato en código.
- La aserción de no-null `!!` es la forma más débil de assertion: hace una afirmación sobre nullabilidad pero no provee mensaje cuando falla. Preferí `requireNotNull(value) { "razón" }` o `checkNotNull(value) { "razón" }` — cumplen el mismo propósito con un [stack trace]({{ "/es/glosario/stack-trace/" | relative_url }}) significativo.
- Las assertions pertenecen en los límites del sistema (input de API, parsing de configuración, deserialización). Dentro de una API interna bien tipada, el sistema de tipos debería hacer que los estados imposibles sean irrepresentables, eliminando la necesidad de assertions en runtime.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
