from dotenv import load_dotenv
load_dotenv()

from tools.arxiv_tool import search_arxiv
from tools.web_search_tool import search_web

print("=" * 50)
print("TEST 1: Tìm kiếm ArXiv")
print("=" * 50)
result = search_arxiv.invoke("agentic RAG multi-agent 2024")
print(result)

print("=" * 50)
print("TEST 2: Tìm kiếm Web")
print("=" * 50)
result = search_web.invoke("agentic AI research 2025")
print(result)