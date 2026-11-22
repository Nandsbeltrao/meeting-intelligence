import csv
import io
import json

from src.minutes_generator import generate_meeting_minutes
from src.schemas import MeetingAnalysis


def export_minutes_to_markdown(
    analysis: MeetingAnalysis,
) -> str:
    """Gera a ata completa em formato Markdown."""

    return generate_meeting_minutes(analysis)


def export_analysis_to_json(
    analysis: MeetingAnalysis,
) -> str:
    """Gera a análise completa em formato JSON."""

    analysis_data = analysis.model_dump(
        mode="json"
    )

    return json.dumps(
        analysis_data,
        ensure_ascii=False,
        indent=2,
    )


def export_action_items_to_csv(
    analysis: MeetingAnalysis,
) -> str:
    """Gera um CSV com as tarefas da reunião."""

    output = io.StringIO()

    fieldnames = [
        "task",
        "owner",
        "deadline",
        "evidence",
        "explicitly_mentioned",
    ]

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
    )

    writer.writeheader()

    for action_item in analysis.action_items:
        writer.writerow(
            {
                "task": action_item.task,
                "owner": (
                    action_item.owner
                    if action_item.owner
                    else "Não informado"
                ),
                "deadline": (
                    action_item.deadline
                    if action_item.deadline
                    else "Não informado"
                ),
                "evidence": action_item.evidence,
                "explicitly_mentioned": (
                    action_item.explicitly_mentioned
                ),
            }
        )

    return output.getvalue()