---
layout: post
title: "@IoDispatcher"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [di, coroutines, testing]
lang: es
permalink: /es/glosario/io-dispatcher/
---

## The Theory (El Qué)

**`@IoDispatcher`** es la anotación *qualifier* convencional de Hilt/Dagger que se usa para inyectar [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) como dependencia `CoroutineDispatcher` en vez de referenciar el singleton directamente. Sus hermanas `@DefaultDispatcher` y `@MainDispatcher` siguen el mismo patrón. Los nombres vienen de los samples de arquitectura de Google; nada en la librería los define — los declarás vos.

```kotlin
// Not found in FAS — standalone example
@Qualifier @Retention(AnnotationRetention.BINARY) annotation class IoDispatcher

@Module @InstallIn(SingletonComponent::class)
object DispatchersModule {
    @Provides @IoDispatcher fun provideIo(): CoroutineDispatcher = Dispatchers.IO
}

class BackupManager @Inject constructor(@IoDispatcher private val io: CoroutineDispatcher) {
    suspend fun exportTo(uri: Uri) = withContext(io) { /* ... */ }
}
```

## The Senior Nuance (El Matiz Senior)

- **El punto es la testabilidad.** Con el dispatcher inyectado, un test unitario pasa `StandardTestDispatcher(testScheduler)` y toda la clase corre en tiempo virtual bajo [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}). Un `Dispatchers.IO` hardcodeado no se puede interceptar.
- **Hace falta un qualifier porque el tipo es el mismo.** `CoroutineDispatcher` para IO, Default y Main son indistinguibles para [Hilt]({{ "/es/glosario/hilt/" | relative_url }}) sin uno; la anotación es lo que desambigua el binding.
- **Proveé los tres desde un único módulo**, sin `@Singleton` — los dispatchers ya son singletons.
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
