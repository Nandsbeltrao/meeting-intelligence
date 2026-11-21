from pydantic import BaseModel, ConfigDict, Field


class Decision(BaseModel):
    """Representa uma decisão explicitamente tomada na reunião."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    description: str = Field(
        min_length=1,
        description="Decisão tomada durante a reunião.",
    )

    evidence: str = Field(
        min_length=1,
        description="Trecho literal da transcrição que sustenta a decisão.",
    )

    explicitly_mentioned: bool = Field(
        description=(
            "Indica se a decisão foi explicitamente mencionada "
            "na reunião."
        ),
    )


class ActionItem(BaseModel):
    """Representa uma tarefa identificada na reunião."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    task: str = Field(
        min_length=1,
        description="Descrição objetiva da tarefa.",
    )

    owner: str | None = Field(
        default=None,
        description=(
            "Responsável explicitamente mencionado. "
            "Use null quando não houver responsável."
        ),
    )

    deadline: str | None = Field(
        default=None,
        description=(
            "Prazo explicitamente mencionado. "
            "Use null quando não houver prazo."
        ),
    )

    evidence: str = Field(
        min_length=1,
        description="Trecho literal que sustenta a tarefa.",
    )

    explicitly_mentioned: bool = Field(
        description=(
            "Indica se a tarefa foi explicitamente mencionada "
            "na reunião."
        ),
    )


class PendingItem(BaseModel):
    """Representa uma questão ou decisão ainda pendente."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    description: str = Field(
        min_length=1,
        description="Descrição da pendência.",
    )

    evidence: str = Field(
        min_length=1,
        description="Trecho literal que sustenta a pendência.",
    )


class Suggestion(BaseModel):
    """Representa uma sugestão que ainda não foi aprovada."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    description: str = Field(
        min_length=1,
        description="Descrição da sugestão.",
    )

    proposed_by: str | None = Field(
        default=None,
        description=(
            "Pessoa que apresentou a sugestão, quando explícita."
        ),
    )

    evidence: str = Field(
        min_length=1,
        description="Trecho literal que sustenta a sugestão.",
    )

    approved: bool = Field(
        description="Indica se a sugestão foi aprovada na reunião.",
    )


class MeetingAnalysis(BaseModel):
    """Estrutura completa da análise de uma reunião."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    title: str = Field(
        min_length=1,
        description="Título curto e objetivo para a reunião.",
    )

    summary: str = Field(
        min_length=1,
        description="Resumo factual da reunião.",
    )

    topics: list[str] = Field(
        default_factory=list,
        description="Principais assuntos discutidos.",
    )

    decisions: list[Decision] = Field(
        default_factory=list,
        description="Decisões explicitamente tomadas.",
    )

    action_items: list[ActionItem] = Field(
        default_factory=list,
        description="Tarefas e encaminhamentos identificados.",
    )

    pending_items: list[PendingItem] = Field(
        default_factory=list,
        description="Questões ou decisões pendentes.",
    )

    suggestions: list[Suggestion] = Field(
        default_factory=list,
        description="Sugestões mencionadas durante a reunião.",
    )