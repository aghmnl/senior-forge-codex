---
layout: post
title: "Compilación JIT"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/jit-compilation/
---

## The Theory (El Qué)

La **compilación Just-In-Time (JIT)** es el proceso de traducir [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) a código máquina nativo *durante* el [tiempo de ejecución]({{ "/es/glosario/runtime/" | relative_url }}), mientras el código se está ejecutando. La [JVM]({{ "/es/glosario/jvm/" | relative_url }}) y el ART de Android usan compiladores JIT: comienzan interpretando bytecode, identifican métodos "hot" que se llaman frecuentemente, y compilan esos métodos a código nativo sobre la marcha. El código compilado se cachea en memoria para que las llamadas subsiguientes se ejecuten a velocidad nativa.

## The Senior Nuance (El Matiz Senior)

- La compilación JIT es el punto medio entre interpretación (lenta pero sin costo de compilación) y [compilación AOT]({{ "/es/glosario/aot-compilation/" | relative_url }}) (ejecución rápida pero con costo upfront). El ART de Android usa las tres: interpretando código frío, compilando JIT los hot paths, y compilando AOT los métodos perfilados en tiempo de instalación.
- JIT tiene acceso a información de runtime que la optimización en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}) no puede conocer: frecuencias reales de llamadas, probabilidades de branches, qué método virtual se llama más frecuentemente en un call site dado (monomorphic dispatch). Esto permite al JIT hacer optimizaciones especulativas — inlining de una llamada virtual con un guard, por ejemplo — que los compiladores estáticos no pueden.
- **Warm-up time**: la compilación JIT agrega latencia durante la primera ejecución de un método. En Android, por eso el startup de la app puede sentirse lento en el primer lanzamiento después de instalar — el JIT todavía no compiló el camino crítico. Los [Baseline Profiles]({{ "/es/glosario/pgo/" | relative_url }}) existen específicamente para mitigar esto.
- El código compilado JIT vive solo en memoria y se pierde cuando el proceso muere. En Android, ART guarda los *datos* de profiling (no el código compilado) a disco, y un [paso AOT]({{ "/es/glosario/aot-compilation/" | relative_url }}) posterior los usa via [PGO]({{ "/es/glosario/pgo/" | relative_url }}) para persistir las decisiones de optimización.
- El JIT HotSpot de la JVM estándar puede realizar optimizaciones como escape analysis (eliminar allocations en heap cuando un objeto no escapa de un método), loop unrolling y devirtualización — optimizaciones que son difíciles o imposibles en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}) porque dependen del comportamiento en runtime.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
