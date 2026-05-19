import type { ChatSource } from "../types/chat";

type SourceCardProps = {
  source: ChatSource;
};

export function SourceCard({ source }: SourceCardProps) {
  return (
    <article className="panel source-card">
      <div className="source-card-header">
        <div>
          <span className="eyebrow">Fonte</span>
          <h3>{source.title}</h3>
        </div>
        {typeof source.score === "number" ? (
          <span className="score-badge">{source.score.toFixed(2)}</span>
        ) : null}
      </div>

      <dl className="source-meta">
        <div>
          <dt>Tipo</dt>
          <dd>{source.type}</dd>
        </div>
        <div>
          <dt>Idioma</dt>
          <dd>{source.language}</dd>
        </div>
        <div>
          <dt>Referência</dt>
          <dd>{source.reference || "N/A"}</dd>
        </div>
      </dl>

      <p className="source-excerpt">{source.excerpt}</p>
    </article>
  );
}

