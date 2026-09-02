---
layout: page
title: Lateinit vs Lazy
lang: es
permalink: /es/01-kotlin-core/lateinit-vs-lazy/
order: 9
---

## The Theory (El Qué)

Tanto `lateinit` como `lazy` ofrecen formas de retrasar la inicialización de propiedades, pero cumplen propósitos técnicos distintos:

- **`lateinit`** es un modificador para variables mutables (`var`) que no son nulables y se inicializarán más tarde — frecuentemente por un framework (Hilt/Dagger vía [inyección]({{ "/es/glosario/dependency-graph/" | relative_url }})), un método de setup en tests, o durante un evento del ciclo de vida. No se puede usar con tipos [primitivos]({{ "/es/glosario/primitives/" | relative_url }}) (`Int`, `Boolean`, etc.) porque la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) no tiene forma de representar "no inicializado" para ellos.
- **`lazy`** es una propiedad delegada para variables de solo lectura (`val`) que calcula el valor solo en su primer acceso y cachea el resultado para todas las lecturas futuras. Internamente, crea un objeto delegado `Lazy<T>` cuyo método `getValue()` protege la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) de inicialización.

La distinción clave: `lateinit` significa "prometo que lo asignaré antes de usarlo"; `lazy` significa "calcúlalo una vez, bajo demanda, y recuérdalo para siempre".

## The Senior Perspective (El Porqué)

Elegir entre ellos es una cuestión de **mutabilidad, seguridad de hilos y propiedad**.

- **Modos de Seguridad de Hilos**: Por defecto, `lazy` es thread-safe (`LazyThreadSafetyMode.SYNCHRONIZED`) — la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) de inicialización se ejecuta dentro de un bloque `synchronized`. Un Senior sabe cuándo usar `NONE` para optimizar el rendimiento si la propiedad se accede solo desde un hilo (ej. el hilo de UI en Compose), o `PUBLICATION` si varios hilos pueden calcular el valor simultáneamente y el primer resultado gana.
- **Patrón de Setup en Tests**: `lateinit` es el patrón estándar para dependencias de test que se conectan en un método `@Before`. Cada clase de test declara sus colaboradores como `lateinit var`, luego el setup crea instancias frescas — garantizando aislamiento entre tests sin boilerplate de nulabilidad. Es el uso más común de `lateinit` en proyectos Android reales.
- **Inyección de Dependencias**: `lateinit` es esencial para la inyección de campos (Hilt/Dagger). Dado que estos frameworks usan [Runtime Reflection]({{ "/es/glosario/runtime-reflection/" | relative_url }}) para asignar valores después de que el objeto es [construido]({{ "/es/glosario/constructor/" | relative_url }}), `lateinit` permite tipos no nulables sin chequeos de nulos. La inyección por [constructor]({{ "/es/glosario/constructor/" | relative_url }}) es preferible arquitectónicamente, pero `lateinit` es inevitable para los entry points de Android (`Activity`, `Fragment`, `Service`).
- **Gestión de Memoria**: `lazy` es ideal para objetos "pesados" (consultas costosas a base de datos, parseo complejo de configuración, o generación de iconos) porque difiere la [allocation]({{ "/es/glosario/allocations/" | relative_url }}) hasta que es estrictamente necesario. Si la propiedad nunca se accede, el objeto nunca se crea.
- **Chequeo de Estado**: Un Senior utiliza `::property.isInitialized` en propiedades `lateinit` para evitar `UninitializedPropertyAccessException` cuando el flujo de inicialización puede ser no lineal o condicional.

## Code in Action

### `lateinit` en setup de tests — dependencias frescas por test

El patrón estándar: declarar colaboradores de test como `lateinit var`, conectarlos en `@Before`, y cada test recibe una instancia fresca y aislada.

```kotlin
// From FollowApp Suite — CleanUpPresetsUseCaseTest.kt
class CleanUpPresetsUseCaseTest {

    private lateinit var presetRepo: FakePresetRepository
    private lateinit var useCase: CleanUpPresetsUseCase

    @Before
    fun setup() {
        presetRepo = FakePresetRepository()
        useCase = CleanUpPresetsUseCase(presetRepo)
    }

    @Test
    fun `deleting label preserves labelFilters`() = runBlocking {
        presetRepo.addPreset(preset("p1", labelFilters = mapOf(
            "Work" to LabelFilterState.INCLUDE
        )))
        useCase.onLabelDeleted("Work")
        val updated = presetRepo.getPresets().first()
        assertTrue(updated.labelFilters.containsKey("Work"))
    }
}
```

### `lateinit` a escala — test de integración con múltiples colaboradores

Cuando un test de integración necesita una base de datos real, un DAO, un DataStore y un importer, `lateinit` mantiene cada declaración no nulable y limpia.

```kotlin
// From FollowApp Suite — LegacyDataImporterTest.kt
@RunWith(AndroidJUnit4::class)
class LegacyDataImporterTest {

    private lateinit var db: MyTasksDatabase
    private lateinit var dao: TaskDao
    private lateinit var preferences: LegacyImportPreferences
    private lateinit var importer: LegacyDataImporter
    private lateinit var dataStoreScope: CoroutineScope

    @Before
    fun setup() {
        db = Room.inMemoryDatabaseBuilder(context, MyTasksDatabase::class.java)
            .allowMainThreadQueries()
            .build()
        dao = db.taskDao()
        dataStoreScope = CoroutineScope(Dispatchers.IO + Job())
        val dataStore = PreferenceDataStoreFactory.create(scope = dataStoreScope) {
            context.preferencesDataStoreFile(dataStoreName)
        }
        preferences = LegacyImportPreferences(dataStore)
        importer = LegacyDataImporter(LegacyTaskReader(context), dao, preferences)
    }
}
```

### `lazy` con caching manual vía `also`

Cuando `by lazy` no es idiomático (ej. un custom property getter que debe permanecer como propiedad calculada), la [scope function]({{ "/es/01-kotlin-core/scope-functions/" | relative_url }}) `also` puede replicar el caching de lazy manualmente.

```kotlin
// From FollowApp Suite — AppIcons.kt
private var _mountainFlag: ImageVector? = null

val MountainFlag: ImageVector
    get() = _mountainFlag ?: SvgToImageVector.createImageVectorFromSvg(
        AppSvgs.MountainFlag
    ).also { _mountainFlag = it }
```

### `lazy` con modo de seguridad de hilos — optimización single-thread

Cuando una propiedad se accede exclusivamente desde el hilo de UI, `LazyThreadSafetyMode.NONE` evita el bloque `synchronized` y elimina el overhead de la inicialización thread-safe.

```kotlin
// Not found in FAS — standalone example
class TaskDetailScreen(private val repository: TaskRepository) {

    val headerConfig: HeaderConfig by lazy(LazyThreadSafetyMode.NONE) {
        repository.loadExpensiveHeaderConfig()
    }
}
```

## The Interview (En el banquillo)

**Pregunta**: ¿Qué ocurre internamente cuando accedes a una propiedad `lazy` por primera vez, y en qué se diferencia de una propiedad `lateinit` a nivel de [bytecode]({{ "/es/glosario/bytecode/" | relative_url }})?

**Respuesta Senior**: Cuando se accede a una propiedad `lazy`, se llama al método delegado `getValue()`. Este comprueba un campo interno `_value`; si es el centinela `UNINITIALIZED_VALUE`, ejecuta la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) de inicialización dentro de un bloque `synchronized` (por defecto) para asegurar la seguridad de hilos, almacena el resultado y lo devuelve. Todos los accesos subsiguientes se saltan la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) y devuelven el valor cacheado directamente. En contraste, `lateinit` no utiliza delegación en absoluto; el compilador simplemente genera un acceso directo al campo pero añade un chequeo de nulos a nivel de [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) — si el backing field es `null`, lanza `UninitializedPropertyAccessException`. La diferencia clave en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}): `lazy` paga por la [allocation]({{ "/es/glosario/allocations/" | relative_url }}) de un objeto delegado más el overhead de sincronización, mientras que `lateinit` tiene cero overhead más allá del null-check.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
