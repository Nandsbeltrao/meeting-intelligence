from copy import deepcopy

from src.schemas import MeetingAnalysis


def apply_action_item_reviews(
    analysis: MeetingAnalysis,
    reviews: list[dict],
) -> MeetingAnalysis:
    """Aplica revisões humanas às tarefas extraídas pela IA."""

    reviewed_analysis = deepcopy(analysis)

    if len(reviews) != len(reviewed_analysis.action_items):
        raise ValueError(
            "A quantidade de revisões deve ser igual "
            "à quantidade de tarefas."
        )

    reviewed_action_items = []

    for action_item, review in zip(
        reviewed_analysis.action_items,
        reviews,
    ):
        if not review.get("include", True):
            continue

        reviewed_task = str(
            review.get("task", action_item.task)
        ).strip()

        if not reviewed_task:
            raise ValueError(
                "A descrição da tarefa não pode ficar vazia."
            )

        reviewed_owner = review.get(
            "owner",
            action_item.owner,
        )

        reviewed_deadline = review.get(
            "deadline",
            action_item.deadline,
        )

        if isinstance(reviewed_owner, str):
            reviewed_owner = reviewed_owner.strip() or None

        if isinstance(reviewed_deadline, str):
            reviewed_deadline = (
                reviewed_deadline.strip() or None
            )

        action_item.task = reviewed_task
        action_item.owner = reviewed_owner
        action_item.deadline = reviewed_deadline

        reviewed_action_items.append(action_item)

    reviewed_analysis.action_items = reviewed_action_items

    return reviewed_analysis