import { http, HttpResponse } from 'msw'

const API_URL = 'http://localhost:8004'

export const handlers = [
  http.post(`${API_URL}/api/chat`, async ({ request }) => {
    const body = await request.json()
    const message = body.message

    if (!message || !message.trim()) {
      return HttpResponse.json(
        { detail: 'Message cannot be empty' },
        { status: 422 }
      )
    }

    await new Promise(resolve => setTimeout(resolve, 100))

    return HttpResponse.json({
      response: `Resposta simulada para: "${message}"`,
    })
  }),
]

export const errorHandlers = [
  http.post(`${API_URL}/api/chat`, () => {
    return HttpResponse.json(
      { detail: 'Internal Server Error' },
      { status: 500 }
    )
  }),
]

export const networkErrorHandlers = [
  http.post(`${API_URL}/api/chat`, () => {
    return HttpResponse.error()
  }),
]