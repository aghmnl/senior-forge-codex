---
layout: post
title: "when Expression"
date: 2026-08-19 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/when-expression/
---

## The Theory (El Qué)

La **expresión `when`** en Kotlin es una construcción de flujo de control poderosa que reemplaza el `switch` de Java con una alternativa más expresiva y segura. A diferencia de `switch`, `when` puede hacer match contra expresiones arbitrarias (no solo constantes), soporta pattern matching con `is` (habilitando [smart casts]({{ "/es/01-kotlin-core/smart-casts/" | relative_url }})), rangos (`in 1..10`), colecciones (`in listOf(...)`), y múltiples condiciones por rama. Cuando se usa como expresión (asignada a una variable o retornada), el compilador exige exhaustividad — todos los casos posibles deben estar manejados.

## The Senior Nuance (El Matiz Senior)

- **`when` exhaustivo + Sealed Classes**: Cuando el sujeto es una [sealed class o interface]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}), el compilador conoce todos los subtipos y exige que cada rama esté cubierta — sin necesidad de `else`. Esta es una red de seguridad en compile time: si se agrega un nuevo subtipo después, cada `when` que maneje ese tipo sealed no compilará hasta que se actualice.
- **Expresión vs. Statement**: `when` como statement no requiere exhaustividad. `when` como expresión (ej. `val result = when(x) { ... }`) sí. El código Senior prefiere la forma de expresión para obtener la garantía de exhaustividad.
- **Sin Fall-Through**: A diferencia del `switch` de Java, el `when` de Kotlin no tiene fall-through entre ramas. Cada rama es independiente, eliminando toda una clase de bugs causados por `break` faltantes.
- **Rendimiento**: El compilador optimiza `when` sobre enums y sealed classes en instrucciones bytecode eficientes `tableswitch` o `lookupswitch`, haciéndolo tan rápido como el `switch` de Java.

```kotlin
sealed interface PaymentMethod {
    data class CreditCard(val last4: String) : PaymentMethod
    data class BankTransfer(val bankName: String) : PaymentMethod
    data object Cash : PaymentMethod
}

// when exhaustivo — el compilador exige todas las ramas
fun describe(method: PaymentMethod): String = when (method) {
    is PaymentMethod.CreditCard -> "Tarjeta terminada en ${method.last4}"
    is PaymentMethod.BankTransfer -> "Transferencia desde ${method.bankName}"
    PaymentMethod.Cash -> "Pago en efectivo"
}
```

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
