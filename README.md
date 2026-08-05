# 🔍 Multi-Agent AI Research System

<p align="center">
  <b>An autonomous multi-agent AI pipeline that researches, writes, and refines reports — powered by LangChain & Mistral AI</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/LangChain-Framework-green" alt="LangChain">
  <img src="https://img.shields.io/badge/Mistral%20AI-LLM-orange" alt="Mistral AI">
  <img src="https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

🔗 **Live Demo:** [multiagent-ai-research-system-pranjal-pandey-2003.streamlit.app](https://multiagent-ai-research-system-pranjal-pandey-2003.streamlit.app/)

---

## 📖 Overview

**Multi-Agent AI Research System** is an autonomous research assistant that mimics how a human research team works. Instead of relying on a single LLM call, it breaks the research process into **four specialized agents**, each handling a distinct part of the workflow — from finding sources to producing a polished, fact-checked report.

Built with **LangChain** for orchestration and **Mistral AI** as the underlying LLM, the system is exposed through a clean, dark-orange themed **Streamlit** interface.

---

## ✨ Features

- 🔎 **Automated Web Search** — Finds the most relevant sources for any given topic
- 🕸️ **Content Scraping** — Extracts and cleans raw content from web sources
- ✍️ **AI Report Writing** — Synthesizes gathered data into a structured, coherent report
- 🧐 **Self-Critique Loop** — A dedicated critic agent reviews and refines the output for accuracy and quality
- 🎨 **Interactive UI** — Simple Streamlit interface with a custom dark-orange theme
- ⚡ **Fast LLM Backend** — Powered by Mistral AI's `mistral-small-2506` model

---

## 🧠 Architecture — 4-Agent Pipeline
User Query
│
▼
┌─────────────┐ ┌──────────────┐ ┌─────────────┐ ┌─────────────┐
│ Search Agent│ ──▶ │Scraper Agent │ ──▶ │ Writer Agent│ ──▶ │ Critic Agent│
└─────────────┘ └──────────────┘ └─────────────┘ └─────────────┘
Finds sources Extracts content Drafts report Refines & polishes
│
▼
Final Report Output
| Agent | Responsibility |
|-------|----------------|
| **Search Agent** | Queries the web and identifies the most relevant sources for the topic |
| **Scraper Agent** | Extracts and cleans raw text content from the identified sources |
| **Writer Agent** | Synthesizes the scraped information into a structured, readable report |
| **Critic Agent** | Reviews the draft for accuracy, clarity, and completeness, then refines it |

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| Language | Python 3.11 |
| Orchestration | LangChain |
| LLM | Mistral AI (`mistral-small-2506`) |
| UI | Streamlit (custom dark-orange theme) |
| Environment Manager | `uv` |

---

## 📂 Project Structure
Multi-Agent-AI-System/
├── agents.py # Definitions for all 4 agents (search, scraper, writer, critic)
├── pipeline.py # Orchestrates the end-to-end multi-agent workflow
├── tools.py # Custom tools used by the agents (search, scraping utilities)
├── app.py # Streamlit UI entry point
├── requirements.txt # Python dependencies
└── .gitignore
---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) package manager
- A Mistral AI API key

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/venom312004/Multi-Agent-AI-System.git
cd Multi-Agent-AI-System

# 2. Create a virtual environment
uv venv --python 3.11

# 3. Activate the environment
.venv\Scripts\Activate.ps1      # Windows
source .venv/bin/activate       # macOS/Linux

# 4. Install dependencies
uv pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

### Run the App

```bash
streamlit run app.py
```

The app will launch in your browser. Enter a research topic, and the pipeline will automatically search, scrape, write, and critique a full report for you.

---

## 📸 How It Works

1. Enter a research topic in the Streamlit UI
2. The **Search Agent** finds relevant web sources
3. The **Scraper Agent** extracts clean content from those sources
4. The **Writer Agent** drafts a structured report
5. The **Critic Agent** reviews and refines the final output
6. The polished report is displayed in the UI

---

## 🗺️ Roadmap

- [ ] Add support for multiple LLM providers
- [ ] Export reports as PDF/DOCX
- [ ] Add citation tracking for sources
- [ ] Parallelize agent execution for faster runs

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/venom312004/Multi-Agent-AI-System/issues).

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Pranjal Pandey**
GitHub: [@venom312004](https://github.com/venom312004)

---

<p align="center">Made with ❤️ using LangChain & Mistral AI</p>
