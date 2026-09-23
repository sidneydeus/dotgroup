import '@testing-library/jest-dom'
import { server } from './msw/node'

vi.stubEnv('VITE_API_URL', 'http://localhost:8004')

Element.prototype.scrollIntoView = vi.fn()

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())