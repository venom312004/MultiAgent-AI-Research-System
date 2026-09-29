from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os

from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Title, URLs, and snippets"""
    results = tavily.search(query=query, max_results=3)  # CHANGED: 5 -> 3
    output = []
    for r in results["results"]:
        output.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:250]}\n"  # CHANGED: 300 -> 250
        )
    return "\n---\n".join(output)


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()  # ADDED: 403/404 pages ka kachra na aaye
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):  # CHANGED: zyada noise hataya
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:2000]  # CHANGED: 3000 -> 2000
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"