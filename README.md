# ⚡ Modal LLM Evaluator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Modal](https://img.shields.io/badge/Powered%20by-Modal-blueviolet)](https://modal.com)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io)

> **Run 1,000 LLM evaluations in 10 minutes instead of 10 hours**

A production-ready platform for evaluating LLM prompts at scale with parallel execution, real-time cost tracking, and comprehensive analytics. Test prompts across multiple models (Claude, GPT-4, Gemini) with beautiful visualizations and Power BI integration.

![Modal LLM Evaluator Banner](docs/images/Banner.png)

**[Quick Start](#-quick-start)** • **[Documentation](docs/)** • **[Examples](examples/)** • **[Contributing](CONTRIBUTING.md)**

---

## 📸 Screenshots

<p align="center">
  <img src="docs/images/homepage.png" width="45%" alt="Home Dashboard" />
  <img src="docs/images/run_evaluation.png" width="45%" alt="Run Evaluation" />
</p>

---

## 🎯 Why This Exists

**The Problem:**
- Testing LLM prompts manually takes hours
- Costs are unpredictable
- Hard to compare models objectively
- Results are scattered and inconsistent

**The Solution:**
- ⚡ **10x-100x faster** - Parallel execution on Modal's serverless infrastructure
- 💰 **Cost control** - Real-time tracking with budget limits
- 📊 **Data-driven** - Systematic comparison across providers
- 🎨 **Beautiful UI** - Streamlit interface for non-technical users

---

## ✨ Features

### 🚀 Core Capabilities

- **Multi-Provider Support** - Claude (Anthropic), GPT (OpenAI), Gemini (Google)
- **Parallel Execution** - Run thousands of evaluations simultaneously on Modal
- **Cost Management** - Real-time tracking, budget limits, cost breakdowns
- **Comprehensive Metrics** - Exact match, similarity, keyword detection, JSON/code validation
- **Beautiful UI** - Streamlit interface with 6 interactive pages
- **Email Notifications** - Automated results delivery
- **Power BI Integration** - Direct database export for dashboards
- **Flexible Export** - JSON, CSV, Excel with summary sheets

### 📊 Evaluation Metrics

- Exact match scoring
- Similarity analysis (0-1 score)
- Keyword detection
- JSON validation
- Code validation
- Sentiment analysis
- Word count validation
- Custom metrics support

### 💰 Cost Tracking

- Per-evaluation cost calculation
- Budget limits with auto-cutoff
- Cost by model/provider breakdowns
- Efficiency scoring (quality/cost)
- Historical cost trends

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Modal account (free tier available)
- At least one LLM API key (Anthropic, OpenAI, or Google)

### Installation

```bash
# Clone repository
git clone https://github.com/GTMVP/modal-llm-evaluator.git
cd modal-llm-evaluator

# Install dependencies
pip install -r requirements.txt

# Set up Modal
python -m modal setup

# Configure API keys (Modal secrets)
python -m modal secret create anthropic-key ANTHROPIC_API_KEY=sk-ant-...
python -m modal secret create openai-key OPENAI_API_KEY=sk-...
python -m modal secret create google-api-key GOOGLE_API_KEY=...
```

### Run Your First Evaluation

```bash
# CLI (for developers)
python -m modal run main.py

# Or launch the Web UI (for everyone)
streamlit run streamlit_app/app.py
```

**Results in ~30 seconds!** ✨

---

## 📖 Usage

### Option 1: Web UI (Recommended)

**Perfect for:** Non-technical users, visual exploration, client demos

```bash
streamlit run streamlit_app/app.py
```

**Features:**
- No-code evaluation configuration
- Live cost estimation
- Interactive results visualization
- Email results to clients
- Export to Excel/CSV/Power BI

### Option 2: Command Line

**Perfect for:** Developers, automation, CI/CD integration

```bash
python -m modal run main.py \
  --experiment-name="my-test" \
  --budget-limit=10.00
```

### Option 3: Python API

**Perfect for:** Custom integrations, programmatic access

```python
from evaluator import LLMEvaluator

evaluator = LLMEvaluator(
    models=["claude-3-5-sonnet-20241022", "gpt-4o"],
    budget_limit=10.00
)

results = evaluator.run(
    prompts=prompts,
    test_cases=test_cases
)

results.save_excel("my_results.xlsx")
```

---

## 🎓 Use Cases

### 1. **Prompt Engineering**

Test 10 prompt variations × 100 test cases × 5 models = 5,000 evaluations in ~10 minutes

```python
# Test multiple prompt styles
prompts = {
    "direct": "Answer this: {question}",
    "cot": "Think step by step: {question}",
    "expert": "As an expert, explain: {question}"
}

# Find the best performer
results = evaluate(prompts, test_cases, models)
best_prompt = results.get_winner()  # Data-driven decision!
```

### 2. **Model Selection**

Compare Claude vs GPT vs Gemini on YOUR specific use case

```python
# Which model is best for your needs?
models = ["claude-3-5-sonnet", "gpt-4o", "gemini-1.5-pro"]
comparison = evaluate(prompts, test_cases, models)

# See cost vs quality trade-offs
comparison.plot_efficiency()  # Quality / Cost chart
```

### 3. **Quality Assurance**

Continuously test LLM outputs to ensure quality

```python
# Run daily evaluations
@schedule(cron="0 9 * * *")  # Every day at 9am
def qa_check():
    results = evaluate(production_prompts, test_suite)
    if results.pass_rate < 0.95:
        alert_team("Quality degradation detected!")
```

### 4. **Client Reporting**

Generate professional reports for clients

```python
# Run evaluation
results = evaluate(prompts, test_cases, models)

# Export to Power BI
results.export_to_powerbi(connection_string)

# Email results
results.email_to("client@example.com",
                 subject="LLM Optimization Results")
```

---

## 📊 Example Results

### Real-World Case Study: Product Description Optimization

**Goal:** Find best prompt + model for e-commerce product descriptions

**Setup:**
- 5 prompt templates
- 50 sample products
- 3 models (Claude, GPT, Gemini)
- = 750 evaluations

**Results:**
- **Time:** 12 minutes
- **Cost:** $12.34
- **Winner:** "Marketing" prompt + Claude 3.5 Sonnet
- **Pass Rate:** 94.3%
- **ROI:** Saved $1,950 in manual testing time

![Results Dashboard](docs/images/run_evaluation.png)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           Streamlit Web UI                  │
│  (Home, Run, Results, Cost, Comparison)     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           Modal Orchestration               │
│  (Parallel execution, Auto-scaling)         │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
    ┌──────┐  ┌──────┐  ┌──────┐
    │Claude│  │ GPT  │  │Gemini│
    └──────┘  └──────┘  └──────┘
        │         │         │
        └─────────┼─────────┘
                  │
        ┌─────────▼─────────┐
        │ Results Storage   │
        │ (Excel, CSV, DB)  │
        └───────────────────┘
```

### Tech Stack

- **Serverless Compute:** Modal
- **Frontend:** Streamlit
- **LLM Providers:** Anthropic, OpenAI, Google
- **Data:** Pandas, SQLAlchemy
- **Visualization:** Plotly, Altair
- **Email:** SMTP (Brevo, SendGrid, etc.)

---

## 📊 Power BI Integration

### Export to Database

```bash
python -m modal run main.py \
  --export-format="database" \
  --database-url="postgresql://user:pass@localhost/mydb"
```

### Supported Databases
- PostgreSQL
- SQL Server (Azure SQL)
- MySQL
- SQLite

### Power BI Setup

1. **Connect Power BI to your database**
   - Get Data → Database → Your database type
   - Connect to table: `llm_evaluation_results`

2. **Create dashboard with these metrics:**
   - Cost by model
   - Pass rate by prompt
   - Latency distribution
   - Success rate over time

3. **Set up scheduled refresh**
   - Modal runs evaluations daily
   - Power BI refreshes automatically
   - Always have current data

---

## 💰 Cost Estimation

### Free Tier

Modal offers 30 free compute hours/month. For LLM costs:

| Evaluations | Estimated Cost | Time      |
|-------------|---------------|-----------|
| 100         | $0.50 - $2    | 2 min     |
| 1,000       | $5 - $20      | 10 min    |
| 10,000      | $50 - $200    | 30 min    |

**Set budget limits** to never exceed your limit!

```python
# Budget protection built-in
evaluate(prompts, tests, models, budget_limit=10.00)
# ✅ Stops automatically at $10
```

---

## 🔧 Configuration

### Command Line Options

```bash
python -m modal run main.py \
  --experiment-name="my-experiment" \
  --prompts-file="prompts.json" \
  --test-cases-file="tests.json" \
  --budget-limit=25.00 \
  --export-format="excel"
```

### Prompts File Format

```json
{
  "prompt1": "You are a helpful assistant. {question}",
  "prompt2": "Answer concisely: {question}",
  "prompt3": "Think step by step. {question}"
}
```

### Test Cases File Format

```json
[
  {
    "id": "test1",
    "question": "What is 2+2?",
    "expected_output": "4",
    "required_keywords": ["4"],
    "min_words": 5,
    "max_words": 50
  },
  {
    "id": "test2",
    "question": "Write a Python function",
    "expect_code": true,
    "code_language": "python"
  }
]
```

See [examples/](examples/) for more configuration examples.

---

## 📚 Documentation

- [**Quick Start Guide**](docs/QUICKSTART.md) - Get running in 5 minutes
- [**Architecture Overview**](docs/ARCHITECTURE.md) - System design and components
- [**Streamlit UI Guide**](docs/STREAMLIT_GUIDE.md) - Web interface documentation
- [**Email Setup**](docs/EMAIL_SETUP.md) - Configure notifications
- [**Power BI Integration**](docs/POWERBI_INTEGRATION.md) - Dashboard setup
- [**API Reference**](docs/API_REFERENCE.md) - Python API documentation
- [**Examples**](examples/) - Real-world use cases

---

## 🤝 Contributing

We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 📖 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repo!

---

## 🛣️ Roadmap

### ✅ Completed (v1.0)

- [x] Multi-provider support (Claude, GPT, Gemini)
- [x] Parallel execution on Modal
- [x] Cost tracking & budget limits
- [x] Streamlit web interface
- [x] Email notifications
- [x] Power BI integration
- [x] Comprehensive documentation

### 🚧 In Progress (v1.1)

- [ ] Live evaluation monitoring
- [ ] Scheduled evaluations (cron)
- [ ] Team collaboration features
- [ ] Custom metrics builder
- [ ] Template marketplace

### 🔮 Planned (v2.0)

- [ ] More LLM providers (Cohere, Together AI)
- [ ] A/B testing framework
- [ ] Regression testing suite
- [ ] Advanced analytics & ML insights
- [ ] Enterprise features (SSO, RBAC)
- [ ] SaaS hosting option

[See full roadmap →](https://github.com/GTMVP/modal-llm-evaluator/issues)

---

## 💼 Professional Services

Built this and got deep expertise in LLM evaluation? **We offer professional services:**

### Services Available

- **Custom Implementations** - Industry-specific templates, integrations
- **Consulting** - LLM strategy, prompt optimization, model selection
- **Managed Service** - We run evaluations for you
- **Training** - Workshops for your team

**Contact:** hello@gtmvp.com
**Website:** [GTMVP.com](https://gtmvp.com)

---

## 🐛 Troubleshooting

### "Token missing" error
**Fix:** Create Modal secrets for your API keys:
```bash
python -m modal secret create anthropic-key ANTHROPIC_API_KEY=your_key
```

### "Budget exceeded" message
**Expected behavior** - Your budget limit is working!
**Fix:** Increase budget or optimize tests:
```bash
--budget-limit=50.00
```

### Slow execution
**Cause:** Not using Modal's parallel execution
**Fix:** Use `.map()` or `.starmap()` for parallel processing

### Import errors
**Fix:** Install dependencies:
```bash
pip install -r requirements.txt
```

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more solutions.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

**Built with:**
- [Modal](https://modal.com) - Serverless compute platform
- [Streamlit](https://streamlit.io) - Web UI framework
- [Anthropic](https://anthropic.com) - Claude AI
- [OpenAI](https://openai.com) - GPT models
- [Google AI](https://ai.google.dev/) - Gemini models

**Inspired by:**
- The need for better LLM evaluation tools
- Data scientists spending too much time on manual testing
- The open source community

---

## ⭐ Star History

If you find this useful, please star the repo! It helps others discover the project.

[![Star History Chart](https://api.star-history.com/svg?repos=GTMVP/modal-llm-evaluator&type=Date)](https://star-history.com/#GTMVP/modal-llm-evaluator&Date)

---

## 📞 Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/GTMVP/modal-llm-evaluator/issues)
- **Discussions:** [GitHub Discussions](https://github.com/GTMVP/modal-llm-evaluator/discussions)
- **Email:** hello@gtmvp.com

---

## 🎯 Keywords

llm evaluation, prompt testing, ai testing, modal, streamlit, anthropic claude, openai gpt-4, google gemini, prompt engineering, llm comparison, cost tracking, parallel execution, serverless, python, machine learning, mlops

---

**Made with ❤️ by [GTMVP](https://gtmvp.com) & [SynapMarketing](https://synapmarketing.com)**

*Help us make LLM evaluation better for everyone!*
