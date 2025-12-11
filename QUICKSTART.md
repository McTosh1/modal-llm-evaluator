# ⚡ Quick Start Guide - Get Running in 5 Minutes

## Step 1: Install Modal & Dependencies (2 minutes)

```bash
# Install Modal
pip install modal

# Navigate to project
cd modal-llm-evaluator

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Authenticate with Modal (1 minute)

```bash
python -m modal setup
```

This will open your browser to authenticate. Once done, you'll see:
```
✓ Token verified successfully!
```

## Step 3: Add Your API Keys (1 minute)

You need at least ONE of these API keys:

### Option A: Anthropic Claude (Recommended)
```bash
python -m modal secret create anthropic-key ANTHROPIC_API_KEY=sk-ant-...
```

**Get your key:** https://console.anthropic.com/account/keys

### Option B: OpenAI
```bash
python -m modal secret create openai-key OPENAI_API_KEY=sk-...
```

**Get your key:** https://platform.openai.com/api-keys

### Option C: Google Gemini
```bash
python -m modal secret create google-api-key GOOGLE_API_KEY=...
```

**Get your key:** https://makersuite.google.com/app/apikey

## Step 4: Run Your First Evaluation (1 minute)

```bash
python -m modal run main.py
```

You'll see:
```
🚀 Starting LLM Evaluation: test_experiment
📝 Prompts: 2
🧪 Test Cases: 2
🤖 Models: 3
📊 Total Evaluations: 12

⚡ Running 12 evaluations in parallel on Modal...

✅ Completed 12 evaluations

📊 EVALUATION SUMMARY
Total Cost: $0.0234
Pass Rate: 91.7%
```

**Results saved to Excel file for easy viewing!**

---

## What Just Happened?

1. ✅ Modal ran 12 LLM evaluations in parallel
2. ✅ Tested 2 different prompts
3. ✅ Across 3 different models (Claude, GPT, Gemini)
4. ✅ On 2 test questions
5. ✅ Tracked costs automatically
6. ✅ Exported results to Excel

**Total time:** ~30 seconds of actual compute time
**Total cost:** ~$0.02

---

## Next Steps

### Try the Examples

**Example 1: Compare prompt styles**
```bash
python -m modal run examples/simple_comparison.py
```

**Example 2: Optimize product descriptions** (great for e-commerce!)
```bash
python examples/prompt_optimization.py
# This creates a config file, then run:
python -m modal run main.py --experiment-name='product-optimization' --budget-limit=5.00
```

### Run With Your Own Data

1. **Create your prompts file** (`my_prompts.json`):
```json
{
  "prompt1": "You are an expert. {question}",
  "prompt2": "Answer briefly: {question}"
}
```

2. **Create your test cases** (`my_tests.json`):
```json
[
  {
    "id": "test1",
    "question": "Your question here",
    "required_keywords": ["keyword1", "keyword2"]
  }
]
```

3. **Run evaluation:**
```bash
python -m modal run main.py \
  --experiment-name="my-experiment" \
  --prompts-file="my_prompts.json" \
  --test-cases-file="my_tests.json" \
  --budget-limit=10.00
```

### Export to Power BI

```bash
python -m modal run main.py \
  --export-format="database" \
  --database-url="postgresql://user:pass@host/database"
```

Then connect Power BI to your database and create dashboards!

---

## Common Issues

### "Token missing" error
**Solution:** Add your API keys (see Step 3 above)

### "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt
```

### Character encoding errors on Windows
**Solution:** Already handled in the code! But if you see issues, run in Windows Terminal instead of old PowerShell.

### Want to test only one model?
**Edit `main.py` line 146 to:**
```python
models = ["claude-3-5-sonnet-20241022"]  # Just test Claude
```

---

## Understanding Your Results

The Excel output has 3 sheets:

1. **Results** - All evaluation details
   - Each row is one evaluation
   - Shows: prompt, model, output, cost, latency, pass/fail

2. **Model Summary** - Performance by model
   - Total cost per model
   - Average latency
   - Pass rate
   - Number of tests

3. **Prompt Summary** - Performance by prompt
   - Which prompt works best
   - Cost per prompt
   - Success rate

**Look for:**
- ✅ High pass rate (>90%)
- ✅ Low cost per test (<$0.01)
- ✅ Fast latency (<2 seconds)

---

## Cost Control

**Set a budget limit:**
```bash
--budget-limit=5.00  # Stop at $5
```

The system will automatically stop when budget is reached.

**Estimate costs:**
- Small test (100 evaluations): ~$0.50
- Medium test (1,000 evaluations): ~$5.00
- Large test (10,000 evaluations): ~$50.00

---

## Getting Help

1. **Check the full README:** `README.md`
2. **Try examples:** `examples/` directory
3. **Modal docs:** https://modal.com/docs
4. **File issues:** GitHub Issues

---

**🎉 You're all set! Start optimizing your LLM prompts at scale!**
