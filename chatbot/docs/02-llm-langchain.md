# Etapa 2 — Integração com LLM

## Objetivo

Integrar o backend FastAPI existente com uma LLM da Groq utilizando LangChain.

A API criada na etapa anterior deve continuar funcionando.

---

## Pré-requisitos

A etapa 1 deve estar concluída.

Antes de modificar o código:

1. Executar os testes existentes.
2. Confirmar que todos passam.
3. Preservar os endpoints existentes.

---

## Dependências

Adicionar:

- langchain
- langchain-groq

Não adicionar bibliotecas desnecessárias.

---

## Configuração

Adicionar ao `.env`:

GROQAI_API_KEY=

GROQAI_MODEL=

A chave nunca deve ser colocada diretamente no código.

Não versionar `.env`.

Atualizar `.gitignore`.

Atualizar `.env.example`.

---

## Integração

Criar uma camada responsável pela comunicação com a LLM.

A rota FastAPI não deve chamar diretamente o cliente da GROQ AI.

Fluxo:

HTTP Request
    ↓
FastAPI Route
    ↓
Chat Service
    ↓
LangChain
    ↓
GROQAI
    ↓
Chat Service
    ↓
HTTP Response

---

## Comportamento

Quando o usuário enviar:

"Como criar uma lista em Python?"

O sistema deverá enviar a pergunta para a LLM e retornar
a resposta gerada.

---

## System Prompt

O chatbot deve assumir o papel de um assistente especializado
em programação Python.

Ele deve:

- responder em português;
- explicar conceitos de forma didática;
- fornecer exemplos de código quando apropriado;
- explicar o código apresentado;
- não responder assuntos que não estejam relacionados à programação com python;

---

## LangChain

Utilizar as abstrações atuais do LangChain para integração com modelos de chat.

Não implementar manualmente chamadas HTTP para a GroqAI.

---

## Memória

Nesta etapa implementar apenas memória de conversação em memória do processo, caso seja necessária para demonstrar conversação.

Não implementar banco de dados.

Não implementar Redis.

Não implementar banco vetorial.

---

## Critérios de conclusão

- API continua funcionando.
- Pergunta chega à LLM.
- Resposta da LLM retorna pela API.
- API key é carregada através de variável de ambiente.
- Nenhuma chave é armazenada no código.
- Testes existentes continuam passando.
- Deve existir pelo menos um teste para o serviço de chat,
  utilizando mock da LLM para não depender da API durante
  os testes automatizados.