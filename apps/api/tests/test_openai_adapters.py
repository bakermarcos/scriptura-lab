from app.services.models.openai_adapters import OpenAIResponsesClient


def test_openai_responses_client_extracts_output_text_helper() -> None:
    client = OpenAIResponsesClient(
        base_url="https://api.openai.com/v1",
        api_key="test-key",
        model="gpt-5.5",
    )

    assert client._extract_output_text({"output_text": " resposta "}) == "resposta"


def test_openai_responses_client_extracts_nested_output_text() -> None:
    client = OpenAIResponsesClient(
        base_url="https://api.openai.com/v1",
        api_key="test-key",
        model="gpt-5.5",
    )
    payload = {
        "output": [
            {
                "type": "message",
                "content": [
                    {"type": "output_text", "text": "Primeira parte."},
                    {"type": "output_text", "text": "Segunda parte."},
                ],
            }
        ]
    }

    assert (
        client._extract_output_text(payload)
        == "Primeira parte.\nSegunda parte."
    )
