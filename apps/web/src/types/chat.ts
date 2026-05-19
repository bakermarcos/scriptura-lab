export type HealthResponse = {
  status: string;
};

export type LlmHealthResponse = {
  provider: string;
  model: string;
  status: string;
  error?: string | null;
};

export type ChatSource = {
  id: string;
  source_id: string;
  title: string;
  type: string;
  language: string;
  reference?: string | null;
  excerpt: string;
  score?: number | null;
};

export type ChatResponse = {
  answer: string;
  sources: ChatSource[];
};

