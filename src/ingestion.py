# src/ingestion.py
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
## DEPRECADO from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import OPENAI_API_KEY, CHROMA_PERSIST

def ingest_folder(folder_name: str = "docs"):
    """
    Indexa todos los PDFs/TXTs de <proyecto_root>/docs en ChromaDB.
    """
    # Primero vamos a definicar la carpeta absoluta de docs, donde estan guardados
    base_path = Path(__file__).parent.parent.resolve()
    folder    = base_path / folder_name

    print(f"🔍 Buscando archivos en: {folder}")
    paths = sorted(folder.glob("*.pdf")) + sorted(folder.glob("*.txt"))
    if not paths:
        print(f"❌ No encontré PDFs en {folder}")
        return

    # Luego vamos a cargar y colección de documentos
    all_docs = []
    for p in paths:
        print(f"▶️ Cargando {p.name}")
        loader = PyPDFLoader(str(p)) if p.suffix.lower() == ".pdf" else TextLoader(str(p), encoding="utf8")
        all_docs.extend(loader.load())

    # Hacemos el split en chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, separators=["\n\n","\n"," "])
    #cada chunk es un documento
    chunks = splitter.split_documents(all_docs)
    print(f" Fragmentos creados: {len(chunks)}")

    # Esta parte es del Embedding + VectorStore
    embedder = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedder,
        persist_directory=CHROMA_PERSIST,
        collection_name="licitaciones"
    )
    vectordb.persist()
    print(f" Indexados {len(chunks)} fragmentos de {len(paths)} archivos.")

# Este guard hace que ingest_folder() se ejecute sólo
# cuando corro el archivo directamente, no al importarlo.
if __name__ == "__main__":
    ingest_folder()
