# Streamlit UI Guide

Complete guide to using the Modal LLM Evaluator web interface.

## Table of Contents

- [Getting Started](#getting-started)
- [Page-by-Page Guide](#page-by-page-guide)
- [Common Workflows](#common-workflows)
- [Tips & Tricks](#tips--tricks)
- [Troubleshooting](#troubleshooting)

---

## Getting Started

### Launch the UI

```bash
# From project root
streamlit run streamlit_app/app.py

# Or specify port
streamlit run streamlit_app/app.py --server.port 8502
```

The UI will open at `http://localhost:8501`

### First Time Setup

1. **Configure API Keys** (via Modal secrets)
   ```bash
   modal secret create anthropic-key ANTHROPIC_API_KEY=sk-ant-...
   modal secret create openai-key OPENAI_API_KEY=sk-...
   modal secret create google-api-key GOOGLE_API_KEY=...
   ```

2. **Verify Modal Connection**
   - Check the sidebar for Modal status indicator
   - Green = Connected, Red = Not configured

3. **Optional: Email Setup**
   - Configure SMTP settings in `.streamlit/secrets.toml`
   - See [EMAIL_SETUP.md](EMAIL_SETUP.md) for details

---

## Page-by-Page Guide

### 🏠 Home Page

**Purpose:** Overview and quick access

**Features:**
- Project statistics
- Recent evaluations
- Quick start buttons
- System status checks

**Key Metrics Displayed:**
- Total evaluations run
- Total cost spent
- Average success rate
- Providers configured

**Actions:**
- ➡️ Quick start new evaluation
- 📊 View recent results
- ⚙️ Go to settings

---

### ▶️ Run Evaluation Page

**Purpose:** Configure and launch evaluations

#### Step 1: Experiment Configuration

```
┌─────────────────────────────────────┐
│ Experiment Name: my-test-001        │
│ Description: Testing prompt styles  │
└─────────────────────────────────────┘
```

**Best Practices:**
- Use descriptive names (include date/purpose)
- Add detailed descriptions for future reference
- Follow naming convention: `project-test-version`

#### Step 2: Configure Prompts

**Option A: Upload JSON File**
```json
{
  "direct": "Answer this: {question}",
  "friendly": "Hi! Can you help with: {question}",
  "expert": "As an expert, explain: {question}"
}
```

**Option B: Manual Entry**
- Click "Add Prompt Template"
- Enter prompt name and template
- Use `{variable}` for placeholders

**Prompt Variables:**
- `{question}` - The test question
- `{context}` - Additional context
- `{examples}` - Few-shot examples
- Custom variables supported

#### Step 3: Configure Test Cases

**Option A: Upload JSON File**
```json
[
  {
    "id": "test_1",
    "question": "What is 2+2?",
    "expected_output": "4",
    "required_keywords": ["4"],
    "min_words": 1,
    "max_words": 50
  }
]
```

**Option B: Manual Entry**
- Click "Add Test Case"
- Fill in required fields
- Configure evaluation criteria

**Test Case Fields:**
- **id** (required) - Unique identifier
- **question** (required) - The input
- **expected_output** (optional) - Expected answer
- **required_keywords** (optional) - Must-have keywords
- **min_words/max_words** (optional) - Length constraints
- **expect_json** (optional) - Validate JSON output
- **expect_code** (optional) - Validate code syntax

#### Step 4: Select Models

**Available Providers:**

**Anthropic Claude:**
- `claude-3-5-sonnet-20241022` (Recommended)
- `claude-3-5-haiku-20241022` (Fast & cheap)
- `claude-3-opus-20240229` (Most capable)

**OpenAI GPT:**
- `gpt-4o` (Recommended)
- `gpt-4o-mini` (Fast & cheap)
- `gpt-4-turbo` (Previous generation)

**Google Gemini:**
- `gemini-1.5-pro` (Most capable)
- `gemini-1.5-flash` (Fast & cheap)

**Model Selection Tips:**
- Start with 2-3 models for comparison
- Mix price points (premium vs budget)
- Consider latency requirements

#### Step 5: Set Budget

```
┌─────────────────────────────────────┐
│ Budget Limit: $10.00               │
│ Estimated Cost: $8.50               │
│ Safety Margin: 15%                  │
└─────────────────────────────────────┘
```

**Budget Controls:**
- Set maximum spend
- See live cost estimation
- Auto-cutoff when limit reached
- Email alert on budget warning (80%)

**Cost Estimation:**
- Calculated before execution
- Based on: prompts × tests × models
- Includes token count estimates
- Shows per-provider breakdown

#### Step 6: Launch

**Pre-flight Checks:**
- ✅ At least 1 prompt configured
- ✅ At least 1 test case configured
- ✅ At least 1 model selected
- ✅ Budget set (if enabled)
- ✅ Modal connection verified

**Launch Options:**
- **Run Now** - Immediate execution
- **Schedule** - Run at specific time (future feature)
- **Dry Run** - Validate without executing (future feature)

**During Execution:**
```
┌─────────────────────────────────────┐
│ Status: Running...                  │
│ Progress: 450 / 1000 evaluations    │
│ Cost so far: $4.23 / $10.00         │
│ Estimated time: 2 minutes remaining │
└─────────────────────────────────────┘
```

---

### 📊 Results Page

**Purpose:** Browse and analyze evaluation results

#### Results Browser

**View Options:**
- **Grid View** - Card-based overview
- **Table View** - Detailed spreadsheet
- **Timeline View** - Chronological history

**Filters:**
- By experiment name
- By date range
- By model/provider
- By success rate
- By cost range

#### Individual Result Details

**Summary Tab:**
```
┌─────────────────────────────────────┐
│ Experiment: prompt-optimization-001 │
│ Date: 2024-12-12 10:30 AM           │
│ Total Evaluations: 750              │
│ Success Rate: 94.3%                 │
│ Total Cost: $12.34                  │
│ Duration: 12 minutes                │
└─────────────────────────────────────┘
```

**Metrics Tab:**
- Pass/Fail by prompt
- Pass/Fail by model
- Average similarity scores
- Keyword detection rates
- Cost efficiency (quality/cost)

**Raw Data Tab:**
- Full evaluation results table
- Input/output for each test
- Token usage details
- Individual costs
- Metric scores

**Visualizations:**
- Success rate by prompt (bar chart)
- Cost by provider (pie chart)
- Quality vs Cost (scatter plot)
- Pass rate trends (line chart)

#### Export Options

**Excel Export:**
- Summary sheet with key metrics
- Detailed results sheet
- Charts and visualizations
- Cost breakdown

**CSV Export:**
- Raw data only
- Easy import to other tools
- Good for further analysis

**Database Export:**
- Direct to PostgreSQL/MySQL
- For Power BI integration
- Automated scheduling option

**Email Results:**
- Send to multiple recipients
- Attach Excel file
- Include summary in email body
- Customizable subject/message

---

### 🔄 Model Comparison Page

**Purpose:** Side-by-side model comparison

#### Comparison View

**Select Experiment:**
- Choose from recent experiments
- Or load from file

**Comparison Metrics:**
```
┌───────────────┬─────────┬────────┬────────┐
│ Metric        │ Claude  │ GPT-4  │ Gemini │
├───────────────┼─────────┼────────┼────────┤
│ Success Rate  │ 94.3%   │ 91.2%  │ 89.7%  │
│ Avg Cost/Test │ $0.024  │ $0.031 │ $0.018 │
│ Avg Latency   │ 1.2s    │ 1.8s   │ 0.9s   │
│ Quality Score │ 0.943   │ 0.912  │ 0.897  │
│ Efficiency    │ 39.3    │ 29.4   │ 49.8   │
└───────────────┴─────────┴────────┴────────┘
```

**Visualizations:**
- Radar chart (multi-dimensional comparison)
- Bar charts (side-by-side metrics)
- Scatter plot (cost vs quality)

**Winner Analysis:**
- Overall winner
- Best for quality
- Best for cost
- Best for speed
- Best efficiency (quality/cost)

**Recommendations:**
- Based on your priorities
- Use case specific
- Trade-off analysis

---

### 💰 Cost Tracker Page

**Purpose:** Cost analytics and budget management

#### Dashboard View

**Total Costs:**
```
┌─────────────────────────────────────┐
│ Today: $45.67                       │
│ This Week: $234.89                  │
│ This Month: $892.45                 │
│ All Time: $3,421.78                 │
└─────────────────────────────────────┘
```

**Cost Breakdown:**
- By provider (Claude vs GPT vs Gemini)
- By experiment
- By date
- By prompt template

**Visualizations:**
- Cost trends over time (line chart)
- Provider distribution (pie chart)
- Daily/weekly/monthly aggregates
- Budget utilization (progress bars)

#### Budget Management

**Set Budgets:**
- Daily budget limit
- Monthly budget limit
- Per-experiment budget

**Budget Alerts:**
- Email at 50% utilization
- Email at 80% utilization
- Auto-cutoff at 100%

**Cost Optimization:**
- Identify expensive prompts
- Compare model costs
- Find cost/quality sweet spot
- Suggestions for savings

---

### ⚙️ Settings Page

**Purpose:** Configuration management

#### API Configuration

**Modal Setup:**
- Verify Modal installation
- Test Modal connection
- View configured secrets

**Provider API Keys:**
- Anthropic API key status
- OpenAI API key status
- Google API key status
- Test API connections

#### Email Configuration

**SMTP Settings:**
- SMTP server
- SMTP port
- Username/password
- TLS/SSL settings
- Test email sending

#### Default Settings

**Evaluation Defaults:**
- Default models to use
- Default budget limit
- Default export format
- Auto-email results

**UI Preferences:**
- Theme (light/dark)
- Results per page
- Default view (grid/table)
- Chart styles

---

## Common Workflows

### Workflow 1: Quick Prompt Test

**Goal:** Test a single prompt quickly

1. Go to "Run Evaluation"
2. Enter experiment name: `quick-test-prompt-v1`
3. Add one prompt manually
4. Add 2-3 simple test cases
5. Select 2 models (e.g., Claude Sonnet + GPT-4o)
6. Set budget: $1.00
7. Click "Run Now"
8. View results in ~30 seconds

**Time:** 2 minutes
**Cost:** ~$0.50

---

### Workflow 2: Comprehensive Model Comparison

**Goal:** Find best model for your use case

1. Prepare prompt templates file (5 variations)
2. Prepare test cases file (50 examples)
3. Go to "Run Evaluation"
4. Upload both files
5. Select 3-5 models to compare
6. Set budget: $25.00
7. Run evaluation
8. Go to "Model Comparison"
9. Analyze trade-offs
10. Export results to Excel

**Time:** 15 minutes
**Cost:** ~$20

---

### Workflow 3: Ongoing Quality Monitoring

**Goal:** Track LLM quality over time

1. Create standard test suite (100 cases)
2. Create production prompts file
3. Schedule daily evaluations (future feature)
4. Set up email alerts
5. Monitor "Cost Tracker" for trends
6. Review "Results" page weekly
7. Export to Power BI for dashboards

**Time:** 30 min setup, 5 min/week monitoring
**Cost:** ~$5/day

---

## Tips & Tricks

### Performance Tips

1. **Use smaller models for testing**
   - Test with Haiku/Mini first
   - Scale to Sonnet/GPT-4 when ready

2. **Batch similar tests**
   - Group related test cases
   - Easier to analyze results

3. **Start with small samples**
   - 5-10 test cases initially
   - Scale to 100+ when validated

### Cost Optimization

1. **Set tight budgets initially**
   - Start with $1-2 limits
   - Increase as needed

2. **Use cost estimation**
   - Review before running
   - Adjust if too expensive

3. **Archive old results**
   - Delete unused experiments
   - Keep costs manageable

### Result Analysis

1. **Use filters effectively**
   - Focus on failed tests
   - Identify patterns

2. **Export to Excel**
   - Better for deep analysis
   - Create custom charts

3. **Compare incrementally**
   - Test 2-3 changes at a time
   - Track what improves results

---

## Troubleshooting

### UI Won't Load

**Error:** `streamlit: command not found`

**Fix:**
```bash
pip install streamlit
streamlit run streamlit_app/app.py
```

---

### "Modal Not Configured" Error

**Cause:** Modal CLI not set up

**Fix:**
```bash
python -m modal setup
# Follow authentication prompts
```

---

### "API Key Missing" Warning

**Cause:** Provider API key not configured

**Fix:**
```bash
# For Claude
modal secret create anthropic-key ANTHROPIC_API_KEY=sk-ant-...

# For GPT
modal secret create openai-key OPENAI_API_KEY=sk-...

# For Gemini
modal secret create google-api-key GOOGLE_API_KEY=...
```

---

### Results Not Showing

**Cause:** Results file missing or corrupted

**Fix:**
- Check `results/` folder exists
- Verify JSON files are valid
- Re-run evaluation if needed

---

### Email Sending Fails

**Cause:** SMTP not configured or wrong settings

**Fix:**
- Check `.streamlit/secrets.toml`
- Test SMTP settings in Settings page
- See [EMAIL_SETUP.md](EMAIL_SETUP.md)

---

### Budget Exceeded Warning

**Cause:** Evaluation costs more than budget

**Expected Behavior:**
- Evaluation stops automatically
- Partial results saved
- Email notification sent

**Fix:**
- Increase budget limit
- Reduce number of tests/models
- Use cheaper models

---

### Slow Performance

**Cause:** Large number of evaluations

**Normal:**
- 100 evals: ~30 seconds
- 1,000 evals: ~5 minutes
- 10,000 evals: ~30 minutes

**If slower:**
- Check internet connection
- Verify Modal status
- Check API rate limits

---

## Advanced Features

### Custom Metrics

Add custom evaluation metrics:

1. Create Python file in `evaluator/metrics/custom_metrics.py`
2. Define metric function
3. Configure in UI Settings
4. Use in evaluations

### Template Library

Save common configurations:

1. Run successful evaluation
2. Export configuration
3. Save to `templates/` folder
4. Load in future evaluations

### Keyboard Shortcuts

- `Ctrl+R` - Refresh page
- `Ctrl+S` - Save current config
- `Esc` - Close dialogs
- `?` - Show help

---

## Need Help?

- **Documentation:** [docs/](.)
- **Issues:** [GitHub Issues](https://github.com/GTMVP/modal-llm-evaluator/issues)
- **Email:** hello@gtmvp.com

---

**Happy Evaluating! 🚀**
