---
layout: post
title: "Member Function"
date: 2026-09-21 12:00:00 +0000
categories: [es, glosario]
tags: [oop, dispatch, syntax]
lang: es
permalink: /es/glosario/member-function/
---

## The Theory (El Qué)

Una **member function** (función miembro) es una función declarada *dentro* del cuerpo de una clase, así que forma parte del tipo y participa del [virtual dispatch]({{ "/es/glosario/virtual-dispatch/" | relative_url }}): una subclase puede hacerle `override` y la llamada se resuelve por el tipo en runtime del objeto. Ese es el contraste decisivo con una [extension function]({{ "/es/glosario/extension-functions/" | relative_url }}), que compila a un método estático y se resuelve por el tipo *declarado*. Cuando existen las dos con la misma firma, **gana siempre el miembro** — en silencio.

```kotlin
// Not found in FAS — standalone example
class Text(val value: String) {
    fun shout() = value.uppercase() + "!"     // función miembro
}
fun Text.shout() = "nunca se llama"           // extensión: sombreada por el miembro

Text("hi").shout()   // "HI!" — gana el miembro
```

## The Senior Nuance (El Matiz Senior)

- **Una actualización de librería puede sombrear tu extensión.** Si una versión nueva agrega un miembro con la misma firma, tu extensión deja de llamarse en silencio y el comportamiento cambia sin error de compilación. Nombres únicos y visibilidad acotada limitan el alcance del daño.
- **Los miembros pueden tocar el estado [`private`]({{ "/es/glosario/private/" | relative_url }}); las extensiones no.** Esa suele ser la razón real por la que cierta lógica va adentro de la clase.
- **Los miembros se pueden mockear, las extensiones no.** Un miembro de una interfaz se puede reemplazar por un fake en un test; una extensión estática no.
- Ver [Extension Functions]({{ "/es/01-kotlin-core/extension-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
