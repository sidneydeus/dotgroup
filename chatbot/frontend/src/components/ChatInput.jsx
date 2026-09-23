function ChatInput({ onSend, input, setInput, loading }) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!loading && input.trim()) {
        onSend();
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!loading && input.trim()) {
      onSend();
    }
  };

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <label htmlFor="message-input" className="visually-hidden">
        Digite sua pergunta
      </label>
      <input
        id="message-input"
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Digite sua pergunta..."
        disabled={loading}
        aria-label="Digite sua pergunta"
        aria-disabled={loading}
      />
      <button
        type="submit"
        disabled={loading || !input.trim()}
        aria-label={loading ? 'Enviando...' : 'Enviar pergunta'}
      >
        {loading ? 'Enviando...' : 'Enviar'}
      </button>
    </form>
  );
}

export default ChatInput;