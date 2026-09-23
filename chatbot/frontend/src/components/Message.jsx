function Message({ message }) {
  const isUser = message.role === 'user';
  return (
    <div className={`message ${isUser ? 'message-user' : 'message-assistant'}`}>
      <div className="message-content">
        <div className="message-bubble">
          <div className="message-text">
            {formatMessage(message.content)}
          </div>
        </div>
      </div>
    </div>
  );
}

function formatMessage(content) {
  const lines = content.split('\n');
  const formatted = [];
  let inCodeBlock = false;
  let codeLanguage = '';
  let codeContent = [];

  for (const line of lines) {
    if (line.startsWith('```')) {
      if (!inCodeBlock) {
        inCodeBlock = true;
        codeLanguage = line.slice(3).trim() || 'text';
        codeContent = [];
      } else {
        inCodeBlock = false;
        formatted.push(
          <pre key={`code-${formatted.length}`} className="code-block">
            <code className={`language-${codeLanguage}`}>
              {codeContent.join('\n')}
            </code>
          </pre>
        );
      }
    } else if (inCodeBlock) {
      codeContent.push(line);
    } else {
      formatted.push(<div key={`line-${formatted.length}`}>{line}</div>);
    }
  }

  return formatted;
}

export default Message;