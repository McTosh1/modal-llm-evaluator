"""
Run Evaluation page - Configure and launch LLM evaluations
"""

import streamlit as st
import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# Model configurations
MODELS = {
    "Anthropic Claude": {
        "claude-opus-4-5": {"name": "Claude Opus 4.5", "cost": "$$$$", "speed": "Slow", "quality": "Best"},
        "claude-3-5-sonnet-20241022": {"name": "Claude 3.5 Sonnet", "cost": "$$", "speed": "Fast", "quality": "Excellent"},
        "claude-3-5-haiku-20241022": {"name": "Claude 3.5 Haiku", "cost": "$", "speed": "Very Fast", "quality": "Good"},
    },
    "OpenAI GPT": {
        "gpt-4o": {"name": "GPT-4o", "cost": "$$", "speed": "Fast", "quality": "Excellent"},
        "gpt-4o-mini": {"name": "GPT-4o Mini", "cost": "$", "speed": "Very Fast", "quality": "Good"},
        "gpt-4-turbo": {"name": "GPT-4 Turbo", "cost": "$$$", "speed": "Medium", "quality": "Excellent"},
    },
    "Google Gemini": {
        "gemini-2.0-flash-exp": {"name": "Gemini 2.0 Flash", "cost": "Free", "speed": "Very Fast", "quality": "Good"},
        "gemini-1.5-pro": {"name": "Gemini 1.5 Pro", "cost": "$$", "speed": "Medium", "quality": "Excellent"},
        "gemini-1.5-flash": {"name": "Gemini 1.5 Flash", "cost": "$", "speed": "Fast", "quality": "Good"},
    }
}

# Prompt templates
PROMPT_TEMPLATES = {
    "Basic": "You are a helpful assistant. {question}",
    "Expert": "You are an expert in the field. Answer this question with authority: {question}",
    "Step-by-step": "Think step by step and answer: {question}",
    "Concise": "Answer concisely in 2-3 sentences: {question}",
    "Detailed": "Provide a detailed, comprehensive answer to: {question}",
    "Custom": ""
}


def show():
    """Display run evaluation page"""

    st.title("▶️ Run LLM Evaluation")
    st.markdown("Configure and launch parallel evaluations across multiple models")

    # Demo notice
    st.warning("""
    ⚠️ **Demo Mode:** This UI preview shows the evaluation configuration interface.

    To run actual evaluations, you need to:
    - Clone the repository locally
    - Set up Modal CLI with your API keys (Anthropic, OpenAI, Google)
    - Run the app from your local environment

    👉 [Full Setup Instructions](https://github.com/GTMVP/modal-llm-evaluator#-quick-start)
    """)

    # Initialize session state
    if 'prompts' not in st.session_state:
        st.session_state.prompts = {}
    if 'test_cases' not in st.session_state:
        st.session_state.test_cases = []

    st.markdown("---")

    # Step 1: Experiment Configuration
    st.markdown("## 1️⃣ Experiment Configuration")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        experiment_name = st.text_input(
            "Experiment Name",
            value=f"eval_{datetime.now().strftime('%Y%m%d_%H%M')}",
            help="Give this evaluation a memorable name"
        )

    with col2:
        budget_limit = st.number_input(
            "Budget Limit ($)",
            min_value=0.0,
            max_value=1000.0,
            value=10.0,
            step=1.0,
            help="Maximum amount to spend on this evaluation"
        )

    with col3:
        enable_email = st.checkbox(
            "📧 Email Results",
            value=st.session_state.get("notify_on_complete", False),
            help="Send email when evaluation completes"
        )

    # Email configuration (if enabled)
    if enable_email:
        with st.expander("📧 Email Settings", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                notify_email = st.text_input(
                    "Send results to",
                    value=st.session_state.get("smtp_username", ""),
                    placeholder="your-email@gmail.com",
                    help="Email address to receive results"
                )

            with col2:
                attach_results = st.checkbox(
                    "📎 Attach Excel file",
                    value=True,
                    help="Include results Excel file as attachment"
                )

            # Check if email is configured
            if not st.session_state.get("smtp_username"):
                st.warning("⚠️ Email not configured. Go to Settings → Email Configuration to set up SMTP.")
                if st.button("Go to Settings"):
                    st.session_state.page = "⚙️ Settings"
                    st.rerun()
            else:
                st.success(f"✅ Email configured: {st.session_state.get('smtp_username')}")

    st.markdown("---")

    # Step 2: Model Selection
    st.markdown("## 2️⃣ Select Models")

    st.markdown("Choose which LLM models to evaluate:")

    selected_models = []

    for provider, models in MODELS.items():
        with st.expander(f"**{provider}**", expanded=True):
            cols = st.columns(3)
            for idx, (model_id, info) in enumerate(models.items()):
                with cols[idx % 3]:
                    if st.checkbox(
                        info["name"],
                        key=f"model_{model_id}",
                        help=f"Cost: {info['cost']} | Speed: {info['speed']} | Quality: {info['quality']}"
                    ):
                        selected_models.append(model_id)
                    st.caption(f"💰 {info['cost']} | ⚡ {info['speed']}")

    if not selected_models:
        st.warning("⚠️ Please select at least one model")
    else:
        st.success(f"✅ Selected {len(selected_models)} model(s)")

    st.markdown("---")

    # Step 3: Prompts
    st.markdown("## 3️⃣ Configure Prompts")

    tab1, tab2, tab3 = st.tabs(["📝 Templates", "✍️ Custom", "📁 Upload"])

    with tab1:
        st.markdown("**Select prompt templates to test:**")

        for template_name, template_text in PROMPT_TEMPLATES.items():
            if template_name != "Custom":
                if st.checkbox(template_name, key=f"template_{template_name}"):
                    st.session_state.prompts[template_name.lower()] = template_text
                    st.code(template_text, language="text")

    with tab2:
        st.markdown("**Write custom prompts:**")

        num_custom = st.number_input("Number of custom prompts", min_value=0, max_value=10, value=0)

        for i in range(num_custom):
            col1, col2 = st.columns([1, 3])
            with col1:
                prompt_id = st.text_input(f"Prompt ID #{i+1}", value=f"custom_{i+1}", key=f"custom_id_{i}")
            with col2:
                prompt_text = st.text_area(f"Prompt Text #{i+1}", key=f"custom_text_{i}", height=100)
                if prompt_text:
                    st.session_state.prompts[prompt_id] = prompt_text

    with tab3:
        st.markdown("**Upload prompts JSON file:**")

        uploaded_prompts = st.file_uploader("Upload prompts.json", type="json", key="upload_prompts")

        if uploaded_prompts:
            try:
                prompts_data = json.load(uploaded_prompts)
                st.session_state.prompts.update(prompts_data)
                st.success(f"✅ Loaded {len(prompts_data)} prompts")
                st.json(prompts_data)
            except Exception as e:
                st.error(f"❌ Error loading prompts: {str(e)}")

    if st.session_state.prompts:
        st.info(f"📝 Total prompts configured: {len(st.session_state.prompts)}")
    else:
        st.warning("⚠️ Please configure at least one prompt")

    st.markdown("---")

    # Step 4: Test Cases
    st.markdown("## 4️⃣ Configure Test Cases")

    tab1, tab2, tab3 = st.tabs(["✍️ Quick Add", "📝 Detailed", "📁 Upload"])

    with tab1:
        st.markdown("**Quick test case entry:**")

        quick_test = st.text_area(
            "Enter test questions (one per line)",
            placeholder="What is the capital of France?\nExplain quantum computing\nWrite a Python function to sort a list",
            height=150
        )

        if quick_test:
            questions = [q.strip() for q in quick_test.split('\n') if q.strip()]
            st.session_state.test_cases = [
                {
                    "id": f"test_{i+1}",
                    "question": q,
                    "min_words": 10
                }
                for i, q in enumerate(questions)
            ]
            st.success(f"✅ Added {len(questions)} test cases")

    with tab2:
        st.markdown("**Detailed test case configuration:**")

        num_tests = st.number_input("Number of test cases", min_value=0, max_value=50, value=0)

        for i in range(num_tests):
            with st.expander(f"Test Case #{i+1}"):
                test_id = st.text_input("Test ID", value=f"test_{i+1}", key=f"test_id_{i}")
                question = st.text_area("Question", key=f"test_q_{i}", height=80)

                col1, col2 = st.columns(2)
                with col1:
                    expected = st.text_input("Expected Output (optional)", key=f"test_exp_{i}")
                    keywords = st.text_input("Required Keywords (comma-separated)", key=f"test_kw_{i}")

                with col2:
                    min_words = st.number_input("Min Words", min_value=0, value=10, key=f"test_min_{i}")
                    max_words = st.number_input("Max Words", min_value=0, value=0, key=f"test_max_{i}")

                if question:
                    test_case = {"id": test_id, "question": question, "min_words": min_words}
                    if expected:
                        test_case["expected_output"] = expected
                    if keywords:
                        test_case["required_keywords"] = [k.strip() for k in keywords.split(',')]
                    if max_words > 0:
                        test_case["max_words"] = max_words

                    # Update or add test case
                    existing = next((tc for tc in st.session_state.test_cases if tc["id"] == test_id), None)
                    if existing:
                        existing.update(test_case)
                    else:
                        st.session_state.test_cases.append(test_case)

    with tab3:
        st.markdown("**Upload test cases JSON file:**")

        uploaded_tests = st.file_uploader("Upload test_cases.json", type="json", key="upload_tests")

        if uploaded_tests:
            try:
                tests_data = json.load(uploaded_tests)
                st.session_state.test_cases = tests_data
                st.success(f"✅ Loaded {len(tests_data)} test cases")
                st.json(tests_data)
            except Exception as e:
                st.error(f"❌ Error loading test cases: {str(e)}")

    if st.session_state.test_cases:
        st.info(f"🧪 Total test cases configured: {len(st.session_state.test_cases)}")
    else:
        st.warning("⚠️ Please configure at least one test case")

    st.markdown("---")

    # Step 5: Review & Launch
    st.markdown("## 5️⃣ Review & Launch")

    col1, col2, col3 = st.columns(3)

    total_evaluations = len(selected_models) * len(st.session_state.prompts) * len(st.session_state.test_cases)

    col1.metric("Models", len(selected_models))
    col2.metric("Prompts", len(st.session_state.prompts))
    col3.metric("Test Cases", len(st.session_state.test_cases))

    st.metric(
        "📊 Total Evaluations",
        f"{total_evaluations:,}",
        help="Models × Prompts × Test Cases"
    )

    # Estimate costs
    if total_evaluations > 0:
        estimated_cost_min = total_evaluations * 0.0005  # Conservative estimate
        estimated_cost_max = total_evaluations * 0.025   # High estimate

        st.markdown(f"""
        <div class="info-box">
        <strong>💰 Estimated Cost: ${estimated_cost_min:.2f} - ${estimated_cost_max:.2f}</strong><br>
        Actual cost depends on response length and models used.<br>
        Budget limit: ${budget_limit:.2f}
        </div>
        """, unsafe_allow_html=True)

    # Validation
    can_launch = (
        len(selected_models) > 0 and
        len(st.session_state.prompts) > 0 and
        len(st.session_state.test_cases) > 0
    )

    st.markdown("---")

    # Launch buttons
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if can_launch:
            if st.button("🚀 Start Evaluation", type="primary", use_container_width=True):
                # Save configuration
                config = {
                    "experiment_name": experiment_name,
                    "budget_limit": budget_limit,
                    "models": selected_models,
                    "prompts": st.session_state.prompts,
                    "test_cases": st.session_state.test_cases,
                    "email_notifications": {
                        "enabled": enable_email,
                        "recipient": notify_email if enable_email else None,
                        "attach_results": attach_results if enable_email else False
                    } if enable_email else None
                }

                config_file = Path(__file__).parent.parent.parent / f"config_{experiment_name}.json"
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=2)

                st.success(f"✅ Configuration saved to {config_file.name}")

                # Show email notification status
                if enable_email and notify_email:
                    st.info(f"📧 Results will be emailed to: {notify_email}")

                st.markdown("""
                <div class="success-box">
                <strong>🎉 Evaluation Ready to Launch!</strong><br><br>
                To run the evaluation, execute this command in your terminal:<br><br>
                <code>python -m modal run main.py --experiment-name="{}" --budget-limit={}</code><br><br>
                Or run it programmatically from code.<br>
                Results will appear in the "Results" tab when complete.{}
                </div>
                """.format(
                    experiment_name,
                    budget_limit,
                    f"<br>📧 Email notification will be sent to {notify_email}" if enable_email and notify_email else ""
                ), unsafe_allow_html=True)

                st.info("💡 **Tip:** This will run in Modal's cloud. Make sure you've set up your API keys!")
        else:
            st.button("🚀 Start Evaluation", type="primary", disabled=True, use_container_width=True)
            st.error("❌ Please complete all configuration steps above")

    # Export config option
    if can_launch:
        st.markdown("---")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="📥 Download Configuration",
                data=json.dumps(config, indent=2),
                file_name=f"config_{experiment_name}.json",
                mime="application/json",
                use_container_width=True
            )


if __name__ == "__main__":
    show()
