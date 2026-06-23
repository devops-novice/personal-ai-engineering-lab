import json
import urllib.request
import urllib.error
from pathlib import Path


API_URL = "http://localhost:8000/triage"
RESULTS_FILE = Path(__file__).parent / "results.json"


TEST_INPUTS = [
    {
        "id": 1,
        "request": "Deployment failed twice after latest release and login is slow."
    },
    {
        "id": 2,
        "request": "Something is wrong with the application."
    },
    {
        "id": 3,
        "request": "Can we improve dashboard loading time next quarter?"
    },
    {
        "id": 4,
        "request": "Users are reporting payment failures after checkout."
    },
    {
        "id": 5,
        "request": "Please add dark mode to the admin portal."
    },
    {
        "id": 6,
        "request": "The service is throwing 500 errors after database migration."
    },
    {
        "id": 7,
        "request": "Need help understanding why build pipeline is slower."
    },
    {
        "id": 8,
        "request": "Security scan found critical vulnerabilities in dependencies."
    },
    {
        "id": 9,
        "request": "It does not work."
    },
    {
        "id": 10,
        "request": "Memory usage increased after yesterday's deployment."
    },
]


def call_triage_api(request_text: str) -> dict:
    payload = json.dumps({"request": request_text}).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {
            "error": f"HTTP {exc.code}",
            "detail": exc.read().decode("utf-8"),
        }
    except Exception as exc:
        return {
            "error": type(exc).__name__,
            "detail": str(exc),
        }


def main() -> None:
    results = []

    print("input_id | category | priority | confidence | human_review_required")
    print("-" * 70)

    for item in TEST_INPUTS:
        response = call_triage_api(item["request"])

        result = {
            "input_id": item["id"],
            "request": item["request"],
            "response": response,
        }

        results.append(result)

        print(
            f"{item['id']} | "
            f"{response.get('category', 'ERROR')} | "
            f"{response.get('priority', 'ERROR')} | "
            f"{response.get('confidence', 'ERROR')} | "
            f"{response.get('human_review_required', 'ERROR')}"
        )

    RESULTS_FILE.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved full results to: {RESULTS_FILE}")


if __name__ == "__main__":
    main()
