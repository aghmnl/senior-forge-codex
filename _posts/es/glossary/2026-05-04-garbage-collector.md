---
layout: post
title: "Garbage Collector (GC)"
date: 2026-05-04 12:00:00 +0000
categories: [es, glossary]
lang: es
permalink: /es/glosario/garbage-collector/
---

## The Theory (El Qué)

El **Garbage Collector (GC)** o Recolector de Basura es un sistema de gestión automática de memoria dentro de Android Runtime (ART) y la Java Virtual Machine (JVM). Su función principal es identificar objetos en el *heap* que ya no son alcanzables por la aplicación y liberar la memoria que ocupan, evitando fugas de memoria y errores de gestión manual.



## The Senior Nuance (El Matiz Senior)

Para un desarrollador Senior en Android, el GC no es solo un proceso en segundo plano, sino un factor crítico de rendimiento:
- **GC Generacional**: ART utiliza un enfoque generacional, dividiendo el *heap* en diferentes regiones (Young, Old) según la vida útil de los objetos para optimizar la frecuencia de recolección.
- **Pausas de GC**: La asignación intensiva de objetos (por ejemplo, dentro de un método `onDraw` o bucles de alta frecuencia) puede disparar ciclos de GC frecuentes, provocando "jank" o caída de *frames* en la interfaz de usuario.
- **Alcance (Reachability)**: La memoria solo se recupera cuando un objeto no tiene "referencias fuertes" que conecten con un *GC Root*. Entender la diferencia entre referencias *Strong*, *Weak* y *Soft* es vital para prevenir fugas en arquitecturas complejas.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
