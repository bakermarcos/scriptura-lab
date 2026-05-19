import { useEffect, useState } from "react";
import { ActionIcon, Group, Loader, Text, Tooltip } from "@mantine/core";
import { AlertTriangle, CheckCircle2, RefreshCw } from "lucide-react";

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
    <section className="status-strip" aria-label="Status dos serviços">
      <Group gap="xs" wrap="wrap">
        {[apiStatus, llmStatus, embeddingStatus].map((item) => (
          <Tooltip
            key={item.label}
            label={item.detail || `${item.label}: ${item.value}`}
            withArrow
          >
            <div className={`status-pill status-${item.tone}`}>
              <StatusIcon tone={item.tone} loading={loading && item.value === "checking"} />
              <span className="status-label">{item.label}</span>
              <Text component="span" className="status-value">
                {item.value}
              </Text>
            </div>
          </Tooltip>
        ))}
      </Group>

      <Tooltip label="Atualizar status" withArrow>
        <ActionIcon
          className="status-refresh"
          aria-label="Atualizar status dos serviços"
          variant="subtle"
          onClick={() => void refresh()}
          disabled={loading}
        >
          {loading ? <Loader size={16} /> : <RefreshCw size={17} />}
        </ActionIcon>
      </Tooltip>
    </section>
  );
}

function StatusIcon({
  tone,
  loading,
}: {
  tone: StatusCard["tone"];
  loading: boolean;
}) {
  if (loading) {
    return <Loader size={14} aria-hidden="true" />;
  }

  if (tone === "positive") {
    return <CheckCircle2 size={15} aria-hidden="true" />;
  }

  if (tone === "negative") {
    return <AlertTriangle size={15} aria-hidden="true" />;
  }

  return <RefreshCw size={15} aria-hidden="true" />;
}
