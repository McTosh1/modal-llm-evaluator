"""
Settings page - Configuration and preferences
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def show():
    """Display settings page"""

    st.title("⚙️ Settings")
    st.markdown("Configure your LLM Evaluator preferences and API keys")

    st.markdown("---")

    # API Keys section
    st.markdown("## 🔑 API Keys")

    st.markdown("""
    API keys are managed through Modal secrets for security.

    **To configure API keys:**

    ```bash
    # Anthropic Claude
    python -m modal secret create anthropic-key ANTHROPIC_API_KEY=sk-ant-...

    # OpenAI GPT
    python -m modal secret create openai-key OPENAI_API_KEY=sk-...

    # Google Gemini
    python -m modal secret create google-api-key GOOGLE_API_KEY=...
    ```

    **To list your secrets:**
    ```bash
    python -m modal secret list
    ```

    **To update a secret:**
    ```bash
    python -m modal secret create anthropic-key ANTHROPIC_API_KEY=new-key --force
    ```
    """)

    st.markdown("### Get API Keys")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Anthropic Claude**")
        st.link_button(
            "Get API Key",
            "https://console.anthropic.com/account/keys",
            use_container_width=True
        )

    with col2:
        st.markdown("**OpenAI GPT**")
        st.link_button(
            "Get API Key",
            "https://platform.openai.com/api-keys",
            use_container_width=True
        )

    with col3:
        st.markdown("**Google Gemini**")
        st.link_button(
            "Get API Key",
            "https://makersuite.google.com/app/apikey",
            use_container_width=True
        )

    st.markdown("---")

    # Email Configuration
    st.markdown("## 📧 Email Configuration")

    st.markdown("""
    Configure email notifications for evaluation results and alerts.
    """)

    with st.expander("📖 How to Get SMTP Credentials", expanded=False):
        st.markdown("""
        ### Brevo (Recommended - Free)

        1. Sign up at [brevo.com](https://www.brevo.com)
        2. Go to **SMTP & API**
        3. Click **Generate a new SMTP key**
        4. Copy the key and use settings below:
           - Server: `smtp-relay.brevo.com`
           - Port: `587`
           - Username: Your Brevo login email
           - Password: The generated SMTP key

        ### Free Tier: 300 emails/day
        """)

    col1, col2 = st.columns(2)

    with col1:
        smtp_server = st.text_input(
            "SMTP Server",
            value=st.session_state.get("smtp_server", "smtp-relay.brevo.com"),
            help="SMTP server address (e.g., smtp-relay.brevo.com)"
        )
        st.session_state.smtp_server = smtp_server

        smtp_port = st.number_input(
            "SMTP Port",
            value=st.session_state.get("smtp_port", 587),
            min_value=1,
            max_value=65535,
            help="Usually 587 for TLS or 465 for SSL"
        )
        st.session_state.smtp_port = smtp_port

    with col2:
        smtp_username = st.text_input(
            "SMTP Username",
            value=st.session_state.get("smtp_username", ""),
            help="Your email address or SMTP username"
        )
        st.session_state.smtp_username = smtp_username

        smtp_password = st.text_input(
            "SMTP Password",
            value=st.session_state.get("smtp_password", ""),
            type="password",
            help="Your SMTP password or API key"
        )
        st.session_state.smtp_password = smtp_password

    col1, col2 = st.columns(2)

    with col1:
        from_email = st.text_input(
            "From Email Address",
            value=st.session_state.get("from_email", "ai@synapmarketing.com"),
            help="The email address to send from"
        )
        st.session_state.from_email = from_email

    with col2:
        from_name = st.text_input(
            "From Name",
            value=st.session_state.get("from_name", "LLM Evaluator"),
            help="The sender name that will appear"
        )
        st.session_state.from_name = from_name

    # Test email section
    st.markdown("### Test Email")

    col1, col2 = st.columns([2, 1])

    with col1:
        test_email = st.text_input(
            "Send test email to",
            placeholder="your-email@gmail.com",
            help="Enter your email to receive a test"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        if st.button("📧 Send Test Email", use_container_width=True):
            if not all([smtp_server, smtp_port, smtp_username, smtp_password, from_email, test_email]):
                st.error("❌ Please fill in all email settings first")
            else:
                with st.spinner("Sending test email..."):
                    try:
                        import sys
                        from pathlib import Path
                        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
                        from evaluator.email_notify import EmailNotifier

                        notifier = EmailNotifier(
                            smtp_server=smtp_server,
                            smtp_port=smtp_port,
                            username=smtp_username,
                            password=smtp_password,
                            from_email=from_email,
                            from_name=from_name
                        )

                        success = notifier.send_test(test_email)

                        if success:
                            st.success(f"✅ Test email sent to {test_email}!")
                            st.info("💡 Check your inbox (and spam folder if needed)")
                        else:
                            st.error("❌ Failed to send email. Check your credentials.")

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.code(str(e))

    # Email preferences
    st.markdown("### Email Preferences")

    col1, col2 = st.columns(2)

    with col1:
        notify_on_complete = st.checkbox(
            "📬 Notify when evaluation completes",
            value=st.session_state.get("notify_on_complete", True),
            help="Send email when evaluation finishes"
        )
        st.session_state.notify_on_complete = notify_on_complete

    with col2:
        notify_on_budget = st.checkbox(
            "💰 Notify when budget limit reached",
            value=st.session_state.get("notify_on_budget", True),
            help="Send alert when budget is exceeded"
        )
        st.session_state.notify_on_budget = notify_on_budget

    # Save confirmation
    if any([smtp_username, smtp_password]):
        st.success("✅ Email settings saved to session")
        st.caption("Note: Settings are saved for this session only. Configure permanently via environment variables.")

    st.markdown("---")

    # Power BI Integration
    st.markdown("## 📊 Power BI Integration")

    st.markdown("""
    Export evaluation results to a database for Power BI dashboards.

    **Supported Databases:**
    - PostgreSQL
    - SQL Server / Azure SQL
    - MySQL
    - SQLite
    """)

    with st.expander("Database Connection Examples"):
        st.code("""
# PostgreSQL
postgresql://username:password@localhost:5432/database_name

# Azure SQL Server
mssql+pyodbc://username:password@server.database.windows.net:1433/dbname?driver=ODBC+Driver+17+for+SQL+Server

# MySQL
mysql+pymysql://username:password@localhost:3306/database_name

# SQLite (local file)
sqlite:///path/to/database.db
        """, language="text")

    db_url = st.text_input(
        "Database Connection String",
        type="password",
        placeholder="postgresql://user:pass@localhost:5432/mydb",
        help="Enter your database connection string"
    )

    if db_url:
        st.success("✅ Connection string saved (in session)")
        st.session_state.database_url = db_url

    st.markdown("---")

    # Modal Configuration
    st.markdown("## 🚀 Modal Configuration")

    st.markdown("""
    ### Check Modal Status
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Check Modal Auth", use_container_width=True):
            import subprocess
            result = subprocess.run(
                ["python", "-m", "modal", "token", "current"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                st.success("✅ Modal is authenticated")
            else:
                st.error("❌ Modal not authenticated. Run: python -m modal setup")

    with col2:
        if st.button("List Modal Secrets", use_container_width=True):
            import subprocess
            result = subprocess.run(
                ["python", "-m", "modal", "secret", "list"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                st.success("✅ See terminal for secrets list")
                st.code(result.stdout)
            else:
                st.error("❌ Error listing secrets")

    st.markdown("---")

    # Preferences
    st.markdown("## 🎨 Preferences")

    col1, col2 = st.columns(2)

    with col1:
        default_budget = st.number_input(
            "Default Budget Limit ($)",
            min_value=1.0,
            max_value=1000.0,
            value=10.0,
            step=1.0
        )
        st.session_state.default_budget = default_budget

    with col2:
        auto_export = st.checkbox(
            "Auto-export to Power BI",
            value=False,
            help="Automatically export results to database after evaluation"
        )
        st.session_state.auto_export = auto_export

    st.markdown("---")

    # About
    st.markdown("## ℹ️ About")

    st.markdown("""
    ### Modal LLM Evaluator v1.0

    A powerful platform for evaluating LLM prompts at scale with:
    - ⚡ Parallel execution on Modal
    - 💰 Real-time cost tracking
    - 📊 Power BI integration
    - 🔄 Multi-provider support

    **Built with:**
    - [Modal](https://modal.com) - Serverless compute
    - [Streamlit](https://streamlit.io) - Web interface
    - [Anthropic](https://anthropic.com) - Claude AI
    - [OpenAI](https://openai.com) - GPT models
    - [Google](https://ai.google.dev/) - Gemini models

    ---

    **Documentation:**
    - 📖 [README](../README.md)
    - 🚀 [Quick Start](../QUICKSTART.md)
    - 💡 [Examples](../examples/)
    - 📋 [Project Summary](../PROJECT_SUMMARY.md)

    ---

    Made with ❤️ for data scientists
    """)

    # System info
    with st.expander("System Information"):
        import pandas as pd

        # Try to import optional dependencies (may not be available on Streamlit Cloud)
        try:
            import modal
            modal_version = modal.__version__
        except ImportError:
            modal_version = "Not installed (run locally)"

        try:
            import anthropic
            anthropic_version = anthropic.__version__
        except ImportError:
            anthropic_version = "Not installed"

        try:
            import openai
            openai_version = openai.__version__
        except ImportError:
            openai_version = "Not installed"

        info = {
            "Modal Version": modal_version,
            "Streamlit Version": st.__version__,
            "Pandas Version": pd.__version__,
            "Anthropic SDK": anthropic_version,
            "OpenAI SDK": openai_version,
            "Python Path": sys.executable,
        }

        for key, value in info.items():
            st.text(f"{key}: {value}")


if __name__ == "__main__":
    show()
