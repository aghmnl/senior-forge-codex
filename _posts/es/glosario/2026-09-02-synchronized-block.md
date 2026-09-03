---
layout: post
title: "Synchronized Block"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/synchronized-block/
---

## The Theory (El Qué)

Un **synchronized block** (bloque sincronizado) es una primitiva de concurrencia que asegura que solo un thread pueda ejecutar una sección protegida de código a la vez. En Kotlin, se expresa como `synchronized(lock) { ... }`, donde `lock` es cualquier objeto usado como mutex. Mientras un thread tiene el lock, cualquier otro thread que llegue al mismo bloque `synchronized` espera hasta que el lock se libere. Esto garantiza exclusión mutua — previniendo data races cuando múltiples threads leen y escriben estado mutable compartido.

```kotlin
// Standalone example — no synchronized usage found in FAS
class ThreadSafeCounter {
    private var count = 0
    private val lock = Any()

    fun increment() = synchronized(lock) {
        count++
    }

    fun get() = synchronized(lock) { count }
}
```

## The Senior Nuance (El Matiz Senior)

- **`lazy` usa `synchronized` por defecto**: `lazy(LazyThreadSafetyMode.SYNCHRONIZED)` — el modo por defecto — wrappea la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) de inicialización en un bloque `synchronized`. Esto asegura que si dos threads acceden a la propiedad simultáneamente, solo uno ejecuta la inicialización; el otro espera y recibe el valor cacheado. Usar `LazyThreadSafetyMode.NONE` skipea esto — apropiado solo cuando el acceso es garantizadamente single-threaded.
- **Las [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) prefieren `Mutex`**: En código de coroutines, `synchronized` se desaconseja porque bloquea el thread (no solo la coroutine). `kotlinx.coroutines.sync.Mutex` provee la misma exclusión mutua pero suspende en lugar de bloquear, manteniendo el thread disponible para otras coroutines.
- **Costo de rendimiento**: `synchronized` incurre en overhead de adquisición de monitor en la [JVM]({{ "/es/glosario/jvm/" | relative_url }}). En [hot loops]({{ "/es/glosario/hot-loops/" | relative_url }}) o escenarios de alta contención, esto puede degradar el throughput. Alternativas como `AtomicInteger`, `ConcurrentHashMap` o algoritmos lock-free evitan este overhead para patrones específicos.
- **Riesgo de deadlock**: Adquirir múltiples locks en orden inconsistente a través de diferentes paths de código es el escenario clásico de deadlock. Los desarrolladores senior minimizan el scope de synchronized (lockear solo lo necesario) y siempre adquieren locks en el mismo orden.
- **`@Volatile` vs `synchronized`**: `@Volatile` asegura visibilidad (todos los threads ven la última escritura) pero no asegura atomicidad de operaciones compuestas (read-modify-write). `synchronized` provee ambas. Para un flag simple, `@Volatile` alcanza; para increment o check-then-act, se necesita `synchronized` o atomics.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
