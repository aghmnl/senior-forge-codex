---
layout: post
title: "Configuration Change"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [android-framework, lifecycle]
lang: en
permalink: /en/glossary/configuration-change/
---

## The Theory (The What)

A **configuration change** happens when something the app's resources depend on changes while it is running: screen rotation, dark mode, the system language, font size, window size (multi-window, foldables). By default Android **destroys and recreates** the [Activity]({{ "/en/glossary/activity/" | relative_url }}) so it reloads the right resources. ViewModels and the [saved instance state]({{ "/en/glossary/saved-instance-state/" | relative_url }}) survive it; plain [`remember`]({{ "/en/glossary/remember/" | relative_url }}) values do not.

## The Senior Nuance

- **Do not disable it to avoid the problem.** Declaring `android:configChanges` in the manifest stops the recreation, but then the app must handle every change itself; the reliable fix is state that survives recreation.
- **Rotation is the easy way to test it**, but [process death]({{ "/en/glossary/process-death/" | relative_url }}) is a harder case that rotation does not cover.
- See [remember & rememberSaveable]({{ "/en/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
