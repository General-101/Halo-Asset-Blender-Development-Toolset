import os
import json

from pathlib import Path

def create_release_notes():
    event_path = os.environ["GITHUB_EVENT_PATH"]
    with open(event_path, encoding="utf-8") as file:
        event = json.load(file)

    commits = event.get("commits", [])
    notes = []
    for commit in commits:
        commit_id = commit["id"][:7]
        message = commit.get("message", "").strip()

        notes.append(f"Commit ({commit_id}):\n{message}")

    if not notes:
        notes.append("No commit details were provided in the push event.")

    output_path = Path("release_notes.md")

    output_path.write_text("\n\n".join(notes) + "\n", encoding="utf-8",)

    print(f"Generated release notes for {len(commits)} commit(s).")
    print(f"Output: {output_path.resolve()}")

if __name__ == "__main__":
    create_release_notes()
