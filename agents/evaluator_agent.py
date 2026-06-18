from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import json
import os

load_dotenv()

EVALUATOR_PROMPT = """You are a scientific research evaluator. 
Evaluate the given research report on EXACTLY these 5 criteria.
Return ONLY a valid JSON object, no explanation, no markdown, no extra text.

{
  "accuracy": <score 1-10>,
  "completeness": <score 1-10>,
  "coherence": <score 1-10>,
  "applicability": <score 1-10>,
  "citation_quality": <score 1-10>,
  "summary": "<one sentence overall assessment in Vietnamese>"
}"""

def evaluate_report(report: str) -> dict:
    """Đánh giá báo cáo theo 5 tiêu chí tự định nghĩa cho hệ thống demo"""
    llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    messages = [
        SystemMessage(content=EVALUATOR_PROMPT),
        HumanMessage(content=f"Evaluate this report:\n\n{report}")
    ]

    response = llm.invoke(messages)

    try:
        # Làm sạch response trước khi parse
        text = response.content.strip()
        # Tìm JSON trong response
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            text = text[start:end]
        scores = json.loads(text)
        return scores
    except Exception as e:
        print(f"Parse error: {e}, raw: {response.content[:200]}")
        # Fallback scores nếu parse lỗi
        return {
            "accuracy": 7,
            "completeness": 7,
            "coherence": 7,
            "applicability": 7,
            "citation_quality": 6,
            "summary": "Đánh giá tự động gặp lỗi, dùng điểm mặc định."
        }