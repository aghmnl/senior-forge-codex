---
layout: post
title: "Dispatchers.Main"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, threading, android-framework]
lang: es
permalink: /es/glosario/dispatchers-main/
---

## The Theory (El Qué)

**`Dispatchers.Main`** es el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) atado al [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) de Android. Se implementa como un `Handler` sobre el [`Looper`]({{ "/es/glosario/looper/" | relative_url }}) principal: reanudar una coroutine acá postea su [continuation]({{ "/es/glosario/continuation/" | relative_url }}) a la cola de mensajes, así que corre después de lo que el thread de UI esté haciendo en ese momento. Es el único dispatcher donde tocar Views, `LiveData.setValue` y la mayoría de las escrituras de estado de Compose son legales.

`Dispatchers.Main` lo provee `kotlinx-coroutines-android`; sin ese artefacto en el classpath lanza una excepción al primer uso.

## The Senior Nuance (El Matiz Senior)

- **Suspender en Main es gratis; bloquear en Main es el bug.** Una coroutine detenida en un [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}) libera el thread para renderizar; una [llamada bloqueante]({{ "/es/glosario/blocking-call/" | relative_url }}) no.
- **Siempre hace post, incluso si ya estás en Main.** Eso cuesta un viaje por la cola. [`Main.immediate`]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }}) se lo saltea cuando puede, y por eso los scopes de lifecycle usan este último.
- **En tests unitarios de JVM no existe** hasta que [`Dispatchers.setMain`]({{ "/es/glosario/set-main/" | relative_url }}) instala un [`TestDispatcher`]({{ "/es/glosario/test-dispatcher/" | relative_url }}).
- **Un repositorio nunca debería cambiar a Main.** Devolvé el valor; dejá que el llamador de la capa de UI — que ya está en Main — decida dónde aterriza.
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
