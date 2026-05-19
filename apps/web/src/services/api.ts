import type {
  ChatResponse,
  HealthResponse,
  LlmHealthResponse,
} from "../types/chat";

const API_BASE_URL = __WEB_API_BASE_URL__.replace(/\/$/, "");

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
    ...init,
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const payload = (await response.json()) as { detail?: string };
      if (payload.detail) {
        message = payload.detail;
      }
    } catch {
      message = response.statusText || message;
    }
    throw new Error(message);
  }

  return (await response.json()) as T;
}

export function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

export function getLlmHealth(): Promise<LlmHealthResponse> {
  return request<LlmHealthResponse>("/health/llm");
}

export function sendChat(question: string): Promise<ChatResponse> {
  return request<ChatResponse>("/chat", {
    method: "POST",
    body: JSON.stringify({ question }),
  });
}

