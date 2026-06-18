# Multi-Agent Research Assistant

A Multi-Agent AI system for academic research assistance.
The system helps users search for academic papers, collect web information, generate Vietnamese research reports, critique outputs, evaluate quality, remember previous research, and improve the workflow through reflection and self-evolution.

## 1. Project Overview

This project focuses on the foundations and applications of **Multi-Agent AI**.
Instead of using only one chatbot to answer a query, the system is designed as a group of specialized agents. Each agent has a specific role in the research pipeline.

The system can:

* Search academic papers from ArXiv
* Search recent information from the web
* Generate research summaries in Vietnamese
* Critique the generated report from different perspectives
* Evaluate report quality using an LLM-as-a-Judge rubric
* Store previous research results using long-term memory
* Use reflection to improve the report after receiving feedback
* Simulate debate between agents
* Use an orchestrator to decide the next action
* Improve prompts through a self-evolving mechanism
* Provide a Streamlit web interface for demonstration

## 2. Main Features

### Search Agent

The Search Agent collects information from academic and web sources.

It uses:

* ArXiv search tool
* Tavily web search tool

The goal of this agent is to collect useful information before the writing stage.

### Writer Agent

The Writer Agent receives search results and generates a structured Vietnamese research report.

The report usually includes:

* Topic overview
* Key concepts
* Related methods or architectures
* Main findings
* Trends and future directions

### Critic Agents

The system includes critic agents that review the generated report from different perspectives.

Examples:

* Academic accuracy critic
* Practical application critic

These agents give comments and improvement suggestions.

### Reflexion Loop

The Reflexion Loop allows the system to improve its answer after receiving feedback.

Basic workflow:

```text
Writer Agent generates report
        ↓
Critic Agents review report
        ↓
Writer Agent revises report
        ↓
Final improved report
```

This makes the output better than a one-shot generation approach.

### Evaluator Agent

The Evaluator Agent scores the report using an LLM-as-a-Judge rubric.

The evaluation criteria include:

* Accuracy
* Completeness
* Coherence
* Practical applicability
* Citation quality

This is used as a relative quality evaluation method for the demo system.

### Memory Agent

The Memory Agent stores previous research results using ChromaDB.

It allows the system to:

* Remember previous topics
* Retrieve related past research
* Reuse useful context
* Avoid starting from zero every time

### Debate Agent

The Debate Agent simulates multi-agent discussion.

Different agents can argue from different viewpoints, such as:

* Academic value
* Practical value
* Technical feasibility
* Research novelty

This helps improve the final report and makes the system more robust.

### Orchestrator Agent

The Orchestrator Agent controls the workflow.

It decides whether the system should:

* Continue improving the report
* Run critic agents
* Run debate
* Stop and output the final result

### Self-Evolving Agent

The Self-Evolving Agent analyzes weak points in previous outputs and suggests prompt improvements.

This makes the system closer to a self-improving multi-agent workflow.

## 3. Project Architecture

```text
User Query
    ↓
Memory Agent
    ↓
Search Agent
    ↓
Writer Agent
    ↓
Critic Agents
    ↓
Evaluator Agent
    ↓
Orchestrator Agent
    ↓
Debate Agent / Reflexion Loop
    ↓
Self-Evolving Agent
    ↓
Final Research Report
```

## 4. Project Structure

```text
multi-agent-research-assistant/
│
├── agents/
│   ├── search_agent.py
│   ├── writer_agent.py
│   ├── critic_agent.py
│   ├── evaluator_agent.py
│   ├── memory_agent.py
│   ├── debate_agent.py
│   ├── orchestrator_agent.py
│   ├── self_evolving_agent.py
│   └── __init__.py
│
├── tools/
│   ├── arxiv_tool.py
│   ├── web_search_tool.py
│   └── __init__.py
│
├── app.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── test_tools.py
├── test_search_agent.py
├── test_debate.py
└── README.md
```

## 5. Technologies Used

* Python
* LangChain
* LangGraph
* Groq API
* Tavily Search API
* ArXiv API
* ChromaDB
* Streamlit
* Plotly
* python-dotenv

## 6. Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/NongNhuUyenn/multi-agent-research-assistant.git
cd multi-agent-research-assistant
```

### Step 2: Create a virtual environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS or Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

## 7. Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Do not push the `.env` file to GitHub because it contains private API keys.

## 8. How to Run

### Run the terminal pipeline

```bash
python main.py
```

### Run the Streamlit web app

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## 9. Testing

Run tool tests:

```bash
python test_tools.py
```

Run Search Agent test:

```bash
python test_search_agent.py
```

Run Debate Agent test:

```bash
python test_debate.py
```

## 10. Example Use Cases

The system can be used for topics such as:

* Agentic RAG
* Multi-Agent AI
* LLM-based research assistants
* AI agents in finance
* AI agents in education
* Agent memory and reflection
* Multi-agent debate systems
* Self-improving AI workflows

Example query:

```text
Agentic RAG multi-agent systems 2024 2025
```

The system will search for related information, generate a report, evaluate it, improve it, and store the final result in memory.

## 11. Research Direction

This project is designed as a foundation for studying Multi-Agent AI.

Main concepts covered:

* Artificial Intelligence
* AI Agent
* Multi-Agent System
* Agentic RAG
* Tool-Using Agent
* Reflection
* Memory-Augmented Agent
* Multi-Agent Debate
* LLM-as-a-Judge
* Self-Evolving Agent

## 12. Motivation

Most simple AI assistants only generate an answer directly from a user prompt.
However, real research work usually requires multiple steps:

1. Searching information
2. Reading and filtering sources
3. Writing a summary
4. Checking accuracy
5. Improving weak parts
6. Remembering previous work

This project models that process as a multi-agent workflow.
Each agent handles a different responsibility, making the system more modular, explainable, and extensible.

## 13. Future Improvements

Possible future extensions include:

* Adding PDF upload and paper summarization
* Adding citation extraction
* Adding automatic reference formatting
* Adding support for more academic databases
* Adding quantitative evaluation with benchmark datasets
* Adding user feedback to improve the memory system
* Adding more domain-specific agents
* Deploying the system online

## 14. Notes

Before pushing code to GitHub, make sure the following files or folders are not committed:

```text
.env
venv/
memory_db/
__pycache__/
```

These should be ignored by `.gitignore`.

## 15. Author

Developed by Nong Nhu Uyen.

GitHub: https://github.com/NongNhuUyenn
