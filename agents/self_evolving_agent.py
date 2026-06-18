from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import json
import os

load_dotenv()

# File lưu prompt đã tối ưu
PROMPT_STORE_FILE = "evolved_prompts.json"

META_AGENT_PROMPT = """You are a Meta-Agent that optimizes prompts for AI agents.
Your job: analyze the current agent's output quality and suggest an improved prompt.

Given:
- Current prompt used
- Output produced  
- Evaluation scores
- Weaknesses identified

Generate an IMPROVED prompt that addresses the weaknesses.
The new prompt should be specific, clear, and address the exact issues found.

Return ONLY valid JSON:
{
  "improved_prompt": "<new improved prompt text>",
  "changes_made": "<brief description of what you changed and why>",
  "expected_improvement": "<what scores should improve>"
}"""

def load_evolved_prompts() -> dict:
    """Load các prompt đã tối ưu từ file"""
    if os.path.exists(PROMPT_STORE_FILE):
        with open(PROMPT_STORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_evolved_prompt(agent_name: str, prompt: str, score: float):
    """Lưu prompt tốt nhất của mỗi agent"""
    store = load_evolved_prompts()
    if agent_name not in store or score > store[agent_name]["score"]:
        store[agent_name] = {
            "prompt": prompt,
            "score": score,
            "version": store.get(agent_name, {}).get("version", 0) + 1
        }
        with open(PROMPT_STORE_FILE, "w", encoding="utf-8") as f:
            json.dump(store, f, ensure_ascii=False, indent=2)
        print(f"🧬 Self-Evolving: Lưu prompt mới cho '{agent_name}' (score: {score:.1f})")
        return True
    return False

def get_best_prompt(agent_name: str, default_prompt: str) -> tuple:
    """Lấy prompt tốt nhất đã lưu, hoặc dùng default"""
    store = load_evolved_prompts()
    if agent_name in store:
        saved = store[agent_name]
        print(f"🧬 Self-Evolving: Dùng prompt v{saved['version']} cho '{agent_name}' (score: {saved['score']:.1f})")
        return saved["prompt"], saved["version"]
    return default_prompt, 0

def evolve_prompt(
    agent_name: str,
    current_prompt: str,
    output: str,
    scores: dict,
    weaknesses: str
) -> dict:
    """
    Meta-Agent tự tối ưu prompt dựa trên kết quả
    Inspired by TextGrad & Self-Evolving Agents (arXiv 2508.07407)
    """
    llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.4,
        api_key=os.getenv("GROQ_API_KEY")
    )

    keys = ['accuracy', 'completeness', 'coherence', 'applicability', 'citation_quality']
    avg_score = sum([scores.get(k, 0) for k in keys]) / len(keys)

    context = f"""
Agent: {agent_name}
Current prompt: {current_prompt[:500]}

Output sample: {output[:400]}

Evaluation scores: {json.dumps(scores)}
Average score: {avg_score:.1f}/10

Weaknesses: {weaknesses}
"""

    response = llm.invoke([
        SystemMessage(content=META_AGENT_PROMPT),
        HumanMessage(content=context)
    ])

    try:
        text = response.content.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            text = text[start:end]
        result = json.loads(text)
        result["avg_score"] = avg_score
        return result
    except Exception as e:
        return {
            "improved_prompt": current_prompt,
            "changes_made": "Parse error, keeping original",
            "expected_improvement": "N/A",
            "avg_score": avg_score
        }