from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

CRITIC_SYSTEM_PROMPT_1 = """You are a strict academic accuracy critic. 
Evaluate the research report below on ACCURACY and COMPLETENESS.
Give a score from 1-10 and specific feedback on what is missing or incorrect.
Respond in Vietnamese. Format:
ĐIỂM: X/10
NHẬN XÉT: ...
CẦN CẢI THIỆN: ..."""

CRITIC_SYSTEM_PROMPT_2 = """You are a practical application critic.
Evaluate the research report below on PRACTICAL VALUE and REAL-WORLD APPLICABILITY.
Give a score from 1-10 and specific feedback.
Respond in Vietnamese. Format:
ĐIỂM: X/10
NHẬN XÉT: ...
CẦN CẢI THIỆN: ..."""

def run_critic_agent(report: str, critic_type: int = 1) -> str:
    llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    system_prompt = CRITIC_SYSTEM_PROMPT_1 if critic_type == 1 else CRITIC_SYSTEM_PROMPT_2

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Báo cáo cần đánh giá:\n\n{report}")
    ]

    response = llm.invoke(messages)
    return response.content