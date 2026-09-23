# Vector Stores e Embeddings

## Estrutura do projeto e conjunto de documentos

### 1. Objetivo

Construir um sistema de **busca semântica de documentos** utilizando:

- um conjunto de documentos de texto;
- um modelo de embeddings;
- uma Vector Store;
- uma função de busca por similaridade semântica.

O desenvolvimento será dividido em partes para permitir a implementação e validação incremental.

### 2. Arquitetura prevista

Fluxo principal:

```text
Documentos
    │
    ▼
Leitura dos textos
    │
    ▼
Chunking / divisão em trechos
    │
    ▼
Modelo de Embeddings
    │
    ▼
Vetores
    │
    ▼
FAISS
    │
    ▼
Busca semântica
    │
    ▼
Documentos mais relevantes
```

Nesta primeira etapa **não implementaremos embeddings nem FAISS**. O objetivo é preparar e validar a entrada do sistema.

### 3. Divisão do desenvolvimento

| Parte | Objetivo | Resultado |
|---|---|---|
| 01 | Estrutura + documentos | Projeto executável e documentos disponíveis |
| 02 | Geração de embeddings | Textos convertidos em vetores |
| 03 | Vector Store | Embeddings armazenados no FAISS |
| 04 | Busca semântica | Consulta retornando documentos relevantes |
| 05 | Testes e demonstração | Exemplos de consultas e resultados |
| 06 | Documentação final | README |

### 4. Estrutura do projeto

Criar inicialmente:

```text
vector-search/
├── data/
│   └── documents/
├── src/
│   ├── __init__.py
│   └── load_documents.py
├── tests/
├── requirements.txt
├── README.md
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

### 5. Conjunto de documentos

Para facilitar os testes, utilizar inicialmente arquivos `.txt`.

Criar pelo menos 5 documentos com assuntos claramente diferentes.

Sugestão:

```text
data/documents/
├── python.txt
├── databases.txt
├── docker.txt
├── artificial_intelligence.txt
└── web_development.txt
```

Os documentos devem conter conteúdo suficiente para que uma consulta possa ser relacionada semanticamente ao assunto.

Exemplo de `python.txt`:

```text
Python é uma linguagem de programação de alto nível conhecida
pela sintaxe simples e pela grande quantidade de bibliotecas
disponíveis. É utilizada em desenvolvimento web, automação,
ciência de dados e inteligência artificial.
```

Exemplo de `docker.txt`:

```text
Docker permite empacotar aplicações e suas dependências em
containers. Containers facilitam a criação de ambientes
reprodutíveis para desenvolvimento, testes e produção.
```

### 6. Carregamento dos documentos

Criar `src/load_documents.py`.

Responsabilidades:

1. localizar os arquivos em `data/documents`;
2. ler o conteúdo;
3. associar o texto ao nome do arquivo;
4. retornar uma estrutura simples que possa ser utilizada pelas próximas etapas.

Estrutura esperada:

```python
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

### 7. Critérios de validação

**Execução local (desenvolvimento):**
```bash
python src/load_documents.py
```

**Execução via Docker (recomendado):**
```bash
docker-compose run --rm app
```

O programa deve:

- localizar os arquivos;
- carregar todos os documentos;
- informar quantos documentos foram encontrados;
- mostrar o nome de cada documento;
- mostrar uma pequena parte do conteúdo.

Exemplo esperado:

```text
Documentos encontrados: 5

- python.txt
- databases.txt
- docker.txt
- artificial_intelligence.txt
- web_development.txt
```

### 7.1. Execução via Docker

O projeto inclui configuração para execução em container via Docker Compose, garantindo reprodutibilidade do ambiente.

**Arquivos de configuração:**
- `Dockerfile` — imagem base `python:3.11-slim`, instala dependências e copia código
- `docker-compose.yml` — orquestra serviços: `app` (aplicação principal) e `faiss` (servidor FAISS para Parte 03+)
- `.dockerignore` — exclui arquivos desnecessários do build (venv, __pycache__, .git, etc.)

**Volumes mapeados:**
- `./data:/app/data` — documentos persistem no host e são acessíveis no container
- `./src:/app/src` — código fonte montado para hot-reload em desenvolvimento

**Comandos úteis:**

```bash
# Build da imagem
docker-compose build

# Executar carregamento de documentos (Parte 01)
docker-compose run --rm app

# Iniciar serviços em background (Para Parte 03+)
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Parar serviços
docker-compose down
```

**Serviço FAISS (preparação para Parte 03):**
O `docker-compose.yml` já inclui o serviço `faiss` (porta 8001) usando imagem oficial. Nas próximas partes, a aplicação conectará a este serviço para indexação e busca vetorial.

### 8. Regra importante

Neste projeto, devemos separar claramente:

**Documento**

Texto original utilizado como fonte.

**Chunk**

Trecho de um documento utilizado para gerar um embedding.

**Embedding**

Representação numérica do texto em um espaço vetorial.

**Vector Store**

Estrutura responsável por armazenar e consultar os vetores.

**Busca semântica**

Processo de transformar uma consulta em embedding e encontrar vetores semanticamente próximos.

Nesta primeira etapa trabalharemos somente com **documentos**.

### 9. Não implementar ainda

Não adicionar nesta etapa:

- FAISS;
- Milvus;
- embeddings;
- transformers;
- busca por similaridade;
- RAG;
- LLM;
- API;
- frontend.

**Nota:** Docker e docker-compose **são implementados nesta etapa** para preparar o ambiente de execução. O FAISS será adicionado como serviço no docker-compose para uso futuro (Parte 03+).

Esses componentes serão adicionados gradualmente nas próximas partes.

## Checklist da estrutura

- [ ] Criar diretório do projeto
- [ ] Criar ambiente virtual
- [ ] Criar diretórios `data`, `src` e `tests`
- [ ] Criar pelo menos 5 documentos `.txt`
- [ ] Criar `load_documents.py`
- [ ] Criar `Dockerfile`
- [ ] Criar `docker-compose.yml`
- [ ] Criar `.dockerignore`
- [ ] Criar `requirements.txt`
- [ ] Executar o carregamento via Docker (`docker-compose run --rm app`)
- [ ] Confirmar que todos os documentos foram encontrados
- [ ] Confirmar que o conteúdo foi carregado corretamente

