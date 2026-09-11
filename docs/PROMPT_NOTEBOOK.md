# The Senior Forge Codex: Gemini Notebook Study Workflow

Este documento define el flujo de trabajo estandarizado para consumir y evaluar los 100 temas técnicos de preparación para entrevistas. El proceso se divide en tres fases consecutivas para optimizar el contexto del modelo, gestionar las fuentes dinámicamente y administrar correctamente la cuota de uso.

## Fase 1: Setup e Inicialización (Gemini Chat)

Esta fase automatiza la recolección de fuentes (artículo principal, glosario y documentación oficial) y crea el entorno de trabajo. Se ejecuta directamente en el chat principal de Gemini.

### Prompt de Inicialización

Copiar y ejecutar el siguiente bloque en Gemini reemplazando los valores de las variables `TOPIC_NAME` y `MAIN_ARTICLE_URL`.

```text
**Context:**
I am preparing for Senior Android Engineering technical interviews. Initialize my NotebookLM study environment for today's topic. Ensure all generated text, documents, and notes are written strictly in Latinamerican Spanish.

**Variables:**
* TOPIC_NAME: "[Nombre del Tema]"
* MAIN_ARTICLE_URL: "[URL exacta del artículo del día en aghmnl.github.io]"

**Execution Steps:**
1. Execute the tool to create a new NotebookLM notebook named exactly as TOPIC_NAME.
2. Browse MAIN_ARTICLE_URL to read its content.
3. Add MAIN_ARTICLE_URL as a web source to the created notebook.
4. Parse the content and extract all internal glossary links (URLs containing `/glosario/`). Add each unique glossary link as a separate web source to the notebook.
5. Identify the distinct core Kotlin or Android framework concepts discussed in the article. For each identified core concept, search the web and add exactly one most relevant official documentation URL (restricted to kotlinlang.org or developer.android.com) as a web source to the notebook.
6. Extract the core architectural reasoning from the "The Senior Perspective (El Porqué)" section of the article. Use the NotebookLM tool to create a text source directly inside the notebook named "Objetivos de Estudio" containing this extracted reasoning translated to Latinamerican Spanish.
7. Reply with the notebook URL and a bulleted list of all successfully added sources.

```

## Fase 2: Herramientas Nativas de Aprendizaje (Interfaz de NotebookLM)

Una vez que Gemini devuelve el enlace del cuaderno creado, se debe ingresar a la interfaz web de NotebookLM para utilizar las herramientas nativas. Estas herramientas no consumen cuota de tokens del chat interactivo.

- **Audio Overview:** Generar el podcast a dos voces para escuchar un debate sobre las decisiones de diseño arquitectónico del tema.
- **Notebook Guide:** Utilizar el panel de guía automática para revisar FAQs, tabla de contenidos y resúmenes ejecutivos generados a partir de las fuentes oficiales y el glosario.

## Fase 3: Evaluación Práctica (NotebookLM Chat)

Esta fase se ejecuta en el chat interno del cuaderno recién creado en NotebookLM. Utiliza las fuentes aisladas para validar el conocimiento técnico simulando el rigor de una entrevista.

### Prompt de Evaluación

Copiar y ejecutar el siguiente bloque en el chat de NotebookLM.

```text
**Context:**
Act as a strict Senior Android Engineering interviewer and technical mentor. We will conduct a study and evaluation session in Latinamerican Spanish based strictly on the provided sources.

**Execution Steps:**
1. **Fase de Fijación (Flashcards):** First, generate 5 advanced conceptual flashcards based on the "Objetivos de Estudio" and the glossary sources. Present them as Question/Answer pairs. Wait for my confirmation to proceed.
2. **Fase de Evaluación Teórica:** Ask me one advanced theoretical question about the architectural decisions discussed in the sources. Wait for my answer, evaluate it strictly, and provide technical feedback.
3. **Fase de Evaluación Práctica:** Present a real-world Android/Kotlin code scenario related to the topic with a design flaw or compile error. Ask me how to fix it based on the sources. Evaluate my response.

```
