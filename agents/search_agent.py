from dotenv import load_dotenv
load_dotenv()

from tools.arxiv_tool import search_arxiv
from tools.web_search_tool import search_web


def run_search_agent(query: str) -> str:
    """
    Tool-Using Search Agent.
    Gọi trực tiếp ArXiv và Web Search để đảm bảo demo ổn định.
    """

    arxiv_result = search_arxiv.invoke(query)
    web_result = search_web.invoke(query)

    return f"""
==============================
ARXIV SEARCH RESULTS
==============================
{arxiv_result}

==============================
WEB SEARCH RESULTS
==============================
{web_result}
"""