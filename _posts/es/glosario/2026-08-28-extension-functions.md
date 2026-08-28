---
layout: post
title: "Extension Functions"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/extension-functions/
---

## The Theory (El Qué)

Las **extension functions** permiten agregar nuevas funciones a clases existentes sin modificar su código fuente ni usar herencia. Sintácticamente lucen como funciones miembro (`receiver.functionName()`), pero se resuelven **estáticamente en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }})** basándose en el tipo declarado del receptor — no en el tipo en [tiempo de ejecución]({{ "/es/glosario/runtime/" | relative_url }}). Internamente, el compilador de Kotlin las traduce a métodos estáticos donde el receptor se convierte en el primer parámetro.

## The Senior Nuance (El Matiz Senior)

- Como las extensiones se resuelven en tiempo de compilación, **no** participan en dispatch virtual. Si una clase base y una subclase tienen una extensión con la misma firma, la que se invoca depende del tipo *declarado*, no del tipo real. Esto es lo opuesto a funciones miembro sobreescritas.
- Las extension functions compilan a métodos estáticos en la [JVM]({{ "/es/glosario/jvm/" | relative_url }}). `fun String.isPalindrome()` se convierte en `public static boolean isPalindrome(String $this$isPalindrome)` en el [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}). No hay overhead en runtime — sin objetos wrapper, sin reflexión.
- En codebases Android/Kotlin, las extension functions son la forma idiomática de escribir utilidades de mapeo/conversión — se leen naturalmente y mantienen los modelos de dominio libres de preocupaciones de infraestructura.
- Las extensiones no pueden acceder a miembros `private` o `protected` de la clase receptora. Solo ven la API pública de la clase, lo que las hace más seguras que la herencia.

```kotlin
// From FollowApp Suite — LabelMapper.kt
fun LabelEntity.toDomain(): Label = Label(
    id = this.id,
    name = this.name,
    type = LabelType.valueOf(this.type),
    createdAt = this.createdAt,
    updatedAt = this.updatedAt
)
```

```kotlin
// From FollowApp Suite — ErrorMapping.kt
@StringRes
fun Throwable.toUserMessage(): Int = when {
    this is SQLiteConstraintException && message.orEmpty().contains("UNIQUE") ->
        R.string.error_duplicate_tag
    else -> R.string.error_generic
}
```

Ambas funciones agregan comportamiento a tipos existentes (`LabelEntity`, `Throwable`) sin modificar esas clases. El compilador resuelve la llamada basándose en el tipo declarado en cada sitio de llamada.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
