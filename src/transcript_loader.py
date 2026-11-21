from pathlib import Path
from typing import BinaryIO, TextIO


MINIMUM_TRANSCRIPT_LENGTH = 50


def decode_content(raw_content: bytes) -> str:
    """Decodifica o conteúdo utilizando formatos comuns de texto."""

    encodings = ["utf-8", "utf-8-sig", "latin-1"]

    for encoding in encodings:
        try:
            return raw_content.decode(encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError(
        "Não foi possível identificar a codificação do arquivo."
    )


def normalize_transcript(text: str) -> str:
    """Remove espaços excessivos sem alterar o conteúdo da reunião."""

    normalized_lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    return "\n".join(normalized_lines)


def validate_transcript(text: str) -> None:
    """Valida se existe conteúdo suficiente para análise."""

    if not text or not text.strip():
        raise ValueError(
            "A transcrição está vazia."
        )

    if len(text.strip()) < MINIMUM_TRANSCRIPT_LENGTH:
        raise ValueError(
            "A transcrição é muito curta para uma análise confiável."
        )


def load_transcript(
    file: Path | BinaryIO | TextIO,
) -> str:
    """Lê e valida uma transcrição em formato TXT."""

    if isinstance(file, Path):
        extension = file.suffix.lower()
        raw_content = file.read_bytes()
    else:
        file_name = getattr(file, "name", "")
        extension = Path(file_name).suffix.lower()
        raw_content = file.read()

    if extension != ".txt":
        raise ValueError(
            "Formato não suportado. Envie um arquivo TXT."
        )

    if isinstance(raw_content, str):
        text = raw_content
    else:
        text = decode_content(raw_content)

    normalized_text = normalize_transcript(text)

    validate_transcript(normalized_text)

    return normalized_text