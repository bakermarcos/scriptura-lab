import { useState } from "react";

import { AnswerView } from "./components/AnswerView";
import { ChatInput } from "./components/ChatInput";
import { HealthStatus } from "./components/HealthStatus";
import { SourceCard } from "./components/SourceCard";
import { sendChat } from "./services/api";
import type { ChatSource } from "./types/chat";

export default function App() {
  const [answer, setAnswer] = useState<string | null>(null);
  const [sources, setSources] = useState<ChatSource[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(question: string) {
    setLoading(true);
    setError(null);

    try {
      const response = await sendChat(question);
      setAnswer(response.answer);
      setSources(response.sources);
    } catch (caughtError) {
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Falha inesperada ao consultar a API.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="hero panel">
        <span className="eyebrow">Scriptura Lab v0.2</span>
        <h1>Estudo bíblico com RAG local, fontes rastreáveis e resposta verificável.</h1>
        <p className="hero-copy">
          Faça uma pergunta, recupere notas indexadas no Qdrant e use o modelo
          configurado para responder apenas com base nas fontes disponíveis.
        </p>
      </section>

      <HealthStatus />

      <div className="content-grid">
        <ChatInput onSubmit={handleSubmit} loading={loading} />
        <AnswerView answer={answer} />
      </div>

      {error ? <div className="error-banner">{error}</div> : null}

      <section className="sources-section">
        <div className="section-heading">
          <span className="eyebrow">Fontes usadas</span>
          <h2>Trechos recuperados</h2>
        </div>

        {sources.length > 0 ? (
          <div className="sources-grid">
            {sources.map((source) => (
              <SourceCard key={source.id} source={source} />
            ))}
          </div>
        ) : (
          <div className="panel empty-state">
            Nenhuma fonte exibida ainda. Após a primeira pergunta, os chunks
            recuperados aparecerão aqui.
          </div>
        )}
      </section>
    </main>
  );
}
