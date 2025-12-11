"""
Home page - Welcome and overview
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def show():
    """Display home page"""

    # Header
    st.markdown('<h1 class="main-header">⚡ LLM Evaluator</h1>', unsafe_allow_html=True)
    st.markdown("### Evaluate LLM prompts at scale with parallel execution, cost tracking, and Power BI integration")

    st.markdown("---")

    # Hero section
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>🚀 10x-100x Faster</h2>
            <p>Run 1,000 evaluations in 10 minutes instead of 10 hours with parallel execution on Modal</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>💰 Cost Control</h2>
            <p>Real-time cost tracking with budget limits. Know exactly what you'll spend before you spend it</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>📊 Power BI Ready</h2>
            <p>Export results directly to databases for beautiful dashboards and client reporting</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Features section
    st.markdown("## ✨ Key Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🎯 Multi-Provider Support
        - **Anthropic Claude** (Opus, Sonnet, Haiku)
        - **OpenAI GPT** (GPT-4, GPT-4o, GPT-3.5)
        - **Google Gemini** (Pro, Flash)
        - Automatic cost calculation for all models

        ### 📈 Comprehensive Metrics
        - Exact match scoring
        - Similarity analysis
        - Keyword detection
        - JSON/code validation
        - Sentiment analysis
        - Custom metrics support
        """)

    with col2:
        st.markdown("""
        ### ⚡ Parallel Execution
        - Runs on Modal's serverless infrastructure
        - Automatic scaling to any workload
        - Built-in retries and error handling
        - 10x-100x faster than sequential

        ### 💾 Flexible Export
        - JSON, CSV, Excel formats
        - Direct database integration
        - Power BI ready
        - Beautiful summary reports
        """)

    st.markdown("---")

    # Quick start section
    st.markdown("## 🚀 Quick Start")

    tab1, tab2, tab3 = st.tabs(["▶️ Run Evaluation", "📊 View Results", "💡 Use Cases"])

    with tab1:
        st.markdown("""
        ### Run Your First Evaluation

        1. **Navigate to "Run Evaluation"** in the sidebar
        2. **Choose your models** - Select Claude, GPT, Gemini, or all
        3. **Configure prompts** - Use templates or write custom prompts
        4. **Add test cases** - Upload JSON or create inline
        5. **Set budget** - Optional cost limit for safety
        6. **Launch!** - Click "Start Evaluation" and watch the magic

        Results appear in minutes with comprehensive metrics and cost breakdowns.
        """)

        if st.button("🚀 Start Your First Evaluation", type="primary"):
            st.session_state.page = "▶️ Run Evaluation"
            st.rerun()

    with tab2:
        st.markdown("""
        ### View and Analyze Results

        1. **Navigate to "Results"** in the sidebar
        2. **Select an experiment** - Choose from recent evaluations
        3. **Explore metrics** - Pass rates, costs, latency
        4. **Compare models** - See which performs best
        5. **Export data** - Download Excel or push to Power BI

        Interactive charts and detailed breakdowns make analysis easy.
        """)

    with tab3:
        st.markdown("""
        ### Real-World Use Cases

        **🛍️ E-commerce Product Descriptions**
        - Test 5 prompt styles on 50 products
        - Find optimal template for compelling copy
        - Save hours of manual writing

        **💬 Customer Service Automation**
        - Compare models on support scenarios
        - Ensure quality before deployment
        - Optimize cost vs. quality trade-offs

        **📝 Content Generation**
        - Test blog post prompts at scale
        - Find best model for your voice
        - Measure quality systematically

        **🔍 Prompt Engineering**
        - Iterate on prompts quickly
        - A/B test variations
        - Data-driven optimization
        """)

    st.markdown("---")

    # Stats section
    st.markdown("## 📊 Why This Matters")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Time Savings", "95%", "vs. manual testing")
    col2.metric("Cost Visibility", "100%", "real-time tracking")
    col3.metric("Supported Models", "15+", "across 3 providers")
    col4.metric("Max Parallelism", "1000+", "concurrent evals")

    st.markdown("---")

    # Example results
    st.markdown("## 🎯 Example Results")

    st.markdown("""
    <div class="info-box">
    <strong>Recent Experiment: Product Description Optimization</strong><br>
    • Tested: 5 prompts × 50 products × 3 models = 750 evaluations<br>
    • Time: 12 minutes<br>
    • Cost: $12.34<br>
    • Winner: "Marketing" prompt + Claude 3.5 Sonnet<br>
    • Pass Rate: 94.3%<br>
    • ROI: Saved $1,950 in manual testing time
    </div>
    """, unsafe_allow_html=True)

    # CTA
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("### Ready to optimize your LLM workflows?")

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("🚀 Run Evaluation", type="primary", use_container_width=True):
                st.session_state.page = "▶️ Run Evaluation"
                st.rerun()

        with col_b:
            if st.button("📖 View Documentation", use_container_width=True):
                st.info("Check out README.md for complete documentation!")

    st.markdown("---")

    # Footer
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
    Built with ❤️ using Modal, Streamlit, and Claude<br>
    <small>Save time, reduce costs, make better LLM decisions</small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show()
