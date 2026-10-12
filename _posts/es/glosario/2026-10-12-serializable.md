---
layout: post
title: "Serializable"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [jvm, serialization]
lang: es
permalink: /es/glosario/serializable/
---

## The Theory (El Qué)

**`java.io.Serializable`** es la interfaz marcadora de Java que permite convertir un objeto en bytes con la serialización de Java. Un [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}) acepta valores `Serializable`, así que es una alternativa a [`Parcelable`]({{ "/es/glosario/parcelable/" | relative_url }}) para pasar objetos.

## The Senior Nuance (El Matiz Senior)

- **Más lento y pesado que [`Parcelable`]({{ "/es/glosario/parcelable/" | relative_url }})** en Android, porque usa reflexión y escribe metadatos de la clase. Mejor [`@Parcelize`]({{ "/es/glosario/parcelize/" | relative_url }}).
- **No confundir con el `@Serializable` de kotlinx.serialization**, que genera serializadores para formatos como JSON y no tiene nada que ver con el [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
