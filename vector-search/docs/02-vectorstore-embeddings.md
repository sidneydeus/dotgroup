# Vector Stores e Embeddings

## Geração de Embeddings

### 1. Objetivo

Transformar os textos carregados em **representações vetoriais (embeddings)**.

Fluxo:

```text
Documentos → load_documents.py → Texto → Modelo de Embeddings → Vetores
```

Nesta etapa ainda **não utilizaremos FAISS**. Primeiro vamos validar a geração dos embeddings.

### 2. Tecnologia escolhida

Utilizaremos:

```text
cohere
```

com o modelo:

```text
embed-english-v3.0
```

O modelo será executado via API da Cohere, necessitando de uma chave de API (`COHERE_API_KEY`).

### 3. Instalação

Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Instale:

```bash
pip install cohere python-dotenv
```

Atualize o arquivo:

```bash
pip freeze > requirements.txt
```

Configure a variável de ambiente (crie arquivo `.env`):

```bash
echo "COHERE_API_KEY=sua-chave-aqui" > .env
```

### 4. Estrutura

```text
questao-3-vector-search/
├── data/
│   └── documents/
├── src/
│   ├── __init__.py
│   ├── load_documents.py
│   └── embeddings.py
├── tests/
├── requirements.txt
└── README.md
```

### 5. Criar `src/embeddings.py`

```python
import os
import numpy as np
import cohere
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "embed-english-v3.0"


def load_model():
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY não configurada. Crie um arquivo .env com COHERE_API_KEY=sua-chave")
    return cohere.ClientV2(api_key=api_key)


def generate_embeddings(documents, client):
    texts = [document["text"] for document in documents]
    
    response = client.embed(
        model=MODEL_NAME,
        texts=texts,
        input_type="search_document",
        embedding_types=["float"]
    )
    
    embeddings = response.embeddings.float
    return np.array(embeddings)
```

### 6. Integrar com os documentos

Adicione ao final do arquivo:

```python
if __name__ == "__main__":
    from load_documents import load_documents

    documents = load_documents()
    model = load_model()
    embeddings = generate_embeddings(documents, model)

    print(f"Documentos: {len(documents)}")
    print(f"Embeddings: {len(embeddings)}")
    print(f"Dimensão: {embeddings.shape[1]}")
```

Execute:

```bash
python src/embeddings.py
```

Na primeira execução, certifique-se de ter configurado o arquivo `.env` com `COHERE_API_KEY`.

### 7. Resultado esperado

Com os cinco documentos da Parte 01:

```text
Documentos: 5
Embeddings: 5
Dimensão: 1024
```

O `embed-english-v3.0` produz vetores com 1024 dimensões.

Conceitualmente:

```text
python.txt
    ↓
[0.023, -0.041, 0.087, ..., 0.017]
    ↓
1024 valores
```

### 8. Validar os embeddings

Para verificar o vetor gerado:

```python
print(embeddings[0][:10])
```

A saída será semelhante a:

```text
[ 0.0231 -0.0412  0.0873 ... ]
```

Os valores exatos podem variar conforme o ambiente e a versão das bibliotecas.

### 9. Validar a correspondência

Confirme que cada documento possui um vetor:

```python
for document, embedding in zip(documents, embeddings):
    print(f"{document['source']} -> {embedding.shape}")
```

Esperado:

```text
python.txt -> (1024,)
databases.txt -> (1024,)
docker.txt -> (1024,)
artificial_intelligence.txt -> (1024,)
web_development.txt -> (1024,)
```

A correspondência deve ser:

```text
documents[0] → embeddings[0]
documents[1] → embeddings[1]
documents[2] → embeddings[2]
```

### 10. Conceito importante

Um embedding é uma representação numérica do conteúdo de um texto.

Não devemos interpretar cada número isoladamente. O objetivo é permitir comparar a posição de diferentes textos no espaço vetorial.

Essa propriedade será utilizada posteriormente para encontrar textos semanticamente próximos.

### 11. Não implementar ainda

Nesta etapa não adicionar:

- FAISS;
- Milvus;
- cálculo de similaridade;
- busca semântica;
- RAG;
- LLM;
- API;
- frontend.

O objetivo é somente:

```text
Texto → Embedding
```

### 12. Checklist

- [ ] Instalar `cohere` e `python-dotenv`
- [ ] Configurar `COHERE_API_KEY` no arquivo `.env`
- [ ] Atualizar `requirements.txt`
- [ ] Criar `src/embeddings.py`
- [ ] Usar modelo `embed-english-v3.0`
- [ ] Carregar os documentos da Parte 01
- [ ] Gerar os embeddings
- [ ] Confirmar a quantidade de embeddings
- [ ] Confirmar dimensão 1024
- [ ] Exibir alguns valores do primeiro embedding
- [ ] Confirmar a correspondência entre documentos e vetores

### 13. Critério para avançar

A Parte 02 está concluída quando:

```bash
python src/embeddings.py
```

produzir algo semelhante a:

```text
Documentos: 5
Embeddings: 5
Dimensão: 1024

python.txt -> (1024,)
databases.txt -> (1024,)
docker.txt -> (1024,)
artificial_intelligence.txt -> (1024,)
web_development.txt -> (1024,)
```

Teremos validado:

```text
DOCUMENTO
    ↓
MODELO DE EMBEDDING
    ↓
VETOR
```

