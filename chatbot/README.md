# Chatbot de Programação Python

Backend FastAPI para um chatbot que responde perguntas sobre programação em Python.

## Estrutura do Projeto

```
chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py                      # FastAPI app
│   │   ├── api/routes/chat.py           # Endpoint POST /api/chat
│   │   ├── schemas/chat.py              # Pydantic models
│   │   ├── services/chat.py             # Lógica de negócio
│   │   ├── core/
│   │   │   ├── config.py                # Configurações (pydantic-settings)
│   │   │   └── langsmith.py             # Cliente LangSmith
│   ├── tests/
│   │   └── test_chat.py                 # Testes automatizados
│   ├── requirements.txt
│   └── .env.example
└── docs/
    ├── 00- contexto.md
    ├── 01-backend-fastapi.md
    ├── 02-llm-langchain.md
    └── 03-langfuse.md
```

## Requisitos

- Python 3.11+
- Ambiente virtual (`venv`)
- Docker e Docker Compose (opcional, para execução containerizada)

## Instalação

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Executando o Servidor

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

O servidor inicia em `http://localhost:8000`.

- Documentação Swagger: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Executando com Docker

### Build e Execução

```bash
# Na raiz do projeto (chatbot/)
docker compose up --build -d
```

O servidor inicia em `http://localhost:8005`.

- Documentação Swagger: `http://localhost:8005/docs`
- Health check: `http://localhost:8005/health`

### Parar os containers

```bash
docker compose down
```

### Ver logs

```bash
docker compose logs -f
```

### Executar testes no container

```bash
docker compose exec backend pytest tests/ -v
```

## Testando a API

### Via curl

**Health check:**
```bash
curl http://localhost:8005/health
# Resposta: {"status": "ok"}
```

**Chat com mensagem válida:**
```bash
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Como criar uma lista em Python?"}'
```

**Chat com sessão (opcional):**
```bash
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Como criar uma lista em Python?", "session_id": "sessao-123"}'
```

**Chat com mensagem vazia (retorna 422):**
```bash
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
```

**Chat sem campo message (retorna 422):**
```bash
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Via Swagger UI

1. Acesse `http://localhost:8005/docs`
2. Clique em `POST /api/chat`
3. Clique em "Try it out"
4. Insira o JSON: `{"message": "sua pergunta", "session_id": "opcional"}`
5. Clique em "Execute"

## Exemplos de Perguntas e Respostas

Abaixo estão exemplos reais de interação com o chatbot demonstrando seu funcionamento:

### 1. Pergunta básica sobre listas

**Pergunta:**
```bash
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Como criar uma lista em Python?"}'
```

**Resposta (resumida):**
```json
{
  "response": "## Como criar uma lista em Python\n\nUma **lista** em Python é uma coleção ordenada e mutável de elementos...\n\n### 1. Sintaxe básica\n```python\nminha_lista = [1, 2, 3, 4, 5]\n```\n\n### 2. Listas heterogêneas\n```python\nmisturada = [42, \"Python\", 3.14, True, None]\n```\n\n### 3. Listas aninhadas\n```python\nmatriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\n```\n\n### 4. Compreensão de listas\n```python\nquadrados = [x**2 for x in range(10)]\n```"
}
```

---

### 2. Pergunta de acompanhamento (com session_id)

**Pergunta:**
```bash
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "E como adicionar itens?", "session_id": "sessao-123"}'
```

**Resposta (resumida):**
```json
{
  "response": "Para adicionar itens a uma lista em Python você tem várias opções:\n\n## 1. `append()` – Adiciona no final\n```python\nlista = [1, 2, 3]\nlista.append(4)          # lista vira [1, 2, 3, 4]\n```\n\n## 2. `insert()` – Adiciona em posição específica\n```python\nlista = ['a', 'b', 'c']\nlista.insert(1, 'x')     # lista vira ['a', 'x', 'b', 'c']\n```\n\n## 3. `extend()` – Adiciona vários itens\n```python\nlista = [1, 2]\nlista.extend([3, 4, 5])  # lista vira [1, 2, 3, 4, 5]\n```"
}
```

---

### 3. Pergunta sobre tuplas

**Pergunta:**
```bash
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "O que são tuplas e como diferem de listas?"}'
```

**Resposta (resumida):**
```json
{
  "response": "## Tuplas em Python\n\nUma **tupla** é uma coleção ordenada e **imutável** de elementos.\n\n### Diferenças principais:\n\n| Característica | Lista | Tupla |\n|----------------|-------|-------|\n| **Mutabilidade** | Mutável | Imutável |\n| **Sintaxe** | `[1, 2, 3]` | `(1, 2, 3)` |\n| **Métodos** | append, insert, remove, etc. | count, index |\n| **Performance** | Mais lenta | Mais rápida |\n\n### Exemplos:\n```python\n# Criando tuplas\ntupla_vazia = ()\ntupla = (1, 2, 3)\ntupla_unico = (42,)  # vírgula necessária\n\n# Acessando elementos\nprint(tupla[0])  # 1\n\n# Tuplas são imutáveis\ntupla[0] = 10  # TypeError!\n```"
}
```

---

### 4. Pergunta sobre dicionários

**Pergunta:**
```bash
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Como criar e manipular dicionários em Python?"}'
```

**Resposta (resumida):**
```json
{
  "response": "## Dicionários em Python\n\nUm **dicionário** é uma coleção de pares chave-valor.\n\n### Criando dicionários:\n```python\n# Sintaxe com chaves\npessoa = {\"nome\": \"Ana\", \"idade\": 30, \"cidade\": \"São Paulo\"}\n\n# Usando dict()\npessoa = dict(nome=\"Ana\", idade=30)\n\n# Vazio\nd = {}\n```\n\n### Operações comuns:\n```python\n# Acessar valor\nprint(pessoa[\"nome\"])  # Ana\n\n# Adicionar/atualizar\npessoa[\"email\"] = \"ana@email.com\"\npessoa[\"idade\"] = 31\n\n# Remover\ndel pessoa[\"cidade\"]\nemail = pessoa.pop(\"email\")\n\n# Verificar existência\n\"nome\" in pessoa  # True\n```"
}
```

---

### 5. Pergunta sobre loops

**Pergunta:**
```bash
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Como fazer loop em Python? Explique for e while."}'
```

**Resposta (resumida):**
```json
{
  "response": "## Loops em Python\n\n### Loop `for`\nO `for` itera sobre sequências (listas, tuplas, strings, range, etc.):\n\n```python\n# Iterando sobre lista\nfrutas = [\"maçã\", \"banana\", \"laranja\"]\nfor fruta in frutas:\n    print(fruta)\n\n# Usando range\nfor i in range(5):\n    print(i)  # 0, 1, 2, 3, 4\n\n# Com enumerate (índice + valor)\nfor i, fruta in enumerate(frutas):\n    print(f\"{i}: {fruta}\")\n```\n\n### Loop `while`\nExecuta enquanto a condição for verdadeira:\n\n```python\ncontador = 0\nwhile contador < 5:\n    print(contador)\n    contador += 1\n```\n\n### Controlando loops:\n- `break` - sai do loop\n- `continue` - pula para próxima iteração\n- `else` - executa se o loop NÃO foi interrompido por `break`"
}
```

---

### 6. Pergunta fora do escopo (Python)

**Pergunta:**
```bash
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual a capital da França?"}'
```

**Resposta:**
```json
{
  "response": "Desculpe, mas só posso ajudar com questões relacionadas à programação em Python. Se você tiver alguma dúvida sobre Python, estou à disposição!"
}
```

---

### 7. Pergunta sobre funções

**Pergunta:**
```bash
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Como definir uma função em Python com parâmetros padrão?"}'
```

**Resposta (resumida):**
```json
{
  "response": "## Funções em Python\n\n### Sintaxe básica:\n```python\ndef saudacao(nome, saudacao=\"Olá\"):\n    return f\"{saudacao}, {nome}!\"\n\nprint(saudacao(\"Ana\"))           # Olá, Ana!\nprint(saudacao(\"Ana\", \"Oi\"))    # Oi, Ana!\n```\n\n### Parâmetros:\n- **Posicionais**: `def soma(a, b)`\n- **Padrão**: `def soma(a, b=0)`\n- **Nomeados**: `soma(b=2, a=1)`\n- **Variáveis (*args, **kwargs)**\n\n### Type hints (Python 3.5+):\n```python\ndef soma(a: int, b: int) -> int:\n    return a + b\n```"
}
```

---

### 8. Pergunta sobre tratamento de erros

**Pergunta:**
```bash
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Como usar try/except em Python?"}'
```

**Resposta (resumida):**
```json
{
  "response": "## Tratamento de Exceções (try/except)\n\n### Sintaxe básica:\n```python\ntry:\n    resultado = 10 / 0\nexcept ZeroDivisionError:\n    print(\"Não é possível dividir por zero!\")\n```\n\n### Múltiplas exceções:\n```python\ntry:\n    valor = int(input(\"Digite um número: \"))\n    resultado = 10 / valor\nexcept ValueError:\n    print(\"Entrada inválida!\")\nexcept ZeroDivisionError:\n    print(\"Não pode dividir por zero!\")\nexcept Exception as e:\n    print(f\"Erro inesperado: {e}\")\n```\n\n### Else e Finally:\n```python\ntry:\n    arquivo = open(\"dados.txt\")\nexcept FileNotFoundError:\n    print(\"Arquivo não encontrado\")\nelse:\n    conteudo = arquivo.read()\n    arquivo.close()\nfinally:\n    print(\"Operação finalizada\")  # Sempre executa\n```\n\n### Levantando exceções:\n```python\ndef sacar(saldo, valor):\n    if valor > saldo:\n        raise ValueError(\"Saldo insuficiente\")\n    return saldo - valor\n```"
}
```

---

## Testando via Swagger UI

Para testar interativamente:

1. Acesse: **http://localhost:8005/docs**
2. Clique em **POST /api/chat**
3. Clique em **"Try it out"**
4. Insira o JSON (exemplos acima)
5. Clique em **"Execute"**

Exemplo de JSON para testar:
```json
{
  "message": "Como criar uma lista em Python?",
  "session_id": "minha-sessao-teste"
}
```

## Próximas Etapas

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### Testes implementados

| Teste | Descrição |
|-------|-----------|
| `test_health_check` | GET /health retorna 200 |
| `test_chat_valid_message` | POST /api/chat com mensagem válida |
| `test_chat_missing_message` | POST /api/chat sem campo message (422) |
| `test_chat_empty_message` | POST /api/chat com message vazia (422) |
| `test_chat_whitespace_only` | POST /api/chat com apenas espaços (422) |
| `test_process_message_with_mock` | ChatService com mock da LLM |
| `test_process_message_python_question` | ChatService responde pergunta Python |
| `test_process_message_raises_error_without_api_key` | Erro sem API key |

## Integração com LLM (Etapa 2 - Concluída)

O backend agora integra com a LLM da Groq via LangChain.

### Configuração

1. Copie o arquivo de exemplo:
```bash
cp backend/.env.example backend/.env
```

2. Edite `backend/.env` e adicione sua chave da Groq:
```env
GROQ_API_KEY=sua_chave_aqui
GROQ_MODEL=openai/gpt-oss-20b
```

Obtenha sua chave em: https://console.groq.com/keys

### System Prompt

O chatbot assume o papel de assistente especializado em Python:
- Responde em português
- Explica conceitos didaticamente
- Fornece exemplos de código
- Não responde assuntos fora de programação Python

## Observabilidade com LangSmith (Etapa 3 - Concluída)

O backend possui instrumentação com LangSmith para rastreamento de execuções, utilizando o skill **langsmith-trace** do repositório [langchain-ai/langsmith-skills](https://github.com/langchain-ai/langsmith-skills).

### Configuração

Adicione ao `backend/.env`:
```env
LANGSMITH_API_KEY=sua_api_key
LANGSMITH_PROJECT=chatbot-python
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_TRACING=true
```

### Rastreamento Automático (LangChain OSS)

Para aplicações LangChain/LangGraph, o tracing é automático bastando definir as variáveis de ambiente (conforme documentação do langsmith-trace):

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
export GROQ_API_KEY=<your-groq-api-key>  # seu provedor LLM
```

Opcional:
- `LANGSMITH_PROJECT` - especifica o projeto (padrão: "default")
- `LANGCHAIN_CALLBACKS_BACKGROUND=false` - para serverless, garante que traces completem antes da saída da função

O LangSmith rastreia automaticamente (via `@traceable` + variáveis de ambiente):
- Entrada do usuário
- Prompt do sistema
- Chamada à LLM
- Resposta da LLM
- Métricas (tokens, latência, modelo, custo)
- Session ID (quando fornecido)
- Erros

### Funcionamento

- Sem a `LANGSMITH_API_KEY`, o chatbot funciona normalmente (observabilidade desabilitada)
- Com credenciais, cada chamada a `POST /api/chat` gera um trace no LangSmith
- O `session_id` opcional permite correlacionar mensagens da mesma conversa
- Falhas no LangSmith não impedem o funcionamento do chatbot

### Verificando traces

1. Configure a `LANGSMITH_API_KEY` no `.env` (obtenha em https://smith.langchain.com)
2. Faça chamadas a `POST /api/chat`
3. Acesse o painel do LangSmith (https://smith.langchain.com) e localize o trace

### Como testar a integração com LangSmith

#### 1. Obtenha a API Key do LangSmith
- Acesse https://smith.langchain.com
- Faça login/crie conta
- Vá em Settings → API Keys → Create Key
- Copie a chave (formato: `lsv2_pt_xxxxxxxxxxxxx`)

#### 2. Configure o ambiente
```bash
# Na raiz do projeto (chatbot/)
cp backend/.env.example backend/.env
# Edite backend/.env e adicione:
LANGSMITH_API_KEY=lsv2_pt_xxxxxxxxxxxxx
LANGSMITH_PROJECT=chatbot-python
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

#### 3. Reinicie o backend
```bash
docker compose down && docker compose up --build -d
```

#### 4. Faça chamadas de teste
```bash
# Primeira mensagem com session_id
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Como criar uma lista em Python?", "session_id": "teste-sessao-1"}'

# Segunda mensagem na mesma sessão
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "E como adicionar itens?", "session_id": "teste-sessao-1"}'

# Mensagem sem sessão (também gera trace)
curl -X POST http://localhost:8005/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "O que são tuplas?"}'
```

#### 5. Verifique no painel do LangSmith
1. Acesse https://smith.langchain.com
2. Selecione o projeto "chatbot-python"
3. Você verá os traces com:
   - **Nome**: `chat_service`
   - **Inputs**: mensagem do usuário + system prompt
   - **Outputs**: resposta da LLM
   - **Metadata**: `session_id` (quando informado)
   - **LLM calls**: modelo Groq, tokens, latência, custo estimado
   - **Erros**: se houver falhas na chamada

#### 6. Execute os testes (devem passar sem LangSmith)
```bash
docker compose exec backend pytest tests/ -v
```

### Consultando traces via CLI (langsmith-cli)

O skill `langsmith-trace` também fornece o CLI `langsmith` para consultar e exportar traces:

```bash
# Instalar o CLI
curl -sSL https://raw.githubusercontent.com/langchain-ai/langsmith-cli/main/scripts/install.sh | sh

# Listar traces recentes
langsmith trace list --limit 10 --project chatbot-python --api-key $LANGSMITH_API_KEY

# Listar traces com metadados (tokens, latência, custo)
langsmith trace list --limit 10 --include-metadata --api-key $LANGSMITH_API_KEY

# Filtrar traces com erro
langsmith trace list --error --last-n-minutes 60 --api-key $LANGSMITH_API_KEY

# Obter trace específico com hierarquia completa
langsmith trace get <trace-id> --api-key $LANGSMITH_API_KEY

# Exportar traces para JSONL (um arquivo por trace)
langsmith trace export ./traces --limit 20 --full --api-key $LANGSMITH_API_KEY

# Filtrar traces lentos (>= 5s)
langsmith trace list --min-latency 5.0 --limit 10 --api-key $LANGSMITH_API_KEY

# Listar runs específicos (ex: apenas LLM calls)
langsmith run list --run-type llm --limit 20 --api-key $LANGSMITH_API_KEY
```

**Diferença importante (do langsmith-trace):**
- **Trace** = árvore completa de execução (root run + todos os child runs) - use primeiro
- **Run** = nó individual na árvore (uma chamada LLM, tool call, etc.)

**Observações importantes:**
- Sem `LANGSMITH_API_KEY`: chatbot funciona normalmente, observabilidade desabilitada
- Com `LANGSMITH_API_KEY`: tracing automático via decorador `@traceable`
- `session_id` opcional permite correlacionar conversas multi-turno
- Falhas no LangSmith não quebram o chatbot (fail-safe)

## Próximas Etapas

1. Memória de conversação
2. Frontend