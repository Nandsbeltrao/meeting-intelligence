from pathlib import Path

from src.meeting_analyzer import analyze_meeting
from src.minutes_generator import generate_meeting_minutes
from src.transcript_loader import load_transcript


transcript = load_transcript(
    Path("data/sample/reuniao_ficticia.txt")
)

analysis = analyze_meeting(transcript)

minutes = generate_meeting_minutes(
    analysis
)

output_path = Path(
    "data/sample/ata_ficticia.md"
)

output_path.write_text(
    minutes,
    encoding="utf-8",
)

print(minutes)
print()
print(
    f"Ata criada em: {output_path}"
)