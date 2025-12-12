# Architecture Overview

This document explains the system architecture, components, and design decisions for the Modal LLM Evaluator.

## Table of Contents

- [System Overview](#system-overview)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [Scaling Strategy](#scaling-strategy)
- [Design Decisions](#design-decisions)

---

## System Overview

The Modal LLM Evaluator is a serverless application that leverages Modal's infrastructure for parallel LLM evaluation at scale.

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  CLI Client  │  │  Streamlit   │  │  Python API  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
┌────────────────────────────▼──────────────────────────────┐
│                   Orchestration Layer                      │
│                  (Modal Functions)                         │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  evaluate_prompts()  - Main orchestrator             │ │
│  │  run_single_evaluation() - Per-test executor         │ │
│  │  Cost Tracker - Budget monitoring                    │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────────┬──────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │  Parallel Map   │
                    │  (Modal .map()) │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
┌─────────▼────────┐ ┌──────▼──────┐ ┌────────▼────────┐
│  Claude Provider │ │ GPT Provider│ │ Gemini Provider │
│  (Anthropic API) │ │ (OpenAI API)│ │  (Google API)   │
└─────────┬────────┘ └──────┬──────┘ └────────┬────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
┌────────────────────────────▼──────────────────────────────┐
│                    Results Processing                      │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Metrics Calculation                                 │ │
│  │  Cost Aggregation                                    │ │
│  │  Statistical Analysis                                │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────────┬──────────────────────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
┌─────────▼────────┐ ┌──────▼──────┐ ┌────────▼────────┐
│  Excel Export    │ │  CSV Export │ │  Database       │
│  (with summary)  │ │  (raw data) │ │  (Power BI)     │
└──────────────────┘ └─────────────┘ └─────────────────┘
```

---

## Core Components

### 1. **Evaluation Engine** (`evaluator/`)

The core evaluation logic that orchestrates the entire process.

**Files:**
- `main.py` - Entry point and CLI interface
- `providers/` - LLM provider implementations
- `metrics/` - Evaluation metrics calculators
- `cost_tracker.py` - Real-time cost monitoring

**Key Functions:**
- `evaluate_prompts()` - Main orchestrator (Modal function)
- `run_single_evaluation()` - Executes one test case
- `calculate_metrics()` - Computes evaluation scores

### 2. **Provider Abstraction** (`evaluator/providers/`)

Unified interface for multiple LLM providers.

```python
class BaseLLMProvider:
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate completion from LLM"""
        raise NotImplementedError

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost based on token usage"""
        raise NotImplementedError
```

**Implementations:**
- `claude_provider.py` - Anthropic Claude (3.5 Sonnet, Opus, Haiku)
- `gpt_provider.py` - OpenAI GPT (GPT-4, GPT-4 Turbo)
- `gemini_provider.py` - Google Gemini (1.5 Pro, Flash)

### 3. **Metrics System** (`evaluator/metrics/`)

Extensible metrics framework for evaluation.

**Built-in Metrics:**
- **Exact Match** - Binary pass/fail on exact string match
- **Similarity Score** - Cosine similarity (0-1 range)
- **Keyword Detection** - Required keywords presence
- **JSON Validation** - Valid JSON structure
- **Code Validation** - Syntax checking for code outputs
- **Word Count** - Min/max word requirements

**Custom Metrics:**
```python
def custom_metric(output: str, expected: str, **kwargs) -> dict:
    return {
        "score": 0.95,
        "passed": True,
        "details": "Custom metric details"
    }
```

### 4. **Cost Tracking** (`evaluator/cost_tracker.py`)

Real-time cost monitoring with budget protection.

**Features:**
- Per-request cost calculation
- Running total tracking
- Budget limit enforcement
- Provider cost breakdown
- Efficiency scoring (quality/cost)

**Implementation:**
```python
class CostTracker:
    def add_cost(self, cost: float, provider: str):
        """Track cost and check budget"""
        self.total_cost += cost
        if self.budget_limit and self.total_cost > self.budget_limit:
            raise BudgetExceededError()
```

### 5. **Streamlit UI** (`streamlit_app/`)

Interactive web interface for non-technical users.

**Pages:**
- **Home** - Overview and quick stats
- **Run Evaluation** - Configure and launch evaluations
- **Results** - Browse and analyze results
- **Model Comparison** - Compare providers side-by-side
- **Cost Tracker** - Cost analytics and trends
- **Settings** - Configuration management

See [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) for details.

---

## Data Flow

### Evaluation Process

```
1. User Input
   ├─ Prompts (JSON file or manual entry)
   ├─ Test Cases (JSON file or manual entry)
   ├─ Model Selection (Claude, GPT, Gemini)
   └─ Budget Limit (optional)

2. Orchestration (Modal)
   ├─ Load configurations
   ├─ Initialize cost tracker
   ├─ Create evaluation matrix
   │  └─ prompts × test_cases × models
   └─ Distribute to workers

3. Parallel Execution
   ├─ Worker 1: Prompt A + Test 1 + Claude
   ├─ Worker 2: Prompt A + Test 1 + GPT
   ├─ Worker 3: Prompt A + Test 2 + Claude
   ├─ ...
   └─ Worker N: Prompt Z + Test M + Gemini

4. Individual Evaluation
   ├─ Call LLM API
   ├─ Calculate token usage
   ├─ Track cost
   ├─ Check budget limit
   ├─ Calculate metrics
   └─ Return results

5. Aggregation
   ├─ Collect all results
   ├─ Calculate statistics
   ├─ Identify best performers
   └─ Generate summary

6. Output
   ├─ Excel file (with summary sheet)
   ├─ CSV file (raw data)
   ├─ Database export (Power BI)
   └─ Email notification (optional)
```

---

## Scaling Strategy

### Parallel Execution with Modal

Modal enables massive parallelization without infrastructure management.

**Example:**
```python
# Sequential (slow) - 1000 evals × 2 seconds = 33 minutes
for test in test_cases:
    result = run_evaluation(test)

# Parallel (fast) - 1000 evals in ~30 seconds
results = run_evaluation.map(test_cases)
```

**Scaling Characteristics:**
- **Concurrency:** Up to 1,000 parallel workers
- **Auto-scaling:** Modal automatically provisions resources
- **Cost efficiency:** Pay only for compute used
- **Cold start:** ~2 seconds for first request

### Performance Benchmarks

| Evaluations | Sequential | Parallel (Modal) | Speedup |
|-------------|-----------|------------------|---------|
| 100         | 3.3 min   | 20 sec           | 10x     |
| 1,000       | 33 min    | 30 sec           | 66x     |
| 10,000      | 5.5 hours | 5 min            | 66x     |

---

## Design Decisions

### Why Modal?

**Alternatives Considered:**
1. **AWS Lambda** - More complex setup, cold starts
2. **Google Cloud Functions** - Similar to Lambda
3. **Kubernetes** - Overkill for this use case
4. **Local multiprocessing** - Limited by hardware

**Why Modal Won:**
- ✅ Zero infrastructure management
- ✅ Fast cold starts (~2 seconds)
- ✅ Excellent Python support
- ✅ Simple deployment (`modal deploy`)
- ✅ Built-in secrets management
- ✅ Fair pricing model

### Why Streamlit?

**Alternatives Considered:**
1. **Flask/FastAPI** - More control but more code
2. **Gradio** - Similar but less flexible
3. **Django** - Too heavyweight

**Why Streamlit Won:**
- ✅ Rapid development (UI in 100 lines)
- ✅ Built-in widgets and visualizations
- ✅ Auto-reloading for development
- ✅ Easy deployment
- ✅ Great for data apps

### Provider Abstraction

**Design Pattern:** Strategy Pattern

**Benefits:**
- Easy to add new providers
- Consistent interface across providers
- Swappable at runtime
- Testable in isolation

**Trade-offs:**
- Some provider-specific features abstracted away
- Slight performance overhead (minimal)

### Cost Tracking Approach

**Design Decision:** Real-time tracking vs post-processing

**Chosen:** Real-time tracking

**Rationale:**
- ✅ Budget protection (stop before exceeding)
- ✅ Live cost visibility
- ✅ Better user experience
- ❌ Slight complexity increase (acceptable)

---

## Security Considerations

### API Key Management

- ✅ Modal secrets (encrypted at rest)
- ✅ Never in code or version control
- ✅ Environment-based access
- ❌ No hardcoded credentials

### Data Privacy

- ✅ No PII storage by default
- ✅ User controls data export
- ✅ Optional database encryption
- ✅ HTTPS for all communications

### Input Validation

- ✅ JSON schema validation
- ✅ Budget limit enforcement
- ✅ File size limits
- ✅ Rate limiting (via providers)

---

## Future Architecture Enhancements

### v1.1 Roadmap

- [ ] **Caching Layer** - Redis for repeated evaluations
- [ ] **Async Results** - Webhook callbacks for long runs
- [ ] **Multi-tenancy** - Team workspaces
- [ ] **Distributed Tracing** - OpenTelemetry integration

### v2.0 Vision

- [ ] **Real-time Streaming** - WebSocket results
- [ ] **ML Pipeline** - Auto-optimize prompts
- [ ] **A/B Testing Framework** - Statistical significance
- [ ] **Enterprise Features** - SSO, RBAC, audit logs

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Adding new providers
- Creating custom metrics
- Extending the UI
- Performance optimization

---

**Questions?** Open an issue or email hello@gtmvp.com
