# Etapa 1 — Backend FastAPI

## Objetivo

Criar o backend inicial do chatbot utilizando FastAPI.

Nesta etapa NÃO implementar integração com LLM, LangChain ou LangFuse.

O objetivo é criar e testar a API que posteriormente receberá a
integração com a inteligência artificial.

---

## Stack

Utilizar:

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- pytest

Utilizar ambiente virtual Python (`venv`).

---

## Estrutura esperada

Criar uma estrutura semelhante a:

backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── chat.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── chat.py
│   └── services/
│       ├── __init__.py
│       └── chat.py
│
├── tests/
│   ├── __init__.py
│   └── test_chat.py
│
├── requirements.txt
└── .env.example

---

## Endpoint

Criar:

POST /api/chat

O endpoint deverá receber:

{
    "message": "Como criar uma lista em Python?"
}

E retornar:

{
    "response": "Resposta simulada..."
}

Nesta primeira etapa a resposta será simulada.

Não utilizar nenhuma LLM.

---

## Schemas

Criar modelos Pydantic para:

### ChatRequest

Campo:

- message: string

O campo deve ser obrigatório.

Não aceitar mensagem vazia ou contendo apenas espaços.

### ChatResponse

Campo:

- response: string

---

## Service

Criar uma camada de serviço responsável pelo processamento da mensagem.

Exemplo conceitual:

ChatService

A implementação inicial deve apenas retornar uma resposta simulada.

Não colocar lógica de negócio diretamente dentro da rota FastAPI.

---

## API

A rota `/api/chat` deve:

1. Receber o ChatRequest.
2. Validar os dados através do Pydantic.
3. Chamar o serviço de chat.
4. Retornar ChatResponse.

---

## Health Check

Criar:

GET /health

Resposta:

{
    "status": "ok"
}

---

## Tratamento de erros

A API deve utilizar os mecanismos padrão do FastAPI para erros de validação.

Uma mensagem vazia deve retornar HTTP 422.

---

## CORS

Configurar CORS de forma que posteriormente seja possível
conectar um frontend separado ao backend.

Durante desenvolvimento pode permitir localhost.

Não utilizar `allow_origins=["*"]` sem necessidade.

---

## Configuração

Criar `.env.example`.

Nesta etapa não são necessárias chaves de API.

Preparar a estrutura para que configurações futuras possam
ser adicionadas através de variáveis de ambiente.

---

## Testes

Criar testes para:

1. GET /health
2. POST /api/chat com mensagem válida
3. POST /api/chat sem message
4. POST /api/chat com mensagem vazia
5. POST /api/chat com mensagem contendo apenas espaços

Utilizar `pytest` e `TestClient` do FastAPI.

---

## Critérios de conclusão

A etapa somente estará concluída quando:

- FastAPI iniciar corretamente.
- `/health` responder HTTP 200.
- `/api/chat` aceitar uma pergunta.
- `/api/chat` retornar uma resposta simulada.
- Validação Pydantic estiver funcionando.
- CORS estiver configurado.
- Todos os testes passarem.

---

## Execução

O backend deve ser executável com:

uvicorn app.main:app --reload

A documentação automática deve estar disponível em:

/docs

---

## Importante

Não implementar nesta etapa:

- OpenAI
- LangChain
- LangSmith
- embeddings
- RAG
- banco vetorial
- memória persistente
- autenticação
- frontend

Apenas o backend HTTP necessário para receber e responder mensagens.