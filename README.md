# AeroAgent: Autonomous AOG Quoting Engine

**AeroAgent** is a production-grade AI agent designed for **Ahmed Jet Support**. It automates the high-pressure workflow of Aircraft on Ground (AOG) logistics by converting unstructured customer requests into verified, compliant parts quotes.

## Project Overview
In commercial aviation, an AOG situation costs airlines thousands of pounds per hour. The "AOG Desk" must quickly identify parts, check stock, verify interchangeability (alternates), and ensure legal traceability (EASA/FAA certification). 

**AeroAgent** handles this entire pipeline in seconds using the Gemini 2.5 Flash model and a relational SQL backend.

---

## Technical Architecture

AeroAgent follows a modular "Chain of Responsibility" design pattern:

1.  **Extraction Engine (`src/extractor.py`):** Uses LLM-based Named Entity Recognition (NER) to transform chaotic emails into strict JSON parameters.
2.  **Inventory Router (`src/router.py`):** An intelligent SQL engine that checks primary stock. If zero, it autonomously queries the `Alternate_Parts` table for approved substitutes.
3.  **Traceability Validator:** Integrated into the router, it verifies that parts have valid release certificates (EASA Form 1 / FAA 8130-3) before offering them.
4.  **Generative Response (`src/generator.py`):** A context-aware generator that drafts a professional MRO response based on the inventory outcome.



---

## Repository Structure

```text
├── data/
│   └── processed/          # SQLite Database (AeroAgent.db)
├── models/
│   └── .gitkeep            # Prompt templates and model configs
├── notebooks/              # Developmental Phase Notebooks (01-04)
├── reports/
│   └── sample_outputs/     # Success, Alternate, and Out-of-Stock Proofs
├── src/                    # Core Production Source Code
│   ├── database.py         # DB Schema and Seed Logic
│   ├── extractor.py        # AI Extraction Logic
│   ├── router.py           # SQL & Alternate Logic
│   ├── generator.py        # AI Email Drafting
│   └── pipeline.py         # Master Orchestrator
├── .env.example            # Environment Variable Template
├── .gitignore              # Security and Cache rules
└── requirements.txt        # Project Dependencies
