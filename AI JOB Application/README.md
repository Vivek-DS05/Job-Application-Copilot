# 💼 Job Application Copilot

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-latest-green)
![LangChain](https://img.shields.io/badge/LangChain-latest-yellow)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![Model](https://img.shields.io/badge/Model-Mistral-orange)

A multi-agent AI system built with LangGraph that takes your resume 
and a job description as input, then generates a complete tailored 
application package — in one click.

---

## What It Does

| Step | Agent | Output |
|------|-------|--------|
| 1 | JD Analyzer | Extracts skills, keywords, tone |
| 2 | Resume Analyzer | Extracts your skills and strengths |
| 3 | Skill Gap Analyzer | Finds matches and missing skills |
| 4 | Resume Tailor | Rewrites resume with job keywords |
| 5 | Cover Letter Writer | Generates personalized cover letter |
| 6 | Interview Coach | Creates questions + suggested answers |
| 7 | Package Assembler | Combines everything into one doc |

---

## Agent Workflow

START
├──→ Analyze JD ──────┐
└──→ Analyze Resume ──┴──→ Skill Gap → ┌──→ Tailor Resume ──┐
└──→ Interview Prep ─┴──→ Cover Letter → Final Package → END


Steps 1-2 run in parallel.
Steps 4-5 run in parallel.
This makes the workflow ~30% faster than sequential execution.

---

## Tech Stack

- LangGraph — agent workflow orchestration
- LangChain — LLM interactions  
- Mistral AI — language model (ministral-8b)
- Streamlit — user interface
- PyPDF — resume PDF parsing
- Python 3.10+

---

## Setup

### 1. Clone the repo
git clone https://github.com/yourusername/job-application-copilot
cd job-application-copilot

### 2. Install dependencies
pip install -r requirements.txt

### 3. Add your API key
Create a .env file:
MISTRAL_API_KEY=your-key-here

Get a free Mistral API key at: https://console.mistral.ai

### 4. Run the app
streamlit run app.py

---

## Project Structure

job-application-copilot/
├── main.py            # LangGraph agents and workflow
├── app.py             # Streamlit UI
├── .env               # API keys (not committed)
├── requirements.txt
└── README.md

---

## Example Output

Given:
- A software engineer resume
- A backend developer job description

You get:
- Skill gap report showing matching and missing skills
- Resume rewritten with job-specific keywords
- Personalized 4-paragraph cover letter
- 10 interview questions with suggested answers
- Full downloadable application package

---

## Requirements

langgraph
langchain
langchain-mistralai
streamlit
pypdf
python-dotenv

---

## License
MIT