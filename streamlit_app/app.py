"""
Modal LLM Evaluator - Streamlit Frontend

A beautiful web interface for running and analyzing LLM evaluations at scale.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Page config
st.set_page_config(
    page_title="LLM Evaluator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("# ⚡ LLM Evaluator")
    st.markdown("---")

    # Navigation
    page = st.radio(
        "Navigation",
        ["🏠 Home", "▶️ Run Evaluation", "📊 Results", "💰 Cost Tracker", "🔄 Model Comparison", "⚙️ Settings"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### Quick Stats")

    # Check for recent results
    results_dir = Path(__file__).parent.parent
    result_files = list(results_dir.glob("results_*.xlsx"))

    if result_files:
        st.metric("Recent Experiments", len(result_files))
        latest = max(result_files, key=os.path.getmtime)
        st.caption(f"Latest: {latest.name[:30]}...")
    else:
        st.info("No evaluations yet")

    st.markdown("---")
    st.markdown("### Links")
    st.markdown("📖 [Documentation](README.md)")
    st.markdown("🚀 [Quick Start](QUICKSTART.md)")
    st.markdown("💡 [Examples](examples/)")

# Main content routing
if page == "🏠 Home":
    from pages import home
    home.show()
elif page == "▶️ Run Evaluation":
    from pages import run_evaluation
    run_evaluation.show()
elif page == "📊 Results":
    from pages import results
    results.show()
elif page == "💰 Cost Tracker":
    from pages import cost_tracker
    cost_tracker.show()
elif page == "🔄 Model Comparison":
    from pages import model_comparison
    model_comparison.show()
elif page == "⚙️ Settings":
    from pages import settings
    settings.show()
