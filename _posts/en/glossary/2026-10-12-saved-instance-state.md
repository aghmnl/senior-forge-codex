---
layout: post
title: "Saved Instance State"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [android-framework, lifecycle, state-management]
lang: en
permalink: /en/glossary/saved-instance-state/
---

## The Theory (The What)

The **saved instance state** is the [`Bundle`]({{ "/en/glossary/bundle/" | relative_url }}) in which Android stores small pieces of UI state before an [Activity]({{ "/en/glossary/activity/" | relative_url }}) can be destroyed, so they can be restored when it is recreated. The system asks for it when the [Activity]({{ "/en/glossary/activity/" | relative_url }}) goes to the background, and hands it back after a [configuration change]({{ "/en/glossary/configuration-change/" | relative_url }}) or after [process death]({{ "/en/glossary/process-death/" | relative_url }}). `onSaveInstanceState`, [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}) and [`SavedStateHandle`]({{ "/en/glossary/saved-state-handle/" | relative_url }}) all write into it.

## The Senior Nuance

- **It survives [process death]({{ "/en/glossary/process-death/" | relative_url }}), the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) does not.** That is the main reason it still matters with modern architecture.
- **It is not cleared on rotation, but it is when the user closes the screen**: pressing back or swiping the app away discards it on purpose.
- **Small values only**: it shares a size limit enforced by the system.
- See [remember & rememberSaveable]({{ "/en/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
