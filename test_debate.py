from dotenv import load_dotenv
load_dotenv()

from agents.debate_agent import run_debate

sample_report = """
Agentic RAG multi-agent systems kết hợp RAG với hệ thống đa tác tử.
Kiến trúc bao gồm Search Agent, Writer Agent và Critic Agent.
Hệ thống có thể tự động tìm kiếm, tổng hợp và cải thiện báo cáo.
Ứng dụng trong giáo dục, y tế và tài chính.
"""

result = run_debate(sample_report, rounds=2)

print("\n" + "=" * 60)
print("✅ DEBATE HOÀN TẤT")
print("=" * 60)
print(f"Số vòng tranh luận: {len(result['debate_history'])}")
print(f"\nVerdict cuối:\n{result['verdict']}")