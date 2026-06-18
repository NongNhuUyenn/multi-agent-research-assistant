import arxiv
from langchain.tools import tool

@tool
def search_arxiv(query: str) -> str:
    """
    Tìm kiếm các bài báo khoa học trên ArXiv.
    Input: câu truy vấn tìm kiếm (tiếng Anh)
    Output: danh sách bài báo với tiêu đề, tác giả, tóm tắt
    """
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for paper in client.results(search):
            results.append({
                "title": paper.title,
                "authors": [a.name for a in paper.authors[:3]],
                "summary": paper.summary[:500],
                "url": paper.entry_id,
                "published": str(paper.published.date())
            })
        
        if not results:
            return "Không tìm thấy bài báo nào phù hợp."
        
        output = f"Tìm thấy {len(results)} bài báo:\n\n"
        for i, paper in enumerate(results, 1):
            output += f"[{i}] {paper['title']}\n"
            output += f"    Tác giả: {', '.join(paper['authors'])}\n"
            output += f"    Ngày đăng: {paper['published']}\n"
            output += f"    Tóm tắt: {paper['summary'][:300]}...\n"
            output += f"    Link: {paper['url']}\n\n"
        
        return output
    
    except Exception as e:
        return f"Lỗi khi tìm kiếm ArXiv: {str(e)}"