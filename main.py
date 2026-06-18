from dotenv import load_dotenv
load_dotenv()

from agents.search_agent import run_search_agent
from agents.writer_agent import run_writer_agent, run_writer_agent_refine
from agents.critic_agent import run_critic_agent
from agents.memory_agent import save_to_memory, query_memory, list_memory
from agents.evaluator_agent import evaluate_report
from agents.debate_agent import run_debate
from agents.orchestrator_agent import orchestrate

def print_scores(scores: dict, label: str):
    keys = ['accuracy', 'completeness', 'coherence', 'applicability', 'citation_quality']
    avg = sum([scores.get(k, 0) for k in keys]) / len(keys)
    print(f"\n [{label}] Trung bình: {avg:.1f}/10")
    for k in keys:
        print(f"   {k:<20}: {scores.get(k, 0)}/10")
    print(f"    {scores.get('summary', '')}")

def run_pipeline(topic: str, max_rounds: int = 3):
    all_scores = []
    keys = ['accuracy', 'completeness', 'coherence', 'applicability', 'citation_quality']

    # Bước 0: Memory
    print("=" * 60)
    print(f"BƯỚC 0: Kiểm tra ký ức")
    print("=" * 60)
    memory_context = query_memory(topic)
    if memory_context:
        print(memory_context)
    else:
        print("Không có ký ức liên quan. Bắt đầu mới.\n")

    # Bước 1: Search
    print("=" * 60)
    print(f"BƯỚC 1: Tìm kiếm")
    print("=" * 60)
    enriched_query = topic
    if memory_context:
        enriched_query = f"{topic}\n\nContext: {memory_context[:300]}"
    search_results = run_search_agent(enriched_query)
    print(search_results)

    # Bước 2: Write
    print("=" * 60)
    print("BƯỚC 2: Viết báo cáo")
    print("=" * 60)
    report = run_writer_agent(topic, search_results)
    print(report)

    scores = evaluate_report(report)
    print_scores(scores, "BAN ĐẦU")
    all_scores.append(("Ban đầu", scores))

    # Orchestrator Loop
    round_num = 0
    while round_num < max_rounds:
        round_num += 1

        # Orchestrator quyết định
        print("\n" + "=" * 60)
        print(f"ORCHESTRATOR quyết định (Round {round_num})")
        print("=" * 60)
        decision = orchestrate(report, scores, round_num)
        print(f"→ Action: {decision['action'].upper()}")
        print(f"→ Lý do: {decision['reason']}")
        print(f"→ Độ ưu tiên: {decision['priority']}")

        if decision['action'] == 'finalize':
            print("\nOrchestrator quyết định FINALIZE - báo cáo đủ chất lượng!")
            break

        elif decision['action'] == 'reflexion':
            print(f"\nREFLEXION ROUND {round_num}")
            critic1 = run_critic_agent(report, critic_type=1)
            print(f"Critic 1:\n{critic1}")
            critic2 = run_critic_agent(report, critic_type=2)
            print(f"Critic 2:\n{critic2}")
            report = run_writer_agent_refine(
                topic, report,
                f"CRITIC 1:\n{critic1}\n\nCRITIC 2:\n{critic2}"
            )
            print(f"Báo cáo đã cải thiện")

        elif decision['action'] == 'debate':
            print(f"\nMULTI-AGENT DEBATE")
            debate_result = run_debate(report, rounds=2)
            print(f"Verdict:\n{debate_result['verdict']}")
            report = run_writer_agent_refine(
                topic, report,
                f"JUDGE VERDICT:\n{debate_result['verdict']}"
            )
            print(f"Báo cáo đã cải thiện theo verdict")

        # Đánh giá sau mỗi action
        scores = evaluate_report(report)
        label = f"Round {round_num} ({decision['action']})"
        print_scores(scores, label)
        all_scores.append((label, scores))


    # Bảng tiến bộ
    print("\n" + "=" * 60)
    print("BẢNG TIẾN BỘ:")
    print("=" * 60)
    header = f"{'Tiêu chí':<22}" + "".join([f"{l[:10]:<12}" for l, _ in all_scores])
    print(header)
    print("-" * len(header))
    for k in keys:
        row = f"{k:<22}" + "".join([f"{s.get(k,0):<12}" for _, s in all_scores])
        print(row)
    avgs = [sum([s.get(k,0) for k in keys])/len(keys) for _, s in all_scores]
    print("-" * len(header))
    print(f"{'TRUNG BÌNH':<22}" + "".join([f"{a:<12.1f}" for a in avgs]))

    # Lưu memory
    print("\n" + "=" * 60)
    print("Lưu memory...")
    save_to_memory(topic, search_results, report)
    memories = list_memory()
    print(f"Tổng ký ức: {len(memories)}")

    



    from agents.self_evolving_agent import evolve_prompt, save_evolved_prompt, load_evolved_prompts
    from agents.writer_agent import WRITER_SYSTEM_PROMPT

    # Self-Evolving: Tối ưu prompt dựa trên kết quả
    print("\n" + "=" * 60)
    print(" SELF-EVOLVING AGENT - Tối ưu prompt")
    print("=" * 60)

    # Lấy điểm và điểm yếu từ vòng cuối
    final_scores = all_scores[-1][1]
    keys = ['accuracy', 'completeness', 'coherence', 'applicability', 'citation_quality']
    weaknesses = []
    for k in keys:
        if final_scores.get(k, 0) < 8:
            weaknesses.append(f"{k}: {final_scores.get(k, 0)}/10")
    weakness_str = ", ".join(weaknesses) if weaknesses else "Không có điểm yếu rõ ràng"

    print(f" Điểm yếu hiện tại: {weakness_str}")
    print(" Meta-Agent đang phân tích và tạo prompt mới...")

    evolution = evolve_prompt(
        agent_name="writer_agent",
        current_prompt=WRITER_SYSTEM_PROMPT,
        output=report[:500],
        scores=final_scores,
        weaknesses=weakness_str
    )

    print(f"\n Thay đổi: {evolution['changes_made']}")
    print(f" Kỳ vọng cải thiện: {evolution['expected_improvement']}")

    # Lưu prompt mới nếu tốt hơn
    avg = sum([final_scores.get(k,0) for k in keys]) / len(keys)
    saved = save_evolved_prompt("writer_agent", evolution["improved_prompt"], avg)

    # Hiển thị lịch sử tiến hóa
    store = load_evolved_prompts()
    if "writer_agent" in store:
        print(f"\n Prompt version: v{store['writer_agent']['version']}")
        print(f" Best score: {store['writer_agent']['score']:.1f}/10")



    print("\n" + "=" * 60)
    print("BÁO CÁO CUỐI CÙNG:")
    print("=" * 60)
    print(report)
    
    return report, all_scores










if __name__ == "__main__":
    topic = "Agentic RAG multi-agent systems 2024 2025"
    run_pipeline(topic)





