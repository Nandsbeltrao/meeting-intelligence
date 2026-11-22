from src.schemas import MeetingAnalysis


def format_optional_value(
    value: str | None,
) -> str:
    """Converte valores ausentes em texto legível."""

    if value is None or not value.strip():
        return "Não informado"

    return value


def generate_meeting_minutes(
    analysis: MeetingAnalysis,
) -> str:
    """Gera uma ata em Markdown a partir da análise."""

    lines = [
        f"# {analysis.title}",
        "",
        "## Resumo",
        "",
        analysis.summary,
        "",
        "## Assuntos principais",
        "",
    ]

    if analysis.topics:
        for topic in analysis.topics:
            lines.append(f"- {topic}")
    else:
        lines.append("- Nenhum assunto principal identificado.")

    lines.extend(
        [
            "",
            "## Decisões",
            "",
        ]
    )

    if analysis.decisions:
        for index, decision in enumerate(
            analysis.decisions,
            start=1,
        ):
            lines.extend(
                [
                    f"### Decisão {index}",
                    "",
                    decision.description,
                    "",
                    f"**Evidência:** {decision.evidence}",
                    "",
                ]
            )
    else:
        lines.append(
            "Nenhuma decisão explícita foi identificada."
        )

    lines.extend(
        [
            "",
            "## Tarefas e encaminhamentos",
            "",
        ]
    )

    if analysis.action_items:
        for index, action_item in enumerate(
            analysis.action_items,
            start=1,
        ):
            owner = format_optional_value(
                action_item.owner
            )

            deadline = format_optional_value(
                action_item.deadline
            )

            lines.extend(
                [
                    f"### Tarefa {index}",
                    "",
                    f"**Tarefa:** {action_item.task}",
                    "",
                    f"**Responsável:** {owner}",
                    "",
                    f"**Prazo:** {deadline}",
                    "",
                    f"**Evidência:** {action_item.evidence}",
                    "",
                ]
            )
    else:
        lines.append(
            "Nenhuma tarefa explícita foi identificada."
        )

    lines.extend(
        [
            "",
            "## Pendências",
            "",
        ]
    )

    if analysis.pending_items:
        for pending_item in analysis.pending_items:
            lines.extend(
                [
                    f"- {pending_item.description}",
                    (
                        f"  - **Evidência:** "
                        f"{pending_item.evidence}"
                    ),
                ]
            )
    else:
        lines.append(
            "Nenhuma pendência foi identificada."
        )

    lines.extend(
        [
            "",
            "## Sugestões",
            "",
        ]
    )

    if analysis.suggestions:
        for suggestion in analysis.suggestions:
            proposed_by = format_optional_value(
                suggestion.proposed_by
            )

            approval_status = (
                "Aprovada"
                if suggestion.approved
                else "Não aprovada"
            )

            lines.extend(
                [
                    f"### {suggestion.description}",
                    "",
                    f"**Proposta por:** {proposed_by}",
                    "",
                    f"**Status:** {approval_status}",
                    "",
                    f"**Evidência:** {suggestion.evidence}",
                    "",
                ]
            )
    else:
        lines.append(
            "Nenhuma sugestão foi identificada."
        )

    lines.extend(
        [
            "",
            "---",
            "",
            (
                "Ata gerada automaticamente pelo Meeting Intelligence. "
                "As informações devem ser revisadas antes do uso oficial."
            ),
        ]
    )

    return "\n".join(lines)
    