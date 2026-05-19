import { Badge, Group, Progress, Text } from "@mantine/core";
import { BookOpenCheck } from "lucide-react";

import type { ChatSource } from "../types/chat";

type SourceCardProps = {
  source: ChatSource;
};

export function SourceCard({ source }: SourceCardProps) {
  const scorePercent =
    typeof source.score === "number"
      ? Math.max(0, Math.min(100, Math.round(source.score * 100)))
      : null;

  return (
    <article className="source-card">
      <div className="source-card-header">
        <div className="source-title-block">
          <span className="eyebrow">Fonte</span>
          <h3>{source.title}</h3>
        </div>
        {scorePercent !== null ? (
          <Badge className="score-badge" variant="light">
            Score {source.score?.toFixed(2)}
          </Badge>
        ) : null}
      </div>

      {scorePercent !== null ? (
        <div className="score-meter" aria-label={`Score ${source.score?.toFixed(2)}`}>
          <Progress value={scorePercent} size="sm" radius="xs" />
        </div>
      ) : null}

      <dl className="source-meta">
        <MetaItem label="Tipo" value={source.type} />
        <MetaItem label="Idioma" value={source.language} />
        <MetaItem label="Referência" value={source.reference || "N/A"} />
      </dl>

      <div className="source-excerpt-wrap">
        <Group gap={8} align="center">
          <BookOpenCheck size={16} aria-hidden="true" />
          <Text className="excerpt-label">Trecho recuperado</Text>
        </Group>
        <p className="source-excerpt">{source.excerpt}</p>
      </div>
    </article>
  );
}

function MetaItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}
