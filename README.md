```markdown

\# 🛡️ Enterprise AI: Agentic Support Router \& Structured Data Extractor



!\[AI Stack](https://img.shields.io/badge/LangChain-Core%20v0.1-blue?logo=langchain) !\[Validation](https://img.shields.io/badge/Pydantic-v2\_Schema\_Enforcement-red?logo=pydantic) !\[Model](https://img.shields.io/badge/Model-Llama\_3.3\_70B\_Versatile-orange?logo=meta) !\[Frontend](https://img.shields.io/badge/Streamlit-UI-green?logo=streamlit)



An production-grade \*\*Agentic Ticket Routing and Data Extraction System\*\* designed to bridge the gap between unpredictable Large Language Model (LLM) text outputs and rigid enterprise databases/APIs.



\---



\## 🎯 The Engineering Problem \& Solution

In enterprise production environments, LLMs inherently output conversational, non-deterministic text (e.g., Markdown, floating strings) that breaks downstream software systems, databases, and automated APIs.



\*\*This system addresses three critical failure modes of standard Generative AI:\*\*

1\. \*\*Hallucination \& Syntax Leakage:\*\* Utilizes \*\*Pydantic v2 schemas\*\* coupled with native LLM function/tool calling to force deterministic JSON contracts. Incorrect data types or conversational fluff are completely suppressed.

2\. \*\*Monolithic Token Waste (Prompt Stuffing):\*\* Instead of evaluating massive prompts with dozens of extraction schemas simultaneously, the pipeline employs a \*\*Two-Stage Routing Architecture\*\* to isolate context windows and minimize input token overhead.

3\. \*\*Model Routing Optimization:\*\* Implements a modular routing decision engine that first categorizes unstructured inputs and computes urgency before activating domain-specific structured extractors.



\---



\## 🏛️ Architecture Pipeline



```text

\[ Unstructured Customer Email ]

&#x20;             │

&#x20;             ▼

&#x20;   ┌──────────────────┐

&#x20;   │  AI Router Agent │  ──(Enforces: RouteDecision Pydantic Schema)

&#x20;   └──────────────────┘

&#x20;             │

&#x20;    ┌────────┴────────┐

&#x20;    ▼                 ▼

\[ Category: Billing ] \[ Category: Tech Bug ]

&#x20;    │                 │

&#x20;    ▼                 ▼

┌───────────────┐ ┌────────────────────┐

│ Billing Schema│ │ Tech Bug Schema    │ ──(Enforces Domain-Specific Types:

└───────────────┘ └────────────────────┘    Floats, Literals, Arrays)

&#x20;    │                 │

&#x20;    ▼                 ▼

\[ Strictly Validated Production JSON Payload ]

```



\---



\## 🛠️ Technical Stack \& Architectural Decisions



| Component | Technology | Engineering Rationale |

| :--- | :--- | :--- |

| \*\*Validation Layer\*\* | \*\*Pydantic v2\*\* | Serves as a deterministic firewall. Enforces strict types (`Literal`, `Optional`, `float`, arrays) so runtime exceptions are caught \*before\* payloads hit databases. |

| \*\*Orchestration\*\* | \*\*LangChain Core\*\* | Utilizes `.with\_structured\_output()` to natively bind Python classes directly to LLM tool-calling endpoints, enabling model-agnostic modularity. |

| \*\*Inference Engine\*\* | \*\*Groq API\*\* | Provides ultra-low latency token generation, necessary for asynchronous automated triage systems requiring near-instantaneous response times. |

| \*\*Language Model\*\* | \*\*Llama 3.3 70B Versatile\*\* | Selected over smaller 8B parameters; massive-parameter models demonstrate superior adherence to nested function calling and schema boundaries without syntax leakage. |

| \*\*Interface\*\* | \*\*Streamlit\*\* | Built to rapidly prototype side-by-side verification dashboards separating meta-reasoning routing output from final SQL/API-ready payload data. |



\---



\## 📦 Extracted Schemas (Example Contracts)



\### 1. The Route Decision Schema

Guarantees strict categorization and prevents imaginary priority tagging:

```python

class RouteDecision(BaseModel):

&#x20;   category: Literal\["billing", "technical\_bug", "general\_inquiry"]

&#x20;   urgency: Literal\["low", "medium", "high", "critical"]

&#x20;   reasoning: str = Field(description="1-sentence explanation of classification.")

```



\### 2. Technical Bug Extractor Schema

Transforms frustrated consumer language into Jira/Developer-ready structured data:

```python

class TechnicalBugReport(BaseModel):

&#x20;   issue\_summary: str

&#x20;   device\_or\_os: Optional\[str] = Field(default="Unknown")

&#x20;   error\_codes: List\[str] = Field(default\_factory=list)

&#x20;   reproduction\_steps: List\[str] = Field(default\_factory=list)

&#x20;   customer\_sentiment: Literal\["frustrated", "neutral", "confused", "angry"]

```



\---



\## 🚀 Local Installation \& Run Guide



\### 1. Clone the repository

```bash

git clone https://github.com/YOUR\_GITHUB\_USERNAME/structured-router-agent.git

cd structured-router-agent

```



\### 2. Initialize Virtual Environment

```bash

\# Windows

py -m venv venv

venv\\Scripts\\activate



\# Linux / Mac

python3 -m venv venv

source venv/bin/activate

```



\### 3. Install Dependencies

```bash

pip install -r requirements.txt

```



\### 4. Configure Environment Variables

Create a `.env` file in the project root containing your free Groq AI Key:

```env

GROQ\_API\_KEY="gsk\_your\_api\_key\_here"

```

\*(Get a free API key at \[console.groq.com/keys](https://console.groq.com/keys))\*



\### 5. Execute Web Dashboard

```bash

\# Windows safe command

py -m streamlit run app.py

```

\*The Streamlit visualization server will launch directly at `http://localhost:8501`.\*



\---



\## 📈 Future Production Evolution (Roadmap)

\* \*\*Webhook Ingestion:\*\* Replace UI with a headless FastAPI endpoint designed to asynchronously process incoming payloads directly from Gmail APIs, Zendesk, or Salesforce webhooks.

\* \*\*Automated Dispatch Integration:\*\* Directly map `TechnicalBugReport` JSON outputs to \*\*Jira REST APIs\*\* for zero-touch bug ticket creation, and map `BillingInquiry` outputs to \*\*Stripe / SQL auditing logs\*\*.

```

