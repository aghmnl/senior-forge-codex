---
layout: post
title: "Crashlytics"
date: 2026-09-13 12:00:00 +0000
categories: [es, glosario]
tags: [error-handling, android-framework, build-tools]
lang: es
permalink: /es/glosario/crashlytics/
---

## The Theory (El Qué)

**Firebase Crashlytics** es el servicio de reporte de crashes con el que se publican la mayoría de las apps Android. El SDK instala un handler de excepciones no capturadas, captura el [stack trace]({{ "/es/glosario/stack-trace/" | relative_url }}), el estado del dispositivo y los breadcrumbs, y los sube en el próximo arranque; la consola agrupa reportes por causa raíz y sigue el porcentaje de usuarios sin crashes por versión.

```xml
<!-- From FollowApp Suite — AndroidManifest.xml -->
<!-- Crashlytics collection: false in debug, true in release. -->
<meta-data
    android:name="firebase_crashlytics_collection_enabled"
    android:value="${crashlyticsCollectionEnabled}" />
```

FAS desactiva la recolección en builds de debug mediante un placeholder de manifest, así los crashes de desarrollo nunca contaminan el dashboard de producción, y la activa solo en `release`.

## The Senior Nuance (El Matiz Senior)

- **La subida del mapping es la funcionalidad que importa.** Los builds de release están [ofuscados]({{ "/es/glosario/obfuscation/" | relative_url }}) por [R8]({{ "/es/glosario/r8/" | relative_url }}); el plugin de Gradle de Crashlytics sube `mapping.txt` al compilar para que la consola muestre nombres reales de clases y métodos. Sin eso cada crash se lee `a.b.c` y el agrupamiento se rompe.
- **[NullPointerException]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) es consistentemente la categoría número uno.** La mayoría se origina en los límites de interop Java/Kotlin — [platform types]({{ "/es/glosario/platform-types/" | relative_url }}) — o en `!!`. El reporte te dice *dónde*; solo un mensaje de excepción significativo te dice *qué* [invariante]({{ "/es/glosario/invariant/" | relative_url }}) se rompió.
- **Los reportes non-fatal son para fallos manejados que igual querés ver.** `recordException(e)` dentro de un `catch` envía el trace sin crashear. Usalo para ramas de "esto no debería pasar nunca"; no lo uses como logging.
- **Las custom keys y los logs dan el contexto que al trace le falta.** Registrar la pantalla actual, el tier del usuario o un feature flag antes del crash convierte "NPE en `TasksViewModel`" en "NPE en `TasksViewModel` en el flujo de archivado con agrupamiento activado".

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
