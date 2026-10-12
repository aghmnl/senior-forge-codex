---
layout: post
title: "Loading (UI State)"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [state-management, sealed-types, architecture]
lang: es
permalink: /es/glosario/loading-state/
---

## The Theory (El Qué)

**`Loading`** es el UI state que dice que la pantalla está esperando datos. En un [sealed state]({{ "/es/glosario/sealed-state/" | relative_url }}) suele ser un [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) sin datos, porque todavía no hay nada para mostrar; en una [flat data class]({{ "/es/glosario/flat-data-class/" | relative_url }}) se convierte en un flag `isLoading` que puede convivir con datos que ya están en pantalla.

## The Senior Nuance (El Matiz Senior)

- **Un `Loading` sealed reemplaza todo lo demás.** Pasar a él durante un refresco oculta los datos actuales y descarta lo que estaba guardado en el estado anterior, como una búsqueda.
- **Distinguir la primera carga de un refresco.** Un refresco sobre datos existentes suele ser un flag (`isRefreshing`) al lado de los datos, no un estado aparte.
- Ver [UI State Modeling: Sealed vs Flat Data Class]({{ "/es/05-architecture/ui-state-modeling/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
