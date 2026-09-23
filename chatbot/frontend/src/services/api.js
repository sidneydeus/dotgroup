const API_URL = import.meta.env.VITE_API_URL;

async function sendMessage(message) {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    if (response.status >= 500) {
      throw new Error('Ocorreu um erro no servidor. Tente novamente.');
    }
    if (response.status >= 400) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Erro na requisição. Verifique a mensagem.');
    }
    throw new Error('Não foi possível conectar ao servidor. Verifique se o backend está em execução.');
  }

  const data = await response.json();
  return data.response;
}

export { sendMessage };