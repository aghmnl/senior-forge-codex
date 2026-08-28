---
layout: post
title: "Polymorphism"
date: 2026-08-19 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/polymorphism/
---

## La Teoría (El Qué)

**Polimorfismo** (del griego: "muchas formas") es un principio fundamental de la programación orientada a objetos donde una única interfaz o tipo de referencia puede representar diferentes implementaciones subyacentes. En Kotlin y la JVM, el polimorfismo se manifiesta en tres formas principales:

- **Polimorfismo de Subtipo (Runtime)**: Una referencia de tipo padre puede apuntar a cualquier instancia de subclase. El dispatch de métodos ocurre en runtime a través de la tabla de métodos virtuales (vtable). Es la forma más común — ej. una `List<Animal>` conteniendo instancias de `Dog` y `Cat`.
- **Polimorfismo Ad-hoc**: Sobrecarga de funciones — múltiples funciones con el mismo nombre pero diferentes firmas de parámetros. Se resuelve en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}).
- **Polimorfismo Paramétrico**: Generics — una única clase o función trabaja con cualquier parámetro de tipo (`List<T>`). En la JVM, los parámetros de tipo se borran en runtime (type erasure), excepto cuando se usan funciones inline `reified` de Kotlin.

## El Matiz Senior

- En Android, el polimorfismo está en todas partes: `ViewModel`, `Fragment`, `RecyclerView.Adapter` están todos diseñados alrededor del polimorfismo de subtipo. Entender el dispatch por vtable ayuda a explicar por qué `final` (o las clases cerradas por defecto de Kotlin) pueden ser una ventaja de rendimiento.
- Las sealed classes combinan polimorfismo con exhaustividad — el compilador conoce todos los subtipos, así que las expresiones `when` son seguras sin `else`.
- Las extension functions en Kotlin **no** son polimórficas — se resuelven estáticamente en compile time basándose en el tipo declarado, no en el tipo en runtime. Esta es una pregunta común de entrevista.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
