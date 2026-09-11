# The Senior Forge Codex: Multi-Agent AI Study Workflow

This document outlines the synchronized workflow between Claude and Gemini/NotebookLM for processing, studying, and evaluating the 100 technical topics for Senior Android Engineering interviews. It complements the `DAILY_WORKFLOW.md` by defining the exact responsibilities of each AI agent and the prompts required for the deep-study phase.

## Agent Responsibilities

- **Claude:**
  - **Content Creation:** Generates the daily technical articles, glossary entries, and maintains the GitHub repository.
  - **Evaluation:** Conducts the final theoretical and practical technical interview simulations based on the generated content.
- **Gemini (Chat):**
  - **Environment Setup:** Orchestrates the creation of the NotebookLM environment, dynamically scrapes glossary links, and fetches official documentation (Kotlin/Android).
- **Gemini Notebook (NotebookLM):**
  - **Deep Study:** Utilizes native tools (Audio Overview, Mind Map, Flashcards, Quiz) to fixate terminology and architectural reasoning without consuming conversational context.

## Phase 1: Content Generation (Claude)

As defined in `DAILY_WORKFLOW.md`, Claude is responsible for drafting the daily article and publishing it to the GitHub pages repository (`aghmnl.github.io/senior-forge-codex/es/`). Once the article is live, proceed to Phase 2.

## Phase 2: NotebookLM Initialization (Gemini Chat)

This phase automates the collection of sources (main article, glossary links, and official documentation) and creates the study workspace. Execute this step in the main Gemini chat.

### Initialization Prompt

Copy and execute the following block in Gemini, replacing the `TOPIC_NAME` and `MAIN_ARTICLE_URL` variables.

```text
**Context:**
I am preparing for Senior Android Engineering technical interviews. Initialize my NotebookLM study environment for today's topic. Ensure all generated text, documents, and notes are written strictly in Latinamerican Spanish.

**Variables:**
* TOPIC_NAME: "[Topic Name]"
* MAIN_ARTICLE_URL: "[Exact URL of the daily article on aghmnl.github.io]"

**Execution Steps:**
1. Execute the tool to create a new NotebookLM notebook named exactly as TOPIC_NAME.
2. Browse MAIN_ARTICLE_URL to read its content.
3. Add MAIN_ARTICLE_URL as a web source to the created notebook.
4. Parse the content and extract all internal glossary links (URLs containing `/glosario/`). Add each unique glossary link as a separate web source to the notebook.
5. Identify the distinct core Kotlin or Android framework concepts discussed in the article. For each identified core concept, search the web and add exactly one most relevant official documentation URL (restricted to kotlinlang.org or developer.android.com) as a web source to the notebook.
6. Extract the core architectural reasoning from the "The Senior Perspective (El Porqué)" section of the article. Use the NotebookLM tool to create a text source directly inside the notebook named "Objetivos de Estudio" containing this extracted reasoning translated to Latinamerican Spanish.
7. Reply with the notebook URL and a bulleted list of all successfully added sources.
```

## Phase 3: Deep Study Tools (NotebookLM UI)

Once Gemini provides the notebook link, navigate to the NotebookLM web interface to use the native study tools in the following sequential order. These tools do not consume interactive chat tokens.

1. **Audio Overview:** Listen to the generated debate based on the sources to internalize high-level concepts and architectural reasoning.
2. **Mind Map:** Generate the visualization to understand the hierarchical relationship between framework concepts and glossary definitions.
3. **Flashcards:** Use this native tool for the fixation phase (memorization of key terminology and syntax).
4. **Quiz:** Complete the quick multiple-choice evaluation provided by the interface to validate reading comprehension before the strict interview.

## Phase 4: Senior Interview Evaluation (Claude)

After completing the deep study in NotebookLM, return to Claude for the technical evaluation. Claude holds the context of the generated article and acts as the strict Senior Android Interviewer.

### Evaluation Prompt

Copy and execute the following block in Claude's interface.

```text
**Context:**
Act as a strict Senior Android Engineering interviewer and technical mentor. I have completed my deep study session on TOPIC_NAME. We will now conduct the evaluation session in Latinamerican Spanish based strictly on the article you generated.

**Execution Steps:**
1. **Theoretical Evaluation:** Ask me exactly one advanced theoretical question about what is discussed in the article's "The Senior Perspective" section. Wait for my answer, evaluate it strictly, and provide technical feedback.
2. **Practical Evaluation:** After the theoretical feedback, present a real-world Android/Kotlin code scenario related to the topic with a design flaw or compile error. Ask me how to fix it based on the studied concepts. Evaluate my response.

```
