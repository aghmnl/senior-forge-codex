---
layout: post
title: "Parcelable"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [android-framework, serialization]
lang: es
permalink: /es/glosario/parcelable/
---

## The Theory (El Qué)

**`Parcelable`** es la interfaz de Android para aplanar un objeto en un `Parcel`, el formato que se usa para mandar datos por Binder entre componentes y procesos. Es la forma en que los objetos propios entran en un [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}), un Intent o el [saved instance state]({{ "/es/glosario/saved-instance-state/" | relative_url }}). Escribirla a mano es verboso; [`@Parcelize`]({{ "/es/glosario/parcelize/" | relative_url }}) la genera.

## The Senior Nuance (El Matiz Senior)

- **Más rápido que [`Serializable`]({{ "/es/glosario/serializable/" | relative_url }})** en Android, porque escribe los campos de forma explícita en lugar de usar reflexión.
- **Ser parcelable no hace chico a un objeto.** Igual cuenta contra el límite de tamaño de la transacción.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
