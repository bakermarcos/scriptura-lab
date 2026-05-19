from app.schemas.source import RetrievedChunk


class PromptBuilder:
    def build(
        self,
        question: str,
        sources: list[RetrievedChunk],
        response_language: str,
    ) -> str:
        rendered_sources = []
        for index, source in enumerate(sources, start=1):
            rendered_sources.append(
                "\n".join(
                    [
                        f"[Fonte {index}]",
                        f"Título: {source.title}",
                        f"Tipo: {source.type}",
                        f"Referência: {source.reference or 'N/A'}",
                        f"Idioma: {source.language}",
                        f"Licença: {source.license}",
                        "Trecho:",
                        source.text.strip(),
                    ]
                )
            )

        sources_block = "\n\n".join(rendered_sources)
        return f"""Você é um assistente de estudo bíblico.

Responda usando apenas as fontes fornecidas abaixo.
Se as fontes não forem suficientes, diga claramente:
"Não encontrei base suficiente nas fontes disponíveis para responder com segurança."

Regras:
- Não invente referências.
- Não afirme como absoluto o que for interpretação.
- Diferencie texto bíblico, contexto histórico e aplicação.
- Quando houver limitações, explique.
- Responda em {response_language}.
- Se usar termos gregos, hebraicos ou aramaicos, explique de forma simples.
- Não produza uma nova tradução autoritativa do texto bíblico.
- Use linguagem como "pode indicar", "é frequentemente entendido como" ou "no contexto da fonte".

Pergunta:
{question}

Fontes:
{sources_block}
"""

