# OpsIntel AI: Stateful Multi-Agent Document Auditor

OpsIntel AI is an enterprise-grade, multi-agent orchestration pipeline that automates the extraction, validation, and reporting of unstructured corporate operations files. Built with **LangGraph** and **Google Gemini**, the system moves past standard linear workflows by introducing autonomous **self-correction loops** and **Human-in-the-Loop (HITL)** escalations.

---

## 🏗️ Architectural Topology

Unlike standard sequential scripts, OpsIntel AI relies on a stateful graph topology that monitors data schemas throughout the lifecycle of execution:

```unset
                 ┌─────────────────── [ Raw Unstructured Document ]
                 │                               │
                 ▼                               ▼
      ┌────────────────────┐          ┌────────────────────┐
      │   State Manager    │ ◄─────── │ 01. Extractor Agent│ 
      │ (LangGraph Memory) │          └────────────────────┘
      └─────────┬──────────┘                     ▲
                │                                │ (If Validation Fails:
                ▼                                │  Loops back with Error Logs)
      ┌────────────────────┐                     │
      │ 02. Validator Agent│ ────────────────────┘
      └─────────┬──────────┘
                │
                ├─► [Confidence < 80%] ──► [ Webhook Dispatcher ] ──► (Slack/Discord Alert)
                │
                ▼ [Confidence Passes]
      ┌────────────────────┐
      │ 03. Reporter Agent │ ──► [ Markdown Audit Reports & ERP Ready Payloads ]
      └────────────────────┘
```

---

## 🤖 Core Agent Ecosystem

### 01. The Extractor Agent
*   **Technology:** Gemini 2.5-Flash + Pydantic Schema Enforcement
*   **Function:** Parses multi-line, unstructured text files and extracts core token signatures into strongly-typed data payloads (`vendor_name`, `payment_terms`, `total_value`, `governing_law`).

### 02. The Validator Agent
*   **Technology:** Hybrid Logic (Probabilistic LLM Evaluation + Deterministic Code Contracts)
*   **Function:** Cross-checks variables against corporate governance rules (e.g., negative balance checks, forbidden term alerts, ERP registered vendor authorization). If a rule fails, it updates the state with logs and returns control to the Extractor.

### 03. The Reporter Agent
*   **Technology:** Event-Driven Webhooks (Slack/Discord API Integration)
*   **Function:** Compiles human-readable Markdown summaries and dispatches high-priority contextual telemetry alerts directly to corporate communications channels when thresholds drop below compliance levels.

---

## 🛠️ Stack & Dependencies

*   **Orchestration Engine:** LangGraph (Stateful directed graph tracking)
*   **LLM Provider:** Google GenAI SDK (`gemini-2.5-flash`)
*   **Data Layouts:** Pydantic V2
*   **Dashboard Wrapper:** Streamlit
*   **Configuration Manager:** Python-Dotenv

---

## ⚙️ Quickstart Installation Guide

### 1. Clone & Install Dependencies
Ensure you have Python 3.10+ installed locally, then install the system packages:
```bash
pip install streamlit google-genai langgraph pydantic python-dotenv
```

### 2. Configure Local Environment Secrets
Create a `.env` file in the root workspace folder to isolate infrastructure tokens securely:
```ini
GEMINI_API_KEY=AIzaSyYourActualKeyHere...
OPERATIONS_WEBHOOK_URL=https://discord.com
```

### 3. Run the System Interface
Launch the clean, minimal dashboard built using modern visual theories:
```bash
streamlit run gui.py
```

---

## 📋 Target Data Sample Structure
To test the loopback pipeline, upload a `.txt` file containing content configured to fail initial financial boundary thresholds, such as:
```text
Agreement Overview: Unknown Startup Ltd has submitted an invoice for a total value of -\$5000. Payment terms are mapped to Net 90.
```
