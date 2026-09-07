---
layout: post
title: "Data Layer"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/data-layer/
---

## The Theory (El Qué)

Una **data layer** (capa de datos) es un nivel lógico en una arquitectura en capas que agrupa clases por su distancia a la fuente de datos o al usuario. En la arquitectura recomendada de Android, las capas estándar son:

- **Capa de datos** — repositories, data sources (Room DAOs, servicios Retrofit, DataStore), y entities. Responsable de obtener, cachear y persistir datos.
- **Capa de dominio** (opcional) — use cases y modelos de dominio. Encapsula lógica de negocio y orquesta llamadas a la capa de datos.
- **Capa de UI** — ViewModels, modelos de estado de UI y composables/views. Consume modelos de dominio y los presenta.

Cada capa tiene sus propios modelos, y las [mapper functions]({{ "/es/glosario/mapper-function/" | relative_url }}) convierten entre ellos en las fronteras. Esta separación es el fundamento del [patrón Mapper]({{ "/es/glosario/mapper-pattern/" | relative_url }}): `Entity → DomainModel → UiState`.

## The Senior Nuance (El Matiz Senior)

- Un Senior impone que las capas solo dependan hacia abajo: UI → Domain → Data. La capa de datos nunca importa clases de UI, y la capa de dominio nunca importa clases del framework (`Context`, `View`, tipos del Android SDK). La inversión de dependencias (interfaces en dominio, implementaciones en datos) habilita esto.
- En un proyecto Android multi-módulo, las capas a menudo se mapean a módulos Gradle: `:core:data`, `:core:domain`, `:feature:tasks:ui`. Las fronteras de módulos refuerzan la disciplina de capas en tiempo de build — un error de compilación es una garantía más fuerte que un comentario de code review.
- La capa de datos es el único lugar donde las preocupaciones de [thread safety]({{ "/es/glosario/thread-safety/" | relative_url }}) alrededor de I/O deberían vivir. Los repositories exponen `Flow` o funciones `suspend`; los callers no necesitan saber si los datos vienen de Room, Retrofit o un caché en memoria. Este es el principio de single-source-of-truth.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
