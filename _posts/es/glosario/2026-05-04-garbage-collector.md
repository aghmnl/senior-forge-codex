---
layout: post
title: "Garbage Collector (GC)"
date: 2026-05-04 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/garbage-collector/
---

## The Theory (El Qué)

El **Garbage Collector (GC)** es un sistema automatizado de gestión de memoria dentro del [Android Runtime (ART)]({{ "/es/glosario/android-runtime/" | relative_url }}) y la [Java Virtual Machine (JVM)]({{ "/es/glosario/jvm/" | relative_url }}). Su responsabilidad principal es identificar objetos en el [heap]({{ "/es/glosario/heap/" | relative_url }}) que ya no son alcanzables por la aplicación y reclamar su memoria, previniendo [memory leaks]({{ "/es/glosario/memory-leaks/" | relative_url }}) y errores de desasignación manual de memoria.

El GC funciona trazando desde un conjunto de **GC roots** (campos estáticos, stacks de threads, referencias JNI) y marcando cada objeto alcanzable. Todo lo no marcado es inalcanzable y puede ser barrido. Los GCs modernos (como el de ART) son concurrentes y generacionales — recolectan objetos de corta vida en la generación joven frecuentemente (minor GC) y objetos de larga vida en la generación vieja menos seguido (major GC).

## The Senior Nuance (El Matiz Senior)

- **GC Generacional**: [ART]({{ "/es/glosario/android-runtime/" | relative_url }}) usa un enfoque generacional, dividiendo el [heap]({{ "/es/glosario/heap/" | relative_url }}) en diferentes regiones (Young, Old) según el tiempo de vida de los objetos para optimizar la frecuencia de recolección. La mayoría de los objetos muere joven (la "hipótesis generacional"), así que las minor GCs son rápidas y baratas.
- **Pausas del GC**: La [asignación]({{ "/es/glosario/allocations/" | relative_url }}) intensiva de objetos (como dentro de `onDraw()` o [hot loops]({{ "/es/glosario/hot-loops/" | relative_url }})) puede disparar ciclos de GC frecuentes, causando "jank" o frames perdidos en la UI. El presupuesto de 16ms por frame no deja margen para pausas del GC — usá [inline functions]({{ "/es/glosario/inline-functions/" | relative_url }}), [`IntArray`]({{ "/es/glosario/intarray/" | relative_url }}) sobre `List<Int>`, y objetos pre-asignados para minimizar [allocations]({{ "/es/glosario/allocations/" | relative_url }}) en hot paths.
- **Alcanzabilidad**: La memoria se reclama solo cuando un objeto no tiene strong references que lleven de vuelta a un GC root. Entender la diferencia entre referencias Strong, Weak (`WeakReference`) y Soft (`SoftReference`) es vital para prevenir [memory leaks]({{ "/es/glosario/memory-leaks/" | relative_url }}) en arquitecturas complejas — especialmente cuando singletons, campos estáticos o callbacks de larga vida mantienen referencias a Activities o Views.
- El **[autoboxing]({{ "/es/glosario/autoboxing/" | relative_url }})** es un impuesto oculto al GC: cada `Int?` o elemento de `List<Int>` crea un objeto `Integer` boxeado en el [heap]({{ "/es/glosario/heap/" | relative_url }}). En [hot loops]({{ "/es/glosario/hot-loops/" | relative_url }}), este churn puede dominar la actividad del GC.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
