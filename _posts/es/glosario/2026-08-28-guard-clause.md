---
layout: post
title: "Guard Clause"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/guard-clause/
---

## La Teoría (El Qué)

Una **guard clause** es un retorno temprano al inicio de una función que rechaza inputs inválidos o casos borde antes de que se ejecute la lógica principal. Al manejar el caso excepcional primero y retornar inmediatamente, el resto de la función puede asumir el camino feliz sin condicionales anidados.

## El Matiz Senior

- En Kotlin, el operador Elvis con `return` (`val x = nullable ?: return`) es la guard clause idiomática para verificaciones de null. Elimina el tipo nullable del resto del [scope]({{ "/es/glosario/scope/" | relative_url }}), haciendo que el código restante trabaje solo con tipos no-null — sin `!!`, sin `if` anidados.
- Las guard clauses también pueden retornar un valor (`?: return false`), lanzar una excepción (`?: throw IllegalArgumentException("razón")`), o continuar un loop (`?: continue`). Cada una comunica un contrato diferente.
- Abusar de las guard clauses puede fragmentar los puntos de salida de una función. Un Senior balancea los retornos tempranos con la legibilidad: si una función tiene más de tres guards, quizás el llamador debería encargarse de la validación.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
