---
layout: post
title: "Operator Overloading"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/operator-overloading/
---

## The Theory (El Qué)

**Operator Overloading** (sobrecarga de operadores) permite definir o redefinir operadores (`+`, `-`, `[]`, `()`, `in`, `..`, etc.) para tus propios tipos escribiendo una función con el modificador `operator` y un nombre predefinido (`plus`, `minus`, `get`, `invoke`, `contains`, `rangeTo`, etc.). Es uno de los bloques fundamentales que habilitan los [DSLs]({{ "/es/glosario/dsl/" | relative_url }}) de Kotlin: el encadenamiento de `Modifier.then()` en [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}), el bloque `dependencies {}` de [Gradle Kotlin DSL]({{ "/es/glosario/gradle-kotlin-dsl/" | relative_url }}), el [destructuring]({{ "/es/glosario/destructuring/" | relative_url }}) de colecciones, e incluso la keyword `by` para propiedades delegadas — todos dependen de convenciones de operadores internamente.

El operador más significativo arquitectónicamente en Android es `invoke` — permite que una instancia de clase se llame como una función usando `()`.

```kotlin
// From FollowApp Suite — GetPresetsUseCase.kt
class GetPresetsUseCase @Inject constructor(
    private val repository: PresetRepository
) {
    operator fun invoke(): Flow<List<Preset>> = repository.getAll()
}
```

```kotlin
// From FollowApp Suite — DeleteLabelUseCase.kt
class DeleteLabelUseCase @Inject constructor(
    private val labelRepository: LabelRepository
) {
    suspend operator fun invoke(labelId: String) {
        labelRepository.deleteLabel(labelId)
    }
}
```

Con `operator fun invoke`, los use cases se llaman como `getPresetsUseCase()` en lugar de `getPresetsUseCase.execute()` — esta es la convención adoptada por las guías de arquitectura de Google para Android.

## The Senior Nuance (El Matiz Senior)

- **`invoke` como Convención de Use Cases**: El patrón `operator fun invoke` convierte una clase en un objeto invocable. Cada use case en un proyecto Android con Clean Architecture sigue esta convención — el ViewModel mantiene una referencia al use case y lo llama como una función. Esto mantiene la API surface mínima (un método público por clase) mientras permite dependencias inyectadas por [constructor]({{ "/es/glosario/constructor/" | relative_url }}).
- **`get` / `set` para acceso indexado**: `operator fun get(index: Int)` permite que tu tipo soporte la sintaxis de corchetes (`myCollection[3]`). Las [Collections]({{ "/es/glosario/collections/" | relative_url }}) como `List` y `Map` usan esto. También lo usa `SnapshotStateList` de Compose.
- **`contains` para chequeos con `in`**: `operator fun contains(element: T): Boolean` habilita la sintaxis `element in myCollection` — más legible que `.contains()` y usada por las [when expressions]({{ "/es/glosario/when-expression/" | relative_url }}) con rangos.
- **Advertencia de Abuso**: Sobrecargar operadores para que signifiquen algo inesperado (ej. `+` para insertar en base de datos) es un antipatrón serio. La semántica del operador debe coincidir con las expectativas del lector. Si no es inmediatamente obvio qué significa `a + b` para tu tipo, usá una función con nombre.
- **Fundamento de DSLs**: Las [funciones de extensión]({{ "/es/01-kotlin-core/extension-functions/" | relative_url }}) con `operator` habilitan sintaxis natural de [DSL]({{ "/es/glosario/dsl/" | relative_url }}) — `rangeTo` impulsa `1..10`, `compareTo` impulsa las comparaciones `<`/`>`, y `provideDelegate` impulsa la delegación con `by`. Entender la tabla de operadores es clave para leer los internals de los [DSLs]({{ "/es/glosario/dsl/" | relative_url }}) de Kotlin.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
