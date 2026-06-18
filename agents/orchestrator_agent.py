from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import json
import os

load_dotenv()

ORCHESTRATOR_PROMPT = """You are the Orchestrator of a multi-agent research system.
Your job is to analyze the current report quality and decide what to do next.

Given the current scores and report, decide:
1. Should we do more Reflexion rounds? (if avg score < 8.0)
2. Should we trigger Debate? (if citation_quality < 7 or applicability < 7)
3. Is the report ready to finalize? (if avg score >= 8.5)

Return ONLY valid JSON:
{
  "action": "reflexion" | "debate" | "finalize",
  "reason": "<brief reason in Vietnamese>",
  "priority": "high" | "medium" | "low"
}"""

def orchestrate(report: str, current_scores: dict, round_num: int) -> dict:
    """
    Orchestrator tự quyết định bước tiếp theo
    Dựa trên bài báo MetaGPT (ICLR 2024)
    """
    llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    keys = ['accuracy', 'completeness', 'coherence', 'applicability', 'citation_quality']
    avg = sum([current_scores.get(k, 0) for k in keys]) / len(keys)

    context = f"""
Current round: {round_num}
Average score: {avg:.1f}/10
Scores: {json.dumps(current_scores, indent=2)}
Report preview: {report[:300]}...
"""

    response = llm.invoke([
        SystemMessage(content=ORCHESTRATOR_PROMPT),
        HumanMessage(content=context)
    ])

    try:
        text = response.content.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            text = text[start:end]
        decision = json.loads(text)
    except:
        # Fallback logic nếu parse lỗi
        if avg >= 8.5:
            decision = {"action": "finalize", "reason": "Điểm đủ cao", "priority": "low"}
        elif current_scores.get('citation_quality', 0) < 7:
            decision = {"action": "debate", "reason": "Citation quality thấp", "priority": "high"}
        else:
            decision = {"action": "reflexion", "reason": "Cần cải thiện thêm", "priority": "medium"}

    return decision