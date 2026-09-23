import os
from pathlib import Path
import numpy as np
import cohere
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

MODEL_NAME = "embed-english-v3.0"


def load_model():
    """Inicializa e retorna o cliente Cohere configurado com a API key.

    Returns:
        cohere.ClientV2: Cliente configurado para chamadas à API Cohere.

    Raises:
        ValueError: Se COHERE_API_KEY não estiver configurada nas variáveis de ambiente.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY não configurada. Crie um arquivo .env com COHERE_API_KEY=sua-chave")
    return cohere.ClientV2(api_key=api_key)


def generate_embeddings(documents, client):
    """Gera embeddings para uma lista de documentos usando o modelo Cohere.

    Usa input_type="search_document" conforme recomendação da Cohere para documentos
    que serão indexados e buscados posteriormente.

    Args:
        documents: Lista de dicionários com chave 'text' contendo o texto do documento.
        client: Instância de cohere.ClientV2 já configurada.

    Returns:
        np.ndarray: Matriz de embeddings com shape (n_documentos, dimensão) e dtype float32.
    """
    texts = [document["text"] for document in documents]
    
    response = client.embed(
        model=MODEL_NAME,
        texts=texts,
        input_type="search_document",
        embedding_types=["float"]
    )
    
    embeddings = response.embeddings.float
    return np.array(embeddings).astype("float32")


def generate_query_embedding(text, client):
    """Gera embedding para uma única query de busca.

    Usa input_type="search_query" conforme recomendação da Cohere para consultas
    que serão comparadas contra documentos indexados.

    Args:
        text: Texto da query de busca.
        client: Instância de cohere.ClientV2 já configurada.

    Returns:
        np.ndarray: Embedding da query com shape (1, dimensão) e dtype float32.
    """
    response = client.embed(
        model=MODEL_NAME,
        texts=[text],
        input_type="search_query",
        embedding_types=["float"]
    )
    return np.array(response.embeddings.float).astype("float32")


if __name__ == "__main__":
    from load_documents import load_documents

    documents = load_documents()
    client = load_model()
    embeddings = generate_embeddings(documents, client)

    print(f"Documentos: {len(documents)}")
    print(f"Embeddings: {len(embeddings)}")
    print(f"Dimensão: {embeddings.shape[1]}")
    print()

    for document, embedding in zip(documents, embeddings):
        print(f"{document['source']} -> {embedding.shape}")

    print()
    print("Primeiros 10 valores do primeiro embedding:")
    print(embeddings[0][:10])