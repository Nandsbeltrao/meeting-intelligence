import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.evidence_checker import validate_analysis_evidence
from src.exporters import (
    export_action_items_to_csv,
    export_analysis_to_json,
    export_minutes_to_markdown,
)
from src.meeting_analyzer import analyze_meeting
from src.review import apply_action_item_reviews
from src.transcript_loader import (
    load_transcript,
    normalize_transcript,
    validate_transcript,
)


load_dotenv()

SAMPLE_DIRECTORY = Path("data/sample")
SAMPLE_TRANSCRIPT = SAMPLE_DIRECTORY / "reuniao_ficticia.txt"


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Meeting Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================


def format_optional_value(
    value: str | None,
) -> str:
    """Converte valores ausentes em texto legível."""

    if value is None or not value.strip():
        return "Não informado"

    return value


def initialize_session_state() -> None:
    """Inicializa os dados mantidos durante a sessão."""

    default_values = {
        "transcript": None,
        "analysis": None,
        "reviewed_analysis": None,
        "evidence_results": [],
        "transcript_name": None,
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_analysis() -> None:
    """Remove a análise quando uma nova transcrição é carregada."""

    st.session_state.analysis = None
    st.session_state.reviewed_analysis = None
    st.session_state.evidence_results = []


initialize_session_state()


# =========================================================
# CABEÇALHO
# =========================================================

st.title("✦ Meeting Intelligence")

st.write(
    "Assistente de inteligência artificial para transformar reuniões "
    "em atas estruturadas, decisões, tarefas e pendências rastreáveis."
)

st.caption(
    "Responsáveis e prazos são preenchidos somente quando aparecem "
    "explicitamente na transcrição. A versão final permanece sujeita "
    "à revisão humana."
)


# =========================================================
# CONFIGURAÇÃO DA IA
# =========================================================

st.sidebar.header("Configuração da IA")

st.sidebar.caption(
    "Informe uma Trial API Key da Cohere ou utilize a chave "
    "configurada no arquivo .env."
)

cohere_api_key = st.sidebar.text_input(
    "Cohere API Key",
    type="password",
    help=(
        "A chave digitada permanece somente durante a sessão atual "
        "e não é armazenada pela aplicação."
    ),
)

environment_api_key = os.getenv("COHERE_API_KEY")

if cohere_api_key:
    os.environ["COHERE_API_KEY"] = cohere_api_key.strip()
    st.sidebar.success("Chave configurada para esta sessão.")

elif environment_api_key:
    os.environ["COHERE_API_KEY"] = environment_api_key
    st.sidebar.success("Chave carregada pelo ambiente.")

else:
    st.warning(
        "Informe uma Cohere API Key na barra lateral "
        "para utilizar a aplicação."
    )
    st.stop()


# =========================================================
# ENTRADA DA TRANSCRIÇÃO
# =========================================================

st.subheader("1. Forneça uma transcrição")

input_mode = st.radio(
    "Como deseja fornecer o conteúdo?",
    options=[
        "Usar transcrição fictícia do projeto",
        "Enviar arquivo TXT",
        "Colar texto",
    ],
)

transcript_to_load = None
transcript_name = None
pasted_transcript = ""


if input_mode == "Usar transcrição fictícia do projeto":
    if SAMPLE_TRANSCRIPT.exists():
        transcript_to_load = SAMPLE_TRANSCRIPT
        transcript_name = SAMPLE_TRANSCRIPT.name

        st.info(
            "A transcrição demonstrativa contém informações fictícias "
            "e foi criada exclusivamente para testar a aplicação."
        )

    else:
        st.error(
            "A transcrição fictícia não foi encontrada em "
            "data/sample/reuniao_ficticia.txt."
        )


elif input_mode == "Enviar arquivo TXT":
    uploaded_file = st.file_uploader(
        "Selecione uma transcrição",
        type=["txt"],
    )

    if uploaded_file is not None:
        transcript_to_load = uploaded_file
        transcript_name = uploaded_file.name


else:
    pasted_transcript = st.text_area(
        "Cole a transcrição da reunião",
        height=260,
        placeholder=(
            "Ana: Precisamos finalizar o regulamento.\n\n"
            "Bruno: Eu posso revisar até sexta-feira."
        ),
    )

    if pasted_transcript.strip():
        transcript_name = "transcricao_colada.txt"


load_button_disabled = (
    transcript_to_load is None
    and not (
        input_mode == "Colar texto"
        and pasted_transcript.strip()
    )
)

load_button = st.button(
    "Carregar transcrição",
    type="primary",
    disabled=load_button_disabled,
)


if load_button:
    try:
        if input_mode == "Colar texto":
            transcript = normalize_transcript(
                pasted_transcript
            )

            validate_transcript(
                transcript
            )

        else:
            transcript = load_transcript(
                transcript_to_load
            )

        st.session_state.transcript = transcript
        st.session_state.transcript_name = transcript_name

        reset_analysis()

        st.success(
            "Transcrição carregada com sucesso!"
        )

    except Exception as error:
        st.error(
            f"Não foi possível carregar a transcrição: {error}"
        )


# =========================================================
# VISUALIZAÇÃO E ANÁLISE
# =========================================================

if st.session_state.transcript:
    transcript = st.session_state.transcript

    metric_column_1, metric_column_2, metric_column_3 = (
        st.columns(3)
    )

    metric_column_1.metric(
        "Arquivo",
        st.session_state.transcript_name or "Transcrição",
    )

    metric_column_2.metric(
        "Caracteres",
        len(transcript),
    )

    metric_column_3.metric(
        "Linhas",
        len(transcript.splitlines()),
    )

    with st.expander(
        "Visualizar transcrição",
        expanded=False,
    ):
        st.text(transcript)

    st.divider()

    st.subheader("2. Analisar a reunião")

    analyze_button = st.button(
        "Analisar com IA",
        type="primary",
    )

    if analyze_button:
        try:
            with st.spinner(
                "Identificando decisões, tarefas e pendências..."
            ):
                analysis = analyze_meeting(
                    transcript
                )

                evidence_results = (
                    validate_analysis_evidence(
                        analysis=analysis,
                        transcript=transcript,
                    )
                )

                st.session_state.analysis = analysis
                st.session_state.reviewed_analysis = None
                st.session_state.evidence_results = (
                    evidence_results
                )

            st.success(
                "Reunião analisada com sucesso!"
            )

        except Exception as error:
            st.error(
                f"Não foi possível analisar a reunião: {error}"
            )


# =========================================================
# RESULTADOS DA ANÁLISE
# =========================================================

if st.session_state.analysis:
    analysis = st.session_state.analysis
    evidence_results = st.session_state.evidence_results

    st.divider()

    st.subheader("3. Resultado da análise")

    st.markdown(
        f"## {analysis.title}"
    )

    st.markdown("### Resumo")

    st.write(
        analysis.summary
    )

    st.markdown("### Assuntos principais")

    if analysis.topics:
        for topic in analysis.topics:
            st.markdown(
                f"- {topic}"
            )
    else:
        st.info(
            "Nenhum assunto principal foi identificado."
        )


    # =====================================================
    # DECISÕES
    # =====================================================

    st.markdown("### Decisões")

    if analysis.decisions:
        for index, decision in enumerate(
            analysis.decisions,
            start=1,
        ):
            with st.container(border=True):
                st.markdown(
                    f"**Decisão {index}:** "
                    f"{decision.description}"
                )

                st.caption(
                    f'Evidência: "{decision.evidence}"'
                )

                explicit_status = (
                    "Sim"
                    if decision.explicitly_mentioned
                    else "Não"
                )

                st.write(
                    "**Explicitamente mencionada:** "
                    f"{explicit_status}"
                )

    else:
        st.info(
            "Nenhuma decisão explícita foi identificada."
        )


    # =====================================================
    # TAREFAS EXTRAÍDAS
    # =====================================================

    st.markdown("### Tarefas e encaminhamentos")

    if analysis.action_items:
        for index, action_item in enumerate(
            analysis.action_items,
            start=1,
        ):
            with st.container(border=True):
                st.markdown(
                    f"#### Tarefa {index}"
                )

                st.write(
                    action_item.task
                )

                owner_column, deadline_column = (
                    st.columns(2)
                )

                owner_column.metric(
                    "Responsável",
                    format_optional_value(
                        action_item.owner
                    ),
                )

                deadline_column.metric(
                    "Prazo",
                    format_optional_value(
                        action_item.deadline
                    ),
                )

                st.caption(
                    f'Evidência: "{action_item.evidence}"'
                )

                explicit_status = (
                    "Sim"
                    if action_item.explicitly_mentioned
                    else "Não"
                )

                st.write(
                    "**Explicitamente mencionada:** "
                    f"{explicit_status}"
                )

    else:
        st.info(
            "Nenhuma tarefa explícita foi identificada."
        )


    # =====================================================
    # PENDÊNCIAS
    # =====================================================

    st.markdown("### Pendências")

    if analysis.pending_items:
        for pending_item in analysis.pending_items:
            with st.container(border=True):
                st.write(
                    pending_item.description
                )

                st.caption(
                    f'Evidência: "{pending_item.evidence}"'
                )

    else:
        st.info(
            "Nenhuma pendência foi identificada."
        )


    # =====================================================
    # SUGESTÕES
    # =====================================================

    st.markdown("### Sugestões")

    if analysis.suggestions:
        for suggestion in analysis.suggestions:
            with st.container(border=True):
                st.write(
                    suggestion.description
                )

                st.write(
                    "**Proposta por:** "
                    f"{format_optional_value(suggestion.proposed_by)}"
                )

                suggestion_status = (
                    "Aprovada"
                    if suggestion.approved
                    else "Não aprovada"
                )

                st.write(
                    f"**Status:** {suggestion_status}"
                )

                st.caption(
                    f'Evidência: "{suggestion.evidence}"'
                )

    else:
        st.info(
            "Nenhuma sugestão foi identificada."
        )


    # =====================================================
    # VALIDAÇÃO DAS EVIDÊNCIAS
    # =====================================================

    st.markdown("### Validação das evidências")

    invalid_evidence = [
        result
        for result in evidence_results
        if not result["evidence_found"]
    ]

    validation_column_1, validation_column_2 = (
        st.columns(2)
    )

    validation_column_1.metric(
        "Itens verificados",
        len(evidence_results),
    )

    validation_column_2.metric(
        "Evidências não localizadas",
        len(invalid_evidence),
    )

    if not invalid_evidence:
        st.success(
            "Todas as evidências apresentadas foram localizadas "
            "na transcrição."
        )

    else:
        st.warning(
            "Existem itens cuja evidência não foi localizada "
            "literalmente na transcrição. Revise-os antes do uso."
        )

        for result in invalid_evidence:
            with st.expander(
                f"Revisar: {result['content']}"
            ):
                st.write(
                    f"**Categoria:** {result['category']}"
                )

                st.write(
                    f"**Evidência:** {result['evidence']}"
                )


    # =====================================================
    # REVISÃO HUMANA DAS TAREFAS
    # =====================================================

    st.divider()

    st.subheader("4. Revisar tarefas")

    st.caption(
        "Revise as tarefas antes de gerar a ata final. "
        "A evidência original permanece preservada."
    )

    if analysis.action_items:
        with st.form(
            "action_items_review_form"
        ):
            reviews = []

            for index, action_item in enumerate(
                analysis.action_items,
                start=1,
            ):
                st.markdown(
                    f"#### Tarefa {index}"
                )

                include = st.checkbox(
                    "Incluir na ata final",
                    value=True,
                    key=f"include_task_{index}",
                )

                reviewed_task = st.text_input(
                    "Descrição da tarefa",
                    value=action_item.task,
                    key=f"review_task_{index}",
                )

                (
                    review_owner_column,
                    review_deadline_column,
                ) = st.columns(2)

                reviewed_owner = (
                    review_owner_column.text_input(
                        "Responsável",
                        value=action_item.owner or "",
                        placeholder="Não informado",
                        key=f"review_owner_{index}",
                    )
                )

                reviewed_deadline = (
                    review_deadline_column.text_input(
                        "Prazo",
                        value=action_item.deadline or "",
                        placeholder="Não informado",
                        key=f"review_deadline_{index}",
                    )
                )

                st.text_area(
                    "Evidência original",
                    value=action_item.evidence,
                    disabled=True,
                    key=f"review_evidence_{index}",
                )

                reviews.append(
                    {
                        "include": include,
                        "task": reviewed_task,
                        "owner": reviewed_owner,
                        "deadline": reviewed_deadline,
                    }
                )

                st.divider()

            confirm_review = st.form_submit_button(
                "Confirmar revisão",
                type="primary",
                use_container_width=True,
            )

        if confirm_review:
            try:
                reviewed_analysis = (
                    apply_action_item_reviews(
                        analysis=analysis,
                        reviews=reviews,
                    )
                )

                st.session_state.reviewed_analysis = (
                    reviewed_analysis
                )

                st.success(
                    "Revisão confirmada. Os arquivos finais "
                    "já podem ser gerados."
                )

            except Exception as error:
                st.error(
                    "Não foi possível confirmar a revisão: "
                    f"{error}"
                )

    else:
        st.info(
            "Nenhuma tarefa foi identificada para revisão."
        )

        st.session_state.reviewed_analysis = analysis


    # =====================================================
    # PRÉVIA DA REVISÃO
    # =====================================================

    if st.session_state.reviewed_analysis:
        reviewed_analysis = (
            st.session_state.reviewed_analysis
        )

        st.markdown("### Prévia das tarefas revisadas")

        if reviewed_analysis.action_items:
            for index, action_item in enumerate(
                reviewed_analysis.action_items,
                start=1,
            ):
                with st.container(border=True):
                    st.markdown(
                        f"**Tarefa {index}:** "
                        f"{action_item.task}"
                    )

                    st.write(
                        "**Responsável:** "
                        f"{format_optional_value(action_item.owner)}"
                    )

                    st.write(
                        "**Prazo:** "
                        f"{format_optional_value(action_item.deadline)}"
                    )

                    st.caption(
                        f'Evidência original: "{action_item.evidence}"'
                    )

        else:
            st.warning(
                "Todas as tarefas foram removidas da versão final."
            )


    # =====================================================
    # DOWNLOADS
    # =====================================================

    st.divider()

    st.subheader("5. Baixar os resultados")

    final_analysis = st.session_state.reviewed_analysis

    if final_analysis is None:
        st.info(
            "Confirme a revisão das tarefas para liberar "
            "os arquivos finais."
        )

    else:
        markdown_content = export_minutes_to_markdown(
            final_analysis
        )

        csv_content = export_action_items_to_csv(
            final_analysis
        )

        json_content = export_analysis_to_json(
            final_analysis
        )

        (
            download_column_1,
            download_column_2,
            download_column_3,
        ) = st.columns(3)

        download_column_1.download_button(
            label="Baixar ata em Markdown",
            data=markdown_content,
            file_name="ata_reuniao.md",
            mime="text/markdown",
            use_container_width=True,
        )

        download_column_2.download_button(
            label="Baixar tarefas em CSV",
            data=csv_content.encode("utf-8-sig"),
            file_name="tarefas_reuniao.csv",
            mime="text/csv",
            use_container_width=True,
        )

        download_column_3.download_button(
            label="Baixar análise em JSON",
            data=json_content,
            file_name="analise_reuniao.json",
            mime="application/json",
            use_container_width=True,
        )