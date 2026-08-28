---
layout: post
title: "ClassCastException"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/class-cast-exception/
---

## La Teoría (El Qué)

Una **ClassCastException** es una excepción de runtime que se lanza cuando un [cast]({{ "/es/glosario/cast/" | relative_url }}) inseguro (`as`) falla — el tipo real del objeto no es compatible con el tipo destino. Es el equivalente en casting de [NullPointerException]({{ "/es/glosario/null-pointer-exception/" | relative_url }}): un crash causado por una suposición incorrecta sobre el tipo de un valor en runtime.

## El Matiz Senior

- En Kotlin, el safe cast `as?` retorna `null` en lugar de lanzar `ClassCastException`, haciéndolo la opción preferida cuando existe incertidumbre de tipo.
- Los [smart casts]({{ "/es/01-kotlin-core/smart-casts/" | relative_url }}) eliminan `ClassCastException` por completo para la mayoría de patrones: después de una verificación `is`, el compilador garantiza que el cast es válido.
- `ClassCastException` todavía puede ocurrir por el borrado de tipos genéricos (type erasure): `listOf(1, 2) as List<String>` tiene éxito en el cast (la JVM solo ve `List`) pero lanza `ClassCastException` después cuando los elementos se acceden como `String`.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
