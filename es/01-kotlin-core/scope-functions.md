---
layout: page
title: Scope Functions
lang: es
permalink: /es/01-kotlin-core/scope-functions/
order: 8
---

## The Theory (El Qué)

Las [scope]({{ "/es/glosario/scope/" | relative_url }}) functions (`let`, `run`, `with`, `apply` y `also`) ejecutan un bloque de código dentro del [contexto]({{ "/es/glosario/context-programming/" | relative_url }}) de un objeto. Son [funciones de orden superior]({{ "/es/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) integradas en la biblioteca estándar de Kotlin. Su diferencia principal radica en dos factores:

- **Cómo se referencia al objeto de contexto**: como `this` ([receiver]({{ "/es/glosario/receiver-type/" | relative_url }}) implícito) o como `it` (argumento de la [lambda]({{ "/es/glosario/lambdas/" | relative_url }})).
- **Qué devuelve la función**: el objeto de contexto en sí, o el resultado de la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}).

Estas funciones no introducen capacidades técnicas nuevas, sino que ofrecen una forma concisa de gestionar el estado del objeto y sus [transformaciones]({{ "/es/glosario/data-transformation/" | relative_url }}) dentro de un [scope]({{ "/es/glosario/scope/" | relative_url }}) temporal.

### Referencia Rápida

| Función  | Ref. objeto | Devuelve          | Uso típico                                |
|----------|------------|-------------------|-------------------------------------------|
| `let`    | `it`       | Resultado lambda  | Cadenas [null-safe]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}), transformaciones |
| `run`    | `this`     | Resultado lambda  | Computación con scope, inicialización     |
| `with`   | `this`     | Resultado lambda  | Múltiples operaciones sobre mismo objeto  |
| `apply`  | `this`     | Objeto contexto   | Configuración de objetos, builders        |
| `also`   | `it`       | Objeto contexto   | Efectos secundarios (logging, caching)    |

## The Senior Perspective (El Porqué)

Un desarrollador Senior ve las [scope]({{ "/es/glosario/scope/" | relative_url }}) functions como herramientas de [señalización de intención]({{ "/es/glosario/intent-signaling/" | relative_url }}), no como simple [syntax sugar]({{ "/es/glosario/syntax-sugar/" | relative_url }}). Elegir la función incorrecta es un code smell común que degrada la mantenibilidad.

- **Claridad de Intención**: Cada [scope]({{ "/es/glosario/scope/" | relative_url }}) function comunica un propósito diferente. Usar `apply` señala "estoy configurando este objeto"; usar `let` señala "estoy transformando este valor". Elegir la correcta hace que el código se auto-documente.
- **Evitar el Anidamiento**: Anidar múltiples [scope]({{ "/es/glosario/scope/" | relative_url }}) functions es un antipatrón significativo. Oscurece el contexto de `this` o `it`, haciendo el código propenso a errores lógicos y reduciendo la legibilidad. Cuando te encuentres anidando, extrae el bloque interno a una función con nombre.
- **Efectos Secundarios vs. Transformaciones**: Usar `also` específicamente para efectos secundarios (como logging o caching) que no alteran el flujo primario del objeto, asegurando una separación clara de responsabilidades. Es el equivalente en [scope]({{ "/es/glosario/scope/" | relative_url }}) functions del Single Responsibility Principle.
- **Rendimiento**: Las cinco [scope]({{ "/es/glosario/scope/" | relative_url }}) functions están declaradas como [inline]({{ "/es/glosario/inline-functions/" | relative_url }}) en la biblioteca estándar, lo que significa que la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) se inlinea en el call site — cero overhead de [allocation]({{ "/es/glosario/allocations/" | relative_url }}) de objetos, cero presión sobre el [Garbage Collector]({{ "/es/glosario/garbage-collector/" | relative_url }}). Úsalas libremente en hot paths.

## Code in Action

### `apply` — Configuración de objetos

Devuelve el objeto de contexto después de configurarlo. Ideal para builders, Intents y serialización.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
private fun taskToJson(task: TaskEntity): JSONObject = JSONObject().apply {
    put("id", task.id)
    put("title", task.title)
    put("description", task.description)
    put("status", task.status)
    put("isCompleted", task.isCompleted)
    put("dueDate", task.dueDate)
    put("createdAt", task.createdAt)
    put("updatedAt", task.updatedAt)
}
```

### `also` — Efectos secundarios sin alterar el flujo

Devuelve el objeto de contexto. El bloque realiza un efecto secundario (caching, logging) mientras el objeto pasa sin modificarse.

```kotlin
// From FollowApp Suite — AppIcons.kt
private var _mountainFlag: ImageVector? = null

val MountainFlag: ImageVector
    get() = _mountainFlag ?: SvgToImageVector.createImageVectorFromSvg(
        AppSvgs.MountainFlag
    ).also { _mountainFlag = it }
```

### `let` — Transformación null-safe

Devuelve el resultado de la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}). El objeto de contexto está disponible como `it` (o con nombre), lo que lo hace ideal para cadenas con valores nulables usando el operador [safe call]({{ "/es/glosario/safe-call/" | relative_url }}) `?.`.

```kotlin
// From FollowApp Suite — DatePickerField.kt
val dateText = dueDate?.let { date ->
    Instant.ofEpochMilli(date)
        .atZone(ZoneId.systemDefault())
        .format(formatter)
}
```

### `with` — Múltiples operaciones con un receiver compartido

Devuelve el resultado de la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}). A diferencia de las demás, `with` recibe el objeto de contexto como argumento, no como [receiver]({{ "/es/glosario/receiver-type/" | relative_url }}).

```kotlin
// From FollowApp Suite — TaskFormSheet.kt
val density = LocalDensity.current
val screenHeightPx = with(density) { LocalConfiguration.current.screenHeightDp.dp.toPx() }
val peekHeightPx = with(density) { PeekHeight.toPx() }
```

### `run` — Computación con scope que devuelve un resultado

Como `with`, pero se invoca directamente sobre el objeto. Útil cuando se necesita acceso a `this` y se quiere devolver un valor computado.

```kotlin
val displayLabel = notification.run {
    if (title.isBlank()) body.take(50)
    else "$title: ${body.take(30)}"
}
```

## The Interview (En el banquillo)

**Pregunta**: ¿Cuándo preferirías estrictamente `run` sobre `let`, y cuál es el riesgo de usar `apply` para [transformaciones]({{ "/es/glosario/data-transformation/" | relative_url }}) de datos?

**Respuesta Senior**: Prefiero `run` sobre `let` cuando la operación requiere acceder a los miembros del objeto directamente vía `this` en lugar del argumento `it`, lo cual es más limpio para inicializaciones complejas que devuelven un resultado. El riesgo de usar `apply` para [transformaciones]({{ "/es/glosario/data-transformation/" | relative_url }}) es que siempre devuelve el objeto de contexto original sin importar la lógica de la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}); si la intención era transformar el objeto en un tipo o valor diferente, `apply` ignorará silenciosamente ese resultado, provocando bugs sutiles donde el objeto original fluye downstream en lugar del valor transformado. La regla de [señalización de intención]({{ "/es/glosario/intent-signaling/" | relative_url }}) es simple: `apply` configura, `run`/`let` transforman.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
