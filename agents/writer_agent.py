from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

WRITER_SYSTEM_PROMPT = """You are an expert academic writer and research synthesizer.
Your job is to take search results about a topic and write a clear, well-structured research summary in Vietnamese.

Your summary should include:
1. Tổng quan về chủ đề (Overview)
2. Các phương pháp/kiến trúc chính (Key methods/architectures)
3. Kết quả nổi bật (Notable results)
4. Xu hướng và hướng nghiên cứu tương lai (Trends and future directions)

Write in Vietnamese, be concise but comprehensive."""

def run_writer_agent(topic: str, search_results: str) -> str:
    llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.3,
        api_key=os.getenv("GROQ_API_KEY")
    )

    messages = [
        SystemMessage(content=WRITER_SYSTEM_PROMPT),
        HumanMessage(content=f"""
Chủ đề: {topic}

Kết quả tìm kiếm:
{search_results}

Hãy viết một bản tổng hợp nghiên cứu chi tiết dựa trên thông tin trên.
""")
    ]

    response = llm.invoke(messages)
    return response.content




def run_writer_agent_refine(topic: str, original_report: str, critic_feedback: str) -> str:
    llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.3,
        api_key=os.getenv("GROQ_API_KEY")
    )

    messages = [
        SystemMessage(content=WRITER_SYSTEM_PROMPT),
        HumanMessage(content=f"""
Chủ đề: {topic}

Báo cáo gốc:
{original_report}

Phản hồi từ các Critic Agent:
{critic_feedback}

Hãy viết lại báo cáo, khắc phục các điểm yếu được chỉ ra trong phản hồi.
""")
    ]

    response = llm.invoke(messages)
    return response.content




from agents.self_evolving_agent import (
    get_best_prompt, evolve_prompt, save_evolved_prompt
)

def run_writer_agent_evolved(topic: str, search_results: str, scores: dict = None, weaknesses: str = "") -> str:
    """Writer Agent với Self-Evolving prompt"""
    from langchain_groq import ChatGroq
    from langchain_core.messages import HumanMessage, SystemMessage
    import os

    # Lấy prompt tốt nhất đã lưu
    best_prompt, version = get_best_prompt("writer_agent", WRITER_SYSTEM_PROMPT)

    llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.3,
        api_key=os.getenv("GROQ_API_KEY")
    )

    messages = [
        SystemMessage(content=best_prompt),
        HumanMessage(content=f"""
Chủ đề: {topic}

Kết quả tìm kiếm:
{search_results}

Hãy viết một bản tổng hợp nghiên cứu chi tiết dựa trên thông tin trên.
""")
    ]

    response = llm.invoke(messages)
    return response.content