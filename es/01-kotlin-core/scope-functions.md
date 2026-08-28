---
layout: page
title: Scope Functions
lang: es
permalink: /es/01-kotlin-core/scope-functions/
order: 8
---

## The Theory (El Qué)

Las scope functions (`let`, `run`, `with`, `apply` y `also`) ejecutan un bloque de código dentro del [contexto]({{ "/es/glosario/context-programming/" | relative_url }}) de un objeto. Su diferencia principal radica en dos factores:

- **Cómo se referencia al objeto de contexto**: como `this` (receptor implícito) o como `it` (argumento de la lambda).
- **Qué devuelve la función**: el objeto de contexto en sí, o el resultado de la lambda.

Estas funciones no introducen capacidades técnicas nuevas, sino que ofrecen una forma concisa de gestionar el estado del objeto y sus [transformaciones]({{ "/es/glosario/data-transformation/" | relative_url }}) dentro de un [scope]({{ "/es/glosario/scope/" | relative_url }}) temporal.

### Referencia Rápida

| Función  | Ref. objeto | Devuelve          | Uso típico                                |
|----------|------------|-------------------|-------------------------------------------|
| `let`    | `it`       | Resultado lambda  | Cadenas null-safe, transformaciones       |
| `run`    | `this`     | Resultado lambda  | Computación con scope, inicialización     |
| `with`   | `this`     | Resultado lambda  | Múltiples operaciones sobre mismo objeto  |
| `apply`  | `this`     | Objeto contexto   | Configuración de objetos, builders        |
| `also`   | `it`       | Objeto contexto   | Efectos secundarios (logging, caching)    |

## The Senior Perspective (El Porqué)

Un desarrollador Senior ve las scope functions como herramientas de [señalización de intención]({{ "/es/glosario/intent-signaling/" | relative_url }}), no como simple [syntax sugar]({{ "/es/glosario/syntax-sugar/" | relative_url }}). Elegir la función incorrecta es un code smell común que degrada la mantenibilidad.

- **Claridad de Intención**: Cada scope function comunica un propósito diferente. Usar `apply` señala "estoy configurando este objeto"; usar `let` señala "estoy transformando este valor". Elegir la correcta hace que el código se auto-documente.
- **Evitar el Anidamiento**: Anidar múltiples scope functions es un antipatrón significativo. Oscurece el contexto de `this` o `it`, haciendo el código propenso a errores lógicos y reduciendo la legibilidad.
- **Efectos Secundarios vs. Transformaciones**: Usar `also` específicamente para efectos secundarios (como logging o caching) que no alteran el flujo primario del objeto, asegurando una separación clara de responsabilidades.

## Code in Action

### `apply` — Configuración de objetos

Devuelve el objeto de contexto después de configurarlo. Ideal para builders, Intents y serialización.

```kotlin
// De FollowApp Suite: BackupSerializer.kt
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
// De FollowApp Suite: AppIcons.kt — caching lazy manual
private var _mountainFlag: ImageVector? = null

val MountainFlag: ImageVector
    get() = _mountainFlag ?: SvgToImageVector.createImageVectorFromSvg(
        AppSvgs.MountainFlag
    ).also { _mountainFlag = it }
```

### `let` — Transformación null-safe

Devuelve el resultado de la lambda. El objeto de contexto está disponible como `it` (o con nombre), lo que lo hace ideal para cadenas con valores nulables.

```kotlin
// De FollowApp Suite: DatePickerField.kt
val dateText = dueDate?.let { date ->
    Instant.ofEpochMilli(date)
        .atZone(ZoneId.systemDefault())
        .format(formatter)
}
```

### `with` — Múltiples operaciones con un receptor compartido

Devuelve el resultado de la lambda. A diferencia de las demás, `with` recibe el objeto de contexto como argumento, no como receptor.

```kotlin
// De FollowApp Suite: TaskFormSheet.kt — conversiones de densidad en Compose
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

**Pregunta**: ¿Cuándo preferirías estrictamente `run` sobre `let`, y cuál es el riesgo de usar `apply` para transformaciones de datos?

**Respuesta Senior**: Prefiero `run` sobre `let` cuando la operación requiere acceder a los miembros del objeto directamente vía `this` en lugar del argumento `it`, lo cual es más limpio para inicializaciones complejas que devuelven un resultado. El riesgo de usar `apply` para transformaciones es que siempre devuelve el objeto de contexto original sin importar la lógica de la lambda; si la intención era transformar el objeto en un tipo o valor diferente, `apply` ignorará silenciosamente ese resultado, provocando bugs sutiles donde el objeto original fluye downstream en lugar del valor transformado.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
