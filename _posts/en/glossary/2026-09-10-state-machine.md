---
layout: post
title: "State Machine (Coroutines)"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/state-machine/
---

## The Theory (The What)

In the context of [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}), a **state machine** is what the compiler turns the body of a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) into. Each [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) becomes a numbered label; the function's locals become fields on the [Continuation]({{ "/en/glossary/continuation/" | relative_url }}) object; and the body is wrapped in a `when(label)` that jumps to the right place on every resume.

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

The function is entered many times — once initially, once per resume — and each time it does exactly the slice of work between two labels.

## The Senior Nuance

- **Zero threads, zero magic.** The state machine is plain [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) in a plain method. Nothing in the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) knows about coroutines; suspension is just "return early with a marker".
- **Debuggers and stack traces see the machine, not your code.** A [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) from a suspended coroutine shows `invokeSuspend` frames and label numbers unless the `kotlinx-coroutines-debug` agent or IDE support reconstructs the logical stack.
- **Locals that cross a suspension are heap-allocated.** A tight loop with a `suspend` call inside allocates nothing per iteration, but every local live across the call is a field write. Rarely matters; occasionally explains a profiler surprise.
- Worked example in [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
