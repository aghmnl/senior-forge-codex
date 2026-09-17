---
layout: post
title: "ContentResolver"
date: 2026-09-17 12:00:00 +0000
categories: [es, glosario]
tags: [android-framework, persistence]
lang: es
permalink: /es/glosario/content-resolver/
---

## The Theory (El Qué)

**`ContentResolver`** es el objeto del framework (obtenido desde cualquier `Context`) a través del cual una app habla con `ContentProvider`s — propios o de otras apps — y con el Storage Access Framework. `openInputStream(uri)` / `openOutputStream(uri)` convierten una URI `content://` que el usuario eligió en un stream crudo; `query`, `insert`, `update`, `delete` hablan con providers como Contactos o MediaStore. Cada una de estas llamadas cruza un límite de proceso y toca disco: son **[blocking calls]({{ "/es/glosario/blocking-call/" | relative_url }})** y deben correr fuera del [main thread]({{ "/es/glosario/main-thread/" | relative_url }}).

```kotlin
// From FollowApp Suite — BackupManager.kt
suspend fun exportTo(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) {
    runCatching {
        val json = BackupSerializer.serialize(bundle)
        context.contentResolver.openOutputStream(uri, "wt").use { stream ->
            requireNotNull(stream) { "Cannot open destination" }
            stream.write(json.toByteArray(Charsets.UTF_8))
        }
    }
}
```

## The Senior Nuance (El Matiz Senior)

- **Es la forma de scoped storage de leer y escribir archivos del usuario.** Desde Android 10 una app no puede abrir paths arbitrarios; el usuario elige un documento, recibís una URI, y `ContentResolver` es la única puerta.
- **El stream puede ser `null`.** `openOutputStream` devuelve `null` cuando el provider no puede servir la URI — de ahí el `requireNotNull`. No le pongas `!!`.
- **Persistí el permiso si vas a necesitar el archivo de nuevo.** `takePersistableUriPermission` — si no, el grant muere con la Activity.
- Ver [Main-Safety]({{ "/es/02-coroutines-flow/main-safety/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
