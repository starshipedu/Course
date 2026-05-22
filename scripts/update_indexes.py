import json
from pathlib import Path
from datetime import date

ROOT = Path("Database/per-university")

today = date.today().isoformat()

for country_folder in ROOT.iterdir():

    if not country_folder.is_dir():
        continue

    print(f"\nProcessing {country_folder.name}")

    universities = []
    total_programs = 0
    total_universities = 0

    country = None
    country_display = None

    for json_file in country_folder.glob("*.json"):

        if json_file.name in ["index.json", "summary.json"]:
            continue

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            program_count = len(data.get("programs", []))

            data["totalPrograms"] = program_count
            data["lastUpdated"] = today

            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(
                    data,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            universities.append({
                "id": data["id"],
                "name": data["name"],
                "totalPrograms": program_count,
                "logo": data.get("logo", "")
            })

            total_programs += program_count
            total_universities += 1

            country = data.get("country")
            country_display = data.get("countryDisplay")

            print(f"✓ {data['name']} ({program_count})")

        except Exception as e:
            print(f"✗ Error {json_file.name}: {e}")

    universities.sort(key=lambda x: x["name"])

    index_path = country_folder / "index.json"

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(
            universities,
            f,
            indent=2,
            ensure_ascii=False
        )

    summary = {
        "country": country,
        "countryDisplay": country_display,
        "totalUniversities": total_universities,
        "totalPrograms": total_programs,
        "lastUpdated": today
    }

    summary_path = country_folder / "summary.json"

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(
            summary,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Updated {country_folder.name}: "
        f"{total_universities} universities, "
        f"{total_programs} programs"
    )

print("\nAll done!")
