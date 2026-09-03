---
layout: post
title: "@InstallIn"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/install-in/
---

## The Theory (El Qué)

**`@InstallIn`** es una anotación de [Hilt]({{ "/es/glosario/hilt/" | relative_url }}) que declara a qué component pertenece un [`@Module`]({{ "/es/glosario/module-annotation/" | relative_url }}). Conecta los bindings del module a un scope específico en el [grafo de dependencias]({{ "/es/glosario/dependency-graph/" | relative_url }}). Sin `@InstallIn`, [Hilt]({{ "/es/glosario/hilt/" | relative_url }}) no sabe dónde instalar el module y el build falla.

```kotlin
// From FollowApp Suite — DatabaseModule.kt
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    // bindings scoped al SingletonComponent de la app
}
```

## The Senior Nuance (El Matiz Senior)

- **Jerarquía de components**: Hilt define un árbol fijo de components — `SingletonComponent` (app-wide), `ActivityRetainedComponent` (sobrevive config changes), `ViewModelComponent`, `ActivityComponent`, `FragmentComponent`, `ViewComponent`, `ServiceComponent`. Cada component hereda bindings de su padre.
- **Matching de scope**: `@InstallIn(SingletonComponent::class)` hace que los bindings estén disponibles en toda la app. `@InstallIn(ViewModelComponent::class)` los scopea por ViewModel. Elegir el component equivocado causa o sobre-compartición (un binding específico de ViewModel disponible en todos lados) o sub-disponibilidad (un binding faltante donde se necesita).
- **Un module, un component**: Un module se instala en exactamente un component. Si el mismo binding se necesita en múltiples scopes, instalá en el component aplicable más amplio o creá modules separados.
- **`@InstallIn` es específico de Hilt**: [Dagger]({{ "/es/glosario/dagger/" | relative_url }}) puro no usa `@InstallIn` — los modules se agregan a components manualmente vía `@Component(modules = [...])`. [Hilt]({{ "/es/glosario/hilt/" | relative_url }}) automatiza este wiring, por eso `@InstallIn` existe.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
