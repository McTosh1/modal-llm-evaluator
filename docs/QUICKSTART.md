# 🚀 Quick Start Guide

Get up and running with Modal LLM Evaluator in 5 minutes!

## Prerequisites

Before you begin, make sure you have:

- ✅ Python 3.11 or higher installed
- ✅ pip package manager
- ✅ At least one LLM API key (Anthropic, OpenAI, or Google)

## Step 1: Clone and Install (2 minutes)

```bash
# Clone the repository
git clone https://github.com/GTMVP/modal-llm-evaluator.git
cd modal-llm-evaluator

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Set Up Modal (1 minute)

```bash
# Initialize Modal
python -m modal setup
```

This will open your browser for authentication. Sign in with your Modal account (or create one - it's free!).

## Step 3: Configure API Keys (1 minute)

Choose at least one LLM provider and configure it:

### Anthropic Claude

```bash
python -m modal secret create anthropic-key \
  ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

Get your API key from: https://console.anthropic.com/

### OpenAI GPT

```bash
python -m modal secret create openai-key \
  OPENAI_API_KEY=sk-your-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### Google Gemini

```bash
python -m modal secret create google-api-key \
  GOOGLE_API_KEY=your-key-here
```

Get your API key from: https://aistudio.google.com/app/apikey

## Step 4: Run Your First Evaluation (1 minute)

### Option A: Web UI (Easiest)

```bash
streamlit run streamlit_app/app.py
```

Then:
1. Click "Run Evaluation" in the sidebar
2. Select at least one model
3. Add a prompt and test case
4. Click "Start Evaluation"
5. See results in real-time!

### Option B: Command Line

```bash
python -m modal run main.py
```

This runs a demo evaluation with default settings.

## 🎉 That's It!

You should see:
- ✅ Evaluation starting on Modal
- ✅ Results appearing in seconds
- ✅ Cost tracking in real-time
- ✅ Summary with pass rates and metrics

## Next Steps

### 1. Try the Examples

```bash
# Compare different prompt styles
python -m modal run examples/prompt_comparison.py

# Test multiple models
python -m modal run examples/model_selection.py

# Product description optimization
python -m modal run examples/product_descriptions.py
```

### 2. Create Custom Evaluations

Create `my_prompts.json`:
```json
{
  "friendly": "Hi! Can you help with: {question}",
  "formal": "Please assist with the following: {question}"
}
```

Create `my_tests.json`:
```json
[
  {
    "id": "test1",
    "question": "What is machine learning?",
    "min_words": 20,
    "required_keywords": ["data", "algorithms"]
  }
]
```

Run it:
```bash
python -m modal run main.py \
  --prompts-file=my_prompts.json \
  --test-cases-file=my_tests.json \
  --budget-limit=5.00
```

### 3. Explore the UI

Launch the Streamlit app and explore:
- **Home** - Overview and quick stats
- **Run Evaluation** - Configure and launch tests
- **Results** - View detailed metrics and charts
- **Cost Tracker** - Monitor spending
- **Model Comparison** - Compare performance
- **Settings** - Configure email and preferences

### 4. Export Results

Results are automatically saved as:
- `results_[timestamp].xlsx` - Excel with multiple sheets
- Downloadable as CSV, JSON
- Exportable to Power BI database

## Troubleshooting

### "Modal setup failed"
Make sure you're connected to the internet and try again:
```bash
python -m modal setup --force
```

### "API key not found"
List your secrets to verify:
```bash
python -m modal secret list
```

If missing, create it:
```bash
python -m modal secret create anthropic-key ANTHROPIC_API_KEY=your-key
```

### "Import error"
Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### "Budget exceeded immediately"
Your budget limit might be too low. Try:
```bash
--budget-limit=10.00
```

## Cost Expectations

For your first test run:
- **Evaluations**: 10-50 tests
- **Cost**: $0.10 - $0.50
- **Time**: 30 seconds - 2 minutes

## Getting Help

- **Documentation**: [docs/](.)
- **Examples**: [examples/](../examples/)
- **Issues**: [GitHub Issues](https://github.com/GTMVP/modal-llm-evaluator/issues)
- **Email**: hello@gtmvp.com

---

**Ready to scale?** Check out the [full documentation](README.md) for advanced features!
