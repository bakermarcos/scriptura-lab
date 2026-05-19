import { FormEvent, useState } from "react";

type ChatInputProps = {
  onSubmit: (question: string) => void;
  loading: boolean;
};

export function ChatInput({ onSubmit, loading }: ChatInputProps) {
  const [question, setQuestion] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = question.trim();
    if (!trimmed) {
      return;
    }

    onSubmit(trimmed);
    setQuestion("");
  }

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="panel-heading">
        <span className="eyebrow">Pergunta</span>
        <h2>Faça uma pergunta bíblica</h2>
      </div>

      <label className="sr-only" htmlFor="question">
        Faça uma pergunta bíblica
      </label>
      <textarea
        id="question"
        className="question-input"
        placeholder="Ex.: Qual a relação entre João 1 e Gênesis 1?"
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
        rows={5}
        disabled={loading}
      />

      <button className="primary-button" type="submit" disabled={loading}>
        {loading ? "Consultando..." : "Perguntar"}
      </button>
    </form>
  );
}

