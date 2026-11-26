from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.vectordb.lancedb import LanceDb

knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="layanan",
        uri="token/lancedb",
        embedder=SentenceTransformerEmbedder()
    )
)

knowledge.insert(
    name="Literatur-Lithium",
    path="literatur_lithium.pdf",
    reader=PDFReader(),
    upsert=True,
)

print("Indexing PDF selesai!")