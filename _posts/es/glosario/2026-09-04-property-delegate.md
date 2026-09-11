---
layout: post
title: "Property Delegate"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
tags: [delegation, syntax, memory]
lang: es
permalink: /es/glosario/property-delegate/
---

## The Theory (El Qué)

Un **property delegate** (clase delegada, también llamado delegate class) es cualquier objeto que maneja la lógica de `get` y/o `set` de una propiedad en nombre de su propietario. En Kotlin, un property delegate se conecta a su propiedad vía la [keyword]({{ "/es/glosario/keyword/" | relative_url }}) [`by`]({{ "/es/glosario/by-delegation/" | relative_url }}):

```kotlin
val name: String by MyDelegate()
```

El delegado debe proveer `operator fun getValue(thisRef: T, property: KProperty<*>): R`. Para propiedades mutables, también debe proveer `operator fun setValue(thisRef: T, property: KProperty<*>, value: R)`. La [standard library]({{ "/es/glosario/standard-library/" | relative_url }}) de Kotlin ofrece las interfaces `ReadOnlyProperty<T, R>` y `ReadWriteProperty<T, R>` para [type safety]({{ "/es/glosario/type-safety/" | relative_url }}), pero implementarlas es opcional — la convención es estructural, resuelta vía [operator overloading]({{ "/es/glosario/operator-overloading/" | relative_url }}).

Los property delegates built-in incluyen `lazy`, `Delegates.observable`, `Delegates.vetoable` y `Delegates.notNull`. El ecosistema Android agrega `viewModels()`, `activityViewModels()` y `mutableStateOf()` de Compose. Ver [Delegated Properties]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}) para el tratamiento completo.

## The Senior Nuance (El Matiz Senior)

- Un Senior diseña property delegates custom para encapsular concerns transversales: loggear cada acceso a propiedad, sincronizar lecturas con un lock, leer desde SharedPreferences con derivación automática de clave vía [KProperty]({{ "/es/glosario/kproperty/" | relative_url }}).`name`, o validar valores antes de almacenarlos.
- El operador `provideDelegate` permite al delegado personalizarse en el momento de instalación — por ejemplo, verificando que el nombre de la propiedad coincida con una clave de configuración esperada. Esta es la diferencia entre un delegado genérico y uno que es consciente de su contexto de instalación.
- Los property delegates son objetos que viven en el [heap]({{ "/es/glosario/heap/" | relative_url }}). Cada declaración `by` crea una instancia de delegado por propiedad. Un Senior es consciente de este [overhead]({{ "/es/glosario/overhead/" | relative_url }}) en clases con muchas propiedades delegadas instanciadas en loops ajustados.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
