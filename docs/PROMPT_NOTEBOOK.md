**Context:**
I am preparing for Senior Android Engineering technical interviews. Initialize my NotebookLM study environment for today's topic. Ensure all generated text, documents, and notes are written in Latinamerican Spanish.

**Variables:**

- TOPIC_NAME: "[Nombre del Tema, ej: Generics, Varianza y Reificación]"
- MAIN_ARTICLE_URL: "[URL exacta del artículo del día en aghmnl.github.io]"

**Execution Steps:**

1. Execute the tool to create a new NotebookLM notebook named exactly as TOPIC_NAME.
2. Browse MAIN_ARTICLE_URL to read its content.
3. Add MAIN_ARTICLE_URL as a web source to the created notebook.
4. Parse the content and extract all internal glossary links (URLs containing `/glosario/`). Add each unique glossary link as a separate web source to the notebook.
5. Identify the core Kotlin/Android framework concepts discussed in the article. Search the web for their official documentation (restricted to kotlinlang.org or developer.android.com) and add the top 2 most relevant official URLs as web sources to the notebook.
6. Extract the core architectural reasoning from the "The Senior Perspective (El Porqué)" section of the article. Use the NotebookLM tool to create a text source directly inside the notebook named "Objetivos de Estudio" containing this extracted reasoning. This text must be in Spanish.
7. Reply with the notebook URL and a bulleted list of all successfully added sources.
