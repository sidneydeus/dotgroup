import os
from pathlib import Path
from typing import List, Dict


def load_documents(documents_dir: str = "data/documents") -> List[Dict[str, str]]:
    """Carrega todos os arquivos .txt do diretório de documentos.

    Args:
        documents_dir: Caminho para o diretório contendo os arquivos .txt.
                       Padrão: "data/documents"

    Returns:
        Lista de dicionários com chaves 'source' (nome do arquivo) e 'text' (conteúdo).
    """
    documents = []
    path = Path(documents_dir)

    for file_path in path.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            documents.append({
                "source": file_path.name,
                "text": f.read().strip()
            })

    return documents


if __name__ == "__main__":
    docs = load_documents()
    print(f"Documentos encontrados: {len(docs)}\n")
    for doc in docs:
        print(f"- {doc['source']}")
        print(f"  {doc['text'][:100]}...\n")