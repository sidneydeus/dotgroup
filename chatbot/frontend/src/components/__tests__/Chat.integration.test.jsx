import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { http, HttpResponse } from 'msw'
import { server } from '../../test/msw/node'
import Chat from '../Chat'

const API_URL = 'http://localhost:8004'

const successHandler = http.post(`${API_URL}/api/chat`, async ({ request }) => {
  const body = await request.json()
  const message = body.message

  if (!message || !message.trim()) {
    return HttpResponse.json(
      { detail: 'Message cannot be empty' },
      { status: 422 }
    )
  }

  await new Promise(resolve => setTimeout(resolve, 50))

  return HttpResponse.json({
    response: `Resposta da IA para: "${message}"`,
  })
})

const errorHandler = http.post(`${API_URL}/api/chat`, () => {
  return HttpResponse.json(
    { detail: 'Internal Server Error' },
    { status: 500 }
  )
})

const networkErrorHandler = http.post(`${API_URL}/api/chat`, () => {
  return HttpResponse.error()
})

describe('Chat - Integração', () => {
  beforeEach(() => {
    server.use(successHandler)
  })

  test('renderiza mensagem inicial do assistente', () => {
    render(<Chat />)

    expect(screen.getByText(/Olá! Sou seu assistente de programação Python/i)).toBeInTheDocument()
    expect(screen.getByText(/Faça uma pergunta sobre Python/i)).toBeInTheDocument()
  })

  test('envia mensagem via botão e mostra resposta', async () => {
    const user = userEvent.setup()
    render(<Chat />)

    const input = screen.getByPlaceholderText(/Digite sua pergunta/i)
    const button = screen.getByRole('button', { name: /Enviar/i })

    await user.type(input, 'Como criar uma lista?')
    await user.click(button)

    await waitFor(() => {
      expect(screen.getByText(/IA está digitando/i)).toBeInTheDocument()
    })

    await waitFor(() => {
      expect(screen.getByText((content) => content.includes('Resposta da IA para: "Como criar uma lista?"'))).toBeInTheDocument()
    })

    expect(screen.getByText((content) => content === 'Como criar uma lista?')).toBeInTheDocument()
  })

  test('envia mensagem via Enter e mostra resposta', async () => {
    const user = userEvent.setup()
    render(<Chat />)

    const input = screen.getByPlaceholderText(/Digite sua pergunta/i)

    await user.type(input, 'Como adicionar um elemento?')
    await user.keyboard('{Enter}')

    await waitFor(() => {
      expect(screen.getByText(/IA está digitando/i)).toBeInTheDocument()
    })

    await waitFor(() => {
      expect(screen.getByText((content) => content.includes('Resposta da IA para: "Como adicionar um elemento?"'))).toBeInTheDocument()
    })
  })

  test('não envia mensagem vazia', async () => {
    const user = userEvent.setup()
    render(<Chat />)

    const button = screen.getByRole('button', { name: /Enviar/i })

    expect(button).toBeDisabled()

    await user.type(screen.getByPlaceholderText(/Digite sua pergunta/i), '   ')
    await user.click(button)

    expect(screen.queryByText(/IA está digitando/i)).not.toBeInTheDocument()
  })

  test('desabilita botão durante carregamento', async () => {
    const user = userEvent.setup()
    render(<Chat />)

    const input = screen.getByPlaceholderText(/Digite sua pergunta/i)
    const button = screen.getByRole('button', { name: /Enviar/i })

    await user.type(input, 'Teste')
    await user.click(button)

    await waitFor(() => {
      expect(button).toBeDisabled()
      expect(screen.getByText(/Enviando.../i)).toBeInTheDocument()
    })
  })

  test('mostra erro quando API retorna 500', async () => {
    server.use(errorHandler)

    const user = userEvent.setup()
    render(<Chat />)

    const input = screen.getByPlaceholderText(/Digite sua pergunta/i)
    const button = screen.getByRole('button', { name: /Enviar/i })

    await user.type(input, 'Teste erro')
    await user.click(button)

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/Ocorreu um erro no servidor. Tente novamente./i)
    })
  })

  test('mostra erro quando rede falha', async () => {
    server.use(networkErrorHandler)

    const user = userEvent.setup()
    render(<Chat />)

    const input = screen.getByPlaceholderText(/Digite sua pergunta/i)
    const button = screen.getByRole('button', { name: /Enviar/i })

    await user.type(input, 'Teste rede')
    await user.click(button)

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/Failed to fetch/i)
    })
  })

  test('mantém histórico de mensagens', async () => {
    const user = userEvent.setup()
    render(<Chat />)

    const input = screen.getByPlaceholderText(/Digite sua pergunta/i)
    const button = screen.getByRole('button', { name: /Enviar/i })

    await user.type(input, 'Primeira pergunta')
    await user.click(button)

    await waitFor(() => {
      expect(screen.getByText((content) => content.includes('Resposta da IA para: "Primeira pergunta"'))).toBeInTheDocument()
    })

    await user.type(input, 'Segunda pergunta')
    await user.click(button)

    await waitFor(() => {
      expect(screen.getByText((content) => content.includes('Resposta da IA para: "Segunda pergunta"'))).toBeInTheDocument()
    })

    const userMessages = screen.getAllByText((content) => content === 'Primeira pergunta' || content === 'Segunda pergunta')
    expect(userMessages).toHaveLength(2)
  })

  test('limpa input após envio', async () => {
    const user = userEvent.setup()
    render(<Chat />)

    const input = screen.getByPlaceholderText(/Digite sua pergunta/i)
    const button = screen.getByRole('button', { name: /Enviar/i })

    await user.type(input, 'Teste limpar')
    await user.click(button)

    await waitFor(() => {
      expect(input).toHaveValue('')
    })
  })
})