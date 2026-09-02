---
layout: post
title: "Single Responsibility Principle"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/single-responsibility-principle/
---

## The Theory (El Qué)

El **Single Responsibility Principle (SRP)** (Principio de Responsabilidad Única) establece que una clase (o módulo, o función) debería tener solo una razón para cambiar — es decir, debería encapsular exactamente una responsabilidad. Es la "S" de los principios SOLID. En la práctica, SRP significa que una clase que maneja tanto persistencia de datos como formateo de UI está haciendo demasiado: los cambios en el schema de la base de datos no deberían forzar cambios en la capa de UI, y viceversa.

En Kotlin y Android, SRP se manifiesta en cada capa: los ViewModels manejan gestión de estado (no data fetching), los Repositories manejan acceso a datos (no lógica de negocio), y los Use Cases encapsulan operaciones de negocio individuales.

## The Senior Nuance (El Matiz Senior)

- **SRP es sobre cohesión, no tamaño**: Una clase de 500 líneas que todas sirven un solo propósito sigue SRP mejor que una clase de 50 líneas que mezcla dos concerns no relacionados. La pregunta es "¿qué causaría que esto cambie?" — si la respuesta es dos stakeholders diferentes o dos razones diferentes, la clase tiene dos responsabilidades.
- **En la arquitectura Android**: El patrón Repository existe por SRP — la lógica de acceso a datos (Room, Retrofit) se separa de la lógica de negocio (Use Cases) y la lógica de presentación (ViewModels). [Hilt]({{ "/es/glosario/hilt/" | relative_url }}) y los [dependency graphs]({{ "/es/glosario/dependency-graph/" | relative_url }}) hacen esta separación en capas práctica al wirear las piezas.
- **A nivel de función**: Las scope functions de Kotlin hacen cumplir un SRP a micro-nivel — `also` maneja side effects (logging, caching) separados de la cadena de transformación principal, manteniendo cada paso enfocado en una sola tarea. Por eso los desarrolladores senior prefieren `also` para side effects en lugar de mezclarlos en bloques `apply` o `let`.
- **Advertencia de sobre-aplicación**: Separar responsabilidades demasiado agresivamente lleva a "ravioli code" — docenas de clases diminutas que individualmente hacen una cosa pero colectivamente oscurecen el flujo. Los ingenieros senior balancean SRP contra legibilidad: si dos responsabilidades siempre cambian juntas, quizás pertenecen a la misma clase.
- **Señal de testing**: Si una clase es difícil de testear porque requiere muchos mocks de dominios no relacionados (un mock de base de datos Y un mock de red Y un mock de UI framework), es señal de que viola SRP. Responsabilidades bien separadas llevan a tests enfocados y fáciles de escribir.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
