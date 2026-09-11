---
layout: post
title: "KProperty"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
tags: [delegation, reflection]
lang: es
permalink: /es/glosario/kproperty/
---

## The Theory (El Qué)

**`KProperty<*>`** es el tipo de reflection en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) que representa una propiedad de Kotlin. Forma parte del paquete `kotlin.reflect` y transporta metadata sobre la propiedad: su nombre, tipo de retorno, visibilidad, y si es `lateinit`, `const`, o una [propiedad delegada]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}).

Cada operador de [propiedad delegada]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}) — `getValue`, `setValue` y `provideDelegate` — recibe un parámetro `KProperty<*>`. El compilador genera este objeto automáticamente en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}) y lo pasa en cada acceso:

```kotlin
operator fun <T> ReadOnlyProperty<Any?, T>.getValue(
    thisRef: Any?,
    property: KProperty<*>
): T
```

La jerarquía es: `KCallable` → `KProperty` → `KProperty0` (top-level) / `KProperty1` (miembro) / `KProperty2` (extensión). Las variantes mutables son `KMutableProperty0`, etc.

## The Senior Nuance (El Matiz Senior)

- Un Senior usa `property.name` dentro de delegates custom para derivación automática de claves — por ejemplo, mapeando nombres de propiedades a claves de SharedPreferences o nombres de columnas de base de datos sin strings hardcodeados. Este es uno de los usos más prácticos del parámetro `KProperty`.
- Acceder a la metadata de `KProperty` no requiere la dependencia completa de `kotlin-reflect`. La interfaz básica `KProperty` y su campo `name` son parte de `kotlin-stdlib`. La reflection completa (anotaciones, parámetros de tipo, bounds genéricos) requiere el artefacto `kotlin-reflect`.
- En [propiedades delegadas]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}), la instancia de `KProperty<*>` se crea una vez por declaración de propiedad (no por acceso) y se reutiliza. El [overhead]({{ "/es/glosario/overhead/" | relative_url }}) es un solo campo estático por propiedad delegada — despreciable en la práctica.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
