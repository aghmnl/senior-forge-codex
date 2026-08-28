---
layout: post
title: "Garbage Collector (GC)"
date: 2026-05-04 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/garbage-collector/
---

## The Theory (El Qué)

El **Garbage Collector (GC)** es un sistema automatizado de gestión de memoria dentro del Android Runtime (ART) y la Java Virtual Machine (JVM). Su responsabilidad principal es identificar objetos en el heap que ya no son alcanzables por la aplicación y reclamar su memoria, previniendo memory leaks y errores de desasignación manual de memoria.

## The Senior Nuance (El Matiz Senior)

Para un Desarrollador Android Senior, el GC no es solo un proceso en segundo plano sino un factor de rendimiento:
- **GC Generacional**: ART usa un enfoque generacional, dividiendo el heap en diferentes regiones (Young, Old) según el tiempo de vida de los objetos para optimizar la frecuencia de recolección.
- **Pausas del GC**: La asignación intensiva de objetos (como dentro de un método `onDraw` o en loops de alta frecuencia) puede disparar ciclos de GC frecuentes, causando "jank" o frames perdidos en la UI.
- **Alcanzabilidad**: La memoria se reclama solo cuando un objeto no tiene "strong references" que lleven de vuelta a un GC Root. Entender la diferencia entre referencias Strong, Weak y Soft es vital para prevenir leaks en arquitecturas complejas.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
