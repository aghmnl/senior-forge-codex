# Senior Forge Codex: Engineering & Contribution Guide

This document serves as the authoritative reference for the architecture, navigation logic, and content creation standards of **The Senior Forge Codex**.

## 🎯 Purpose
The Codex is a professional documentation of the journey to Android Seniority. It functions as:
1. A permanent technical reference for "The Senior Forge" articles.
2. A comprehensive study guide for Senior Android Developer technical interviews.
3. A demonstration of senior-level engineering standards in documentation and infrastructure.

---

## 📂 Site Organization
The site is organized into **10 Strategic Chapters** across two parallel languages:
- **English (`/`)**: Default root.
- **Español (`/es/`)**: Fully localized mirror.

### The 10 Chapters:
1. Kotlin Core
2. Coroutines & Flow
3. Jetpack Compose
4. Android Framework & Lifecycle
5. Architecture & Design Patterns
6. Dependency Injection
7. Networking & Data
8. Testing & CI/CD
9. Performance & Security
10. Artificial Intelligence

---

## 🗺 Navigation System

### 1. Top Navigation Bar
- **Breadcrumbs**: Custom logic in `_includes/topbar.html` that maps directory slugs (e.g., `01-kotlin-core`) to their professional titles.
- **Dynamic Flag**: A high-visibility flag on the far left. It is **context-aware**—clicking it will take you to the same chapter/article in the other language instead of resetting to Home.

### 2. Sidebar
- **Chapter Highlighting**: The parent chapter is automatically highlighted when viewing any article inside it.
- **Active Article Display**: The current article title appears as a nested sub-item under its chapter with professional indentation.
- **Attribution**: The "Maintained by: aghmnl" footer is persistent and linked to the author's profile.
- **Theme Toggle**: A dark/light mode switch is centered at the bottom next to a secondary language flag.

### 3. Search Bar
- **Scope**: Configured via `assets/js/data/search.json` to index both **Pages** (the 10 chapters) and future **Posts**.
- **Usage**: Provides real-time filtering of technical topics across the entire repository.

---

## 🛠 Engineering Learnings & Bug Fixes

During the initialization of this "Forge," several critical engineering lessons were documented:

### 🔗 Relative Links & BaseURL
- **The Bug**: On GitHub Pages, project sites are hosted in subdirectories (`/senior-forge-codex/`). Hardcoded links starting with `/` fail.
- **The Fix**: Every internal link **must** be wrapped in the Liquid `relative_url` filter.
    - *Bad*: `[Link](/path/)`
    - *Good*: `[Link]({{ "/path/" | relative_url }})`

### 📑 Explicit Permalinks (Avoiding 404s)
- **The Bug**: Deployed sites often fail to resolve `.md` extensions or nested folders correctly.
- **The Fix**: Every new article **must** define an explicit `permalink` in the front matter with a trailing slash.
    - *Example*: `permalink: /en/01-kotlin-core/my-topic/`

### 🍞 Breadcrumb "Ghost" Layers
- **The Bug**: Splitting a URL with a leading slash creates an empty first segment in Liquid, resulting in an extra `>` separator in the breadcrumb.
- **The Fix**: The logic in `topbar.html` explicitly ignores empty string segments to ensure a clean `Home / Chapter / Article` path.

---

## ✍️ Content Creation Standard

To add a new item, use the following checklist:

1. **Front Matter**:
   ```yaml
   ---
   layout: page
   title: [Exact Title]
   lang: [en|es]
   permalink: /[en|es]/[chapter-path]/[slug]/
   ---
   ```
2. **Formatting**:
   - **No H1**: Do not use `# Title` in the body; the theme renders it from front matter.
   - **Code Spacing**: Exactly one blank line before and after ` ```kotlin ` blocks.
   - **Line Numbers**: Enabled automatically by the site config for all code blocks.
   - **Bullet Points**: Use the dash `-` style.
3. **Internal Navigation**: Always add a `[Back to Chapters]({{ "correct-path" | relative_url }})` link at the bottom.
4. **Localization**: Ensure you create both versions and update the respective `index.md` in the chapter folder.

---
**Maintained by: aghmnl**
