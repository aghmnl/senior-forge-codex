---
layout: post
title: "Polymorphism"
date: 2026-08-19 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/polymorphism/
---

## The Theory (El Qué)

**Polimorfismo** (del griego: "muchas formas") es un principio fundamental de la programación orientada a objetos donde una única interfaz o tipo de referencia puede representar diferentes implementaciones subyacentes. En Kotlin y la JVM, el polimorfismo se manifiesta en tres formas principales:

- **Polimorfismo de Subtipo (Runtime)**: Una referencia de tipo padre puede apuntar a cualquier instancia de subclase. El dispatch de métodos ocurre en runtime a través del mecanismo de [virtual dispatch]({{ "/es/glosario/virtual-dispatch/" | relative_url }}) y la [vtable]({{ "/es/glosario/vtable/" | relative_url }}). Es la forma más común — ej. una `List<Animal>` conteniendo instancias de `Dog` y `Cat`.
- **Polimorfismo Ad-hoc**: [Sobrecarga de funciones]({{ "/es/glosario/function-overloading/" | relative_url }}) — múltiples funciones con el mismo nombre pero diferentes firmas de parámetros. Se resuelve en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}) vía [static dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }}).
- **Polimorfismo Paramétrico**: Generics — una única clase o función trabaja con cualquier parámetro de tipo (`List<T>`). En la JVM, los parámetros de tipo se borran en runtime ([type erasure]({{ "/es/glosario/type-erasure/" | relative_url }})), excepto cuando se usan funciones inline `reified` de Kotlin.

## The Senior Nuance (El Matiz Senior)

- En Android, el polimorfismo está en todas partes: `ViewModel`, `Fragment`, `RecyclerView.Adapter` están todos diseñados alrededor del polimorfismo de subtipo. Entender el dispatch por [vtable]({{ "/es/glosario/vtable/" | relative_url }}) ayuda a explicar por qué [final]({{ "/es/glosario/final/" | relative_url }}) (o las clases cerradas por defecto de Kotlin) pueden ser una ventaja de rendimiento — el JIT compiler puede devirtualizar métodos [final]({{ "/es/glosario/final/" | relative_url }}) en [static dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }}).
- Las [sealed classes]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}) combinan polimorfismo con [exhaustividad]({{ "/es/glosario/exhaustiveness/" | relative_url }}) — el compilador conoce todos los subtipos, así que las expresiones `when` son seguras sin `else`. Agregar un nuevo subtipo dispara un error de [compile time]({{ "/es/glosario/compile-time/" | relative_url }}) en cada `when` no manejado.
- Las [extension functions]({{ "/es/glosario/extension-functions/" | relative_url }}) en Kotlin **no** son polimórficas — se resuelven estáticamente en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}) basándose en el tipo declarado, no en el tipo en runtime. Esta es una pregunta común de entrevista que testea si un candidato realmente entiende [static dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }}) vs [virtual dispatch]({{ "/es/glosario/virtual-dispatch/" | relative_url }}).
- [Type erasure]({{ "/es/glosario/type-erasure/" | relative_url }}) limita el polimorfismo paramétrico en runtime: no podés chequear `is List<String>` porque el argumento de tipo se borra. La combinación `reified` + `inline` de Kotlin es el escape hatch.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
