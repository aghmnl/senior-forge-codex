---
layout: post
title: "State Machine (Coroutines)"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, compiler, jvm]
lang: es
permalink: /es/glosario/state-machine/
---

## The Theory (El Qué)

En el contexto de las [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}), una **state machine** (máquina de estados) es en lo que el compilador convierte el cuerpo de una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}). Cada [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}) se convierte en una etiqueta numerada; las locales de la función pasan a ser campos del objeto [Continuation]({{ "/es/glosario/continuation/" | relative_url }}); y el cuerpo se envuelve en un `when(label)` que salta al lugar correcto en cada reanudación.

```kotlin
// Not found in FAS — standalone example (simplified)
fun load(id: String, cont: Continuation<Task>): Any? {
    val sm = cont as? LoadSM ?: LoadSM(cont)
    when (sm.label) {
        0 -> { sm.label = 1; val r = fetch(id, sm); if (r == COROUTINE_SUSPENDED) return r; sm.raw = r }
        1 -> { sm.raw = sm.result }
    }
    // ... next label
}
```

La función se entra muchas veces — una inicial, una por cada resume — y cada vez hace exactamente la porción de trabajo entre dos etiquetas.

## The Senior Nuance (El Matiz Senior)

- **Cero threads, cero magia.** La state machine es [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) común en un método común. Nada en la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) sabe de coroutines; suspender es solo "devolver temprano con un marcador".
- **Los debuggers y stack traces ven la máquina, no tu código.** Un [stack trace]({{ "/es/glosario/stack-trace/" | relative_url }}) de una coroutine suspendida muestra frames `invokeSuspend` y números de etiqueta, salvo que el agente `kotlinx-coroutines-debug` o el soporte del IDE reconstruyan el stack lógico.
- **Las locales que cruzan una suspensión se asignan en el heap.** Un loop apretado con una llamada `suspend` adentro no asigna nada por iteración, pero cada local viva a través de la llamada es una escritura de campo. Rara vez importa; ocasionalmente explica una sorpresa en el profiler.
- Ejemplo desarrollado en [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
