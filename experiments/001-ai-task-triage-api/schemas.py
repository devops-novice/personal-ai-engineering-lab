from typing import Literal

from pydantic import BaseModel, Field


class TriageRequest(BaseModel):
    request: str = Field(..., min_length=1, description="Engineering request to triage")


class TriageResponse(BaseModel):
    category: Literal[
        "incident",
        "performance",
        "deployment",
        "bug",
        "security",
        "support",
        "other",
    ]
    priority: Literal["low", "medium", "high", "critical"]
    summary: str = Field(..., min_length=1)
    missing_information: list[str]
    human_review_required: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
