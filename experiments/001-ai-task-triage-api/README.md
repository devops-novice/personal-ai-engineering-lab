# Experiment 001: AI Task Triage API

Goal:
Build a small API that accepts a synthetic engineering request and returns structured triage output using a GPT model.

Example input:
"Deployment failed twice after the latest change and customer login is slow."

Expected output:
A structured JSON response containing category, priority, summary, missing information, human review flag, and confidence.

Learning focus:
- GPT model call
- structured JSON output
- schema validation
- basic audit logging
- failure testing

## Setup

From this folder, install the minimal dependencies:

```bash
pip install -r requirements.txt
```

Set an OpenAI API key in your shell before running the API:

```bash
export OPENAI_API_KEY="your-key"
```

On PowerShell:

```powershell
$env:OPENAI_API_KEY="your-key"
```

## Run

```bash
uvicorn main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Triage request:

```bash
curl -X POST http://127.0.0.1:8000/triage \
  -H "Content-Type: application/json" \
  -d '{"request":"Deployment failed twice after the latest change and login is slow."}'
```

## Test

```bash
pytest
```

Tests mock the model call and do not require a real OpenAI API key.

## Audit Logging

The API writes safe request metadata to `audit.log`. It does not log raw request text, API keys, headers, tokens, or environment variables.

Logged fields:
- timestamp
- request_id
- input_length
- input_sha256
- category
- priority
- confidence
- human_review_required

## Out of Scope

- UI
- database
- RAG
- OpenClaw
- multi-agent workflow
- company data
- authentication
- production deployment
