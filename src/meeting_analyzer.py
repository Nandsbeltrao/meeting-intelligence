import os

import cohere
from dotenv import load_dotenv
from pydantic import ValidationError

from src.schemas import MeetingAnalysis


load_dotenv()

CHAT_MODEL = os.getenv(
    "COHERE_CHAT_MODEL",
    "command-a-plus-05-2026",
)


def get_cohere_client() -> cohere.ClientV2:
    """Cria o cliente da Cohere usando a chave configurada."""

    api_key = os.getenv("COHERE_API_KEY")

    if not api_key:
        raise ValueError(
            "A variável COHERE_API_KEY não foi encontrada."
        )

    return cohere.ClientV2(
        api_key=api_key,
    )


def extract_response_text(response) -> str:
    """Extrai o texto JSON retornado pela Cohere."""

    for content_item in response.message.content:
        text = getattr(
            content_item,
            "text",
            None,
        )

        if text:
            return text.strip()

    raise ValueError(
        "A Cohere não retornou conteúdo textual."
    )


def analyze_meeting(
    transcript: str,
) -> MeetingAnalysis:
    """Analisa uma transcrição e devolve dados estruturados."""

    if not transcript or not transcript.strip():
        raise ValueError(
            "A transcrição não pode estar vazia."
        )

    client = get_cohere_client()

    system_prompt = """
Você é um assistente especializado em transformar reuniões
em informações estruturadas e rastreáveis.

Analise exclusivamente a transcrição recebida.

REGRAS OBRIGATÓRIAS:

1. Não utilize conhecimento externo.
2. Não invente decisões, tarefas, responsáveis ou prazos.
3. Responsáveis só podem ser preenchidos quando forem
   explicitamente associados à tarefa.
4. Prazos só podem ser preenchidos quando forem
   explicitamente associados à tarefa.
5. Quando não houver responsável, use null.
6. Quando não houver prazo, use null.
7. Não transforme sugestões em decisões.
8. Não transforme assuntos discutidos em tarefas.
9. Cada decisão, tarefa, pendência e sugestão deve conter
   uma evidência literal retirada da transcrição.
10. O campo explicitly_mentioned deve ser true somente
    quando o conteúdo estiver explícito na transcrição.
11. Não interprete uma pessoa mencionada em outro contexto
    como responsável por uma tarefa.
12. Preserve datas exatamente como aparecem na transcrição.
13. Retorne somente um objeto JSON válido.
14. Não inclua explicações antes ou depois do JSON.

O JSON deve seguir exatamente esta estrutura:

{
  "title": "Título curto da reunião",
  "summary": "Resumo factual da reunião",
  "topics": [
    "Assunto principal"
  ],
  "decisions": [
    {
      "description": "Decisão tomada",
      "evidence": "Trecho literal da transcrição",
      "explicitly_mentioned": true
    }
  ],
  "action_items": [
    {
      "task": "Descrição objetiva da tarefa",
      "owner": "Nome explícito ou null",
      "deadline": "Prazo explícito ou null",
      "evidence": "Trecho literal da transcrição",
      "explicitly_mentioned": true
    }
  ],
  "pending_items": [
    {
      "description": "Descrição da pendência",
      "evidence": "Trecho literal da transcrição"
    }
  ],
  "suggestions": [
    {
      "description": "Descrição da sugestão",
      "proposed_by": "Nome explícito ou null",
      "evidence": "Trecho literal da transcrição",
      "approved": false
    }
  ]
}

Se uma categoria não possuir itens, retorne uma lista vazia.
""".strip()

    response = client.chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": (
                    "Analise a transcrição abaixo:\n\n"
                    f"{transcript}"
                ),
            },
        ],
        response_format={
            "type": "json_object",
        },
        temperature=0,
    )

    response_text = extract_response_text(
        response
    )

    try:
        return MeetingAnalysis.model_validate_json(
            response_text
        )

    except ValidationError as error:
        raise ValueError(
            "A resposta da IA não corresponde ao formato "
            "estruturado esperado."
        ) from error