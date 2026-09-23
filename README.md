# dotgroup

Este repositório contém 3 aplicações de teste com foco em **backend IA**:

## Aplicações

| Aplicação | Descrição | Tecnologias Principais |
|-----------|-----------|------------------------|
| **[vector-search](./vector-search)** | Busca semântica de documentos usando embeddings Cohere + FAISS | Python, Cohere API, FAISS, pytest |
| **[chatbot](./chatbot)** | Chatbot backend para programação Python com FastAPI + LangChain + Groq + LangSmith | FastAPI, LangChain, Groq, LangSmith, Docker |
| **[library-api](./library-api)** | REST API para gerenciamento de biblioteca virtual | FastAPI, SQLAlchemy 2.0, SQLite, Alembic |

Cada aplicação possui seu próprio `README.md` com instruções detalhadas de instalação, configuração e execução.

## Estrutura do Repositório

```
dotgroup/
├── vector-search/    # Busca semântica (IA/Embeddings)
├── chatbot/          # Chatbot Python (LLM/LangChain)
├── library-api/      # API REST (CRUD/FastAPI)
└── README.md         # Este arquivo
```

## Como Começar

Escolha uma aplicação e siga as instruções no seu respectivo README:

```bash
# Exemplo: entrar no vector-search
cd vector-search
cat README.md
```

---

*Projeto para fins de estudo e demonstração de backends com IA.*