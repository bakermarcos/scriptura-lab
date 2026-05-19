import { useEffect, useState } from "react";

import { getEmbeddingHealth, getHealth, getLlmHealth } from "../services/api";

type StatusCard = {
  label: string;
  value: string;
  tone: "neutral" | "positive" | "negative";
  detail?: string;
};

export function HealthStatus() {
  const [loading, setLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState<StatusCard>({
    label: "API",
    value: "checking",
    tone: "neutral",
  });
  const [llmStatus, setLlmStatus] = useState<StatusCard>({
    label: "LLM",
    value: "checking",
    tone: "neutral",
  });
  const [embeddingStatus, setEmbeddingStatus] = useState<StatusCard>({
    label: "Embeddings",
    value: "checking",
    tone: "neutral",
  });

  async function refresh() {
    setLoading(true);

    const [apiResult, llmResult, embeddingResult] = await Promise.allSettled([
      getHealth(),
      getLlmHealth(),
      getEmbeddingHealth(),
    ]);

    if (apiResult.status === "fulfilled" && apiResult.value.status === "ok") {
      setApiStatus({
        label: "API",
        value: "online",
        tone: "positive",
      });
    } else {
      setApiStatus({
        label: "API",
        value: "offline",
        tone: "negative",
        detail:
          apiResult.status === "rejected"
            ? apiResult.reason instanceof Error
              ? apiResult.reason.message
              : "Unknown API error"
            : "Unexpected API response",
      });
    }

    if (llmResult.status === "fulfilled") {
      const payload = llmResult.value;
      setLlmStatus({
        label: "LLM",
        value: payload.status,
        tone: payload.status === "available" ? "positive" : "negative",
        detail: payload.error || `${payload.provider}: ${payload.model}`,
      });
    } else {
      setLlmStatus({
        label: "LLM",
        value: "unreachable",
        tone: "negative",
        detail:
          llmResult.reason instanceof Error
            ? llmResult.reason.message
            : "Unknown LLM error",
      });
    }

    if (embeddingResult.status === "fulfilled") {
      const payload = embeddingResult.value;
      setEmbeddingStatus({
        label: "Embeddings",
        value: payload.status,
        tone: payload.status === "available" ? "positive" : "negative",
        detail: payload.error || `${payload.provider}: ${payload.model}`,
      });
    } else {
      setEmbeddingStatus({
        label: "Embeddings",
        value: "unreachable",
        tone: "negative",
        detail:
          embeddingResult.reason instanceof Error
            ? embeddingResult.reason.message
            : "Unknown embedding error",
      });
    }

    setLoading(false);
  }

  useEffect(() => {
    void refresh();
  }, []);

  return (
    <section className="panel status-panel">
      <div className="panel-heading status-heading">
        <div>
          <span className="eyebrow">Status</span>
          <h2>Serviços locais</h2>
        </div>
        <button
          className="secondary-button"
          type="button"
          onClick={() => void refresh()}
          disabled={loading}
        >
          {loading ? "Verificando..." : "Atualizar"}
        </button>
      </div>

      <div className="status-grid">
        {[apiStatus, llmStatus, embeddingStatus].map((item) => (
          <article className="status-item" key={item.label}>
            <span className="status-label">{item.label}</span>
            <span className={`status-pill status-${item.tone}`}>{item.value}</span>
            {item.detail ? <p className="status-detail">{item.detail}</p> : null}
          </article>
        ))}
      </div>
    </section>
  );
}
