# Etapa 5 — Implementação do Frontend com React

## Objetivo

Criar uma interface web para o chatbot de programação Python
utilizando React.

O frontend deverá consumir a API existente do backend FastAPI.

O usuário deverá conseguir:

1. visualizar a conversa;
2. digitar uma pergunta;
3. enviar a pergunta;
4. visualizar a resposta da IA;
5. continuar a conversa.

Nesta etapa não modificar a implementação da LLM, LangChain ou
LangSmith.

---

# 1. Pré-requisitos

O backend FastAPI deve estar funcionando.

O endpoint principal é:

```http
POST /api/chat
```

Request:

```json
{
  "message": "Como criar uma lista em Python?"
}
```

Response:

```json
{
  "response": "Uma lista em Python pode ser criada usando..."
}
```

Também deve existir:

```http
GET /health
```

Antes de iniciar o frontend:

1. iniciar o backend;
2. verificar `/health`;
3. testar `/api/chat`;
4. confirmar que a API retorna respostas corretamente.

---

# 2. Tecnologia

Utilizar:

* React
* Vite
* JavaScript
* CSS

Não utilizar TypeScript nesta etapa.

Não utilizar bibliotecas adicionais de UI sem necessidade.

O objetivo é criar uma aplicação React simples, organizada e
fácil de compreender.

---

# 3. Criação do projeto

Criar o frontend utilizando Vite.

O projeto deverá ser independente do backend.

Estrutura inicial:

```text
frontend/
├── public/
├── src/
│   ├── components/
│   ├── services/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
├── vite.config.js
└── .gitignore
```

Utilizar o gerenciador de pacotes já adotado pelo ambiente.

---

# 4. Estrutura de componentes

Organizar a interface em componentes.

Estrutura sugerida:

```text
src/
├── components/
│   ├── Chat.jsx
│   ├── MessageList.jsx
│   ├── Message.jsx
│   ├── ChatInput.jsx
│   └── Loading.jsx
│
├── services/
│   └── api.js
│
├── App.jsx
├── main.jsx
└── index.css
```

### Responsabilidade dos componentes

#### App

Componente principal da aplicação.

Responsável por montar a interface do chatbot.

---

#### Chat

Responsável pelo estado principal da conversa.

Deve controlar, quando necessário:

* mensagens;
* estado de carregamento;
* erros.

---

#### MessageList

Responsável por renderizar a lista de mensagens.

---

#### Message

Responsável por renderizar uma mensagem individual.

Deve diferenciar:

* mensagem do usuário;
* mensagem da IA.

---

#### ChatInput

Responsável por:

* campo de texto;
* botão enviar;
* envio através do Enter;
* validação de mensagem vazia.

---

#### Loading

Responsável pelo indicador visual enquanto a IA está
processando uma resposta.

---

# 5. Estado da aplicação

Utilizar os recursos nativos do React para gerenciamento de estado.

O estado mínimo deverá contemplar:

```javascript
messages
loading
error
input
```

Exemplo conceitual:

```javascript
const [messages, setMessages] = useState([]);
const [input, setInput] = useState("");
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
```

Não utilizar Redux ou outro gerenciador de estado global.

O estado necessário para esta aplicação é pequeno e pode ser
gerenciado pelo próprio React.

---

# 6. Modelo de mensagem

Utilizar uma estrutura consistente para as mensagens.

Exemplo:

```javascript
{
  id: 1,
  role: "user",
  content: "Como criar uma lista em Python?"
}
```

Resposta da IA:

```javascript
{
  id: 2,
  role: "assistant",
  content: "Uma lista em Python pode ser criada..."
}
```

Utilizar `id` estável para a propriedade `key` durante a
renderização das mensagens.

Não utilizar o índice do array como `key` quando houver uma
alternativa adequada.

---

# 7. Serviço de API

A comunicação com o backend deve ficar isolada em:

```text
src/services/api.js
```

Não realizar chamadas `fetch()` diretamente em vários
componentes.

Criar uma função responsável pelo envio da mensagem.

Exemplo conceitual:

```javascript
async function sendMessage(message) {
    // chamada para o backend
}
```

A função deverá:

1. enviar a mensagem;
2. verificar o status HTTP;
3. interpretar o JSON;
4. retornar a resposta;
5. lançar um erro quando a API não responder corretamente.

---

# 8. URL da API

Não espalhar a URL do backend pelo código.

Utilizar variável de ambiente do Vite.

Criar:

```text
.env
```

com:

```env
VITE_API_URL=http://localhost:8000
```

Criar também:

```text
.env.example
```

com:

```env
VITE_API_URL=http://localhost:8000
```

No código utilizar:

```javascript
const API_URL = import.meta.env.VITE_API_URL;
```

A chamada deverá ser:

```javascript
fetch(`${API_URL}/api/chat`, ...)
```

O arquivo `.env` não deve ser versionado.

---

# 9. Comunicação com o backend

A requisição deverá utilizar:

```http
POST /api/chat
Content-Type: application/json
```

Body:

```json
{
  "message": "Pergunta do usuário"
}
```

A resposta esperada:

```json
{
  "response": "Resposta da IA"
}
```

O frontend deve extrair o campo:

```text
response
```

e adicioná-lo ao histórico.

---

# 10. Fluxo de envio

O fluxo deverá ser:

```text
Usuário digita pergunta
        ↓
Validar mensagem
        ↓
Adicionar mensagem do usuário
        ↓
Limpar input
        ↓
setLoading(true)
        ↓
POST /api/chat
        ↓
Receber resposta
        ↓
Adicionar mensagem da IA
        ↓
setLoading(false)
```

Se ocorrer erro:

```text
POST /api/chat
        ↓
ERRO
        ↓
setLoading(false)
        ↓
Mostrar mensagem de erro
```

---

# 11. Validação

Não permitir o envio de mensagens vazias.

Por exemplo:

```javascript
if (!input.trim()) {
    return;
}
```

O botão de envio também deve ficar desabilitado enquanto
`loading === true`.

Isso evita múltiplas requisições simultâneas.

---

# 12. Envio através do teclado

O usuário deve conseguir enviar a pergunta pressionando:

```text
Enter
```

No componente `ChatInput`, tratar o evento de teclado.

Não utilizar Enter para enviar quando o campo estiver
intencionalmente configurado como textarea multilinha.

Para uma primeira versão simples, um campo de texto de uma
linha pode utilizar Enter para envio.

---

# 13. Estado de carregamento

Enquanto a API estiver processando a pergunta, mostrar um
indicador:

```text
IA está digitando...
```

ou uma animação equivalente.

Durante o carregamento:

* desabilitar o botão;
* impedir novo envio;
* manter o input em estado apropriado;
* informar visualmente que a resposta está sendo processada.

Após a resposta:

```javascript
setLoading(false);
```

---

# 14. Mensagem inicial

Ao abrir a aplicação, apresentar:

```text
Olá! Sou seu assistente de programação Python.

Faça uma pergunta sobre Python e tentarei explicar
o conceito de forma didática.
```

Essa mensagem pode ser criada inicialmente no estado do React.

Não enviar essa mensagem para o backend.

---

# 15. Interface

Criar uma interface de chat limpa e responsiva.

Estrutura:

```text
┌──────────────────────────────────────────────┐
│ Python AI Assistant                          │
│ Assistente de programação Python             │
├──────────────────────────────────────────────┤
│                                              │
│ 🤖 Olá! Como posso ajudar?                   │
│                                              │
│                 Como criar uma lista? 👤     │
│                                              │
│ 🤖 Uma lista em Python pode ser criada...    │
│                                              │
│                                              │
├──────────────────────────────────────────────┤
│ Digite sua pergunta...              [Enviar] │
└──────────────────────────────────────────────┘
```

Utilizar CSS próprio.

Não é necessário utilizar Bootstrap, Tailwind ou outra
biblioteca visual.

---

# 16. Mensagens

As mensagens devem possuir estilos diferentes conforme o papel.

### Usuário

Alinhar visualmente à direita.

### Assistente

Alinhar visualmente à esquerda.

Exemplo:

```text
Usuário:
Como criar uma lista?
```

```text
Assistente:
Você pode criar uma lista utilizando colchetes:
```

O objetivo é tornar a conversa visualmente fácil de acompanhar.

---

# 17. Histórico

O histórico deve permanecer disponível enquanto a aplicação
estiver aberta.

Exemplo:

```text
Usuário:
Como criar uma lista?

IA:
Você pode utilizar colchetes.

Usuário:
Como adicionar um item?

IA:
Utilize o método append().
```

Nesta etapa não persistir o histórico.

Não utilizar:

* banco de dados;
* localStorage;
* cookies;
* autenticação.

O histórico ficará apenas no estado do React.

---

# 18. Memória da LLM

O frontend não deve implementar memória da LLM.

Se o backend possuir memória ou sessão, o frontend deverá
utilizar a interface fornecida pela API.

Não duplicar no React nenhuma lógica responsável por contexto
da conversa.

---

# 19. Formatação de respostas

A resposta da IA poderá conter:

* texto;
* listas;
* código Python;
* explicações.

O frontend deve apresentar o conteúdo de forma legível.

Se a API retornar Markdown, utilizar uma biblioteca apropriada
para renderização segura de Markdown somente se necessário.

Qualquer HTML retornado pela LLM deve ser tratado como conteúdo
não confiável.

Não utilizar:

```javascript
element.innerHTML = response;
```

para inserir diretamente conteúdo recebido da API.

Evitar permitir execução de HTML ou JavaScript retornado pela LLM.

---

# 20. Código Python

Respostas contendo código Python devem possuir apresentação
diferenciada.

Exemplo:

```python
numeros = [1, 2, 3, 4]

for numero in numeros:
    print(numero)
```

O código deve ser legível.

Se for implementado botão de copiar código, ele deve copiar
somente o conteúdo do bloco correspondente.

Essa funcionalidade é opcional.

---

# 21. Scroll da conversa

Quando uma nova mensagem for adicionada, a área da conversa
deve acompanhar a mensagem mais recente.

Exemplo:

```text
mensagem
mensagem
mensagem
mensagem  ← última mensagem visível
```

Evitar que o usuário precise rolar manualmente até o final
a cada resposta.

---

# 22. Tratamento de erros

Implementar tratamento para:

### Backend indisponível

Mostrar:

```text
Não foi possível conectar ao servidor.
Verifique se o backend está em execução.
```

### HTTP 4xx

Mostrar uma mensagem apropriada.

### HTTP 5xx

Mostrar:

```text
Ocorreu um erro no servidor. Tente novamente.
```

### Erro de rede

Mostrar:

```text
Não foi possível realizar a comunicação com o servidor.
```

Não mostrar stack traces ou informações internas.

---

# 23. Segurança

O frontend nunca deve possuir:

```text
OPENAI_API_KEY
LANGSMITH_API_KEY
LANGSMITH_API_SECRET
```

Nem qualquer outra credencial do backend.

O frontend deve conversar somente com o FastAPI:

```text
React
  ↓
FastAPI
  ↓
LangChain
  ↓
OpenAI
```

O LangSmith permanece exclusivamente no backend para
observabilidade.

---

# 24. CORS

O backend FastAPI deve permitir a origem do frontend.

Durante desenvolvimento, considerando o Vite, normalmente:

```text
http://localhost:5173
```

deve ser permitido pelo backend.

Não configurar CORS com:

```python
allow_origins=["*"]
```

sem necessidade.

---

# 25. Acessibilidade

Utilizar HTML semântico.

Garantir:

* navegação por teclado;
* foco visível;
* botão acessível;
* label ou `aria-label` no campo de entrada;
* contraste adequado;
* mensagens não dependentes apenas de cores.

O usuário deve conseguir utilizar o chatbot sem depender
exclusivamente do mouse.

---

# 26. Responsividade

A interface deve funcionar em:

* desktop;
* tablet;
* celular.

Em telas pequenas:

* reduzir margens;
* permitir que mensagens ocupem mais largura;
* manter o campo de entrada acessível;
* evitar overflow horizontal.

---

# 27. Testes manuais

## Teste 1 — Inicialização

Abrir o frontend.

Confirmar que a interface é exibida.

---

## Teste 2 — Pergunta

Enviar:

```text
Como criar uma lista em Python?
```

Confirmar:

* mensagem do usuário aparece;
* indicador de carregamento aparece;
* resposta da IA aparece.

---

## Teste 3 — Conversa

Enviar:

```text
Como adicionar um elemento?
```

Confirmar que a nova mensagem aparece abaixo da anterior.

---

## Teste 4 — Campo vazio

Tentar enviar:

```text
"   "
```

Confirmar que nenhuma requisição é realizada.

---

## Teste 5 — Enter

Digite uma pergunta e pressione Enter.

Confirmar que a mensagem é enviada.

---

## Teste 6 — Múltiplos envios

Enviar várias perguntas.

Confirmar que o histórico permanece correto.

---

## Teste 7 — Backend desligado

Parar o FastAPI.

Tentar enviar uma pergunta.

Confirmar que o frontend apresenta uma mensagem amigável.

---

## Teste 8 — Código Python

Enviar:

```text
Mostre um exemplo de list comprehension em Python.
```

Confirmar que o código retornado aparece de forma legível.

---

## Teste 9 — Responsividade

Testar em diferentes larguras de tela.

Confirmar que não existe overflow horizontal e que o campo
de entrada permanece utilizável.

---

# 28. Critérios de aceitação

A etapa estará concluída quando:

* [ ] Projeto React criado com Vite.
* [ ] Aplicação inicia corretamente.
* [ ] Interface do chatbot é exibida.
* [ ] Usuário consegue digitar uma pergunta.
* [ ] Usuário consegue enviar pelo botão.
* [ ] Usuário consegue enviar através do Enter.
* [ ] Frontend utiliza `POST /api/chat`.
* [ ] Resposta da IA aparece na conversa.
* [ ] Usuário e IA possuem estilos diferentes.
* [ ] Estado de carregamento funciona.
* [ ] Botão é desabilitado durante a requisição.
* [ ] Mensagens vazias não são enviadas.
* [ ] Erros de comunicação são tratados.
* [ ] Histórico permanece durante a sessão.
* [ ] Interface é responsiva.
* [ ] Código Python é apresentado de forma legível.
* [ ] Nenhuma credencial está presente no frontend.
* [ ] CORS funciona corretamente.
* [ ] Backend não precisou ser alterado além da configuração
  necessária para permitir o frontend.

---

# 29. Execução

Durante o desenvolvimento:

Backend:

```bash
uvicorn app.main:app --reload
```

Frontend:

```bash
npm run dev
```

O frontend deverá estar disponível no endereço fornecido
pelo Vite, normalmente:

```text
http://localhost:5173
```

O backend normalmente estará em:

```text
http://localhost:8000
```

---

# 30. Restrições

Não implementar nesta etapa:

* autenticação;
* cadastro de usuários;
* banco de dados;
* RAG;
* embeddings;
* upload de arquivos;
* WebSocket;
* streaming de resposta;
* painel administrativo;
* avaliação automática;
* chamadas diretas à OpenAI;
* chamadas diretas ao LangSmith;
* Redux;
* sistema complexo de gerenciamento de estado.

O frontend deve permanecer simples e concentrado na experiência
de conversação.

---

# 31. Resultado esperado

Ao final desta etapa, o projeto deverá possuir:

```text
chatbot-python/
│
├── backend/
│   └── FastAPI
│
└── frontend/
    ├── React
    ├── Vite
    ├── components/
    └── services/
```

O fluxo completo será:

```text
┌──────────────┐
│    React     │
│   Frontend   │
└──────┬───────┘
       │
       │ POST /api/chat
       ▼
┌──────────────┐
│   FastAPI    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   LangChain  │
└──────┬───────┘
       │
       ├──────────────► OpenAI
       │
       └──────────────► LangSmith
                         Observabilidade
```

Responsabilidades:

* **React:** interface e estado visual da conversa.
* **FastAPI:** API HTTP.
* **LangChain:** orquestração da interação com a LLM.
* **OpenAI:** geração da resposta.
* **LangSmith:** observabilidade e tracing.

O frontend não deve conter lógica relacionada à integração
com a LLM.
