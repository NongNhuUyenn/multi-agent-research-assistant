import chromadb
import hashlib
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Khởi tạo ChromaDB lưu local
client = chromadb.PersistentClient(path="./memory_db")
collection = client.get_or_create_collection(
    name="research_memory",
    metadata={"hnsw:space": "cosine"}
)

def _make_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def save_to_memory(topic: str, search_results: str, final_report: str):
    """Lưu kết quả nghiên cứu vào bộ nhớ dài hạn"""
    doc_id = _make_id(topic)

    metadata = {
        "topic": topic,
        "timestamp": datetime.now().isoformat(),
        "type": "research"
    }

    document = f"""
TOPIC: {topic}

SEARCH RESULTS:
{search_results}

FINAL REPORT:
{final_report}
"""

    collection.upsert(
        ids=[doc_id],
        documents=[document],
        metadatas=[metadata]
    )

    print(f"Memory: Đã lưu/cập nhật ký ức về '{topic}'")

def query_memory(topic: str, n_results: int = 3) -> str:
    """Tra cứu ký ức liên quan trước khi tìm kiếm mới"""
    try:
        count = collection.count()
        if count == 0:
            return ""

        results = collection.query(
            query_texts=[topic],
            n_results=min(n_results, count)
        )

        if not results["documents"][0]:
            return ""

        memory_text = "KÝ ỨC LIÊN QUAN TỪ CÁC NGHIÊN CỨU TRƯỚC:\n\n"
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            memory_text += f"[{i+1}] Chủ đề: {meta.get('topic', 'N/A')}\n"
            memory_text += f"    Thời gian: {meta.get('timestamp', 'N/A')[:10]}\n"
            # Chỉ lấy phần report ngắn gọn
            report_start = doc.find("FINAL REPORT:")
            if report_start != -1:
                short = doc[report_start+13:report_start+300]
                memory_text += f"    Tóm tắt: {short.strip()}...\n\n"

        return memory_text
    except Exception as e:
        return ""

def list_memory() -> list:
    """Liệt kê tất cả ký ức đã lưu"""
    try:
        results = collection.get()
        memories = []
        if results and results.get("metadatas"):
            for meta in results["metadatas"]:
                memories.append({
                    "topic": meta.get("topic", "N/A"),
                    "timestamp": meta.get("timestamp", "N/A")[:10]
                })
        return memories
    except Exception as e:
        print(f"Lỗi list_memory: {e}")
        return []