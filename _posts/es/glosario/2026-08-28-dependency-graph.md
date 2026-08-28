---
layout: post
title: "Grafo de Dependencias"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/dependency-graph/
---

## The Theory (El Qué)

Un **grafo de dependencias** es un grafo dirigido donde los nodos representan componentes (clases, módulos, bibliotecas) y las aristas representan relaciones "depende de". En frameworks de inyección de dependencias como Dagger/Hilt, el grafo se construye y valida en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}) mediante [procesamiento de anotaciones]({{ "/es/glosario/annotation-processing/" | relative_url }}): cada constructor `@Inject`, `@Module`, `@Provides` y `@Binds` se convierte en un nodo o arista. Si alguna dependencia falta o es circular, el build falla — antes de que la app se ejecute.

## The Senior Nuance (El Matiz Senior)

- Dagger/Hilt genera el grafo de dependencias completo como [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) concreto en tiempo de compilación. A diferencia de service locators (Koin), no hay resolución en [tiempo de ejecución]({{ "/es/glosario/runtime/" | relative_url }}) ni reflexión — cada búsqueda de dependencia es una llamada directa a método, lo que es type-safe y rápido.
- La estructura del grafo refleja la arquitectura de la aplicación: `SingletonComponent` contiene dependencias de ámbito de app, `ViewModelComponent` las de ámbito de ViewModel, y `ActivityComponent` / `FragmentComponent` manejan instancias de ámbito de UI. Entender el scoping es entender los límites de ciclo de vida del grafo.
- Los límites de módulos Gradle también forman un grafo de dependencias — `core:domain` no depende de nada, `core:data` depende de `core:domain`, y `app:mytasks` depende de ambos. Las dependencias circulares entre módulos causan fallos de build y señalan problemas arquitectónicos.
- En un proyecto Android bien estructurado, el grafo de dependencias DI y el grafo de módulos Gradle se refuerzan mutuamente: los módulos exponen interfaces, DI vincula implementaciones, y ninguna capa alcanza "hacia abajo" en el grafo.

```kotlin
// From FollowApp Suite — RepositoryModule.kt
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    abstract fun bindTaskRepository(
        taskRepositoryImpl: TaskRepositoryImpl
    ): TaskRepository

    @Binds
    abstract fun bindPremiumRepository(
        premiumRepositoryImpl: PremiumRepositoryImpl
    ): PremiumRepository
}
```

Cada declaración `@Binds` agrega una arista al grafo de dependencias: `TaskRepository → TaskRepositoryImpl`, `PremiumRepository → PremiumRepositoryImpl`. El procesador de anotaciones de Hilt valida en tiempo de compilación que cada `@Inject constructor` en cada implementación pueda ser satisfecho.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
