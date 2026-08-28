---
layout: post
title: "Singleton"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/singleton/
---

## The Theory (El Qué)

Un **Singleton** es un patrón de diseño que garantiza que existe exactamente una instancia de una clase durante toda la vida de la aplicación. En Kotlin, la declaración `object` es la forma idiomática de crear un singleton — el compilador maneja la inicialización lazy thread-safe y previene la creación de instancias adicionales. No se necesita ni se permite constructor.

```kotlin
// De FollowApp Suite — BackupSerializer.kt
object BackupSerializer {
    private const val FORMAT = "followapp-mytasks-backup"
    private const val VERSION = 1

    fun serialize(bundle: BackupBundle): String {
        val root = JSONObject()
        root.put("format", FORMAT)
        root.put("version", VERSION)
        root.put("exportedAt", System.currentTimeMillis())
        root.put("tasks", JSONArray(bundle.tasks.map(::taskToJson)))
        root.put("labels", JSONArray(bundle.labels.map(::labelToJson)))
        return root.toString()
    }
}
```

## The Senior Nuance (El Matiz Senior)

- El `object` de Kotlin compila a una clase Java con un constructor `private` y un campo `static final INSTANCE`, inicializado en un bloque `static {}`. Esto es thread-safe por especificación de la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) — sin necesidad de `synchronized` ni `volatile`.
- En [jerarquías selladas]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}), `object` (o `data object`) se usa para hojas sin estado — ramas que no llevan datos. Como son singletons, producen cero allocations cuando se emiten a través de `StateFlow` o se comparan en [colecciones]({{ "/es/glosario/collections/" | relative_url }}).
- El peligro principal de los singletons es el estado global oculto. Un singleton sin estado con funciones puras (como el ejemplo FAS) es seguro. Un singleton con estado mutable se convierte en una dependencia mutable compartida — difícil de testear, difícil de razonar en código concurrente. Preferí inyección de dependencias para servicios con estado.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
