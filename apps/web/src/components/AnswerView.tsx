type AnswerViewProps = {
  answer: string | null;
};

export function AnswerView({ answer }: AnswerViewProps) {
  return (
    <section className="panel answer-panel">
      <div className="panel-heading">
        <span className="eyebrow">Resposta</span>
        <h2>Resultado</h2>
      </div>
      <p className={answer ? "answer-text" : "answer-placeholder"}>
        {answer ||
          "A resposta aparecerá aqui depois que a API recuperar fontes e consultar o modelo local."}
      </p>
    </section>
  );
}

