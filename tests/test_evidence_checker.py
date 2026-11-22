from pathlib import Path

from src.evidence_checker import validate_analysis_evidence
from src.meeting_analyzer import analyze_meeting
from src.transcript_loader import load_transcript


transcript = load_transcript(
    Path("data/sample/reuniao_ficticia.txt")
)

analysis = analyze_meeting(transcript)

results = validate_analysis_evidence(
    analysis=analysis,
    transcript=transcript,
)

for result in results:
    print(
        result["category"],
        "|",
        result["evidence_found"],
        "|",
        result["content"],
    )

invalid_results = [
    result
    for result in results
    if not result["evidence_found"]
]

print()
print("Total validado:", len(results))
print(
    "Evidências não localizadas:",
    len(invalid_results),
)