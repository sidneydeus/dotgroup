# Vector Stores e Embeddings

## Implementação da Vector Store com FAISS

### 1. Objetivo

Nesta etapa vamos armazenar no **FAISS** os embeddings gerados pelo **Cohere**.

O fluxo do projeto passa a ser:

```text
Documentos
    ↓
Cohere Embeddings API
    ↓
Embeddings
    ↓
FAISS
    ↓
Índice vetorial
```

Nesta etapa ainda não vamos implementar a busca semântica completa.

O objetivo é validar que:

1. os embeddings gerados pelo Cohere podem ser utilizados pelo FAISS;
2. os vetores são adicionados corretamente ao índice;
3. o índice pode ser consultado;
4. o índice pode ser persistido em disco;
5. o índice pode ser carregado novamente.

---

## 2. O que é FAISS?

FAISS é uma biblioteca para busca eficiente por similaridade entre vetores.

Neste projeto, o Cohere será responsável por transformar textos em vetores, enquanto o FAISS será responsável por armazenar e consultar esses vetores.

```text
             Cohere
Texto ──────────────────> Embedding
                              │
                              ▼
                           FAISS
                              │
                              ▼
                       Índice vetorial
```

O FAISS não precisa conhecer o significado dos textos.

Ele trabalha exclusivamente com os vetores produzidos pelo modelo de embeddings.

---

## 3. Instalação

Com o ambiente virtual ativado:

```bash
pip install faiss-cpu
```

Atualize o `requirements.txt`:

```bash
pip freeze > requirements.txt
```

O pacote utilizado para a Vector Store será:

```text
faiss-cpu
```

O cliente do Cohere já deverá estar instalado/configurado conforme a Parte 02.

---

## 4. Estrutura do projeto

Após esta etapa, a estrutura deverá estar aproximadamente assim:

```text
questao-3-vector-search/
├── data/
│   └── documents/
│       ├── python.txt
│       ├── databases.txt
│       ├── docker.txt
│       ├── artificial_intelligence.txt
│       └── web_development.txt
│
├── storage/
│   └── faiss/
│
├── src/
│   ├── __init__.py
│   ├── load_documents.py
│   ├── embeddings.py
│   └── vector_store.py
│
├── tests/
│
├── requirements.txt
└── README.md
```

O diretório:

```text
storage/faiss/
```

será utilizado para armazenar o índice persistido.

---

# 5. Descobrindo a dimensão dos embeddings

Não devemos assumir:

```python
dimension = 384
```
Com o Cohere, a dimensão depende do modelo de embeddings escolhido.

Portanto, devemos obter a dimensão diretamente do vetor gerado:

```python
dimension = embeddings.shape[1]
```

Isso deixa o código independente da dimensão específica do modelo.

Por exemplo:

```text
embeddings.shape

(5, N)
```

onde:

```text
5 = quantidade de documentos
N = dimensão do embedding
```

---

# 6. Criar o módulo da Vector Store

Criar:

```text
src/vector_store.py
```

Implementação inicial:

```python
import faiss


def create_index(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index
```

As principais operações são:

### Obter a dimensão

```python
dimension = embeddings.shape[1]
```

### Criar o índice

```python
index = faiss.IndexFlatL2(dimension)
```

### Adicionar os embeddings

```python
index.add(embeddings)
```

---

# 7. Por que utilizar `IndexFlatL2`?

Para este exercício acadêmico, `IndexFlatL2` é uma implementação simples para demonstrar uma Vector Store.

Ela utiliza a distância Euclidiana:

```text
L2 = distância Euclidiana
```

Conceitualmente:

```text
distância menor
      ↓
vetores mais próximos
```

Existem outras estruturas disponíveis no FAISS, inclusive alternativas mais apropriadas para grandes volumes de dados.

Entretanto, para o conjunto pequeno de documentos deste exercício, `IndexFlatL2` é suficiente para demonstrar o conceito.

---

# 8. Atenção à métrica utilizada

Existe uma consideração importante ao utilizar embeddings do Cohere.

O modelo de embeddings possui características próprias e pode recomendar uma determinada métrica de similaridade.

Por isso, devemos verificar qual modelo do Cohere está sendo utilizado e qual métrica é recomendada para esse modelo.

Se estivermos utilizando **similaridade de cosseno**, uma estratégia comum com FAISS é normalizar os vetores e utilizar:

```python
faiss.IndexFlatIP(dimension)
```

onde `IP` significa **Inner Product**.

Nesse caso:

```text
vetores normalizados
        ↓
Inner Product
        ↓
similaridade de cosseno
```

### Não altere a métrica sem verificar o modelo

Antes de escolher entre:

```python
faiss.IndexFlatL2(...)
```

e:

```python
faiss.IndexFlatIP(...)
```

verifique qual métrica está sendo utilizada pelo embedding do Cohere configurado na Parte 02.

Para o restante deste documento, vamos utilizar `IndexFlatL2` como exemplo inicial.

Se a implementação da Parte 02 estiver configurada para similaridade de cosseno, adapte a criação do índice conforme essa configuração.

---

# 9. Garantir o formato dos embeddings

O FAISS espera uma matriz NumPy com formato:

```text
quantidade_de_documentos × dimensão_do_embedding
```

Por exemplo:

```text
5 × N
```

Podemos verificar:

```python
print(embeddings.shape)
```

Resultado conceitual:

```text
(5, N)
```

Também podemos verificar:

```python
print(embeddings.dtype)
```

É recomendável utilizar `float32` para os vetores enviados ao FAISS.

Caso necessário:

```python
embeddings = embeddings.astype("float32")
```

---

# 10. Testar a criação do índice

Podemos integrar o código com os módulos das partes anteriores:

```python
if __name__ == "__main__":
    from embeddings import generate_embeddings
    from load_documents import load_documents

    documents = load_documents()

    embeddings = generate_embeddings(documents)

    embeddings = embeddings.astype("float32")

    index = create_index(embeddings)

    print(f"Documentos: {len(documents)}")
    print(f"Shape dos embeddings: {embeddings.shape}")
    print(f"Vetores no FAISS: {index.ntotal}")
```

Executar:

```bash
python src/vector_store.py
```

O resultado deverá ser semelhante a:

```text
Documentos: 5
Shape dos embeddings: (5, N)
Vetores no FAISS: 5
```

O valor de `N` depende do modelo do Cohere escolhido na Parte 02.

---

# 11. Testar uma consulta diretamente no FAISS

Ainda não vamos transformar uma frase em embedding.

Para testar apenas o funcionamento do FAISS, podemos utilizar um dos embeddings já existentes:

```python
query_embedding = embeddings[0:1]
```

Depois:

```python
distances, indices = index.search(
    query_embedding,
    3
)
```

Exibir:

```python
print("Índices encontrados:")
print(indices)

print("Distâncias:")
print(distances)
```

Resultado conceitual:

```text
Índices encontrados:
[[0 3 4]]

Distâncias:
[[0.0 1.23 1.87]]
```

Os valores reais dependerão dos documentos e do modelo utilizado.

---

# 12. Entendendo `search()`

A chamada:

```python
index.search(query_embedding, 3)
```

solicita os três vetores mais próximos.

Ela retorna:

```python
distances
indices
```

### `indices`

Representa a posição dos vetores no índice:

```text
[0, 3, 4]
```

Consequentemente:

```python
documents[0]
documents[3]
documents[4]
```

são os documentos associados aos resultados.

### `distances`

Representa a distância entre o vetor de consulta e os vetores encontrados.

A interpretação depende da métrica utilizada.

Com L2:

```text
menor distância = maior proximidade
```

Com Inner Product normalizado:

```text
maior similaridade = maior proximidade
```

Por isso, a métrica escolhida precisa ser considerada ao interpretar os resultados.

---

# 13. Associação entre FAISS e documentos

O FAISS armazena os vetores, mas não sabe automaticamente que:

```text
índice 0 = python.txt
```

Precisamos manter essa associação.

A ordem será preservada:

```text
documents[0]
      ↕
embeddings[0]
      ↕
FAISS index 0
```

e:

```text
documents[1]
      ↕
embeddings[1]
      ↕
FAISS index 1
```

Essa relação será utilizada na Parte 04 para recuperar os documentos originais.

---

# 14. Persistir o índice

Uma das vantagens de utilizar uma Vector Store é poder persistir o índice.

Criar:

```python
def save_index(index, path):
    faiss.write_index(index, path)
```

Salvar em:

```text
storage/faiss/index.faiss
```

Exemplo:

```python
INDEX_PATH = "storage/faiss/index.faiss"

save_index(index, INDEX_PATH)

print(f"Índice salvo em: {INDEX_PATH}")
```

---

# 15. Carregar o índice

Criar:

```python
def load_index(path):
    return faiss.read_index(path)
```

Teste:

```python
loaded_index = load_index(
    "storage/faiss/index.faiss"
)

print(
    f"Vetores carregados: "
    f"{loaded_index.ntotal}"
)
```

Resultado esperado:

```text
Vetores carregados: 5
```

---

# 16. Fluxo de persistência

Na primeira execução:

```text
Documentos
    ↓
Cohere
    ↓
Embeddings
    ↓
FAISS
    ↓
index.faiss
```

Depois:

```text
index.faiss
    ↓
FAISS
    ↓
Busca
```

Isso permite separar o processo de ingestão do processo de consulta.

---

# 17. Persistência dos documentos

O arquivo:

```text
index.faiss
```

não deve ser considerado um armazenamento dos textos originais.

Precisamos manter também os documentos/metadados.

Uma estrutura futura será:

```text
storage/
└── faiss/
    ├── index.faiss
    └── documents.json
```

Exemplo:

```json
[
    {
        "source": "python.txt",
        "text": "Python é uma linguagem..."
    },
    {
        "source": "docker.txt",
        "text": "Docker permite..."
    }
]
```

A implementação dessa associação ficará para a Parte 04.

---

# 18. Não implementar ainda

Nesta etapa não implementar:

* embedding da consulta;
* busca por texto;
* busca semântica completa;
* ranking apresentado ao usuário;
* API;
* frontend;
* RAG;
* LLM.

O objetivo é validar somente:

```text
Cohere
   ↓
Embedding
   ↓
FAISS
   ↓
Índice
   ↓
Persistência
```

---

# 19. Checklist

Antes de avançar:

* [ ] Instalar `faiss-cpu`
* [ ] Atualizar `requirements.txt`
* [ ] Criar `storage/faiss/`
* [ ] Criar `src/vector_store.py`
* [ ] Obter a dimensão dos embeddings dinamicamente
* [ ] Converter os embeddings para `float32`, se necessário
* [ ] Criar o índice FAISS
* [ ] Adicionar os embeddings
* [ ] Confirmar `index.ntotal`
* [ ] Executar uma busca usando um embedding existente
* [ ] Confirmar que os índices são retornados
* [ ] Confirmar que as distâncias/similaridades são retornadas
* [ ] Salvar `storage/faiss/index.faiss`
* [ ] Carregar o índice novamente
* [ ] Confirmar a quantidade de vetores carregados

---

# 20. Critério para avançar

Está concluída quando:

```bash
python src/vector_store.py
```

produzir algo semelhante a:

```text
Documentos: 5
Shape dos embeddings: (5, N)
Vetores no FAISS: 5

Índices encontrados:
[[0 3 4]]

Distâncias:
[[0.0 ... ...]]

Índice salvo em:
storage/faiss/index.faiss

Vetores carregados: 5
```

O valor de `N`, os índices e as distâncias dependem do modelo Cohere e dos documentos utilizados.

O importante é validar:

```text
5 documentos
      ↓
5 embeddings Cohere
      ↓
5 vetores no FAISS
      ↓
índice persistido
      ↓
índice carregado novamente
```
---


