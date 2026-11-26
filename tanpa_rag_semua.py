import time
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq

load_dotenv()

agent = Agent(model=Groq(id="qwen/qwen3.8-27b", max_tokens=800), markdown=True)

with open("pertanyaan.txt", encoding="utf-8") as f:
    daftar = [baris.strip() for baris in f if baris.strip()]

with open("hasil_tanpa_rag.md", "w", encoding="utf-8") as out:
    for i, tanya in enumerate(daftar, 1):
        print(f"[{i}/{len(daftar)}] {tanya[:60]}...")
        try:
            jawab = agent.run(tanya).content
        except Exception as e:
            jawab = f"ERROR: {e}"
        out.write(f"## {tanya}\n\n{jawab}\n\n---\n\n")
        out.flush()
        time.sleep(5)

print("Selesai! Lihat file hasil_tanpa_rag.md")