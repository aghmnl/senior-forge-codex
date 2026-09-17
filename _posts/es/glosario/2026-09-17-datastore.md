---
layout: post
title: "DataStore"
date: 2026-09-17 12:00:00 +0000
categories: [es, glosario]
tags: [persistence, coroutines, android-framework]
lang: es
permalink: /es/glosario/datastore/
---

## The Theory (El Qué)

**Jetpack DataStore** es el reemplazo de `SharedPreferences`: un almacén chico clave-valor (`Preferences DataStore`) o tipado (`Proto DataStore`) cuya API entera está construida sobre [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) y [`Flow`]({{ "/es/glosario/flow/" | relative_url }}). Las lecturas son un `Flow<Preferences>` que [colectás]({{ "/es/glosario/collect/" | relative_url }}) (o `.first()`); las escrituras son un `edit { }` [suspend]({{ "/es/glosario/suspend-functions/" | relative_url }}) transaccional y atómico. Toda operación es **main-safe por construcción** — DataStore hace su I/O de archivo en [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) internamente.

```kotlin
// From FollowApp Suite — LanguagePreferences.kt
@Singleton
class LanguagePreferences @Inject constructor(
    private val dataStore: DataStore<Preferences>
) {
    private val languageKey = stringPreferencesKey("language")

    fun getLanguage(): Flow<String> = dataStore.data.map { it[languageKey] ?: "system" }

    suspend fun setLanguage(tag: String) {
        dataStore.edit { it[languageKey] = tag }
    }
}
```

## The Senior Nuance (El Matiz Senior)

- **No lo envuelvas en `withContext(IO)`.** Ya cambia de dispatcher; el wrapper es ruido y le dice al próximo lector que la API no es main-safe.
- **La primera lectura paga una apertura fría de archivo.** Varias preferencias en el mismo archivo cuestan *una* apertura; varios archivos cuestan varias. Agrupá keys relacionadas.
- **Una instancia de `DataStore` por archivo, en todo el proceso.** Dos instancias sobre el mismo archivo lo corrompen — de ahí el `@Singleton` y el delegate `preferencesDataStore` de nivel superior.
- **Las lecturas de `SharedPreferences` bloquean; las de DataStore suspenden.** Esa diferencia es toda la razón por la que existe.
- Ver [Main-Safety]({{ "/es/02-coroutines-flow/main-safety/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
