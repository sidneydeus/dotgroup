import os
import faiss
import numpy as np
import json

INDEX_PATH = "storage/faiss/index.faiss"
DOCUMENTS_PATH = "storage/faiss/documents.json"


def create_index(embeddings):
    """Cria um índice FAISS IndexFlatIP (Inner Product) para busca por similaridade de cosseno.

    O IndexFlatIP com vetores normalizados equivale à similaridade de cosseno.
    É a métrica recomendada para embeddings do Cohere.

    Args:
        embeddings: Matriz numpy com shape (n_vetores, dimensão) e dtype float32.

    Returns:
        faiss.IndexFlatIP: Índice FAISS populado com os embeddings.
    """
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


def save_index(index, path):
    """Salva o índice FAISS em disco.

    Cria o diretório pai se não existir.

    Args:
        index: Índice FAISS a ser salvo.
        path: Caminho do arquivo de saída (ex: "storage/faiss/index.faiss").
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    faiss.write_index(index, path)


def load_index(path):
    """Carrega um índice FAISS do disco.

    Args:
        path: Caminho do arquivo do índice salvo.

    Returns:
        faiss.Index: Índice FAISS carregado.
    """
    return faiss.read_index(path)


def save_documents(documents, path):
    """Salva a lista de documentos em formato JSON.

    Necessário para recuperar os textos originais após a busca no FAISS,
    já que o índice armazena apenas os vetores.

    Args:
        documents: Lista de dicionários com chaves 'source' e 'text'.
        path: Caminho do arquivo JSON de saída.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)


def load_documents(path):
    """Carrega a lista de documentos salvos em JSON.

    Args:
        path: Caminho do arquivo JSON com os documentos.

    Returns:
        Lista de dicionários com chaves 'source' e 'text'.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)