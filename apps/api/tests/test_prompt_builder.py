from app.schemas.source import RetrievedChunk
from app.services.rag.prompt_builder import PromptBuilder


def test_prompt_builder_renders_question_language_and_sources() -> None:
    prompt = PromptBuilder().build(
        question="Qual a relação entre João 1 e Gênesis 1?",
        response_language="pt-BR",
        sources=[
            RetrievedChunk(
                id="john-1-note::chunk-0",
                source_id="john-1-note",
                text="João 1 conecta o Logos ao princípio e à criação.",
                title="João 1 - Nota de estudo",
                type="study_note",
                language="pt-BR",
                license="project-created",
                reference="John 1",
                status="approved",
                use_in_rag=True,
                score=0.91,
            )
        ],
    )

    assert "Responda em pt-BR." in prompt
    assert "Qual a relação entre João 1 e Gênesis 1?" in prompt
    assert "[Fonte 1]" in prompt
    assert "Título: João 1 - Nota de estudo" in prompt
    assert "Trecho:\nJoão 1 conecta o Logos ao princípio e à criação." in prompt

