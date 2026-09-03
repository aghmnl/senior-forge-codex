---
layout: post
title: "Ktor Routing"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/ktor-routing/
---

## The Theory (El Qué)

**Ktor Routing** es el [DSL]({{ "/es/glosario/dsl/" | relative_url }}) que define endpoints HTTP en Ktor, el framework asincrónico de JetBrains para servidores y clientes en Kotlin. Las rutas se declaran como [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) anidadas con [receiver types]({{ "/es/glosario/receiver-type/" | relative_url }}), haciendo que la estructura refleje la jerarquía de URLs. Cada handler (`get`, `post`, `put`, `delete`) es una [función de orden superior]({{ "/es/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) que recibe una suspend lambda — el handler de la ruta — ejecutado dentro de un receiver `PipelineContext` que provee acceso a `call`, `request` y `response`.

```kotlin
// Not found in FAS — standalone example
fun Application.configureRouting() {
    routing {
        route("/api/v1") {
            get("/tasks") {
                val tasks = taskRepository.getAll()
                call.respond(tasks)
            }
            post("/tasks") {
                val request = call.receive<CreateTaskRequest>()
                val created = taskRepository.create(request)
                call.respond(HttpStatusCode.Created, created)
            }
            route("/tasks/{id}") {
                get {
                    val id = call.parameters["id"] ?: return@get call.respond(
                        HttpStatusCode.BadRequest
                    )
                    val task = taskRepository.getById(id)
                        ?: return@get call.respond(HttpStatusCode.NotFound)
                    call.respond(task)
                }
                delete {
                    val id = call.parameters["id"] ?: return@delete call.respond(
                        HttpStatusCode.BadRequest
                    )
                    taskRepository.delete(id)
                    call.respond(HttpStatusCode.NoContent)
                }
            }
        }
    }
}
```

## The Senior Nuance (El Matiz Senior)

- Ktor Routing demuestra el mismo patrón de [DSL]({{ "/es/glosario/dsl/" | relative_url }}) que [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) y [Gradle Kotlin DSL]({{ "/es/glosario/gradle-kotlin-dsl/" | relative_url }}): [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) con [receivers]({{ "/es/glosario/receiver-type/" | relative_url }}) crean [scopes]({{ "/es/glosario/scope/" | relative_url }}) anidados que restringen los métodos disponibles. Dentro de `routing {}`, solo las funciones de nivel de ruta son visibles; dentro de `get {}`, el contexto del handler provee `call`.
- El anidamiento de `route("/path") {}` es composicional: podés extraer un grupo de rutas en una [función de extensión]({{ "/es/01-kotlin-core/extension-functions/" | relative_url }}) sobre `Route` — `fun Route.taskRoutes()` — y llamarla desde el bloque de routing principal. Es un patrón de clean architecture: un archivo por recurso, compuesto en el nivel superior.
- Todos los handlers de ruta son suspend [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}), lo que significa que se ejecutan sobre el motor basado en coroutines de Ktor sin bloquear hilos. Los métodos `call.receive<T>()` y `call.respond()` son suspend functions en sí mismos — Ktor es completamente non-blocking desde el handler hasta la serialización.
- Para desarrolladores Android, entender Ktor Routing es relevante en entrevistas para posiciones full-stack Kotlin y proyectos Kotlin Multiplatform (KMP) donde el backend también es Kotlin.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
