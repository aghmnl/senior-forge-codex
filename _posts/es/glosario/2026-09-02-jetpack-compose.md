---
layout: post
title: "Jetpack Compose"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/jetpack-compose/
---

## The Theory (El Qué)

**Jetpack Compose** es el toolkit declarativo moderno de UI para Android. En lugar de construir vistas imperativamente (crear objeto → mutar estado → invalidar), describís *cómo* debería verse la pantalla para un estado dado, y el framework se encarga del rendering, el diffing y las actualizaciones. Compose es un [DSL]({{ "/es/glosario/dsl/" | relative_url }}) de Kotlin: cada función `@Composable` es una [función de orden superior]({{ "/es/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) que acepta una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) `content` con un [receiver type]({{ "/es/glosario/receiver-type/" | relative_url }}) — `ColumnScope.() -> Unit`, `RowScope.() -> Unit` — de modo que solo los métodos válidos dentro de ese layout están disponibles.

```kotlin
// From FollowApp Suite — ConfirmationDialog.kt
@Composable
fun ConfirmationDialog(
    title: String,
    message: String,
    confirmLabel: String,
    dismissLabel: String,
    onConfirm: (dontAskAgain: Boolean) -> Unit,
    onDismiss: () -> Unit,
    dontAskAgainLabel: String? = null,
) {
    var dontAskAgain by remember { mutableStateOf(false) }
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(title) },
        text = {
            Column {
                Text(message)
                if (dontAskAgainLabel != null) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { dontAskAgain = !dontAskAgain }
                            .padding(top = 16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Checkbox(
                            checked = dontAskAgain,
                            onCheckedChange = { dontAskAgain = it }
                        )
                        Text(dontAskAgainLabel, style = MaterialTheme.typography.bodyMedium)
                    }
                }
            }
        },
        confirmButton = {
            TextButton(onClick = { onConfirm(dontAskAgain) }) { Text(confirmLabel) }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text(dismissLabel) }
        }
    )
}
```

## The Senior Nuance (El Matiz Senior)

- Compose es un [DSL]({{ "/es/glosario/dsl/" | relative_url }}) construido sobre [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) con [receivers]({{ "/es/glosario/receiver-type/" | relative_url }}). La anotación `@LayoutScopeMarker` actúa como un `@DslMarker` para prevenir la fuga de [scope]({{ "/es/glosario/scope/" | relative_url }}) — no podés llamar a `Modifier.weight()` de `Column` dentro de un `Row`. Esto es seguridad en [compile-time]({{ "/es/glosario/compile-time/" | relative_url }}) que los layouts XML nunca tuvieron.
- El plugin del compilador de Compose transforma las funciones `@Composable` a nivel de [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) — agrega parámetros ocultos `Composer` y `$changed` que habilitan el tracking de recomposición. No es Kotlin estándar; la anotación `@Composable` es un contrato con el compilador, no solo metadata.
- La cadena de `Modifier` en Compose es una API fluent cuyo **orden importa**: `.padding(16.dp).background(Color.Red)` aplica padding y luego colorea, `.background(Color.Red).padding(16.dp)` colorea y luego aplica padding. Entender esto es un diferenciador común en entrevistas.
- A diferencia de las vistas basadas en XML, Compose no usa [herencia]({{ "/es/glosario/inheritance/" | relative_url }}) para el layout. Cada elemento de UI es una función, y la composición reemplaza a la herencia — un cambio fundamental alineado con el principio de favorecer composición sobre herencia.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
