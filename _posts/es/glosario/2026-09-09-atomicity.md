---
layout: post
title: "Atomicity"
date: 2026-09-09 12:00:00 +0000
categories: [es, glosario]
tags: [concurrency, state-management, immutability]
lang: es
permalink: /es/glosario/atomicity/
---

## The Theory (El Qué)

Una operación es **atómica** cuando es indivisible desde el punto de vista de cualquier otro thread: ocurrió completa o no ocurrió, y ningún observador puede ver un estado intermedio. Leer un valor, decidir algo a partir de él y escribir un valor nuevo son *tres* operaciones — atómicas por separado, no atómicas en conjunto.

```kotlin
// NO atómico: leer, calcular, escribir — otro thread puede intercalarse entre medio
_uiState.value = _uiState.value.copy(count = _uiState.value.count + 1)

// Atómico: todo el read-modify-write es un único paso indivisible
_uiState.update { it.copy(count = it.count + 1) }
```

## The Senior Nuance (El Matiz Senior)

- `MutableStateFlow.value` está respaldado por `@Volatile`, así que un get o un set individual es atómico y visible entre threads. Justamente por eso el compuesto `value = value.copy(...)` *parece* seguro y no lo es: cada mitad es atómica, el par es una [Race Condition]({{ "/es/glosario/race-condition/" | relative_url }}).
- La atomicidad se logra sin locks mediante [Compare-and-Set]({{ "/es/glosario/compare-and-set/" | relative_url }}): leer el valor actual, calcular el siguiente, y publicarlo solo si el actual no cambió; reintentar en caso contrario. Es lo que hace [`update`]({{ "/es/glosario/update/" | relative_url }}) por debajo.
- La atomicidad solo compone con la [Inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }}). CAS compara *referencias*; si el objeto de estado se puede mutar in-place, la referencia queda igual mientras el contenido cambia, y la comparación tiene éxito sobre un valor que ya no es el que se leyó. El estado inmutable es la precondición, no una preferencia de estilo.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
