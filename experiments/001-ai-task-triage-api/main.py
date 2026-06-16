from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from audit import write_audit_event
from schemas import TriageRequest, TriageResponse
from service import triage_request


app = FastAPI(title="Experiment 001: AI Task Triage API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/triage", response_model=TriageResponse)
def triage(payload: TriageRequest) -> TriageResponse:
    request_id = str(uuid4())

    try:
        result = TriageResponse.model_validate(triage_request(payload.request))
    except ValidationError as exc:
        raise HTTPException(
            status_code=502,
            detail="Model response failed schema validation.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to triage request.",
        ) from exc

    write_audit_event(
        request_id=request_id,
        request_text=payload.request,
        result=result,
    )
    return result
