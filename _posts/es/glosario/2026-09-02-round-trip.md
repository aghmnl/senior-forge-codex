---
layout: post
title: "Round-Trip"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/round-trip/
---

## The Theory (El Qué)

Un **round-trip** (viaje de ida y vuelta) es un ciclo completo de request-response entre dos boundaries del sistema — típicamente entre la capa de UI y un data source (base de datos, API de red, o file system). El request viaja "hacia afuera" al data source y la response viaja "de vuelta", de ahí "round-trip". El tiempo que esto toma es el **round-trip time (RTT)**, y es frecuentemente el factor dominante en la latencia percibida de la UI.

```
UI ──request──▶ Repository ──query──▶ Database
UI ◀──response── Repository ◀──result── Database
         └───────── round-trip ─────────┘
```

En Android, minimizar round-trips es una estrategia core de performance: cada query a la base de datos, llamada de red, o IPC (comunicación inter-proceso) agrega latencia que puede causar frame drops o spinners de carga.

## The Senior Nuance (El Matiz Senior)

- Las **actualizaciones optimistas** eliminan el round-trip percibido actualizando la UI inmediatamente con el resultado esperado, y luego confirmando con el data source en background. Si el data source no está de acuerdo, la UI hace rollback. Este patrón — usado en el `updateSelectedTasksOptimistically` de FAS — hace que la app se sienta instantánea incluso con backends lentos.
- El **batching** reduce round-trips combinando múltiples operaciones en un solo request. En vez de N inserts individuales a la base de datos, usá una sola transacción. En vez de N llamadas a la API, usá un batch endpoint. El ahorro es proporcional al número de trips evitados.
- En arquitecturas offline-first (Room + WorkManager), el "round-trip" a la base de datos local es de milisegundos, mientras que el round-trip de red puede ser de segundos o infinito (offline). Separar estos dos round-trips — lectura local rápida, sync eventual por red — es la fundación de apps Android responsivas.
- El **caching** es evitación de round-trips: si el dato ya está en memoria o en una base de datos local, el round-trip a la red se elimina por completo. El `StateFlow` de Kotlin actúa como un cache en memoria — los collectors downstream leen el valor cacheado instantáneamente, con cero round-trip.
- En Compose, la recomposición innecesaria es una especie de "round-trip interno" — la UI se re-renderiza sin que ningún dato haya cambiado realmente. Los tipos estables y `remember {}` evitan este trabajo desperdiciado.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
