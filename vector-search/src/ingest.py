from src.load_documents import load_documents
from src.embeddings import load_model, generate_embeddings
from src.vector_store import create_index, save_index, save_documents, INDEX_PATH, DOCUMENTS_PATH


def ingest():
    """Executa o pipeline completo de ingestão de documentos.

    Fluxo:
    1. Carrega documentos .txt do diretório data/documents
    2. Inicializa cliente Cohere
    3. Gera embeddings para todos os documentos (input_type=search_document)
    4. Cria índice FAISS IndexFlatIP (similaridade de cosseno)
    5. Persiste índice em storage/faiss/index.faiss
    6. Persiste documentos em storage/faiss/documents.json

    O índice e documentos salvos são usados posteriormente pelo pipeline de busca (search.py).
    """
    print("Carregando documentos...")
    documents = load_documents()
    print(f"Documentos carregados: {len(documents)}")

    print("Carregando modelo Cohere...")
    client = load_model()

    print("Gerando embeddings...")
    embeddings = generate_embeddings(documents, client)
    print(f"Embeddings gerados: {embeddings.shape}")

    print("Criando índice FAISS (IndexFlatIP)...")
    index = create_index(embeddings)
    print(f"Vetores no índice: {index.ntotal}")

    print(f"Salvando índice em {INDEX_PATH}...")
    save_index(index, INDEX_PATH)

    print(f"Salvando documentos em {DOCUMENTS_PATH}...")
    save_documents(documents, DOCUMENTS_PATH)

    print("Ingestão concluída!")


if __name__ == "__main__":
    ingest()