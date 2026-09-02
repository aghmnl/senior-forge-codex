---
layout: post
title: "Memory Leaks"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/memory-leaks/
---

## The Theory (El Qué)

Un **memory leak** (fuga de memoria) ocurre cuando un objeto ya no es necesario por la aplicación pero no puede ser reclamado por el [Garbage Collector]({{ "/es/glosario/garbage-collector/" | relative_url }}) porque una cadena de strong references todavía lo alcanza desde un GC root. El objeto permanece en el [heap]({{ "/es/glosario/heap/" | relative_url }}), consumiendo memoria indefinidamente. Con el tiempo, los leaks acumulados agotan el [heap]({{ "/es/glosario/heap/" | relative_url }}), llevando a `OutOfMemoryError` o performance degradada a medida que el GC trabaja más.

```kotlin
// Not found in FAS — standalone example
// Leak clásico de Android: inner class mantiene referencia implícita a Activity
class MyActivity : AppCompatActivity() {
    private val handler = object : Handler(Looper.getMainLooper()) {
        override fun handleMessage(msg: Message) {
            // 'this' mantiene una referencia a MyActivity
            // Si hay un mensaje demorado pendiente cuando la Activity se destruye,
            // la Activity no puede ser recolectada por el GC
        }
    }
}
```

La solución es romper la cadena de referencias: usar un `WeakReference`, cancelar trabajo pendiente en `onDestroy()`, o usar componentes lifecycle-aware que se desregistran automáticamente.

## The Senior Nuance (El Matiz Senior)

- En Android, los leaks más comunes vienen de mantener referencias a `Activity`, `Context` o `View` más allá de su lifecycle. Un singleton que cachea un context de `Activity` filtra toda la jerarquía de views. Siempre usá `applicationContext` para referencias de larga vida.
- **LeakCanary** es la herramienta estándar para detectar leaks en builds de debug. Monitorea Activities, Fragments, ViewModels y Services destruidos, y reporta un leak trace mostrando la cadena de referencias desde el GC root hasta el objeto filtrado. Los desarrolladores senior lo integran en cada proyecto.
- Las coroutines atadas a `lifecycleScope` o `viewModelScope` se cancelan automáticamente cuando el lifecycle owner se destruye — esto previene leaks de funciones suspend de larga duración. Usar `GlobalScope` o un `CoroutineScope` custom sin cancelación es una fuente común de leaks.
- Las [inline functions]({{ "/es/glosario/inline-functions/" | relative_url }}) y los [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) pueden capturar variables externas, creando referencias implícitas. Un lambda pasado a un callback de larga vida (ej. un listener registrado en un singleton) mantiene una referencia a su clase contenedora — que puede ser una Activity.
- Los memory leaks no son solo sobre RAM: una `Activity` filtrada mantiene todo su view tree, caches de drawables y potencialmente buffers de bitmaps. Un solo leak de Activity puede desperdiciar 50+ MB en un dispositivo con un límite de [heap]({{ "/es/glosario/heap/" | relative_url }}) de 256 MB.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
