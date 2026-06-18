import streamlit as st

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🤖",
    layout="wide"
)


st.write("Uyên EAT")

import plotly.graph_objects as go
from dotenv import load_dotenv
load_dotenv()

from agents.search_agent import run_search_agent
from agents.writer_agent import run_writer_agent, run_writer_agent_refine
from agents.critic_agent import run_critic_agent
from agents.memory_agent import save_to_memory, query_memory, list_memory
from agents.evaluator_agent import evaluate_report



def draw_radar_chart(all_scores: list):
    criteria = ['Accuracy', 'Completeness', 'Coherence', 'Applicability', 'Citation']
    keys = ['accuracy', 'completeness', 'coherence', 'applicability', 'citation_quality']
    colors = ['#636EFA', '#EF553B', '#00CC96']

    fig = go.Figure()
    for idx, (label, scores) in enumerate(all_scores):
        values = [scores.get(k, 0) for k in keys]
        values.append(values[0])  # đóng vòng
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=criteria + [criteria[0]],
            fill='toself',
            name=label,
            line_color=colors[idx % len(colors)],
            opacity=0.7
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        title="📊 Radar Chart: Tiến bộ qua các vòng Reflexion",
        height=450
    )
    return fig

def draw_progress_bar(all_scores: list):
    labels = [label for label, _ in all_scores]
    avgs = []
    keys = ['accuracy', 'completeness', 'coherence', 'applicability', 'citation_quality']
    for _, scores in all_scores:
        avg = sum([scores.get(k, 0) for k in keys]) / len(keys)
        avgs.append(avg)

    fig = go.Figure(go.Bar(
        x=labels,
        y=avgs,
        marker_color=['#636EFA', '#EF553B', '#00CC96'],
        text=[f"{a:.1f}/10" for a in avgs],
        textposition='auto'
    ))
    fig.update_layout(
        title="⭐ Điểm trung bình qua các vòng",
        yaxis=dict(range=[0, 10]),
        height=300
    )
    return fig

# ===== UI =====
st.title("🤖 Multi-Agent Research Assistant")
st.markdown("*Hệ thống nghiên cứu tự động: Search → Write → Reflect → Evaluate → Memory*")
st.divider()

with st.sidebar:
    st.header("⚙️ Cài đặt")
    reflexion_rounds = st.slider("Số vòng Reflexion", 1, 3, 2)
    st.divider()
    st.markdown("**🧠 Kiến trúc hệ thống:**")
    st.markdown(" 🔍 Search Agent (ArXiv + Web)")
    st.markdown(" ✍️ Writer Agent (Tổng hợp)")
    st.markdown(" 🎯 Critic Agent x2 (Phản hồi)")
    st.markdown(" 📊 Evaluator Agent (Chấm điểm)")
    st.markdown(" 🧠 Memory Agent (ChromaDB)")
    st.markdown(" 🧭 Orchestrator Agent (Quyết định bước tiếp theo)")
    st.markdown(" 🎭 Debate Agent (Tranh luận đa tác nhân)")
    st.markdown(" 🧬 Self-Evolving Agent (Tự tối ưu prompt)")
    st.divider()
    
    st.divider()
    memories = list_memory()
    st.markdown(f"**🗂️ Ký ức đã lưu: {len(memories)}**")
    for m in memories:
        st.markdown(f"- [{m['timestamp']}] {m['topic'][:30]}...")

topic = st.text_input(
    "🔍 Nhập chủ đề nghiên cứu:",
    placeholder="Ví dụ: Agentic RAG multi-agent systems 2025"
)

if st.button("🚀 Bắt đầu nghiên cứu", type="primary", width='stretch'):
    if not topic:
        st.warning("Vui lòng nhập chủ đề!")
    else:
        all_scores = []

        # Bước 0: Memory
        with st.expander("🧠 Bước 0: Kiểm tra ký ức", expanded=False):
            memory_context = query_memory(topic)
            if memory_context:
                st.info(memory_context)
            else:
                st.write("Không có ký ức liên quan. Bắt đầu nghiên cứu mới.")

        # Bước 1: Search
        with st.expander("🔍 Bước 1: Tìm kiếm thông tin", expanded=True):
            with st.spinner("Search Agent đang tìm kiếm..."):
                enriched_query = topic
                if memory_context:
                    enriched_query = f"{topic}\n\nContext: {memory_context[:300]}"
                search_results = run_search_agent(enriched_query)
            st.success("✅ Tìm kiếm hoàn tất!")
            st.markdown(search_results)

        # Bước 2: Write
        with st.expander("✍️ Bước 2: Báo cáo ban đầu", expanded=True):
            with st.spinner("Writer Agent đang tổng hợp..."):
                report = run_writer_agent(topic, search_results)
            st.markdown(report)

            with st.spinner("Evaluator đang chấm điểm..."):
                scores = evaluate_report(report)
            all_scores.append(("Ban đầu", scores))
            keys = ['accuracy', 'completeness', 'coherence', 'applicability', 'citation_quality']
            avg = sum([scores.get(k, 0) for k in keys]) / len(keys)
            st.metric("⭐ Điểm ban đầu", f"{avg:.1f}/10")

        # Reflexion Loops
        for i in range(reflexion_rounds):
            with st.expander(f"🔁 Reflexion Round {i+1}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    with st.spinner("🎯 Critic 1 đánh giá..."):
                        critic1 = run_critic_agent(report, critic_type=1)
                    st.markdown("**Critic 1 — Độ chính xác:**")
                    st.markdown(critic1)
                with col2:
                    with st.spinner("🎯 Critic 2 đánh giá..."):
                        critic2 = run_critic_agent(report, critic_type=2)
                    st.markdown("**Critic 2 — Tính ứng dụng:**")
                    st.markdown(critic2)

                combined = f"CRITIC 1:\n{critic1}\n\nCRITIC 2:\n{critic2}"
                with st.spinner("✍️ Writer cải thiện báo cáo..."):
                    report = run_writer_agent_refine(topic, report, combined)
                st.markdown("**📄 Báo cáo sau cải thiện:**")
                st.markdown(report)

                with st.spinner("📊 Đánh giá..."):
                    scores = evaluate_report(report)
                all_scores.append((f"Round {i+1}", scores))
                avg = sum([scores.get(k, 0) for k in keys]) / len(keys)
                st.metric(f"⭐ Điểm Round {i+1}", f"{avg:.1f}/10")

        # Charts
        st.divider()
        st.subheader("📈 Kết quả đánh giá")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(draw_radar_chart(all_scores), width='stretch')
        with col2:
            st.plotly_chart(draw_progress_bar(all_scores), width='stretch')

        # Lưu memory
        save_to_memory(topic, search_results, report)
        st.success("💾 Đã lưu vào bộ nhớ!")

        # Download
        st.download_button(
            label="📥 Tải báo cáo cuối (.txt)",
            data=report,
            file_name="research_report.txt",
            mime="text/plain",
            width='stretch'
        )