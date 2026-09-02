---
layout: post
title: "Ktor Routing"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/ktor-routing/
---

## The Theory (The What)

**Ktor Routing** is the [DSL]({{ "/en/glossary/dsl/" | relative_url }}) that defines HTTP endpoints in Ktor, JetBrains' asynchronous Kotlin framework for servers and clients. Routes are declared as nested [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) with [receiver types]({{ "/en/glossary/receiver-type/" | relative_url }}), making the structure mirror the URL hierarchy. Each handler (`get`, `post`, `put`, `delete`) is a [higher-order function]({{ "/en/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) that receives a suspend lambda — the route handler — executed within a `PipelineContext` receiver that provides access to `call`, `request`, and `response`.

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

## The Senior Nuance

- Ktor Routing demonstrates the same [DSL]({{ "/en/glossary/dsl/" | relative_url }}) pattern as [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) and [Gradle Kotlin DSL]({{ "/en/glossary/gradle-kotlin-dsl/" | relative_url }}): [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) with [receivers]({{ "/en/glossary/receiver-type/" | relative_url }}) create nested [scopes]({{ "/en/glossary/scope/" | relative_url }}) that restrict available methods. Inside `routing {}`, only route-level functions are visible; inside `get {}`, the handler context provides `call`.
- The `route("/path") {}` nesting is compositional: you can extract a group of routes into an [extension function]({{ "/en/01-kotlin-core/extension-functions/" | relative_url }}) on `Route` — `fun Route.taskRoutes()` — and call it from the main routing block. This is a clean-architecture pattern: one file per resource, composed at the top level.
- All route handlers are `suspend` [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}), which means they execute on Ktor's coroutine-based engine without blocking threads. The `call.receive<T>()` and `call.respond()` methods are suspend functions themselves — Ktor is fully non-blocking from handler to serialization.
- For Android developers, understanding Ktor Routing is interview-relevant for full-stack Kotlin positions and Kotlin Multiplatform (KMP) projects where the backend is also Kotlin.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
