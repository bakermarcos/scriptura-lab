import { useState } from "react";
import { Alert, Badge, Button, Group, Stack, Text } from "@mantine/core";
import { BookOpenText, Database, Library, Network, RefreshCw } from "lucide-react";

import { AnswerView } from "./components/AnswerView";
import { ChatInput } from "./components/ChatInput";
import { HealthStatus } from "./components/HealthStatus";
import { RagTrail } from "./components/RagTrail";
import { SourceCard } from "./components/SourceCard";
import { sendChat } from "./services/api";
import type { ChatSource } from "./types/chat";

const suggestedQuestions = [
  "Qual a relação entre João 1 e Gênesis 1?",
  "Como Efésios 2 descreve a graça?",
  "O que Romanos 8 diz sobre esperança?",
];

export default function App() {
  const [question, setQuestion] = useState("");
  const [lastQuestion, setLastQuestion] = useState<string | null>(null);
  const [answer, setAnswer] = useState<string | null>(null);
  const [sources, setSources] = useState<ChatSource[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(nextQuestion = question) {
    const trimmed = nextQuestion.trim();
    if (!trimmed) {
      return;
    }

    setLoading(true);
    setError(null);
    setLastQuestion(trimmed);
    setAnswer(null);
    setSources([]);

    try {
      const response = await sendChat(trimmed);
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
    <div className="app-frame">
      <header className="topbar">
        <Group className="brand-lockup" gap="md" wrap="nowrap">
          <span className="brand-mark" aria-hidden="true">
            <BookOpenText size={24} strokeWidth={1.8} />
          </span>
          <div>
            <Group gap="xs">
              <Text className="brand-name">Scriptura Lab</Text>
              <Badge className="version-badge" variant="outline">
                v0.2
              </Badge>
            </Group>
            <Text className="brand-subtitle">RAG bíblico com fontes verificáveis</Text>
          </div>
        </Group>

        <HealthStatus />
      </header>

      <main className="app-shell">
        <section className="hero-band" aria-labelledby="page-title">
          <div className="hero-card">
            <div className="hero-kicker">
              <Library size={16} aria-hidden="true" />
              Workspace editorial de estudo
            </div>
            <h1 id="page-title">Estudo bíblico com fontes verificáveis</h1>
            <p>
              Faça perguntas, acompanhe o pipeline RAG e revise cada trecho usado
              antes de confiar na resposta.
            </p>
            <Group className="hero-tags" gap="xs" justify="center">
              <Badge variant="light">RAG local-first</Badge>
              <Badge variant="light">Qdrant</Badge>
              <Badge variant="light">LLM configurável</Badge>
            </Group>
          </div>
        </section>

        <RagTrail
          loading={loading}
          question={lastQuestion}
          sourceCount={sources.length}
          hasAnswer={Boolean(answer)}
        />

        <section className="workspace-grid" aria-label="Consulta RAG">
          <ChatInput
            question={question}
            onQuestionChange={setQuestion}
            onSubmit={handleSubmit}
            loading={loading}
            suggestions={suggestedQuestions}
          />

          <AnswerView
            answer={answer}
            error={error}
            loading={loading}
            sourceCount={sources.length}
            onRetry={() => void handleSubmit(lastQuestion || question)}
          />
        </section>

        <section className="sources-section" aria-labelledby="sources-title">
          <div className="section-heading">
            <div>
              <span className="eyebrow">Fontes usadas</span>
              <h2 id="sources-title">Trechos recuperados</h2>
            </div>
            <Badge className="source-count-badge" variant="light">
              {sources.length} chunks
            </Badge>
          </div>

          {sources.length > 0 ? (
            <div className="sources-grid">
              {sources.map((source) => (
                <SourceCard key={source.id} source={source} />
              ))}
            </div>
          ) : (
            <Alert
              className="empty-state"
              icon={<Database size={18} />}
              title="Nenhuma fonte exibida ainda"
              variant="light"
            >
              Envie uma pergunta para ver quais trechos foram recuperados antes
              da resposta ser gerada.
            </Alert>
          )}
        </section>

        {error ? (
          <Button
            className="floating-retry"
            leftSection={<RefreshCw size={16} />}
            variant="filled"
            onClick={() => void handleSubmit(lastQuestion || question)}
          >
            Tentar novamente
          </Button>
        ) : null}

        <Stack className="footer-note" gap={4}>
          <Group gap={8}>
            <Network size={15} aria-hidden="true" />
            <Text>Modelo e embeddings são configuráveis por provider.</Text>
          </Group>
        </Stack>
      </main>
    </div>
  );
}
