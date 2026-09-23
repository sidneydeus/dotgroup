import { useState, useCallback } from 'react';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import Loading from './Loading';
import { sendMessage } from '../services/api';

function Chat() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Olá! Sou seu assistente de programação Python.\n\nFaça uma pergunta sobre Python e tentarei explicar o conceito de forma didática.',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  let messageId = 2;

  const handleSend = useCallback(async () => {
    if (!input.trim() || loading) return;

    const userMessage = {
      id: messageId++,
      role: 'user',
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const response = await sendMessage(userMessage.content);
      const assistantMessage = {
        id: messageId++,
        role: 'assistant',
        content: response,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err.message);
      const errorMessage = {
        id: messageId++,
        role: 'assistant',
        content: `Erro: ${err.message}`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  }, [input, loading]);

  return (
    <div className="chat">
      <header className="chat-header">
        <h1>Python AI Assistant</h1>
        <p>Assistente de programação Python</p>
      </header>
      <MessageList messages={messages} />
      {loading && <Loading />}
      {error && <div className="error-message" role="alert">{error}</div>}
      <ChatInput
        onSend={handleSend}
        input={input}
        setInput={setInput}
        loading={loading}
      />
    </div>
  );
}

export default Chat;