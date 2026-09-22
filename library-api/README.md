# Library API

REST API para gerenciamento de uma biblioteca virtual construída com FastAPI, SQLite e SQLAlchemy.

## Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy 2.0** - ORM síncrono
- **SQLite** - Banco de dados (arquivo local)
- **Alembic** - Migrações de banco de dados
- **Pydantic** - Validação de dados
- **pytest** - Testes unitários

## Estrutura do Projeto

```
library-api/
├── alembic/                 # Migrações de banco
├── app/
│   ├── api/v1/endpoints/    # Endpoints da API
│   ├── core/                # Configurações e database
│   ├── models/              # Modelos SQLAlchemy
│   ├── schemas/             # Schemas Pydantic
│   ├── services/            # Lógica de negócio
│   └── main.py              # Entry point
├── tests/                   # Testes unitários
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── pytest.ini
```

## Como Executar

### Com Docker (Recomendado)

```bash
# Build e start
docker compose up --build -d

# Ver logs
docker compose logs -f api

# Parar
docker compose down
```

A API estará disponível em: **http://localhost:9000**

Documentação automática (Swagger): **http://localhost:9000/docs**

### Local (sem Docker)

```bash
# Criar venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload --port 8000
```

## Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/books/` | Cadastrar novo livro |
| GET | `/api/v1/books/` | Listar livros (com filtros) |
| GET | `/health` | Health check |

### Exemplos de Uso

**Cadastrar livro:**
```bash
curl -X POST http://localhost:9000/api/v1/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean Code",
    "author": "Robert Martin",
    "publication_date": "2008-08-01",
    "summary": "A handbook of agile software craftsmanship"
  }'
```

**Listar todos os livros:**
```bash
curl http://localhost:9000/api/v1/books/
```

**Filtrar por título:**
```bash
curl "http://localhost:9000/api/v1/books/?title=clean"
```

**Filtrar por autor:**
```bash
curl "http://localhost:9000/api/v1/books/?author=martin"
```

**Filtrar por ambos:**
```bash
curl "http://localhost:9000/api/v1/books/?title=clean&author=martin"
```

## Testes

```bash
# Com Docker
docker compose exec api pytest tests/ -v

# Local
pytest tests/ -v
```

Os testes usam banco de dados em memória (SQLite `:memory:`) para isolamento.

## Migrações (Alembic)

```bash
# Criar nova migração
alembic revision --autogenerate -m "descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Ver histórico
alembic history

# Reverter última migração
alembic downgrade -1
```

## Estrutura do Livro

```json
{
  "id": 1,
  "title": "string (obrigatório, max 200 chars)",
  "author": "string (obrigatório, max 100 chars)",
  "publication_date": "date (YYYY-MM-DD, obrigatório)",
  "summary": "string (opcional, max 2000 chars)"
}
```

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz (opcional):

```env
APP_NAME="Library API"
DEBUG=true
```

## Health Check

```bash
curl http://localhost:9000/health
# Resposta: {"status": "healthy"}
```