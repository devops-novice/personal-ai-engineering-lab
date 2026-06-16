import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from schemas import TriageResponse


DEFAULT_AUDIT_LOG = Path(__file__).with_name("audit.log")


def request_hash(request_text: str) -> str:
    return hashlib.sha256(request_text.encode("utf-8")).hexdigest()


def write_audit_event(
    *,
    request_id: str,
    request_text: str,
    result: TriageResponse,
    audit_log_path: Path = DEFAULT_AUDIT_LOG,
) -> None:
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "input_length": len(request_text),
        "input_sha256": request_hash(request_text),
        "category": result.category,
        "priority": result.priority,
        "confidence": result.confidence,
        "human_review_required": result.human_review_required,
    }

    with audit_log_path.open("a", encoding="utf-8") as audit_file:
        audit_file.write(json.dumps(event, sort_keys=True) + "\n")
