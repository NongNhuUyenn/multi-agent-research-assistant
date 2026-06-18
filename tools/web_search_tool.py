from langchain_tavily import TavilySearch
from langchain.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()


@tool
def search_web(query: str) -> str:
    """
    Tìm kiếm thông tin mới nhất trên internet.
    Input: câu truy vấn tìm kiếm
    Output: danh sách kết quả tìm kiếm từ web
    """
    try:
        tavily = TavilySearch(
            max_results=5,
            api_key=os.getenv("TAVILY_API_KEY")
        )

        try:
            raw = tavily.invoke({"query": query})
        except Exception:
            raw = tavily.invoke(query)

        if isinstance(raw, dict):
            results = raw.get("results", [])
        elif isinstance(raw, list):
            results = raw
        else:
            return f"Kết quả Tavily không đúng định dạng: {type(raw)}"

        if not results:
            return "Không tìm thấy kết quả nào."

        output = "Kết quả tìm kiếm web:\n\n"

        for i, result in enumerate(results, 1):
            if not isinstance(result, dict):
                continue

            title = result.get("title", "Không có tiêu đề")
            url = result.get("url", "")
            content = result.get("content", "")

            output += f"[{i}] {title}\n"
            output += f"    URL: {url}\n"
            output += f"    Nội dung: {content[:300]}...\n\n"

        return output

    except Exception as e:
        return f"Lỗi khi tìm kiếm web: {str(e)}"