# Experiment 001: AI Task Triage API

Goal:
Build a small API that accepts an engineering request and returns structured triage output using a GPT model.

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

Out of scope:
- RAG
- UI
- database
- multi-agent workflow
- OpenClaw
