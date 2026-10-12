---
layout: post
title: "Process Death"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [android-framework, lifecycle, memory]
lang: en
permalink: /en/glossary/process-death/
---

## The Theory (The What)

**Process death** is when Android kills an app's process while it is in the background, to reclaim memory. The user does not see it: when they return, Android starts a new process and recreates the [Activity]({{ "/en/glossary/activity/" | relative_url }}) from its [saved instance state]({{ "/en/glossary/saved-instance-state/" | relative_url }}), so the app looks like it never left. Everything that lived only in memory (ViewModels, [singletons]({{ "/en/glossary/singleton/" | relative_url }}), [`remember`]({{ "/en/glossary/remember/" | relative_url }}) values) is gone; only the [saved instance state]({{ "/en/glossary/saved-instance-state/" | relative_url }}) and persistent storage survive.

## The Senior Nuance

- **Developers rarely see it, users hit it constantly** (switching to the camera, a long call). Test it with "Don't keep [activities]({{ "/en/glossary/activity/" | relative_url }})" or by killing the process with adb while the app is in the background.
- **It is the case [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}) and [`SavedStateHandle`]({{ "/en/glossary/saved-state-handle/" | relative_url }}) exist for.**
- See [remember & rememberSaveable]({{ "/en/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
