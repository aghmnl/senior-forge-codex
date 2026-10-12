---
layout: post
title: "TransactionTooLargeException"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [android-framework, error-handling, memory]
lang: es
permalink: /es/glosario/transaction-too-large-exception/
---

## The Theory (El Qué)

**`TransactionTooLargeException`** se lanza cuando los datos que se envían por Binder superan el buffer de transacciones, que es de alrededor de **1 MB compartido por todas las transacciones en curso** del proceso. La causa habitual es un [saved instance state]({{ "/es/glosario/saved-instance-state/" | relative_url }}) o unos extras de Intent grandes: listas largas, bitmaps u objetos de dominio puestos en un [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}).

## The Senior Nuance (El Matiz Senior)

- **Muchas veces rompe cuando la app pasa a background**, porque ahí es cuando el [estado guardado]({{ "/es/glosario/saved-instance-state/" | relative_url }}) se envía al sistema, lejos del código que lo causó.
- **La solución es guardar menos**, no atraparla: ids en lugar de objetos, y datos que se recargan desde una base de datos o el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}).
- Ver [remember & rememberSaveable]({{ "/es/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
