from dotenv import load_dotenv
load_dotenv()

from agents.search_agent import run_search_agent

print("=" * 60)
print("TEST Search Agent")
print("=" * 60)

result = run_search_agent(
    "Tìm các bài báo mới nhất về Agentic RAG năm 2024-2025"
)

print("\nKẾT QUẢ CUỐI:")
print(result)