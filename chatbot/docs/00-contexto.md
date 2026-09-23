# Chatbot de Programação Python

## Objetivo

Desenvolver um chatbot capaz de responder perguntas de usuários
sobre programação em Python utilizando uma LLM.

## Requisitos

O sistema deverá:

1. Receber perguntas em texto.
2. Enviar a pergunta para um backend.
3. Utilizar LangChain para integração com uma LLM.
4. Utilizar um modelo da OpenAI.
5. Retornar a resposta ao usuário.
6. Possuir memória de conversação.
7. Possuir observabilidade utilizando LangSmith.
8. Possuir testes automatizados.

## Stack

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn

### IA
- LangChain
- OpenAI
- LangSmith

### Frontend
- HTML/CSS/JavaScript ou framework escolhido posteriormente.

## Arquitetura

O projeto será desenvolvido em etapas:

1. Backend FastAPI
2. Integração com LLM através do LangChain
3. Observabilidade com Langfuse
4. Testes
5. Frontend

## Restrição de desenvolvimento

Cada etapa deve ser implementada e validada antes do início da
próxima etapa.

Não implementar frontend antes da API estar funcionando.

Não integrar a LLM durante a primeira etapa.

Não adicionar funcionalidades não especificadas sem necessidade.