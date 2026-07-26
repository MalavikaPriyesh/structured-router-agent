# Structured Router Agent

LangChain Core v0.1 | Pydantic v2 Schema Enforcement | Llama 3.3 70B Versatile | Streamlit

A production-grade agentic ticket routing and data extraction system. It takes unstructured customer support messages and converts them into strictly validated JSON that downstream systems, databases, and APIs can consume without parsing errors.

---

## Problem and Solution

In production, LLMs output conversational, non-deterministic text. Paragraphs, markdown formatting, and floating strings break downstream software. If an API expects an integer for a dollar amount and the model outputs "$149 dollars", the system crashes.

This project addresses three common failure modes:

1. Hallucination and syntax leakage. Pydantic v2 schemas coupled with native LLM tool calling force deterministic JSON contracts. Incorrect data types or conversational filler are suppressed at the validation layer.
2. Monolithic token waste. Instead of stuffing a single prompt with dozens of extraction schemas, the pipeline uses a two-stage routing architecture to isolate context windows and reduce input token overhead.
3. Model routing optimization. A modular routing decision engine categorizes unstructured inputs and evaluates urgency before activating domain-specific structured extractors.

---

## Architecture

```text
[ Unstructured Customer Email ]
              |
              v
    +------------------+
    |  AI Router Agent |  -- (Enforces: RouteDecision Pydantic Schema)
    +------------------+
              |
     +--------+--------+
     v                 v
[ Category: Billing ] [ Category: Tech Bug ]
     |                 |
     v                 v
+---------------+ +----------------------+
| Billing Schema| | Tech Bug Schema      | -- (Enforces Domain-Specific Types:
+---------------+ +----------------------+    Floats, Literals, Arrays)
     |                 |
     v                 v
[ Strictly Validated Production JSON Payload ]
```

---

## Tech Stack and Decisions

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| Validation Layer | Pydantic v2 | Acts as a deterministic firewall. Enforces strict types (Literal, Optional, float, arrays) so runtime exceptions are caught before payloads hit databases. |
| Orchestration | LangChain Core | Uses `.with_structured_output()` to bind Python classes directly to LLM tool-calling endpoints. Keeps the pipeline model-agnostic. |
| Inference Engine | Groq API | Ultra-low latency token generation. Required for asynchronous automated triage systems that need near-instantaneous response times. |
| Language Model | Llama 3.3 70B Versatile | Chosen over smaller 8B models. Larger parameter counts demonstrate better adherence to nested function calling and schema boundaries without syntax leakage. |
| Interface | Streamlit | Used to prototype a side-by-side verification dashboard separating meta-reasoning output from final SQL/API-ready payload data. |

---

## Extracted Schemas

### Route Decision Schema

Guarantees strict categorization and prevents the model from inventing priority levels.

```python
class RouteDecision(BaseModel):
    category: Literal["billing", "technical_bug", "general_inquiry"]
    urgency: Literal["low", "medium", "high", "critical"]
    reasoning: str = Field(description="1-sentence explanation of classification.")
```

### Technical Bug Extractor Schema

Turns frustrated consumer language into structured data a developer or Jira ticket can actually use.

```python
class TechnicalBugReport(BaseModel):
    issue_summary: str
    device_or_os: Optional[str] = Field(default="Unknown")
    error_codes: List[str] = Field(default_factory=list)
    reproduction_steps: List[str] = Field(default_factory=list)
    customer_sentiment: Literal["frustrated", "neutral", "confused", "angry"]
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/structured-router-agent.git
cd structured-router-agent
```

### 2. Initialize Virtual Environment

```bash
# Windows
py -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with your Groq API key:

```env
GROQ_API_KEY="gsk_your_api_key_here"
```

You can get a free key at https://console.groq.com/keys.

### 5. Run the App

```bash
# Windows
py -m streamlit run app.py
```

The dashboard will open at http://localhost:8501.

---

## Future Work

- Webhook Ingestion: Replace the Streamlit UI with a headless FastAPI endpoint to process incoming payloads from Gmail APIs, Zendesk, or Salesforce webhooks.
- Automated Dispatch: Map `TechnicalBugReport` JSON outputs to the Jira REST API for zero-touch ticket creation. Map `BillingInquiry` outputs to Stripe or a SQL database for automated auditing.
```
