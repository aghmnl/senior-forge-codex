---
layout: post
title: "@Module"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/module-annotation/
---

## The Theory (El Qué)

**`@Module`** es una anotación de [Dagger]({{ "/es/glosario/dagger/" | relative_url }}) que marca una clase como proveedora de bindings de dependencias. Un module le dice al pipeline de [procesamiento de anotaciones]({{ "/es/glosario/annotation-processing/" | relative_url }}) cómo suministrar tipos que no pueden inyectarse por constructor — interfaces (vía [`@Binds`]({{ "/es/glosario/binds/" | relative_url }})), clases de terceros, o instancias que requieren lógica de creación custom (vía `@Provides`). En [Hilt]({{ "/es/glosario/hilt/" | relative_url }}), cada `@Module` debe también declarar [`@InstallIn`]({{ "/es/glosario/install-in/" | relative_url }}) para especificar a qué component (scope) pertenecen los bindings.

```kotlin
// From FollowApp Suite — DatabaseModule.kt
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideMyTasksDatabase(
        @ApplicationContext context: Context
    ): MyTasksDatabase {
        return Room.databaseBuilder(
            context,
            MyTasksDatabase::class.java,
            "mytasks_database.db"
        )
            .addMigrations(MIGRATION_1_2)
            .build()
    }
}
```

## The Senior Nuance (El Matiz Senior)

- **`object` vs `abstract class`**: Usá `object` para modules con métodos `@Provides` (implementaciones concretas). Usá `abstract class` para modules con métodos [`@Binds`]({{ "/es/glosario/binds/" | relative_url }}) (mapeos de interface a implementación). Mezclar ambos en un module es posible pero suele ser un code smell.
- **`@Provides` crea instancias**: Cada función `@Provides` es un factory. [Dagger]({{ "/es/glosario/dagger/" | relative_url }}) genera código que la llama cuando el tipo de retorno es necesitado. Combiná con `@Singleton` (u otro scope) para cachear la instancia.
- **Organización de modules**: Agrupá bindings relacionados en el mismo module (e.g., `DatabaseModule` para todos los providers de [DAO]({{ "/es/glosario/dao/" | relative_url }}), `RepositoryModule` para todos los bindings de repositorios). Esto mantiene el [grafo de dependencias]({{ "/es/glosario/dependency-graph/" | relative_url }}) legible.
- **Seguridad en compile-time**: Si falta un binding, el build falla — el procesador de [Dagger]({{ "/es/glosario/dagger/" | relative_url }}) emite un error claro listando la dependencia insatisfecha. Esto es una ventaja clave sobre frameworks de DI basados en [runtime reflection]({{ "/es/glosario/runtime-reflection/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
