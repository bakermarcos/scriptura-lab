import { Alert, Badge, Button, Group, Skeleton, Stack, Text } from "@mantine/core";
import { AlertCircle, BookMarked, RefreshCw } from "lucide-react";

type AnswerViewProps = {
  answer: string | null;
  error: string | null;
  loading: boolean;
  sourceCount: number;
  onRetry: () => void;
};

export function AnswerView({
  answer,
  error,
  loading,
  sourceCount,
  onRetry,
}: AnswerViewProps) {
  return (
    <section className="answer-panel" aria-live="polite">
      <Group className="panel-heading" justify="space-between" align="flex-start">
        <div>
          <span className="eyebrow">Resposta</span>
          <h2>Resultado fundamentado</h2>
        </div>
        <Badge className="answer-badge" variant="light">
          {sourceCount} fontes
        </Badge>
      </Group>

      {loading ? (
        <Stack className="answer-skeleton" gap="sm">
          <Skeleton height={18} radius="xs" />
          <Skeleton height={18} width="92%" radius="xs" />
          <Skeleton height={18} width="78%" radius="xs" />
          <Skeleton height={18} width="86%" radius="xs" />
        </Stack>
      ) : error ? (
        <Alert
          className="answer-error"
          icon={<AlertCircle size={18} />}
          title="Não foi possível consultar a API"
          variant="light"
        >
          <Text>{error}</Text>
          <Button
            className="inline-retry"
            leftSection={<RefreshCw size={16} />}
            onClick={onRetry}
            variant="light"
          >
            Tentar novamente
          </Button>
        </Alert>
      ) : answer ? (
        <article className="answer-body">
          <p>{answer}</p>
        </article>
      ) : (
        <div className="answer-empty">
          <BookMarked size={28} strokeWidth={1.7} aria-hidden="true" />
          <Text className="answer-empty-title">Aguardando uma pergunta</Text>
          <Text>
            A resposta aparecerá aqui depois que a API recuperar fontes e consultar
            o provider configurado.
          </Text>
        </div>
      )}
    </section>
  );
}
