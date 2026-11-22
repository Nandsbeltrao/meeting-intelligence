
import re
import unicodedata

from src.schemas import MeetingAnalysis


def normalize_text(text: str) -> str:
    """Normaliza texto para comparação."""

    normalized = unicodedata.normalize("NFKD", text)

    without_accents = "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )

    return re.sub(
        r"\s+",
        " ",
        without_accents.lower(),
    ).strip()


def evidence_exists(
    evidence: str,
    transcript: str,
) -> bool:
    """Verifica se a evidência existe na transcrição."""

    if not evidence or not evidence.strip():
        return False

    return normalize_text(evidence) in normalize_text(transcript)


def create_validation_result(
    category: str,
    content: str,
    evidence: str,
    transcript: str,
) -> dict:
    """Cria o resultado da validação de uma evidência."""

    return {
        "category": category,
        "content": content,
        "evidence": evidence,
        "evidence_found": evidence_exists(
            evidence=evidence,
            transcript=transcript,
        ),
    }


def validate_analysis_evidence(
    analysis: MeetingAnalysis,
    transcript: str,
) -> list:
    """Valida todas as evidências extraídas pela IA."""

    results = []

    for decision in analysis.decisions:
        results.append(
            create_validation_result(
                category="decision",
                content=decision.description,
                evidence=decision.evidence,
                transcript=transcript,
            )
        )

    for action_item in analysis.action_items:
        results.append(
            create_validation_result(
                category="action_item",
                content=action_item.task,
                evidence=action_item.evidence,
                transcript=transcript,
            )
        )

    for pending_item in analysis.pending_items:
        results.append(
            create_validation_result(
                category="pending_item",
                content=pending_item.description,
                evidence=pending_item.evidence,
                transcript=transcript,
            )
        )

    for suggestion in analysis.suggestions:
        results.append(
            create_validation_result(
                category="suggestion",
                content=suggestion.description,
                evidence=suggestion.evidence,
                transcript=transcript,
            )
        )

    return results
