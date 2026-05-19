import { FormEvent, useState } from "react";
import { Button, Group, Stack, Text, Textarea } from "@mantine/core";
import { CornerDownLeft, Search } from "lucide-react";

type ChatInputProps = {
  question: string;
  onQuestionChange: (question: string) => void;
  onSubmit: (question: string) => void;
  loading: boolean;
  suggestions: string[];
};

export function ChatInput({
  question,
  onQuestionChange,
  onSubmit,
  loading,
  suggestions,
}: ChatInputProps) {
  const [touched, setTouched] = useState(false);
  const trimmed = question.trim();
  const showError = touched && !trimmed;

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setTouched(true);
    if (!trimmed) {
      return;
    }

    onSubmit(trimmed);
  }

  return (
    <form className="query-panel" onSubmit={handleSubmit}>
      <Stack gap="lg">
        <div>
          <span className="eyebrow">Pergunta</span>
          <h2>Faça uma pergunta bíblica</h2>
          <Text className="panel-copy">
            O sistema recupera fontes aprovadas antes de consultar o modelo.
          </Text>
        </div>

        <Textarea
          id="question"
          className="question-input"
          label="Pergunta"
          placeholder="Ex.: Qual a relação entre João 1 e Gênesis 1?"
          value={question}
          onBlur={() => setTouched(true)}
          onChange={(event) => onQuestionChange(event.currentTarget.value)}
          autosize
          minRows={6}
          maxRows={10}
          disabled={loading}
          error={showError ? "Digite uma pergunta antes de consultar." : undefined}
        />

        <div className="suggestions-block" aria-label="Perguntas sugeridas">
          <Text className="suggestions-label">Sugestões rápidas</Text>
          <Group gap="xs">
            {suggestions.map((suggestion) => (
              <button
                className="suggestion-chip"
                key={suggestion}
                type="button"
                onClick={() => onQuestionChange(suggestion)}
                disabled={loading}
              >
                {suggestion}
              </button>
            ))}
          </Group>
        </div>

        <Group justify="space-between" gap="md" align="center">
          <Text className="input-hint">
            A pergunta fica preservada para ajustes e novas tentativas.
          </Text>
          <Button
            className="primary-action"
            type="submit"
            loading={loading}
            disabled={!trimmed}
            leftSection={loading ? undefined : <Search size={17} />}
            rightSection={loading ? undefined : <CornerDownLeft size={15} />}
          >
            {loading ? "Consultando" : "Perguntar"}
          </Button>
        </Group>
      </Stack>
    </form>
  );
}
