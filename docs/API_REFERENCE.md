# API Reference

Complete Python API documentation for Modal LLM Evaluator.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Classes](#core-classes)
- [Providers](#providers)
- [Metrics](#metrics)
- [Results](#results)
- [Examples](#examples)

---

## Installation

```bash
pip install -r requirements.txt
python -m modal setup
```

---

## Quick Start

```python
from evaluator import LLMEvaluator

# Initialize evaluator
evaluator = LLMEvaluator(
    models=["claude-3-5-sonnet-20241022", "gpt-4o"],
    budget_limit=10.00
)

# Define prompts
prompts = {
    "direct": "Answer this question: {question}",
    "friendly": "Hi! Can you help me with this? {question}"
}

# Define test cases
test_cases = [
    {
        "id": "test_1",
        "question": "What is the capital of France?",
        "expected_output": "Paris",
        "required_keywords": ["Paris"]
    }
]

# Run evaluation
results = evaluator.run(prompts, test_cases)

# Export results
results.save_excel("results.xlsx")
```

---

## Core Classes

### LLMEvaluator

Main orchestrator for running evaluations.

#### Constructor

```python
LLMEvaluator(
    models: List[str],
    budget_limit: Optional[float] = None,
    parallel: bool = True,
    timeout: int = 300
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `models` | List[str] | Required | List of model identifiers to evaluate |
| `budget_limit` | float | None | Maximum cost in USD (stops when exceeded) |
| `parallel` | bool | True | Enable parallel execution on Modal |
| `timeout` | int | 300 | Timeout per evaluation in seconds |

**Example:**
```python
evaluator = LLMEvaluator(
    models=["claude-3-5-sonnet-20241022", "gpt-4o"],
    budget_limit=25.00,
    parallel=True,
    timeout=60
)
```

---

#### run()

Execute evaluation across all prompts, test cases, and models.

```python
evaluator.run(
    prompts: Dict[str, str],
    test_cases: List[Dict],
    experiment_name: Optional[str] = None
) -> EvaluationResults
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompts` | Dict[str, str] | Required | Dictionary of {name: template} |
| `test_cases` | List[Dict] | Required | List of test case configurations |
| `experiment_name` | str | Auto-generated | Name for this evaluation run |

**Returns:** `EvaluationResults` object

**Example:**
```python
prompts = {
    "concise": "Answer briefly: {question}",
    "detailed": "Explain in detail: {question}"
}

test_cases = [
    {
        "id": "test_1",
        "question": "What is Python?",
        "expected_output": "A programming language",
        "min_words": 5,
        "max_words": 100
    }
]

results = evaluator.run(prompts, test_cases, "python-explanation-test")
```

---

#### run_single()

Run evaluation for a single combination (useful for testing).

```python
evaluator.run_single(
    prompt: str,
    test_case: Dict,
    model: str
) -> Dict
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | str | The formatted prompt text |
| `test_case` | Dict | Test case configuration |
| `model` | str | Model identifier |

**Returns:** Dictionary with evaluation results

**Example:**
```python
result = evaluator.run_single(
    prompt="Answer this: What is 2+2?",
    test_case={
        "id": "test_1",
        "question": "What is 2+2?",
        "expected_output": "4"
    },
    model="claude-3-5-sonnet-20241022"
)

print(result["output"])  # Model's response
print(result["passed"])  # True/False
print(result["cost"])    # Cost in USD
```

---

### EvaluationResults

Container for evaluation results with analysis and export methods.

#### Properties

```python
results.total_evaluations: int        # Total number of evaluations run
results.total_cost: float             # Total cost in USD
results.average_cost: float           # Average cost per evaluation
results.overall_success_rate: float   # Overall pass rate (0-1)
results.experiment_name: str          # Name of the experiment
results.start_time: datetime          # When evaluation started
results.end_time: datetime            # When evaluation finished
results.duration: timedelta           # Total duration
```

---

#### get_summary()

Get summary statistics.

```python
results.get_summary() -> Dict
```

**Returns:**
```python
{
    "experiment_name": "prompt-test-001",
    "total_evaluations": 750,
    "total_cost": 12.34,
    "average_cost": 0.0165,
    "success_rate": 0.943,
    "duration_minutes": 12.5,
    "by_model": {
        "claude-3-5-sonnet-20241022": {
            "evaluations": 250,
            "cost": 6.00,
            "success_rate": 0.96
        },
        # ... other models
    },
    "by_prompt": {
        "direct": {
            "evaluations": 150,
            "success_rate": 0.92
        },
        # ... other prompts
    }
}
```

---

#### get_best_performer()

Find the best performing model and prompt combination.

```python
results.get_best_performer(
    metric: str = "success_rate"
) -> Dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `metric` | str | "success_rate" | Metric to optimize ("success_rate", "cost", "efficiency") |

**Returns:**
```python
{
    "model": "claude-3-5-sonnet-20241022",
    "prompt": "expert",
    "success_rate": 0.976,
    "cost": 0.024,
    "efficiency": 40.67  # success_rate / cost
}
```

**Example:**
```python
# Best for quality
best_quality = results.get_best_performer(metric="success_rate")

# Best for cost
best_cost = results.get_best_performer(metric="cost")

# Best efficiency (quality/cost)
best_efficiency = results.get_best_performer(metric="efficiency")
```

---

#### filter()

Filter results by various criteria.

```python
results.filter(
    model: Optional[str] = None,
    prompt: Optional[str] = None,
    passed: Optional[bool] = None,
    min_cost: Optional[float] = None,
    max_cost: Optional[float] = None
) -> EvaluationResults
```

**Example:**
```python
# Get only failed tests
failed = results.filter(passed=False)

# Get Claude results
claude_results = results.filter(model="claude-3-5-sonnet-20241022")

# Get expensive evaluations
expensive = results.filter(min_cost=0.05)
```

---

#### save_excel()

Export results to Excel with summary sheet.

```python
results.save_excel(
    filepath: str,
    include_summary: bool = True,
    include_charts: bool = True
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filepath` | str | Required | Output file path |
| `include_summary` | bool | True | Add summary sheet |
| `include_charts` | bool | True | Add visualizations |

**Example:**
```python
results.save_excel(
    "reports/evaluation_results.xlsx",
    include_summary=True,
    include_charts=True
)
```

**Output Structure:**
- Sheet 1: Summary (KPIs, charts)
- Sheet 2: Detailed Results (all evaluations)
- Sheet 3: By Model (aggregated)
- Sheet 4: By Prompt (aggregated)

---

#### save_csv()

Export results to CSV.

```python
results.save_csv(filepath: str)
```

**Example:**
```python
results.save_csv("results.csv")
```

---

#### export_to_database()

Export to database for Power BI integration.

```python
results.export_to_database(
    connection_string: str,
    table_name: str = "llm_evaluations",
    if_exists: str = "append"
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `connection_string` | str | Required | Database connection URL |
| `table_name` | str | "llm_evaluations" | Target table name |
| `if_exists` | str | "append" | What to do if table exists ("append", "replace", "fail") |

**Example:**
```python
results.export_to_database(
    connection_string="postgresql://user:pass@localhost/llm_db",
    table_name="evaluations",
    if_exists="append"
)
```

---

#### email_results()

Email results to recipients.

```python
results.email_results(
    recipients: List[str],
    subject: Optional[str] = None,
    body: Optional[str] = None,
    attach_excel: bool = True,
    smtp_config: Optional[Dict] = None
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `recipients` | List[str] | Required | List of email addresses |
| `subject` | str | Auto-generated | Email subject |
| `body` | str | Auto-generated | Email body |
| `attach_excel` | bool | True | Attach Excel file |
| `smtp_config` | Dict | From secrets | SMTP configuration |

**Example:**
```python
results.email_results(
    recipients=["team@example.com", "client@example.com"],
    subject="LLM Evaluation Complete: My Experiment",
    attach_excel=True
)
```

---

## Providers

### Base Provider

All providers inherit from `BaseLLMProvider`:

```python
class BaseLLMProvider:
    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """Generate completion"""
        pass

    def calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost in USD"""
        pass
```

---

### ClaudeProvider

Anthropic Claude models.

```python
from evaluator.providers import ClaudeProvider

provider = ClaudeProvider(
    model="claude-3-5-sonnet-20241022",
    api_key="sk-ant-..."  # Or from Modal secrets
)

response = provider.generate(
    prompt="Explain quantum computing",
    max_tokens=500,
    temperature=0.5
)
```

**Available Models:**
- `claude-3-5-sonnet-20241022` - Best balance
- `claude-3-5-haiku-20241022` - Fast and cheap
- `claude-3-opus-20240229` - Most capable

**Pricing (per 1M tokens):**
- Sonnet: $3 input / $15 output
- Haiku: $0.25 input / $1.25 output
- Opus: $15 input / $75 output

---

### GPTProvider

OpenAI GPT models.

```python
from evaluator.providers import GPTProvider

provider = GPTProvider(
    model="gpt-4o",
    api_key="sk-..."  # Or from Modal secrets
)

response = provider.generate(
    prompt="Explain quantum computing",
    max_tokens=500,
    temperature=0.7
)
```

**Available Models:**
- `gpt-4o` - Best OpenAI model
- `gpt-4o-mini` - Fast and cheap
- `gpt-4-turbo` - Previous generation

**Pricing (per 1M tokens):**
- GPT-4o: $2.50 input / $10 output
- GPT-4o-mini: $0.15 input / $0.60 output

---

### GeminiProvider

Google Gemini models.

```python
from evaluator.providers import GeminiProvider

provider = GeminiProvider(
    model="gemini-1.5-pro",
    api_key="..."  # Or from Modal secrets
)

response = provider.generate(
    prompt="Explain quantum computing",
    max_tokens=500,
    temperature=0.7
)
```

**Available Models:**
- `gemini-1.5-pro` - Most capable
- `gemini-1.5-flash` - Fast and cheap

**Pricing (per 1M tokens):**
- Pro: $3.50 input / $10.50 output
- Flash: $0.075 input / $0.30 output

---

## Metrics

### Built-in Metrics

```python
from evaluator.metrics import (
    exact_match,
    similarity_score,
    keyword_detection,
    json_validation,
    code_validation,
    word_count_validation
)
```

---

### exact_match()

Binary pass/fail on exact string match.

```python
exact_match(
    output: str,
    expected: str,
    case_sensitive: bool = False
) -> Dict
```

**Returns:**
```python
{
    "score": 1.0,  # 1.0 if match, 0.0 if not
    "passed": True,
    "details": "Exact match found"
}
```

---

### similarity_score()

Cosine similarity between output and expected (0-1 range).

```python
similarity_score(
    output: str,
    expected: str,
    threshold: float = 0.8
) -> Dict
```

**Returns:**
```python
{
    "score": 0.95,
    "passed": True,  # True if >= threshold
    "details": "High similarity"
}
```

---

### keyword_detection()

Check if required keywords are present.

```python
keyword_detection(
    output: str,
    required_keywords: List[str],
    case_sensitive: bool = False
) -> Dict
```

**Returns:**
```python
{
    "score": 1.0,
    "passed": True,
    "details": "All keywords found",
    "found_keywords": ["keyword1", "keyword2"],
    "missing_keywords": []
}
```

---

### json_validation()

Validate output is valid JSON.

```python
json_validation(
    output: str,
    schema: Optional[Dict] = None
) -> Dict
```

**Returns:**
```python
{
    "score": 1.0,
    "passed": True,
    "details": "Valid JSON",
    "parsed_data": {...}
}
```

---

### code_validation()

Validate output is valid code.

```python
code_validation(
    output: str,
    language: str = "python"
) -> Dict
```

**Supported Languages:**
- python
- javascript
- java
- go
- rust

**Returns:**
```python
{
    "score": 1.0,
    "passed": True,
    "details": "Valid Python code",
    "syntax_errors": []
}
```

---

### Custom Metrics

Define custom evaluation metrics:

```python
def custom_sentiment_check(output: str, expected: str, **kwargs) -> Dict:
    """Check if output has positive sentiment"""
    # Your custom logic here
    sentiment_score = analyze_sentiment(output)

    return {
        "score": sentiment_score,
        "passed": sentiment_score > 0.7,
        "details": f"Sentiment: {sentiment_score}"
    }

# Use in evaluation
evaluator = LLMEvaluator(
    models=["claude-3-5-sonnet-20241022"],
    custom_metrics=[custom_sentiment_check]
)
```

---

## Examples

### Example 1: Simple Prompt Test

```python
from evaluator import LLMEvaluator

# Test a single prompt
evaluator = LLMEvaluator(
    models=["claude-3-5-sonnet-20241022"],
    budget_limit=1.00
)

prompts = {
    "v1": "Answer this: {question}"
}

test_cases = [
    {"id": "1", "question": "What is 2+2?", "expected_output": "4"}
]

results = evaluator.run(prompts, test_cases)
print(f"Success: {results.overall_success_rate}")
```

---

### Example 2: Model Comparison

```python
# Compare 3 models
evaluator = LLMEvaluator(
    models=[
        "claude-3-5-sonnet-20241022",
        "gpt-4o",
        "gemini-1.5-pro"
    ],
    budget_limit=20.00
)

prompts = {"standard": "Explain {topic}"}
test_cases = [
    {"id": "1", "topic": "machine learning"},
    {"id": "2", "topic": "blockchain"},
]

results = evaluator.run(prompts, test_cases)

# Find best model
best = results.get_best_performer()
print(f"Best model: {best['model']}")
print(f"Success rate: {best['success_rate']}")
```

---

### Example 3: Prompt Optimization

```python
# Test multiple prompt variations
prompts = {
    "direct": "Answer this: {question}",
    "cot": "Think step by step: {question}",
    "expert": "As an expert, explain: {question}",
    "simple": "In simple terms: {question}",
    "detailed": "Provide a detailed answer: {question}"
}

# Load test cases from file
import json
with open("test_cases.json") as f:
    test_cases = json.load(f)

# Run evaluation
evaluator = LLMEvaluator(
    models=["claude-3-5-sonnet-20241022"],
    budget_limit=15.00
)

results = evaluator.run(prompts, test_cases, "prompt-optimization")

# Find best prompt
best_prompt = results.get_best_performer()
results.save_excel("prompt_analysis.xlsx")
```

---

### Example 4: Continuous Monitoring

```python
import schedule
import time

def daily_quality_check():
    evaluator = LLMEvaluator(
        models=["claude-3-5-sonnet-20241022"],
        budget_limit=5.00
    )

    # Production prompts
    prompts = load_production_prompts()
    test_cases = load_test_suite()

    results = evaluator.run(prompts, test_cases, "daily-qa")

    # Alert if quality drops
    if results.overall_success_rate < 0.95:
        results.email_results(
            recipients=["team@example.com"],
            subject="⚠️ Quality Alert"
        )

    # Export to database
    results.export_to_database(
        "postgresql://user:pass@localhost/metrics"
    )

# Schedule daily at 9 AM
schedule.every().day.at("09:00").do(daily_quality_check)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Error Handling

```python
from evaluator.exceptions import (
    BudgetExceededError,
    ProviderError,
    ValidationError
)

try:
    results = evaluator.run(prompts, test_cases)
except BudgetExceededError as e:
    print(f"Budget limit reached: {e.cost_used}/{e.budget_limit}")
    print(f"Partial results available: {e.partial_results}")
except ProviderError as e:
    print(f"API error: {e.provider} - {e.message}")
except ValidationError as e:
    print(f"Invalid input: {e.message}")
```

---

## Need Help?

- **Documentation:** [docs/](.)
- **Examples:** [examples/](../examples/)
- **Issues:** [GitHub Issues](https://github.com/GTMVP/modal-llm-evaluator/issues)
- **Email:** hello@gtmvp.com

---

**Happy Coding! 🚀**
