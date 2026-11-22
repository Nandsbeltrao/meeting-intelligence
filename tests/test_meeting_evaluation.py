from pathlib import Path

from src.evidence_checker import validate_analysis_evidence
from src.meeting_analyzer import analyze_meeting
from src.transcript_loader import load_transcript


transcript = load_transcript(
    Path("data/sample/reuniao_avaliacao.txt")
)

analysis = analyze_meeting(transcript)

evidence_results = validate_analysis_evidence(
    analysis=analysis,
    transcript=transcript,
)


def contains_text(
    values: list[str],
    expected_text: str,
) -> bool:
    """Verifica se um texto aparece parcialmente em uma lista."""

    expected_text = expected_text.lower()

    return any(
        expected_text in value.lower()
        for value in values
    )


results = []


# 1. Decisão explícita
decision_descriptions = [
    decision.description
    for decision in analysis.decisions
]

results.append(
    {
        "id": 1,
        "test": "Decisão explícita identificada",
        "approved": contains_text(
            decision_descriptions,
            "divulgação",
        ),
    }
)


# 2. Tarefa com responsável e prazo
regulation_tasks = [
    action_item
    for action_item in analysis.action_items
    if "regulamento" in action_item.task.lower()
]

test_2_approved = bool(
    regulation_tasks
    and regulation_tasks[0].owner == "Bruno"
    and regulation_tasks[0].deadline is not None
    and "30 de novembro" in regulation_tasks[0].deadline.lower()
)

results.append(
    {
        "id": 2,
        "test": "Tarefa com responsável e prazo",
        "approved": test_2_approved,
    }
)


# 3. Tarefa sem responsável
form_tasks = [
    action_item
    for action_item in analysis.action_items
    if "formulário" in action_item.task.lower()
]

test_3_approved = bool(
    form_tasks
    and form_tasks[0].owner is None
)

results.append(
    {
        "id": 3,
        "test": "Ausência de responsável preservada",
        "approved": test_3_approved,
    }
)


# 4. Tarefa sem prazo
page_tasks = [
    action_item
    for action_item in analysis.action_items
    if "página" in action_item.task.lower()
]

test_4_approved = bool(
    page_tasks
    and page_tasks[0].deadline is None
)

results.append(
    {
        "id": 4,
        "test": "Ausência de prazo preservada",
        "approved": test_4_approved,
    }
)


# 5. Pendência identificada
pending_descriptions = [
    pending_item.description
    for pending_item in analysis.pending_items
]

results.append(
    {
        "id": 5,
        "test": "Pendência sobre plataforma identificada",
        "approved": contains_text(
            pending_descriptions,
            "plataforma",
        ),
    }
)


# 6. Sugestão não aprovada
spreadsheet_suggestions = [
    suggestion
    for suggestion in analysis.suggestions
    if "planilha" in suggestion.description.lower()
]

test_6_approved = bool(
    spreadsheet_suggestions
    and spreadsheet_suggestions[0].approved is False
)

results.append(
    {
        "id": 6,
        "test": "Sugestão não aprovada preservada",
        "approved": test_6_approved,
    }
)


# 7. Nome citado não atribuído como responsável
pedro_assigned_as_owner = any(
    action_item.owner
    and action_item.owner.lower() == "pedro"
    for action_item in analysis.action_items
)

results.append(
    {
        "id": 7,
        "test": "Nome citado não virou responsável",
        "approved": not pedro_assigned_as_owner,
    }
)


# 8. Evidências literais localizadas
invalid_evidence = [
    result
    for result in evidence_results
    if not result["evidence_found"]
]

results.append(
    {
        "id": 8,
        "test": "Todas as evidências foram localizadas",
        "approved": len(invalid_evidence) == 0,
    }
)


approved_count = sum(
    result["approved"]
    for result in results
)

print()
print("RESULTADOS DA AVALIAÇÃO")
print("=" * 60)

for result in results:
    status = (
        "APROVADO"
        if result["approved"]
        else "REPROVADO"
    )

    print(
        f"{result['id']}. {status} | {result['test']}"
    )

print("=" * 60)
print(
    f"Resultado final: {approved_count}/{len(results)}"
)

print()
print("ANÁLISE GERADA")
print("=" * 60)
print(
    analysis.model_dump_json(
        indent=2,
    )
)