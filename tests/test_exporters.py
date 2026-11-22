from pathlib import Path

from src.exporters import (
    export_action_items_to_csv,
    export_analysis_to_json,
    export_minutes_to_markdown,
)
from src.meeting_analyzer import analyze_meeting
from src.transcript_loader import load_transcript


transcript_path = Path(
    "data/sample/reuniao_ficticia.txt"
)

transcript = load_transcript(
    transcript_path
)

analysis = analyze_meeting(
    transcript
)

markdown_content = export_minutes_to_markdown(
    analysis
)

csv_content = export_action_items_to_csv(
    analysis
)

json_content = export_analysis_to_json(
    analysis
)

markdown_path = Path(
    "data/sample/ata_exportada.md"
)

csv_path = Path(
    "data/sample/tarefas_exportadas.csv"
)

json_path = Path(
    "data/sample/analise_exportada.json"
)

markdown_path.write_text(
    markdown_content,
    encoding="utf-8",
)

csv_path.write_text(
    csv_content,
    encoding="utf-8-sig",
)

json_path.write_text(
    json_content,
    encoding="utf-8",
)

print("Arquivos criados:")
print(markdown_path)
print(csv_path)
print(json_path)

print()
print("Prévia do CSV:")
print(csv_content)