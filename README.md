# AskPharmova: Agentic RAG Medical Chatbot

A sophisticated medical information chatbot that combines **Agentic Retrieval-Augmented Generation (RAG)** with multi-loop fact verification to deliver accurate, evidence-based health information sourced exclusively from trusted medical authorities.

## Overview

AskPharmova is designed to answer medical questions with clinical accuracy by integrating an intelligent agent-based retrieval system that iteratively validates and enriches medical context before generating responses. Rather than relying on single-pass retrieval, the system uses a feedback loop to identify information gaps and refine search queries until sufficient evidence is gathered.

## Agentic RAG Architecture

The core innovation of AskPharmova is its **loop-based agentic architecture** that treats information retrieval as an iterative refinement process:

```
User Query
    ↓
[1] CLASSIFY → Is this a medical question?
    ↓ (if YES)
[2] DECOMPOSE → Break into search queries (multi-context reformulation)
    ↓
[3] RETRIEVE → Search trusted medical sources (Tavily + domain filters)
    ↓
[4] ASSEMBLE → Organize retrieved documents into a unified context block
    ↓
[5] EVALUATE → Is the context sufficient to answer? (Critic Agent)
    ↓
    ├─→ [YES] → Generate response and render citations
    │
    └─→ [NO] → Identify missing info → LOOP (back to [2]) up to max_loops=2
    
Follow-up Query Detection
    ↓
[Check Topic Relevance] → Is this related to the previous query?
    ↓ (if NO) → Start fresh agentic loop
    └─ (if YES) → Use cached context + add conversation history
```

### Key Architectural Principles

1. **Query Classification** - Rejects non-medical queries before consuming retrieval budget
2. **Multi-Context Decomposition** - Splits complex medical questions into targeted search queries
3. **Deterministic Context Evaluation** - Uses a specialized Critic Agent to assess information completeness
4. **Corrective Reformulation** - When gaps are identified, refines search strategy based on missing information
5. **Citation Grounding** - Every response is traced back to specific sources with clickable links

## Pipeline Components

### 1. **Classifier** (`pipeline/classifier.py`)
- **Model**: Llama 3.1 8B (Groq API)
- **Role**: Binary classification of whether a query is medically relevant
- **Output**: Boolean flag to enable/disable further processing
- **Also provides**: Topic relevance checking for follow-up conversations

### 2. **Reformulator** (`pipeline/reformulator.py`)
- **Model**: Llama 3.1 8B (Groq API)
- **Role**: Decomposes complex medical questions into multiple targeted search queries
- **Modes**: 
  - Initial decomposition for new queries
  - Corrective reformulation when information gaps are detected
- **Output**: JSON list of search queries
- **Handles**: Multi-context clinical topics (e.g., "What are treatment options for diabetes?" → searches for symptoms, medications, lifestyle changes, complications)

### 3. **Retriever** (`pipeline/retriever.py`)
- **Search Engine**: Tavily API
- **Domain Filter**: Restricts results to 10 trusted medical sources (PubMed, NIH, Mayo Clinic, etc.)
- **Query Strategy**: Executes all reformulated queries and deduplicates results
- **Output**: List of documents with URL, title, and content snippets

### 4. **Assembler** (`pipeline/assembler.py`)
- **Role**: Consolidates raw retrieval results into a structured context block
- **Format**: Numbered source references with URL-to-content mapping
- **Output**: 
  - `context_block`: Formatted text for the generator
  - `source_map`: Dictionary mapping citation numbers to URLs and titles

### 5. **Critic Agent** (`pipeline/critic.py`)
- **Model**: Llama 3.1 8B (Groq API)
- **Role**: Evaluates whether retrieved context is sufficient to answer the original query
- **Decision Logic**: Returns JSON with `sufficient` (bool) and `missing_info` (str) fields
- **Integration**: Drives the agentic loop—if insufficient, triggers corrective reformulation
- **Temperature**: 0.0 for deterministic verification

### 6. **Generator** (`pipeline/generator.py`)
- **Model**: Gemini 2.5 Flash (Google Generative AI)
- **Role**: Synthesizes clinical responses grounded in retrieved context
- **Modes**:
  - Initial response generation (new query)
  - Follow-up response generation (includes conversation history)
- **System Prompt**: Enforces strict adherence to provided sources, markdown formatting, and medical accuracy
- **Output**: Rich markdown response with embedded citation markers

### 7. **Orchestrator** (`pipeline/orchestrator.py`)
- **Role**: Coordinates the entire agentic loop with state management
- **Features**:
  - Stateful multi-loop execution (up to 2 loops by default)
  - Yields live progress updates for UI rendering
  - Handles policy violations (non-medical redirects)
  - Tracks sufficient context, missing info, and loop count
- **Output**: Stream of status updates + final state dict

## Key Features

### 🔄 **Iterative Context Refinement**
- Queries are processed up to 2 times: initial retrieval + optional corrective loop
- If the Critic detects missing information (e.g., "treatment options not covered"), the system reformulates and retrieves again
- Prevents gaps in medical evidence before generation

### 🏥 **Trusted Source Filtering**
Restricts all searches to medically authoritative domains:
- PubMed (pubmed.ncbi.nlm.nih.gov)
- NIH (nih.gov)
- Mayo Clinic (mayoclinic.org)
- WHO (who.int)
- New England Journal of Medicine (nejm.org)
- NHS, CDC, BMJ, MedlinePlus, and Nature

### 📎 **Interactive Citations**
- Every claim in the response is tagged with a source reference
- Rendered as clickable markdown links in the Streamlit UI
- Full source metadata displayed in a "Sources" section below responses

### 🔗 **Conversation Continuity**
- Follow-up questions within the same medical topic reuse cached context
- Topic relevance detection prevents context drift
- Conversation history is passed to the generator for coherent multi-turn dialogs

### 🛡️ **Policy Enforcement**
- Non-medical queries are detected and redirected with a clear message
- Prevents misuse as a general-purpose chatbot

## Setup & Installation

### Prerequisites
- Python 3.8+
- API keys for:
  - **Groq** (for Classifier, Reformulator, Critic agents)
  - **Google Generative AI** (for Generator)
  - **Tavily** (for medical source search)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd askPharmova
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Dependencies
- **streamlit** - Web UI framework
- **groq** - Groq API client (Classifier, Reformulator, Critic)
- **google-genai** - Google Generative AI client (Generator)
- **tavily-python** - Medical search API
- **python-dotenv** - Environment variable management

## Running the Application

```bash
streamlit run app.py
```

The chatbot will be available at `http://localhost:8501`

## Usage Examples

### Example 1: Complex Multi-Context Query
**User Input**: *"What are the treatment options for type 2 diabetes?"*

**Agentic Flow**:
1. Classifier confirms it's medical
2. Reformulator breaks it into: `["type 2 diabetes treatments", "medication options for diabetes", "lifestyle management diabetes", "diabetes complications prevention"]`
3. First loop retrieves documents on medications, insulin, lifestyle changes
4. Critic evaluates: "Missing information on newer GLP-1 medications and their effectiveness"
5. Second loop reformulates: `["GLP-1 agonists diabetes treatment", "semaglutide tirzepatide effectiveness"]`
6. Context now sufficient → Generator synthesizes comprehensive response with citations
7. Response includes medication classes, lifestyle strategies, and emerging treatments all grounded in sources

### Example 2: Follow-up Question
**Previous Query**: *"How is diabetes diagnosed?"*
**Follow-up**: *"What do the blood glucose levels mean?"*

**Agentic Flow**:
1. Topic relevance check confirms it's related to diabetes
2. Skip reformulation loop, reuse cached context
3. Generator adds conversation history context
4. Response addresses the follow-up while maintaining narrative continuity

## Model Configuration

All models are configured in `config.py`:

| Component | Model | Provider | Temperature |
|-----------|-------|----------|-------------|
| Classifier | Llama 3.1 8B Instant | Groq | 0.0 |
| Reformulator | Llama 3.1 8B Instant | Groq | 0.1 |
| Critic | Llama 3.1 8B Instant | Groq | 0.0 |
| Generator | Gemini 2.5 Flash | Google GenAI | 0.2 |

**Low temperatures** are used for task agents (classification, fact-checking) to ensure determinism. The generator uses slightly higher temperature (0.2) for natural language quality while remaining grounded in sources.

## Project Structure

```
askPharmova/
├── app.py                          # Streamlit UI + session management
├── config.py                       # Global configuration & trusted sources
├── requirements.txt                # Python dependencies
├── .env                           # API keys (git-ignored)
├── .env.example                   # API key template
│
├── pipeline/                       # Core agentic RAG components
│   ├── orchestrator.py            # Multi-loop orchestration engine
│   ├── classifier.py              # Medical relevance + topic checking
│   ├── reformulator.py            # Query decomposition & correction
│   ├── retriever.py               # Tavily integration + domain filtering
│   ├── assembler.py               # Context block assembly
│   ├── critic.py                  # Sufficiency evaluation agent
│   └── generator.py               # Response synthesis with Gemini
│
├── prompts/                        # Agent system prompts
│   ├── classifier_prompt.py
│   ├── reformulator_prompt.py
│   ├── critic_prompt.py
│   └── generator_prompt.py
│
├── utils/                          # Utility functions
│   └── citation_utils.py          # Citation rendering & markdown formatting
│
└── tests/                          # Unit tests for each component
```

## Testing

Run component tests to validate the pipeline:

```bash
# Test individual components
python -m pytest tests/test_classifier.py
python -m pytest tests/test_reformulator.py
python -m pytest tests/test_retriever.py
python -m pytest tests/test_critic.py
python -m pytest tests/test_generator.py
```