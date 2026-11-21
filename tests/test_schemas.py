from src.schemas import ActionItem, MeetingAnalysis


analysis = MeetingAnalysis(
    title="Planejamento do evento fictício",
    summary=(
        "A equipe discutiu o regulamento, "
        "a divulgação e as inscrições."
    ),
    topics=[
        "Regulamento",
        "Divulgação",
        "Inscrições",
    ],
    action_items=[
        ActionItem(
            task="Revisar o regulamento",
            owner="Bruno",
            deadline="sexta-feira, 27 de novembro",
            evidence=(
                "Bruno: Eu posso revisar o regulamento "
                "até sexta-feira, 27 de novembro."
            ),
            explicitly_mentioned=True,
        ),
        ActionItem(
            task="Preparar o formulário de inscrição",
            owner=None,
            deadline=None,
            evidence=(
                "Bruno: Também precisamos preparar o formulário "
                "de inscrição, mas ainda não definimos uma pessoa "
                "responsável nem um prazo."
            ),
            explicitly_mentioned=True,
        ),
    ],
)

print(analysis.model_dump_json(indent=2))