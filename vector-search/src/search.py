from src.embeddings import load_model, generate_query_embedding
from src.vector_store import load_index, load_documents, INDEX_PATH, DOCUMENTS_PATH
import argparse
import sys


def search(query, index, documents, client, top_k=3):
    """Realiza busca semântica no índice FAISS.

    Transforma a query em embedding (input_type=search_query), busca os vetores
    mais similares no índice e retorna os documentos correspondentes com scores.

    Args:
        query: Texto da consulta do usuário.
        index: Índice FAISS carregado (IndexFlatIP).
        documents: Lista de documentos originais (mesma ordem do índice).
        client: Cliente Cohere configurado.
        top_k: Número de resultados a retornar. Padrão: 3. Limitado ao total de vetores no índice.

    Returns:
        Dicionário com:
        - "query": Texto da consulta original
        - "results": Lista de dicts com "source", "text", "score" (maior = mais similar)
    """
    top_k = min(top_k, index.ntotal)

    query_embedding = generate_query_embedding(query, client)

    scores, indices = index.search(query_embedding, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        doc = documents[idx]
        results.append({
            "source": doc["source"],
            "text": doc["text"],
            "score": float(score)
        })

    return {
        "query": query,
        "results": results
    }


def print_results(result):
    """Imprime resultados da busca formatados no console.

    Args:
        result: Dicionário retornado pela função search().
    """
    print(f"\nQuery: {result['query']}")
    print("-" * 60)
    for i, r in enumerate(result["results"], 1):
        print(f"{i}. {r['source']}")
        print(f"   Score: {r['score']:.4f}")
        print(f"   Texto: {r['text'][:200]}...")
        print()


def parse_args():
    parser = argparse.ArgumentParser(description="Busca semântica com FAISS + Cohere")
    parser.add_argument("query", nargs="*", help="Termo de busca (se omitido, roda testes padrão)")
    parser.add_argument("-k", "--top-k", type=int, default=3, help="Número de resultados (padrão: 3)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    print("Carregando índice FAISS...")
    index = load_index(INDEX_PATH)
    print(f"Vetores no índice: {index.ntotal}")

    print("Carregando documentos...")
    documents = load_documents(DOCUMENTS_PATH)
    print(f"Documentos carregados: {len(documents)}")

    print("Carregando modelo Cohere...")
    client = load_model()

    if args.query:
        # Busca com termo fornecido pelo usuário
        query = " ".join(args.query)
        result = search(query, index, documents, client, top_k=args.top_k)
        print_results(result)
    else:
        # Testes padrão
        test_queries = [
            "Como executar aplicações em ambientes isolados?",
            "Qual linguagem é bastante utilizada em inteligência artificial?",
            "Como trabalhar com dados armazenados em tabelas?"
        ]

        print("\n" + "=" * 60)
        print("TESTE DE BUSCA SEMÂNTICA")
        print("=" * 60)

        for query in test_queries:
            result = search(query, index, documents, client, top_k=args.top_k)
            print_results(result)