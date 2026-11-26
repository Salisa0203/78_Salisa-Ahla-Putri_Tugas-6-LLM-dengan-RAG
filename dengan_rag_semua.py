import time
from dotenv import load_dotenv
from agno.agent import Agent
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.models.groq import Groq

load_dotenv()

knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="layanan",
        uri="token/lancedb",
        search_type=SearchType.vector,
        embedder=SentenceTransformerEmbedder(),
    )
)

# Agent tanpa pencarian otomatis; konteks kita sisipkan sendiri
agent = Agent(
    model=Groq(id="qwen/qwen3.8-27b", max_tokens=600),
    markdown=True,
)

with open("pertanyaan.txt", encoding="utf-8") as f:
    daftar = [baris.strip() for baris in f if baris.strip()]

def ambil_konteks(tanya, k=3, maks_char=1500):
    hasil = knowledge.search(query=tanya, max_results=k)
    potongan = [(d.content or "")[:maks_char] for d in hasil]
    return "\n\n---\n\n".join(potongan)

gagal = 0
with open("hasil_dengan_rag.md", "w", encoding="utf-8") as out:
    for i, tanya in enumerate(daftar, 1):
        print(f"[{i}/{len(daftar)}] {tanya[:60]}...")
        konteks = ambil_konteks(tanya)
        prompt = (
            "Jawab pertanyaan berdasarkan KONTEKS berikut. "
            "Jika konteks tidak cukup, katakan bagian mana yang tidak ada.\n\n"
            f"KONTEKS:\n{konteks}\n\nPERTANYAAN: {tanya}"
        )
        jawab = None
        for percobaan in range(1, 4):
            try:
                jawab = agent.run(prompt).content
                if jawab:
                    break
            except Exception as e:
                print(f"   gagal (percobaan {percobaan}/3): {str(e)[:120]}")
                time.sleep(60)
        if not jawab:
            jawab = "ERROR: gagal setelah 3 percobaan"
            gagal += 1
        out.write(f"## {tanya}\n\n**Konteks yang diambil:**\n\n{konteks}\n\n**Jawaban:**\n\n{jawab}\n\n---\n\n")
        out.flush()
        time.sleep(25)

print(f"Selesai! Gagal: {gagal} dari {len(daftar)}. Lihat hasil_dengan_rag.md")