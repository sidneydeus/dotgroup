# Vector Search - Busca Semântica de Documentos

Sistema de busca semântica utilizando embeddings da **Cohere** e **FAISS**, desenvolvido em etapas incrementais.

## Estrutura do Projeto

```
vector-search/
├── data/
│   └── documents/              # Documentos de texto (.txt)
├── storage/
│   └── faiss/                  # Índice FAISS e documentos persistidos
│       ├── index.faiss
│       └── documents.json
├── src/
│   ├── __init__.py
│   ├── load_documents.py       # Carregamento de documentos
│   ├── embeddings.py           # Geração de embeddings (Cohere)
│   ├── vector_store.py         # Operações FAISS (IndexFlatIP)
│   ├── ingest.py               # Pipeline de ingestão (cria índice)
│   └── search.py               # Pipeline de busca semântica
├── tests/
│   ├── test_load_documents.py
│   ├── test_embeddings.py
│   ├── test_vector_store.py
│   ├── test_ingest.py
│   └── test_search.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .env.example                # Modelo para configuração da API key
└── README.md
```

## Pré-requisitos

- Python 3.10+
- Chave de API da Cohere (gratuita em https://dashboard.cohere.com/api-keys)

## Instalação Local

```bash
cd vector-search
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Configuração da API Key

```bash
cp .env.example .env
# Edite .env e adicione sua chave:
# COHERE_API_KEY=sua-chave-aqui
```

## Como Executar

### 1. Ingestão (executa uma vez)

Cria o índice FAISS e persiste os documentos:

```bash
PYTHONPATH=. python src/ingest.py
```

Saída esperada:
```
Carregando documentos...
Documentos carregados: 5
Carregando modelo Cohere...
Gerando embeddings...
Embeddings gerados: (5, 1024)
Criando índice FAISS (IndexFlatIP)...
Vetores no índice: 5
Salvando índice em storage/faiss/index.faiss...
Salvando documentos em storage/faiss/documents.json...
Ingestão concluída!
```

### 2. Busca Semântica

Executa consultas de teste usando o índice persistido:

```bash
PYTHONPATH=. python src/search.py
```

Saída esperada:
```
Query: Como executar aplicações em ambientes isolados?
------------------------------------------------------------
1. docker.txt
   Score: 0.4375
   Texto: Docker permite empacotar aplicações...

Query: Qual linguagem é bastante utilizada em inteligência artificial?
------------------------------------------------------------
1. artificial_intelligence.txt
   Score: 0.6783
   Texto: Inteligência Artificial (IA) é a área...

Query: Como trabalhar com dados armazenados em tabelas?
------------------------------------------------------------
1. databases.txt
   Score: 0.5015
   Texto: Bancos de dados são sistemas organizados...
```

## Testes

```bash
# Todos os testes
python -m pytest tests/ -v

# Testes específicos
python -m pytest tests/test_embeddings.py -v
python -m pytest tests/test_vector_store.py -v
python -m pytest tests/test_ingest.py -v
python -m pytest tests/test_search.py -v
python -m pytest tests/test_load_documents.py -v
```

Resultado esperado: **29 testes passando**

## Tecnologias Utilizadas

| Componente | Tecnologia | Versão |
|------------|------------|--------|
| Embeddings | Cohere `embed-english-v3.0` | 1024 dims |
| Vector Store | FAISS `IndexFlatIP` | cosine similarity |
| API Client | Cohere Python SDK | v2 |
| Config | python-dotenv | - |
| Testes | pytest | - |

## Arquitetura

### Ingestão (offline, executada uma vez)
```
Documentos (.txt)
       ↓
Cohere Embeddings (search_document)
       ↓
FAISS IndexFlatIP (cosine similarity)
       ↓
storage/faiss/index.faiss + documents.json
```

### Busca (online, executada a cada consulta)
```
Query do usuário
       ↓
Cohere Embeddings (search_query)
       ↓
FAISS Search (top-k)
       ↓
Índices → Documentos originais
       ↓
Resultados ranqueados por score (maior = mais similar)
```

## Documentação Detalhada

- `docs/01-estrutura.md` — Estrutura inicial e carregamento de documentos
- `docs/02-vectorstore-embeddings.md` — Geração de embeddings com Cohere
- `docs/03-faiss.md` — Vector Store com FAISS
- `docs/04-busca-semantica.md` — Busca semântica completa

## Execução via Docker

```bash
docker-compose build
docker-compose run --rm app python src/ingest.py
docker-compose run --rm app python src/search.py
```

## Notas Importantes

- **Métrica**: Usa `IndexFlatIP` (Inner Product) com vetores normalizados = similaridade de cosseno, recomendada para embeddings Cohere
- **Input Types**: Documentos usam `search_document`, queries usam `search_query` (best practice Cohere)
- **Persistência**: Índice e documentos salvos em `storage/faiss/` para separar ingestão de consulta
- **Dimensão**: 1024 (definida pelo modelo `embed-english-v3.0`, obtida dinamicamente no código)