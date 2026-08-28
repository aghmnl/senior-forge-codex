---
layout: post
title: "Compilación AOT"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/aot-compilation/
---

## The Theory (El Qué)

La **compilación Ahead-of-Time (AOT)** es el proceso de traducir [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) a código máquina nativo *antes* de que la aplicación se ejecute, en lugar de durante el [tiempo de ejecución]({{ "/es/glosario/runtime/" | relative_url }}). En Android, la compilación AOT ocurre en el momento de instalación de la app (o durante mantenimiento en idle) como parte del pipeline del Android Runtime (ART). El resultado es un archivo nativo `.oat` que el dispositivo ejecuta directamente, evitando el overhead de interpretar o [compilar JIT]({{ "/es/glosario/jit-compilation/" | relative_url }}) el bytecode en cada lanzamiento.

## The Senior Nuance (El Matiz Senior)

- El ART de Android usa una **estrategia híbrida**: compilación AOT en tiempo de instalación para rendimiento base, [compilación JIT]({{ "/es/glosario/jit-compilation/" | relative_url }}) para hot paths descubiertos en runtime, y [optimización guiada por perfiles (PGO)]({{ "/es/glosario/pgo/" | relative_url }}) para refinar la compilación AOT en instalaciones o actualizaciones subsiguientes. Entender este pipeline explica por qué la "primera ejecución después de instalar" puede comportarse diferente a las siguientes.
- La compilación AOT elimina la penalización de startup de interpretar bytecode, pero aumenta el tiempo de instalación y el espacio en disco — el código nativo `.oat` es más grande que el [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) `.dex` original. Este trade-off es la razón por la que Android no compila AOT todo — usa perfiles para identificar qué métodos vale la pena compilar con anticipación.
- R8/D8 (que se ejecutan en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}) en la máquina del desarrollador) producen bytecode `.dex` optimizado. El compilador AOT de ART luego traduce ese `.dex` a código nativo para la arquitectura específica del dispositivo (ARM64, x86). Son dos etapas de compilación separadas con objetivos de optimización diferentes.
- Kotlin/Native usa compilación AOT exclusivamente (sin JVM, sin intérprete) para producir binarios independientes para iOS, macOS, Linux, etc. No hay fase JIT — todas las optimizaciones deben ocurrir en tiempo de compilación.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
