from datetime import date  # ADDED (ab use nahi, pipeline se aata hai; chaho to hata do)
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from rich import print
from dotenv import load_dotenv
load_dotenv()
import streamlit as st

for key in ("GROQ_API_KEY", "TAVILY_API_KEY"):
    if key not in os.environ and key in st.secrets:
        os.environ[key] = st.secrets[key]

# bada model: sirf writer/critic ke liye
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_retries=5,
    timeout=60,
    max_tokens=2000,
)

# chhota model: search + reader agents ke liye
small_llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_retries=5,
    timeout=60,
    max_tokens=1500,
    reasoning_effort="low",
)


def build_search_agent():
    return create_agent(model=small_llm, tools=[web_search])


def build_search_reader_agent():
    return create_agent(model=small_llm, tools=[scrape_url])


# writer chain
# CHANGED: {today} add kiya, aur "sirf research se facts lo" instruction
writer_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an expert research writer. Today's date is {today}. "
     "Write clear, structured and insightful reports. "
     "Use only facts present in the research provided; do not invent facts or dates."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional.""")
])

parser = StrOutputParser()

writer_chain = writer_prompt | llm | parser


# critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | parser