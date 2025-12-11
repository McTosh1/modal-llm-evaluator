# 🎨 Streamlit Frontend for LLM Evaluator

Beautiful web interface for running and analyzing LLM evaluations!

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This includes Streamlit and visualization libraries.

### 2. Launch the App

```bash
cd modal-llm-evaluator
streamlit run streamlit_app/app.py
```

The app will open in your browser at `http://localhost:8501`

## 📱 Features

### 🏠 Home
- Beautiful landing page
- Feature overview
- Quick start guide
- Example use cases

### ▶️ Run Evaluation
- Interactive evaluation configuration
- Model selection with descriptions
- Prompt template library
- Test case builder
- Cost estimation
- One-click launch

### 📊 Results
- Interactive results viewer
- Beautiful charts and visualizations
- Pass rate analysis
- Cost breakdowns
- Detailed drill-down
- Export to CSV/Excel/JSON

### 💰 Cost Tracker
- Total spending overview
- Cost by model/provider
- Cost trends over time
- Efficiency analysis
- Budget recommendations

### 🔄 Model Comparison
- Side-by-side model analysis
- Radar chart comparison
- Cost vs quality trade-offs
- Winner analysis
- Smart recommendations

### ⚙️ Settings
- API key management
- Power BI integration
- Modal configuration
- Preferences
- System information

## 🎯 Usage Flow

### Option 1: Use the Web UI

1. **Launch Streamlit**
   ```bash
   streamlit run streamlit_app/app.py
   ```

2. **Configure Evaluation**
   - Go to "Run Evaluation"
   - Select models (Claude, GPT, Gemini)
   - Choose prompt templates or write custom
   - Add test cases
   - Set budget limit

3. **Get Command**
   - App generates the Modal command for you
   - Copy and run in terminal:
   ```bash
   python -m modal run main.py --experiment-name="my-eval" --budget-limit=10.00
   ```

4. **View Results**
   - Go to "Results" tab
   - Select your experiment
   - Explore charts and metrics
   - Download reports

### Option 2: CLI + Web UI

1. **Run evaluation via CLI**
   ```bash
   python -m modal run main.py
   ```

2. **View results in Streamlit**
   ```bash
   streamlit run streamlit_app/app.py
   ```

3. **Navigate to Results tab** to see beautiful visualizations

## 📊 Screenshots

### Home Page
Beautiful landing page with feature highlights and quick start.

### Run Evaluation
Interactive configuration with live cost estimation.

### Results Viewer
Rich visualizations with drill-down capabilities.

### Cost Tracker
Comprehensive cost analytics and efficiency analysis.

### Model Comparison
Side-by-side performance comparison with recommendations.

## 🎨 Customization

### Custom CSS
Edit `streamlit_app/app.py` to customize colors and styling:

```python
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #YOUR_COLOR 0%, #YOUR_COLOR_2 100%);
    }
    </style>
""", unsafe_allow_html=True)
```

### Add New Pages
Create new page in `streamlit_app/pages/`:

```python
# streamlit_app/pages/my_page.py
def show():
    st.title("My Custom Page")
    # Your code here
```

Add navigation in `streamlit_app/app.py`.

## 🔧 Configuration

### Theme
Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Server Settings
```toml
[server]
port = 8501
headless = false
enableCORS = false
```

## 📱 Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Deploy!

**Note:** Modal evaluations still run from CLI, Streamlit is for visualization.

### Deploy with Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app/app.py"]
```

```bash
docker build -t llm-evaluator .
docker run -p 8501:8501 llm-evaluator
```

## 💡 Tips

### Performance
- Results load faster with pagination
- Use filters to reduce data shown
- Export large datasets to CSV

### Workflow
1. Configure in Streamlit
2. Copy generated command
3. Run in terminal
4. View results in Streamlit

### Best Practices
- Set budget limits before running
- Save configurations for reuse
- Export results for Power BI
- Compare models before production use

## 🐛 Troubleshooting

### App Won't Start
```bash
# Check Streamlit is installed
pip install streamlit

# Verify Python path
which python
```

### No Results Showing
- Make sure you've run evaluations first
- Check that results_*.xlsx files exist
- Refresh the page

### Charts Not Loading
```bash
# Install visualization libraries
pip install plotly altair
```

### Module Import Errors
```bash
# Run from project root
cd modal-llm-evaluator
streamlit run streamlit_app/app.py
```

## 🎉 Features

✅ Beautiful, modern UI
✅ Interactive visualizations
✅ Real-time cost tracking
✅ Model comparison
✅ Export capabilities
✅ Mobile responsive
✅ Dark mode support (via Streamlit settings)
✅ No coding required for basic use
✅ Professional charts for presentations
✅ Power BI integration guide

## 🔜 Coming Soon

- [ ] Live evaluation monitoring
- [ ] Real-time progress bars
- [ ] Scheduled evaluations
- [ ] Team collaboration
- [ ] Template marketplace
- [ ] Advanced filtering
- [ ] Custom metrics builder
- [ ] API key testing

## 📚 Learn More

- **Streamlit Docs:** https://docs.streamlit.io
- **Plotly Charts:** https://plotly.com/python
- **Modal Docs:** https://modal.com/docs

---

**Built with ❤️ using Streamlit, Plotly, and Modal**

*Make LLM evaluation beautiful and easy!* ✨
