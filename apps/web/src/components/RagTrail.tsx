import { Badge, Group, Text } from "@mantine/core";
import { Bot, Database, FileText, MessageSquareText, Sigma } from "lucide-react";

type RagTrailProps = {
  loading: boolean;
  question: string | null;
  sourceCount: number;
  hasAnswer: boolean;
};

const steps = [
  {
    label: "Pergunta",
    description: "Entrada do usuário",
    icon: MessageSquareText,
  },
  {
    label: "Embeddings",
    description: "Vetor semântico",
    icon: Sigma,
  },
  {
    label: "Qdrant",
    description: "Busca por chunks",
    icon: Database,
  },
  {
    label: "Prompt",
    description: "Fontes montadas",
    icon: FileText,
  },
  {
    label: "Modelo",
    description: "Resposta final",
    icon: Bot,
  },
];

export function RagTrail({
  loading,
  question,
  sourceCount,
  hasAnswer,
}: RagTrailProps) {
  const activeIndex = getActiveIndex({ loading, question, sourceCount, hasAnswer });

  return (
    <section className="rag-trail" aria-label="Fluxo RAG">
      <Group className="rag-trail-heading" justify="space-between" gap="md">
        <div>
          <span className="eyebrow">Pipeline</span>
          <h2>Da pergunta à resposta</h2>
        </div>
        <Badge className="rag-badge" variant="outline">
          {loading ? "processando" : hasAnswer ? "concluído" : "aguardando"}
        </Badge>
      </Group>

      <div className="rag-steps">
        {steps.map((step, index) => {
          const Icon = step.icon;
          const state =
            index < activeIndex ? "complete" : index === activeIndex ? "active" : "idle";

          return (
            <article className={`rag-step rag-step-${state}`} key={step.label}>
              <span className="rag-step-icon" aria-hidden="true">
                <Icon size={18} strokeWidth={1.9} />
              </span>
              <div>
                <Text className="rag-step-label">{step.label}</Text>
                <Text className="rag-step-description">{step.description}</Text>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

function getActiveIndex({
  loading,
  question,
  sourceCount,
  hasAnswer,
}: RagTrailProps): number {
  if (hasAnswer) {
    return steps.length;
  }
  if (loading && sourceCount > 0) {
    return 4;
  }
  if (loading && question) {
    return 2;
  }
  if (question) {
    return 1;
  }
  return 0;
}
