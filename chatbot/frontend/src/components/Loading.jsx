function Loading() {
  return (
    <div className="loading" aria-live="polite" role="status">
      <span className="loading-dots">
        <span className="dot"></span>
        <span className="dot"></span>
        <span className="dot"></span>
      </span>
      <span className="loading-text">IA está digitando...</span>
    </div>
  );
}

export default Loading;