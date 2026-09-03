---
layout: post
title: "@Before"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/junit-before/
---

## The Theory (El Qué)

**`@Before`** es una anotación de JUnit 4 (y `@BeforeEach` en JUnit 5) que marca un método para ejecutarse antes de cada método de test en la clase. Es el hook estándar de setup para test fixtures: crear instancias frescas de colaboradores, inicializar propiedades `lateinit`, configurar mocks y preparar el sistema bajo test. El método corre una vez por test, asegurando aislamiento entre tests.

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
}
```

Cada test recibe un `FakePresetRepository` y `CleanUpPresetsUseCase` frescos — sin estado mutable compartido entre tests.

## The Senior Nuance (El Matiz Senior)

- **`@Before` + `lateinit` es el patrón canónico**: Las clases de test declaran dependencias como `lateinit var` (evitando tipos nullable) y las inicializan en `@Before`. Esto mantiene el código de test limpio — sin operadores `!!`, sin checks `?`, sin delegación `lazy` — solo acceso directo a propiedades que se lee como código de producción.
- **`@Before` vs `@BeforeClass`/`@BeforeAll`**: `@Before` corre por test (setup a nivel de instancia); `@BeforeClass` (JUnit 4) / `@BeforeAll` (JUnit 5) corre una vez por clase (setup compartido). Los desarrolladores senior usan setup por test por defecto y solo comparten setup cuando es costoso y probadamente stateless (ej. arrancar una base de datos en memoria).
- **Pareado con teardown**: `@After` corre después de cada test y debería liberar recursos adquiridos en `@Before` — cerrar bases de datos, cancelar [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) scopes, limpiar estado compartido. Olvidarse de `@After` puede causar contaminación de tests donde el estado de un test leakea al siguiente.
- **Tests instrumentados Android**: En tests `@RunWith(AndroidJUnit4::class)`, `@Before` frecuentemente setea bases de datos Room en memoria, DataStores con scopes de test, o componentes Hilt de test. El codebase de FAS usa este patrón extensivamente para tests de integración.
- **Interacción con Rules**: Los campos `@Rule` de JUnit 4 se inicializan antes de que corra `@Before`. Esto significa que rules como `InstantTaskExecutorRule` o `MainCoroutineRule` ya están activas cuando tu método de setup ejecuta — un detalle sutil de orden que importa cuando el código de setup toca LiveData o [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
