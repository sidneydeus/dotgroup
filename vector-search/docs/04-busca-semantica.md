# Vector Stores e Embeddings

## Implementação da Busca Semântica

### 1. Objetivo

Implementar a **busca semântica completa** utilizando:

- documentos em arquivos `.txt`;
- embeddings gerados pelo **Cohere**;
- **FAISS** como Vector Store;
- busca `top-k`;
- recuperação dos documentos originais.

O fluxo completo será:

```text
Consulta do usuário
        ↓
Cohere Embeddings
        ↓
Embedding da consulta
        ↓
FAISS
        ↓
Busca por similaridade
        ↓
Índices encontrados
        ↓
Documentos originais
        ↓
Resultados relevantes
```
---

# 2. O que é busca semântica?

Uma busca tradicional normalmente procura correspondências entre palavras.

Por exemplo:

```text
consulta:
"programação em Python"
```

poderia procurar literalmente as palavras:

```text
Python
programação
```

Na busca semântica, a consulta também é transformada em um vetor.

Por exemplo:

```text
"programação em Python"
        ↓
Cohere
        ↓
[0.12, -0.04, 0.31, ...]
```

O FAISS compara esse vetor com os vetores dos documentos.

Assim, documentos que utilizam palavras diferentes, mas possuem significado relacionado, podem ser encontrados.

---

# 3. Fluxo completo

A partir desta etapa teremos:

```text
                 INGESTÃO
                    │
                    ▼
             Documentos .txt
                    │
                    ▼
                Cohere
                    │
                    ▼
              Embeddings
                    │
                    ▼
                  FAISS
                    │
                    │
                    ▼
              index.faiss


                  CONSULTA
                    │
                    ▼
            Texto da consulta
                    │
                    ▼
                Cohere
                    │
                    ▼
          Embedding da consulta
                    │
                    ▼
                  FAISS
                    │
                    ▼
             Índices + scores
                    │
                    ▼
          Documentos relevantes
```

---

# 4. Importante: documento e consulta

Antes geramos embeddings para os documentos.

Agora transformação para a consulta.

Por exemplo:

```text
Documento:

"Docker permite executar aplicações
em ambientes isolados chamados containers."
```

e:

```text
Consulta:

"Como funcionam os containers?"
```

Ambos são enviados ao mesmo modelo de embeddings do Cohere.

```text
Documento
    ↓
Cohere
    ↓
Embedding documento


Consulta
    ↓
Cohere
    ↓
Embedding consulta
```

Isso permite comparar os vetores.

---

# 5. Reutilizar o código existente

Reutilizar:

```text
src/load_documents.py
src/embeddings.py
src/vector_store.py
```

Evite duplicar a lógica existente.

A nova responsabilidade será implementada em:

```text
src/search.py
```

A estrutura ficará:

```text
src/
├── __init__.py
├── load_documents.py
├── embeddings.py
├── vector_store.py
└── search.py
```

---

# 6. Função para gerar embedding da consulta

O módulo `embeddings.py` deverá permitir gerar embeddings tanto para documentos quanto para consultas.

Caso ainda tenha somente uma função para vários documentos, adicionar uma função específica:

```python
def generate_query_embedding(text, model):
    embedding = model.encode(
        [text],
        convert_to_numpy=True
    )

    return embedding.astype("float32")
```

A ideia é receber:

```text
"Como funcionam os containers?"
```

e retornar uma matriz com formato:

```text
(1, dimensão)
```

Por exemplo:

```text
(1, N)
```

---

# 7. Atenção ao modelo Cohere

A consulta deve ser transformada em embedding utilizando **o mesmo modelo e a mesma configuração de embeddings adotados na Parte 02**.

Não devemos utilizar um modelo para os documentos e outro modelo para a consulta.

O princípio é:

```text
documentos ──┐
             ├──> mesmo modelo/configuração ──> espaço vetorial
consulta ────┘
```

Isso garante que os vetores possam ser comparados corretamente.

Se a implementação do Cohere utiliza tipos específicos para:

```text
document
query
```

mantenha essa configuração de forma consistente.

---

# 8. Criar `search.py`

Criar:

```text
src/search.py
```

A primeira função será responsável por realizar a busca:

```python
def search(
    query_embedding,
    index,
    top_k=3
):
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    return distances[0], indices[0]
```

O retorno será:

```text
distâncias/scores
índices
```

Por exemplo:

```text
indices:
[2, 0, 4]

distances:
[0.41, 0.72, 0.91]
```

---

# 9. Recuperar os documentos

O FAISS retorna somente os índices.

Por exemplo:

```text
[2, 0, 4]
```

Precisamos transformar isso em documentos:

```python
def get_documents(
    documents,
    indices,
    distances
):
    results = []

    for index, distance in zip(
        indices,
        distances
    ):
        document = documents[index]

        results.append({
            "source": document["source"],
            "text": document["text"],
            "score": float(distance)
        })

    return results
```

Assim teremos:

```python
[
    {
        "source": "docker.txt",
        "text": "Docker permite...",
        "score": 0.41
    },
    {
        "source": "python.txt",
        "text": "Python é...",
        "score": 0.72
    }
]
```

---

# 10. Implementar a busca completa

Podemos criar uma função que encapsula todo o processo:

```python
def semantic_search(
    query,
    model,
    index,
    documents,
    top_k=3
):
    query_embedding = generate_query_embedding(
        query,
        model
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    return get_documents(
        documents,
        indices[0],
        distances[0]
    )
```

O fluxo fica:

```text
query
  ↓
generate_query_embedding()
  ↓
query_embedding
  ↓
FAISS search()
  ↓
indices + distances
  ↓
get_documents()
  ↓
resultados
```

---

# 11. Cuidado com L2 versus similaridade

Foi definido o tipo de índice.

Se estiver utilizando:

```python
faiss.IndexFlatL2(...)
```

o valor retornado representa uma distância.

Nesse caso:

```text
menor valor = mais próximo
```

Exemplo:

```text
0.32 → mais próximo
0.81 → segundo
1.47 → terceiro
```

Não devemos chamar esse valor de "similaridade" sem considerar a métrica.

Se o projeto estiver utilizando:

```python
faiss.IndexFlatIP(...)
```

com vetores normalizados, o comportamento é diferente:

```text
maior valor = mais similar
```

A apresentação dos resultados deve refletir a métrica realmente utilizada.

---

# 12. Executar a busca

Podemos criar um exemplo no final de `search.py`:

```python
if __name__ == "__main__":
    from load_documents import load_documents
    from embeddings import (
        load_model,
        generate_query_embedding
    )
    from vector_store import (
        create_index
    )

    documents = load_documents()

    model = load_model()

    # Gera embeddings dos documentos
    embeddings = generate_embeddings(
        documents,
        model
    )

    embeddings = embeddings.astype("float32")

    # Cria o índice
    index = create_index(embeddings)

    # Consulta
    query = "Como funcionam os containers?"

    results = semantic_search(
        query,
        model,
        index,
        documents,
        top_k=3
    )

    print(f"\nConsulta: {query}\n")

    for result in results:
        print(
            f"Documento: {result['source']}"
        )
        print(
            f"Score: {result['score']}"
        )
        print(
            f"Texto: {result['text'][:200]}"
        )
        print("-" * 50)
```

Ajuste os imports de acordo com a implementação real.

---

# 13. Melhorar a arquitetura

Embora seja possível reconstruir o índice a cada execução durante o desenvolvimento, o projeto final deve aproveitar o índice persistido criado na Parte 03.

A arquitetura ideal será:

```text
              INGESTÃO
                  │
                  ▼
             Documentos
                  │
                  ▼
               Cohere
                  │
                  ▼
             Embeddings
                  │
                  ▼
                FAISS
                  │
          ┌───────┴────────┐
          ▼                ▼
     index.faiss      documents.json


              CONSULTA
                  │
                  ▼
          Texto da consulta
                  │
                  ▼
               Cohere
                  │
                  ▼
         Embedding da query
                  │
                  ▼
         index.faiss / FAISS
                  │
                  ▼
              índices
                  │
                  ▼
          documents.json
                  │
                  ▼
             resultados
```

Isso separa claramente:

### Ingestão

Processo mais pesado:

```text
documentos → embeddings → FAISS
```

### Consulta

Processo executado a cada pesquisa:

```text
query → embedding → FAISS → resultados
```

---

# 14. Persistir os documentos

Para utilizar o índice persistido, precisamos também salvar os documentos.

Criar uma função:

```python
import json


def save_documents(documents, path):
    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            documents,
            file,
            ensure_ascii=False,
            indent=2
        )
```

Salvar em:

```text
storage/faiss/documents.json
```

Exemplo:

```python
save_documents(
    documents,
    "storage/faiss/documents.json"
)
```

---

# 15. Carregar os documentos

Adicionar:

```python
def load_saved_documents(path):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)
```

Assim, a consulta poderá utilizar:

```text
index.faiss
+
documents.json
```

sem precisar reler os arquivos originais.

---

# 16. Separar ingestão e consulta

Neste ponto é recomendável separar dois processos.

### Processo de ingestão

```text
src/ingest.py
```

Responsável por:

```text
ler documentos
      ↓
gerar embeddings
      ↓
criar FAISS
      ↓
salvar index.faiss
      ↓
salvar documents.json
```

### Processo de busca

```text
src/search.py
```

Responsável por:

```text
carregar index.faiss
      ↓
carregar documents.json
      ↓
receber query
      ↓
gerar embedding da query
      ↓
consultar FAISS
      ↓
recuperar documentos
      ↓
mostrar resultados
```

Essa separação é mais próxima de uma arquitetura real de sistemas de busca vetorial.

---

# 17. Criar exemplos de consultas

Para demonstrar a busca semântica, crie consultas que não sejam necessariamente cópias literais dos documentos.

Exemplo:

```text
"Quero entender como executar aplicações isoladas"
```

Pode estar relacionado semanticamente a:

```text
docker.txt
```

Outra:

```text
"Qual linguagem possui muitas bibliotecas para inteligência artificial?"
```

Pode retornar:

```text
python.txt
```

Outra:

```text
"Como armazenar informações estruturadas em tabelas?"
```

Pode retornar:

```text
databases.txt
```

A ideia é demonstrar que a busca não depende somente da coincidência exata das palavras.

---

# 18. Exemplo de execução

Execute:

```bash
python src/search.py
```

Exemplo conceitual:

```text
Consulta: Quero entender como executar aplicações isoladas

Resultados:

1. docker.txt
   Score: 0.42

2. web_development.txt
   Score: 0.88

3. python.txt
   Score: 1.17
```

Os valores são apenas ilustrativos.

Os resultados reais dependem dos documentos, do modelo Cohere e da métrica utilizada.

---

# 19. Testar diferentes consultas

Faça pelo menos três consultas relacionadas a assuntos diferentes.

### Consulta 1

```text
Como executar aplicações em ambientes isolados?
```

Esperado:

```text
docker.txt
```

### Consulta 2

```text
Qual linguagem é bastante utilizada em inteligência artificial?
```

Esperado:

```text
python.txt
```

### Consulta 3

```text
Como trabalhar com dados armazenados em tabelas?
```

Esperado:

```text
databases.txt
```

O objetivo não é garantir que o primeiro resultado seja sempre exatamente o esperado, mas verificar se os documentos semanticamente relacionados aparecem entre os resultados.

---

# 20. Testar `top_k`

A função deve permitir controlar a quantidade de resultados:

```python
semantic_search(
    query,
    model,
    index,
    documents,
    top_k=3
)
```

Por exemplo:

```text
top_k=1
```

retorna:

```text
1 documento
```

Enquanto:

```text
top_k=5
```

retorna:

```text
até 5 documentos
```

Isso será útil para demonstrar como o sistema controla a quantidade de resultados recuperados.

---

# 21. Tratamento de `top_k`

Não devemos solicitar ao FAISS mais documentos do que existem no índice.

Podemos proteger a função:

```python
top_k = min(
    top_k,
    index.ntotal
)
```

Assim:

```text
5 documentos no índice
top_k = 10
```

será ajustado para:

```text
top_k = 5
```

---

# 22. Resultado final recomendado

É interessante retornar uma estrutura padronizada:

```python
{
    "query": "Como funcionam os containers?",
    "results": [
        {
            "source": "docker.txt",
            "score": 0.42,
            "text": "Docker permite..."
        },
        {
            "source": "python.txt",
            "score": 0.91,
            "text": "Python é..."
        }
    ]
}
```

Isso facilita uma futura integração com:

- API;
- frontend;
- chatbot;
- RAG.

---

# 23. Não adicionar RAG ainda

Embora busca semântica seja uma das etapas utilizadas em aplicações RAG, **não é necessário adicionar um LLM agora**.

O exercício pede:

```text
consulta
   ↓
embedding
   ↓
vector store
   ↓
documentos relevantes
```

Não:

```text
consulta
   ↓
RAG
   ↓
LLM
   ↓
resposta gerada
```

Portanto, mantenha o projeto focado no requisito da questão.

---

# 24. Checklist

Antes de considerar concluído:

- [ ] Criar função para gerar embedding da consulta
- [ ] Utilizar o mesmo modelo/configuração Cohere dos documentos
- [ ] Criar `src/search.py`
- [ ] Implementar `semantic_search()`
- [ ] Enviar o embedding da consulta ao FAISS
- [ ] Implementar `top_k`
- [ ] Recuperar os índices retornados
- [ ] Recuperar os documentos correspondentes
- [ ] Retornar `source`, `text` e `score`
- [ ] Considerar corretamente a métrica utilizada
- [ ] Persistir `documents.json`
- [ ] Testar carregamento do índice persistido
- [ ] Testar pelo menos três consultas semânticas
- [ ] Verificar se os documentos relacionados aparecem nos resultados

---

# 25. Critério para considerar a busca semântica funcionando

Está concluída quando for possível executar uma consulta como:

```text
"Quero entender como executar aplicações isoladas"
```

e receber resultados semelhantes a:

```text
Consulta:
Quero entender como executar aplicações isoladas

Resultados:

1. docker.txt
   Score: ...

2. web_development.txt
   Score: ...

3. python.txt
   Score: ...
```

O ponto principal é que:

```text
consulta
    ↓
embedding Cohere
    ↓
FAISS
    ↓
documentos semanticamente relacionados
```

esteja funcionando.

---

# 26. Estado final do projeto

Depois desta etapa, teremos:

```text
vector-search/
│
├── data/
│   └── documents/
│
├── storage/
│   └── faiss/
│       ├── index.faiss
│       └── documents.json
│
├── src/
│   ├── __init__.py
│   ├── load_documents.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── ingest.py
│   └── search.py
│
├── tests/
│
├── requirements.txt
└── README.md
```

O sistema já será capaz de realizar:

```text
DOCUMENTOS
    ↓
COHERE
    ↓
EMBEDDINGS
    ↓
FAISS
    ↓
BUSCA SEMÂNTICA
    ↓
DOCUMENTOS RELEVANTES
```

---

