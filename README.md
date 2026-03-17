# Scout: Autonomous Funding Agent for Nonprofits

🏆 Built at NVIDIA Agents for Impact Hackathon 2026

Scout is an autonomous agentic system designed to help nonprofits discover, evaluate, and apply for grants. Unlike traditional grant search tools, Scout executes a full agentic workflow: reasoning about opportunities, retrieving relevant context from internal documents, and producing actionable outputs like proposal drafts and submission plans.

The system is built to showcase **NVIDIA’s agent ecosystem**, including Nemotron models for reasoning, NIM for inference, and the NeMo Agent Toolkit for orchestration.

---

## 🚩 The Problem

Nonprofits spend significant time on repetitive, inefficient tasks:

- **Manual Searching:** Sifting through dozens of funding sites.
- **Complex RFPs:** Reading lengthy Request for Proposal (RFP) documents.
- **Eligibility Hurdles:** Determining if they meet specific funder criteria.
- **Customization:** Writing tailored proposals for every application.

| Tool Type            | What It Does              |
| :------------------- | :------------------------ |
| **Grant databases**  | Help search opportunities |
| **AI writing tools** | Assist with drafting      |
| **CRM tools**        | Track deadlines           |

**Scout addresses the gap** by combining discovery, eligibility analysis, and proposal preparation into a single automated workflow.

---

## 🚀 Product Overview

Scout takes a nonprofit profile and executes the following sequence:

1.  **Understand:** Processes the nonprofit’s mission and internal documents.
2.  **Discover:** Finds relevant grant opportunities.
3.  **Extract:** Pulls specific eligibility requirements from each grant.
4.  **Compare:** Measures requirements against the nonprofit profile.
5.  **Rank:** Prioritizes opportunities by match quality.
6.  **Generate:** Creates proposal content for the top matches.
7.  **Plan:** Produces a submission checklist and timeline.

---

## 🛠️ System Architecture

The system consists of five main layers:

- **Frontend:** Next.js
- **Backend:** FastAPI
- **Orchestration:** NeMo Agent Toolkit
- **Reasoning Layer:** Nemotron models via NVIDIA NIM
- **Knowledge Layer:** Tools + RAG Retrieval

### Core Technologies

- **Nemotron Models:** Used for high-level reasoning (extraction, scoring, drafting).
  - _Primary:_ Nemotron 3 Super
  - _Fallback/Dev:_ Nemotron 3 Nano
- **NVIDIA NIM:** Provides the inference layer with optimized model serving and a standardized API.
- **NeMo Agent Toolkit:** Manages the router + specialist agent architecture, execution traces, and multi-step workflows.

---

## 🤖 Agent Workflow

Scout utilizes a **Router + Specialist Agent** architecture:

- **Opportunity Discovery Agent:** Searches web and databases for new grants.
- **Requirements Extraction Agent:** Parses PDFs and web pages for hard/soft criteria.
- **Eligibility Scoring Agent:** Compares nonprofit data against grant requirements.
- **Proposal Drafting Agent:** Generates grounded content based on RAG context.

### Tooling

Agents interact with the environment via specialized tools:

- `search_grants_web`: Search grant websites and funding databases.
- `fetch_page`: Retrieve HTML content.
- `parse_pdf`: Extract text from complex PDF documents.
- `retrieve_context`: Fetch relevant chunks from indexed nonprofit documents.
- `rank_opportunities`: Score grants using profile data.

---

## 📂 Repository Structure

```text
scout/
  app/                  # Next.js frontend
  backend/              # FastAPI Backend
    main.py             # Entry point
    agents/             # Specialist agent definitions
    tools/              # Search, fetch, and parsing tools
    retrieval/          # Ingestion and RAG logic
    workflows/          # NeMo Agent Toolkit workflow orchestration
    prompts/            # System prompts for Nemotron
  docs/                 # Architecture and demo scripts

```

## 📄 RAG Pipeline

Scout uses a lightweight RAG pipeline to ground reasoning in reality:

Ingestion: Processes annual reports, program summaries, and IRS letters.

Chunking & Embedding: Converts documents into searchable vectors.

Retrieval: Injects relevant context into prompts during eligibility analysis and drafting to prevent hallucinations.
