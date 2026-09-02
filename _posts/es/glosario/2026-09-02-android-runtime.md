---
layout: post
title: "Android Runtime (ART)"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/android-runtime/
---

## The Theory (El Qué)

**Android Runtime (ART)** es el runtime gestionado que ejecuta las apps Android. Reemplazó a Dalvik en Android 5.0 (Lollipop). ART compila [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) (archivos `.dex`) a código máquina nativo, gestiona el [heap]({{ "/es/glosario/heap/" | relative_url }}), ejecuta el [Garbage Collector]({{ "/es/glosario/garbage-collector/" | relative_url }}) y aplica sandboxing de seguridad. A diferencia de la [JVM]({{ "/es/glosario/jvm/" | relative_url }}), ART está diseñado específicamente para mobile: optimiza para batería, memoria y latencia de inicio.

ART usa una estrategia de compilación híbrida:

- **AOT (Ahead-of-Time)**: en tiempo de instalación o durante mantenimiento idle, ART compila métodos hot a código nativo almacenado en archivos `.oat`/`.art`.
- **[JIT (Just-in-Time)]({{ "/es/glosario/jit-compilation/" | relative_url }})**: en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}), ART compila métodos ejecutados frecuentemente al vuelo, usando datos de perfil para guiar la optimización.
- **Baseline profiles**: hints provistos por el desarrollador que le dicen a ART qué métodos compilar AOT en la primera instalación, eliminando la penalización JIT del cold-start.

## The Senior Nuance (El Matiz Senior)

- El GC de ART es concurrente, generacional y con compactación (moving). "Moving" significa que las direcciones de los objetos cambian durante la compactación — por eso el código JNI debe usar `GetObjectRefType` y global references con cuidado; las local references pueden invalidarse después de un GC.
- El [heap]({{ "/es/glosario/heap/" | relative_url }}) de ART está limitado por app (típicamente 256–512 MB). A diferencia de JVMs de escritorio, no podés tunear `-Xmx`. El flag `largeHeap` del manifest eleva el límite pero señala mala higiene de memoria — preferí corregir [memory leaks]({{ "/es/glosario/memory-leaks/" | relative_url }}) antes que pedir más heap.
- Los Baseline Profiles (introducidos con Jetpack ProfileInstaller) te permiten enviar un perfil que ART usa para compilación AOT en la primera instalación. Esto reduce directamente el jank de cold-start y es una optimización clave de nivel senior para apps en producción.
- ART impone restricciones estrictas de hidden-API desde Android 9. Acceder a métodos privados del framework vía reflection dispara warnings o fallos duros — una restricción que no existe en la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) estándar.
- R8 (el optimizador de build-time) trabaja en conjunto con ART: reduce, ofusca y optimiza el bytecode `.dex` que ART luego compilará a código nativo. Entender el pipeline R8 → ART es esencial para debuggear crashes de producción donde los stack traces están ofuscados.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
