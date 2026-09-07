---
layout: post
title: "Thread Safety"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/thread-safety/
---

## The Theory (El Qué)

La **thread safety** (seguridad de hilos) significa que un fragmento de código se comporta correctamente cuando se accede desde múltiples hilos concurrentemente, sin race conditions, corrupción de datos ni crashes. En Kotlin y Android, la thread safety se logra a través de varios mecanismos:

- **[Inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }})** — los objetos que no pueden cambiar no necesitan sincronización. `val`, [data classes]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) inmutables y [colecciones]({{ "/es/glosario/collections/" | relative_url }}) inmutables son inherentemente thread-safe.
- **Confinamiento** — restringir el estado mutable a un solo hilo (ej., el hilo principal para estado de UI, un `Dispatchers.IO` single-threaded para una conexión de base de datos).
- **Sincronización** — bloques `synchronized`, `Mutex`, `@Volatile` y clases atómicas (`AtomicReference`, `AtomicInteger`) protegen estado mutable compartido.
- **Concurrencia estructurada** — las coroutines de Kotlin con `CoroutineScope` y `Dispatchers` aseguran que el trabajo se ejecute en el hilo correcto y se cancele apropiadamente.

## The Senior Nuance (El Matiz Senior)

- Un Senior usa la [inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }}) como estrategia principal de thread safety. Un `StateFlow` que emite snapshots inmutables de [data class]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) no requiere sincronización — el único punto de mutación es el setter de `MutableStateFlow.value`, que ya es atómico.
- En Android, la mayoría de los bugs de thread safety ocurren en las fronteras entre capas: un repository que retorna una `MutableList` desde un hilo de background que la UI lee en el hilo principal. Copias defensivas (`toList()`, `toMap()`) o tipos verdaderamente inmutables eliminan esto.
- `lazy(LazyThreadSafetyMode.SYNCHRONIZED)` (el default) usa un bloque `synchronized` para inicialización thread-safe. `LazyThreadSafetyMode.NONE` omite la sincronización por completo — seguro solo cuando la propiedad está garantizada de ser accedida desde un solo hilo (ej., una propiedad solo de UI). `PUBLICATION` permite inicialización concurrente pero garantiza que solo un resultado sea visible. Un Senior elige el modo que coincida con el patrón de acceso.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
