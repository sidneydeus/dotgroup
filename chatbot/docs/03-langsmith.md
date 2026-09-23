# Implementação do LangSmith

## Objetivo

Adicionar observabilidade ao chatbot através do LangSmith.

O chatbot já possui:

* Backend em FastAPI
* Serviço de chat
* Integração com LangChain
* Integração com GroqAi

Nesta etapa, o objetivo é instrumentar a aplicação para que as
execuções do chatbot possam ser observadas no LangSmith.

---

# 1. Pré-requisitos

Antes de iniciar a implementação:

1. Verificar se o backend está funcionando.
2. Verificar se `POST /api/chat` está funcionando.
3. Verificar se a integração com a LLM está funcionando.
4. Executar os testes existentes.
5. Não alterar o contrato da API.

A implementação do LangSmith deve ser incremental.

Não refatorar partes não relacionadas ao objetivo desta etapa.

---

# 2. Dependências

Adicionar as dependências necessárias ao projeto.

Utilizar:

* LangSmith
* integração oficial/atual do LangSmith com LangChain, quando necessária

Antes de implementar, verificar a versão atualmente instalada do LangChain e utilizar a API compatível com essa versão.

Evitar utilizar APIs depreciadas.

Atualizar `requirements.txt`.

---

# 3. Configuração de ambiente

Adicionar as seguintes variáveis ao `.env`:

```env
LangSmith_PUBLIC_KEY=
LangSmith_SECRET_KEY=
LangSmith_HOST=
```

O `LangSmith_HOST` deve apontar para a instância utilizada.

Não considerar ambiente de nuvem, somente local.

Não inserir valores reais no código.

---

# 4. Arquivo `.env.example`

Atualizar o `.env.example`:

```env
LangSmith_PUBLIC_KEY=
LangSmith_SECRET_KEY=
LangSmith_HOST=
```

Não adicionar credenciais reais.

---

# 5. Segurança

Garantir que `.env` esteja no `.gitignore`.

Nunca:

* colocar `LangSmith_SECRET_KEY` no código;
* colocar `GROQAI_API_KEY` no código;
* imprimir secrets no terminal;
* retornar secrets através da API;
* registrar secrets nos traces.

Verificar também se logs da aplicação não estão expondo variáveis de ambiente.

---

# 6. Configuração da aplicação

Criar ou utilizar uma camada de configuração da aplicação.

A configuração deve centralizar as variáveis de ambiente.

Exemplo conceitual:

```text
app/
├── config/
│   └── settings.py
```

A configuração deve permitir acessar:

```text
LangSmith_PUBLIC_KEY
LangSmith_SECRET_KEY
LangSmith_HOST
```

Evitar acessar `os.getenv()` diretamente em vários arquivos.

---

# 7. Integração com LangChain

Instrumentar a execução existente do LangChain utilizando a integração recomendada pelo LangSmith para a versão utilizada.

O fluxo deve permanecer:

```text
POST /api/chat
       ↓
FastAPI
       ↓
ChatService
       ↓
LangChain
       ↓
GroqAI
       ↓
LangChain
       ↓
ChatService
       ↓
Response
```

O LangSmith deve observar esse fluxo sem assumir responsabilidade pela lógica de negócio.

---

# 8. Tracing

Cada chamada ao endpoint:

```http
POST /api/chat
```

deve produzir uma execução observável no LangSmith.

O trace deve permitir identificar, quando suportado pela integração utilizada:

```text
Trace
 ├── entrada do usuário
 ├── execução do chatbot
 ├── prompt
 ├── chamada da LLM
 ├── resposta da LLM
 └── métricas
```

Não criar manualmente uma estrutura de tracing complexa se a integração LangChain + LangSmith já fornecer essas informações automaticamente.

Primeiro utilizar a integração nativa.

---

# 9. Sessão da conversa

O chatbot possui conceito de conversa/sessão.

Quando existir um identificador de sessão, utilizar esse identificador para permitir que diferentes mensagens da mesma conversa sejam correlacionadas no LangSmith.

Exemplo conceitual:

```text
session_id = abc123
```

As interações:

```text
"Como criar uma lista?"
"Como adicionar um item?"
"E como remover?"
```

devem poder ser associadas à mesma sessão quando a arquitetura do chatbot fornecer esse identificador.

Não criar banco de dados nesta etapa.

---

# 10. Usuário

Se o sistema possuir identificação de usuário, utilizar essa
informação somente quando apropriado.

Não enviar para o LangSmith informações pessoais desnecessárias.

Caso o chatbot seja anônimo nesta etapa, não criar artificialmente
um sistema de identificação de usuários.

---

# 11. Prompt

O prompt utilizado pelo chatbot deve aparecer na observabilidade
quando possível.

O sistema possui um prompt responsável por orientar a LLM como
assistente especializado em programação Python.

Exemplo conceitual:

```text
Você é um assistente especializado em programação Python.
Responda em português.
Explique os conceitos de forma didática.
Utilize exemplos de código quando apropriado.
Não responda sobre assuntos fora do contexto de programação Python.
```

Não é necessário implementar neste momento um sistema avançado
de gerenciamento de prompts.

O objetivo inicial é conseguir observar o prompt utilizado
durante uma execução.

---

# 12. Métricas

Verificar se o LangSmith está recebendo as métricas disponibilizadas
pela integração e pelo provedor da LLM.

Quando disponíveis, devem ser observáveis:

* tokens de entrada;
* tokens de saída;
* tokens totais;
* latência;
* modelo utilizado;
* custo estimado.

Não implementar cálculo manual de custo nesta etapa se o LangSmith
já fornecer essa informação.

---

# 13. Erros

Quando ocorrer uma exceção durante a execução da LLM, a execução
deve ser registrada no LangSmith quando suportado pela integração.

Exemplo:

```text
Usuário
   ↓
FastAPI
   ↓
LangChain
   ↓
GroqAI
   ↓
ERRO
```

O erro deve ser observável no LangSmith.

A API deve continuar retornando uma resposta HTTP apropriada
para o cliente.

Não retornar informações internas ou secrets.

---

# 14. Falha do LangSmith

A observabilidade não deve impedir o funcionamento principal
do chatbot.

O fluxo principal continua sendo:

```text
Usuário
   ↓
FastAPI
   ↓
LangChain
   ↓
GroqAI
   ↓
Resposta
```

O LangSmith é uma camada de observabilidade.

Uma falha no envio de telemetria não deve causar falha na
resposta do chatbot, desde que isso seja compatível com a
integração utilizada.

---

# 15. Testes

Os testes unitários não devem depender do LangSmith.

Utilizar mocks para chamadas externas.

Os testes devem continuar funcionando mesmo sem:

```text
LangSmith_PUBLIC_KEY
LangSmith_SECRET_KEY
```

quando a configuração permitir execução sem observabilidade.

Criar pelo menos os seguintes testes:

### Teste 1

Verificar que o serviço de chat continua funcionando.

### Teste 2

Verificar que uma chamada para:

```http
POST /api/chat
```

continua retornando uma resposta válida.

### Teste 3

Verificar comportamento quando a LLM retorna erro.

### Teste 4

Verificar que a configuração do LangSmith não expõe credenciais.

---

# 16. Teste manual

Depois da implementação:

## Passo 1

Iniciar o backend:

```bash
uvicorn app.main:app --reload
```

## Passo 2

Abrir:

```text
http://localhost:8000/docs
```

## Passo 3

Executar:

```http
POST /api/chat
```

com:

```json
{
    "message": "Como criar uma lista em Python?"
}
```

## Passo 4

Confirmar que a LLM respondeu.

## Passo 5

Abrir o painel do LangSmith.

## Passo 6

Localizar o trace correspondente à execução.

## Passo 7

Verificar:

* trace;
* entrada;
* saída;
* modelo;
* prompt;
* latência;
* tokens, quando disponíveis;
* custo, quando disponível;
* eventuais erros.

---

# 17. Critérios de aceitação

A implementação será considerada concluída quando:

* [ ] LangSmith estiver instalado.
* [ ] Variáveis de ambiente estiverem configuradas.
* [ ] `.env` estiver protegido pelo `.gitignore`.
* [ ] O chatbot continuar funcionando.
* [ ] `POST /api/chat` continuar funcionando.
* [ ] Uma execução gerar um trace no LangSmith.
* [ ] A chamada da LLM puder ser identificada.
* [ ] Prompt e resposta puderem ser observados.
* [ ] Modelo utilizado puder ser identificado.
* [ ] Métricas disponíveis puderem ser observadas.
* [ ] Erros puderem ser identificados.
* [ ] Nenhum secret aparecer nos traces.
* [ ] Testes automatizados continuarem passando.

---

# 18. Limitações desta etapa

Não implementar ainda:

* RAG;
* embeddings;
* banco vetorial;
* avaliação automática das respostas;
* agentes;
* ferramentas externas;
* frontend;
* autenticação;
* persistência de histórico;
* dashboard próprio;
* sistema complexo de gerenciamento de prompts.

O objetivo desta etapa é exclusivamente implementar
observabilidade com LangSmith.

---

# 19. Regra para implementação

Antes de escrever código:

1. Inspecionar a estrutura atual do projeto.
2. Identificar a versão do LangChain instalada.
3. Identificar como a LLM está sendo instanciada.
4. Verificar a API atual do LangSmith compatível com essas versões.
5. Escolher a integração recomendada.
6. Implementar a menor alteração necessária.
7. Executar os testes.
8. Fazer uma chamada real à API.
9. Confirmar o trace no LangSmith.
10. Somente então considerar a etapa concluída.

Não substituir componentes existentes sem necessidade.

Não atualizar versões de dependências não relacionadas
ao objetivo desta etapa.
