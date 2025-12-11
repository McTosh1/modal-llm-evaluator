# Examples

This folder contains example configurations and use cases for Modal LLM Evaluator.

## Quick Examples

### 1. Simple Prompt Comparison

Compare different prompt styles on basic questions:

```bash
python -m modal run main.py \
  --prompts-file=examples/prompts_simple.json \
  --test-cases-file=examples/test_cases_simple.json \
  --budget-limit=2.00
```

**What it does:**
- Tests 5 different prompt styles (direct, friendly, expert, concise, detailed)
- Runs 3 test cases (factual, explanatory, code generation)
- Compares results across selected models

### 2. Product Description Optimization

Test which prompt generates the best product descriptions:

```bash
python -m modal run main.py \
  --prompts-file=examples/product_description_prompts.json \
  --test-cases-file=examples/product_test_cases.json \
  --budget-limit=5.00
```

**What it does:**
- Tests 5 marketing-focused prompts (basic, marketing, SEO, luxury, casual)
- Evaluates on 3 different products
- Finds the best prompt for e-commerce descriptions

## Example Files

### Prompt Files

| File | Description | Use Case |
|------|-------------|----------|
| `prompts_simple.json` | Basic prompt variations | General testing, learning the tool |
| `product_description_prompts.json` | E-commerce focused | Product descriptions, marketing copy |

### Test Case Files

| File | Description | Features |
|------|-------------|----------|
| `test_cases_simple.json` | General knowledge questions | Keyword validation, word count, code detection |
| `product_test_cases.json` | Product description tests | Real products, marketing requirements |

## Creating Your Own Examples

### Prompt File Structure

```json
{
  "prompt_id": "Your prompt template with {variables}",
  "another_prompt": "Different style: {variables}"
}
```

**Tips:**
- Use clear, descriptive IDs
- Include variables in {curly braces}
- Test different tones and styles
- Keep prompts focused on one approach

### Test Case File Structure

```json
[
  {
    "id": "unique_test_id",
    "question": "Or any other variable name you use",
    "expected_output": "Optional: what you expect",
    "required_keywords": ["word1", "word2"],
    "min_words": 10,
    "max_words": 100,
    "expect_code": false,
    "code_language": "python"
  }
]
```

**Available Validations:**
- `expected_output` - Exact match check
- `required_keywords` - Must contain these words
- `min_words` / `max_words` - Length constraints
- `expect_code` - Should output contain code
- `code_language` - Specific language expected

## Advanced Examples

### Model Comparison

Test the same prompts across all providers:

```bash
# Compare Claude, GPT, and Gemini
python -m modal run main.py \
  --prompts-file=examples/prompts_simple.json \
  --test-cases-file=examples/test_cases_simple.json \
  --models="claude-3-5-sonnet-20241022,gpt-4o,gemini-1.5-pro" \
  --budget-limit=10.00
```

### Large Scale Testing

Run comprehensive evaluations:

```bash
# 5 prompts × 50 test cases × 3 models = 750 evaluations
python -m modal run main.py \
  --prompts-file=examples/product_description_prompts.json \
  --test-cases-file=your_large_test_set.json \
  --budget-limit=25.00
```

### Budget-Conscious Testing

Start small and scale up:

```bash
# Test with just 1-2 models first
python -m modal run main.py \
  --prompts-file=examples/prompts_simple.json \
  --test-cases-file=examples/test_cases_simple.json \
  --models="claude-3-5-haiku-20241022" \
  --budget-limit=1.00
```

## Real-World Use Cases

### 1. Customer Support Responses

**Scenario:** Find the best prompt for support ticket responses

**Setup:**
- Create prompts with different tones (empathetic, professional, concise)
- Use real support tickets as test cases
- Validate for clarity, helpfulness, professionalism

### 2. Content Generation

**Scenario:** Optimize blog post introductions

**Setup:**
- Test various intro styles (hook, question, statistic, story)
- Use different blog topics as test cases
- Check for engagement, clarity, SEO keywords

### 3. Code Generation

**Scenario:** Best prompts for generating Python functions

**Setup:**
- Different instruction styles (explicit, minimal, example-based)
- Various programming tasks as test cases
- Validate for correctness, efficiency, documentation

### 4. Translation Quality

**Scenario:** Compare models for translating marketing copy

**Setup:**
- Same source text, different models
- Validate for accuracy, tone preservation, cultural appropriateness
- Human review of top results

## Tips for Creating Examples

### Good Prompts

✅ Clear and specific
✅ Consistent formatting
✅ Appropriate for the task
✅ Test one variable at a time

### Good Test Cases

✅ Representative of real use
✅ Varied difficulty levels
✅ Clear success criteria
✅ Enough samples (10+ minimum)

### Good Validations

✅ Measurable criteria
✅ Balanced (not too strict/loose)
✅ Relevant to use case
✅ Consistent across tests

## Getting Help

- **More Examples**: Check [GitHub Discussions](https://github.com/GTMVP/modal-llm-evaluator/discussions)
- **Share Your Examples**: Submit a PR to add your examples here!
- **Questions**: Open an issue or email hello@gtmvp.com

---

**Start with simple examples, then customize for your specific needs!**
