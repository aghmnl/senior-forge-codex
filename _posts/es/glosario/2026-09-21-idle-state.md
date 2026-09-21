---
layout: post
title: "Idle (UI State)"
date: 2026-09-21 12:00:00 +0000
categories: [es, glosario]
tags: [state-management, sealed-types, architecture]
lang: es
permalink: /es/glosario/idle-state/
---

## The Theory (El Qué)

**`Idle`** es el nombre convencional del miembro en reposo de una jerarquía sellada de estado de UI: todavía no se pidió nada, nada está cargando, nada falló. No lleva payload, así que se declara como [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) — una sola instancia, un `toString` limpio y cero [allocations]({{ "/es/glosario/allocations/" | relative_url }}) sin importar cuántas veces se emita. Sus hermanos típicos son `Loading`, [`Success`]({{ "/es/glosario/success-state/" | relative_url }}) y `Error`.

```kotlin
// Not found in FAS — standalone example
sealed interface UploadState {
    data object Idle : UploadState          // todavía no se pidió nada
    data object Uploading : UploadState
    data class Done(val url: String) : UploadState
    data class Failed(val cause: String) : UploadState
}
```

## The Senior Nuance (El Matiz Senior)

- **`Idle` no es `Empty`.** `Idle` significa "todavía no preguntamos"; `Empty` significa "preguntamos y no hay nada". Unificarlos en un solo estado hace imposible que la UI distinga una primera pantalla en blanco de un resultado genuinamente vacío.
- **Es el valor inicial natural.** `MutableStateFlow<UploadState>(UploadState.Idle)` no necesita un tipo nullable ni un default con `?:` en cada lectura.
- **Volver a `Idle` es una transición real.** Después de descartar un error o cancelar un flujo, volver a `Idle` — en vez de dejar el último estado — es lo que hace que el reintento se comporte de forma predecible.
- Ver [Data Objects: Singleton & Memory Savings]({{ "/es/01-kotlin-core/data-objects/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
