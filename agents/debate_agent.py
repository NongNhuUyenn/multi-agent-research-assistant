from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

DEBATE_AGENT_1_PROMPT = """You are Debater A — an AI researcher who focuses on TECHNICAL ACCURACY.
You will debate with another AI about the quality of a research report.
Be critical, specific, and constructive. Point out technical flaws and missing details.
Respond in Vietnamese. Keep response under 200 words."""

DEBATE_AGENT_2_PROMPT = """You are Debater B — an AI researcher who focuses on PRACTICAL VALUE.
You will debate with another AI about the quality of a research report.
Be critical, specific, and constructive. Point out missing real-world applications and impact.
Respond in Vietnamese. Keep response under 200 words."""

JUDGE_PROMPT = """You are the Judge in a multi-agent debate about a research report.
You have seen arguments from two debaters. Synthesize their views into:
1. Top 3 most important improvements needed
2. Final verdict on report quality
Respond in Vietnamese. Be concise and actionable."""

def run_debate(report: str, rounds: int = 2) -> dict:
    """
    Chạy tranh luận giữa 2 agent về chất lượng báo cáo
    Dựa trên bài báo ChatEval (arXiv 2308.07201)
    """
    llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.3,
        api_key=os.getenv("GROQ_API_KEY")
    )

    debate_history = []
    debater_a_position = ""
    debater_b_position = ""

    print("\n🎭 BẮT ĐẦU MULTI-AGENT DEBATE")
    print("=" * 50)

    for round_num in range(1, rounds + 1):
        print(f"\n📢 DEBATE ROUND {round_num}/{rounds}")

        # Debater A phát biểu
        if round_num == 1:
            prompt_a = f"Đánh giá báo cáo nghiên cứu này từ góc độ kỹ thuật:\n\n{report[:1500]}"
        else:
            prompt_a = f"""Báo cáo:\n{report[:800]}
            
Debater B vừa nói: {debater_b_position}

Hãy phản bác hoặc bổ sung ý kiến của Debater B từ góc độ kỹ thuật."""

        response_a = llm.invoke([
            SystemMessage(content=DEBATE_AGENT_1_PROMPT),
            HumanMessage(content=prompt_a)
        ])
        debater_a_position = response_a.content
        print(f"\n🔵 Debater A (Kỹ thuật):\n{debater_a_position}")

        # Debater B phản bác
        if round_num == 1:
            prompt_b = f"""Báo cáo:\n{report[:800]}

Debater A vừa nói: {debater_a_position}

Hãy phản bác hoặc bổ sung từ góc độ thực tiễn."""
        else:
            prompt_b = f"""Báo cáo:\n{report[:800]}

Debater A vừa nói: {debater_a_position}

Hãy phản bác hoặc đồng ý và bổ sung từ góc độ thực tiễn."""

        response_b = llm.invoke([
            SystemMessage(content=DEBATE_AGENT_2_PROMPT),
            HumanMessage(content=prompt_b)
        ])
        debater_b_position = response_b.content
        print(f"\n🔴 Debater B (Thực tiễn):\n{debater_b_position}")

        debate_history.append({
            "round": round_num,
            "debater_a": debater_a_position,
            "debater_b": debater_b_position
        })

    # Judge tổng hợp
    print(f"\n⚖️ JUDGE tổng hợp kết quả tranh luận...")
    debate_summary = ""
    for h in debate_history:
        debate_summary += f"\nRound {h['round']}:\nA: {h['debater_a']}\nB: {h['debater_b']}\n"

    judge_response = llm.invoke([
        SystemMessage(content=JUDGE_PROMPT),
        HumanMessage(content=f"Báo cáo gốc:\n{report[:500]}\n\nLịch sử tranh luận:\n{debate_summary}")
    ])

    verdict = judge_response.content
    print(f"\n⚖️ VERDICT CỦA JUDGE:\n{verdict}")

    return {
        "debate_history": debate_history,
        "verdict": verdict
    }