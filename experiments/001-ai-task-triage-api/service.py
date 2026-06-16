import json

from openai import OpenAI

from schemas import TriageResponse


TRIAGE_JSON_SCHEMA = {
    "name": "task_triage",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "category": {
                "type": "string",
                "enum": [
                    "incident",
                    "performance",
                    "deployment",
                    "bug",
                    "security",
                    "support",
                    "other",
                ],
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high", "critical"],
            },
            "summary": {"type": "string"},
            "missing_information": {
                "type": "array",
                "items": {"type": "string"},
            },
            "human_review_required": {"type": "boolean"},
            "confidence": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
            },
        },
        "required": [
            "category",
            "priority",
            "summary",
            "missing_information",
            "human_review_required",
            "confidence",
        ],
    },
    "strict": True,
}


def triage_request(request_text: str, model: str = "gpt-4.1-mini") -> TriageResponse:
    client = OpenAI()
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You triage synthetic engineering requests. Return only the "
                    "requested structured JSON. Do not include company data, secrets, "
                    "or unsupported fields."
                ),
            },
            {"role": "user", "content": request_text},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": TRIAGE_JSON_SCHEMA,
        },
    )

    content = completion.choices[0].message.content
    return TriageResponse.model_validate(json.loads(content))
