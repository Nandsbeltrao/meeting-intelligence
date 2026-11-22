from src.review import apply_action_item_reviews
from src.schemas import ActionItem, MeetingAnalysis


original_analysis = MeetingAnalysis(
    title="Reunião de planejamento",
    summary="A equipe discutiu tarefas do evento.",
    topics=["Planejamento"],
    action_items=[
        ActionItem(
            task="Revisar o regulamento",
            owner="Bruno",
            deadline="sexta-feira",
            evidence=(
                "Bruno: Eu posso revisar o regulamento "
                "até sexta-feira."
            ),
            explicitly_mentioned=True,
        ),
        ActionItem(
            task="Preparar o formulário",
            owner=None,
            deadline=None,
            evidence=(
                "Também precisamos preparar o formulário."
            ),
            explicitly_mentioned=True,
        ),
    ],
)

reviews = [
    {
        "include": True,
        "task": "Revisar e validar o regulamento",
        "owner": "Bruno",
        "deadline": "sexta-feira",
    },
    {
        "include": True,
        "task": "Preparar o formulário de inscrição",
        "owner": "Carla",
        "deadline": "",
    },
]

reviewed_analysis = apply_action_item_reviews(
    analysis=original_analysis,
    reviews=reviews,
)

print(
    reviewed_analysis.model_dump_json(
        indent=2,
    )
)

assert (
    reviewed_analysis.action_items[0].task
    == "Revisar e validar o regulamento"
)

assert (
    reviewed_analysis.action_items[1].owner
    == "Carla"
)

assert (
    reviewed_analysis.action_items[1].deadline
    is None
)

assert (
    reviewed_analysis.action_items[1].evidence
    == "Também precisamos preparar o formulário."
)

assert (
    original_analysis.action_items[1].owner
    is None
)

print()
print("Revisão humana validada com sucesso.")