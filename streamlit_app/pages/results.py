"""
Results page - View and analyze evaluation results
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def load_results(file_path):
    """Load results from Excel file"""
    try:
        # Load all sheets
        xl_file = pd.ExcelFile(file_path)
        sheets = {}
        for sheet_name in xl_file.sheet_names:
            sheets[sheet_name] = pd.read_excel(file_path, sheet_name=sheet_name)
        return sheets
    except Exception as e:
        st.error(f"Error loading results: {str(e)}")
        return None


def show():
    """Display results page"""

    st.title("📊 Evaluation Results")
    st.markdown("Analyze and explore your LLM evaluation results")

    st.markdown("---")

    # Find result files
    results_dir = Path(__file__).parent.parent.parent
    result_files = sorted(
        results_dir.glob("results_*.xlsx"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    if not result_files:
        st.info("""
        ### 🔍 No Results Found

        Run an evaluation first to see results here!

        👉 Go to **Run Evaluation** to get started
        """)
        return

    # File selector
    selected_file = st.selectbox(
        "Select Experiment",
        result_files,
        format_func=lambda x: x.name
    )

    if not selected_file:
        return

    # Load results
    with st.spinner("Loading results..."):
        sheets = load_results(selected_file)

    if not sheets:
        return

    results_df = sheets.get("Results")
    model_summary = sheets.get("Model Summary")
    prompt_summary = sheets.get("Prompt Summary")

    # Overview metrics
    st.markdown("## 📈 Overview")

    col1, col2, col3, col4 = st.columns(4)

    if results_df is not None:
        total_evals = len(results_df)
        successful = results_df["success"].sum() if "success" in results_df.columns else 0
        total_cost = results_df["cost"].sum() if "cost" in results_df.columns else 0
        pass_rate = results_df["pass"].mean() * 100 if "pass" in results_df.columns else 0

        col1.metric("Total Evaluations", f"{total_evals:,}")
        col2.metric("Success Rate", f"{(successful/total_evals*100):.1f}%")
        col3.metric("Total Cost", f"${total_cost:.2f}")
        col4.metric("Pass Rate", f"{pass_rate:.1f}%")

    st.markdown("---")

    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Detailed Results", "🤖 By Model", "📝 By Prompt"])

    with tab1:
        st.markdown("### Performance Overview")

        if results_df is not None and len(results_df) > 0:
            # Pass rate by model
            if "model" in results_df.columns and "pass" in results_df.columns:
                fig1 = px.bar(
                    results_df.groupby("model")["pass"].mean().reset_index(),
                    x="model",
                    y="pass",
                    title="Pass Rate by Model",
                    labels={"pass": "Pass Rate", "model": "Model"},
                    color="pass",
                    color_continuous_scale="RdYlGn"
                )
                fig1.update_traces(texttemplate='%{y:.1%}', textposition='outside')
                fig1.update_layout(showlegend=False, yaxis_tickformat='.0%')
                st.plotly_chart(fig1, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                # Cost by model
                if "model" in results_df.columns and "cost" in results_df.columns:
                    cost_by_model = results_df.groupby("model")["cost"].sum().reset_index()
                    fig2 = px.pie(
                        cost_by_model,
                        values="cost",
                        names="model",
                        title="Cost Distribution by Model"
                    )
                    st.plotly_chart(fig2, use_container_width=True)

            with col2:
                # Latency by model
                if "model" in results_df.columns and "latency" in results_df.columns:
                    fig3 = px.box(
                        results_df,
                        x="model",
                        y="latency",
                        title="Latency Distribution by Model",
                        labels={"latency": "Latency (seconds)", "model": "Model"}
                    )
                    st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        st.markdown("### Detailed Results")

        if results_df is not None:
            # Filters
            col1, col2, col3 = st.columns(3)

            with col1:
                if "model" in results_df.columns:
                    model_filter = st.multiselect(
                        "Filter by Model",
                        options=results_df["model"].unique(),
                        default=[]
                    )

            with col2:
                if "prompt_id" in results_df.columns:
                    prompt_filter = st.multiselect(
                        "Filter by Prompt",
                        options=results_df["prompt_id"].unique(),
                        default=[]
                    )

            with col3:
                if "pass" in results_df.columns:
                    pass_filter = st.selectbox(
                        "Filter by Result",
                        options=["All", "Passed", "Failed"]
                    )

            # Apply filters
            filtered_df = results_df.copy()

            if model_filter:
                filtered_df = filtered_df[filtered_df["model"].isin(model_filter)]

            if prompt_filter:
                filtered_df = filtered_df[filtered_df["prompt_id"].isin(prompt_filter)]

            if pass_filter == "Passed":
                filtered_df = filtered_df[filtered_df["pass"] == True]
            elif pass_filter == "Failed":
                filtered_df = filtered_df[filtered_df["pass"] == False]

            st.markdown(f"**Showing {len(filtered_df)} of {len(results_df)} results**")

            # Display table
            display_cols = ["model", "prompt_id", "test_case_id", "pass", "cost", "latency", "success"]
            display_cols = [col for col in display_cols if col in filtered_df.columns]

            st.dataframe(
                filtered_df[display_cols],
                use_container_width=True,
                height=400
            )

            # Expandable detailed view
            if len(filtered_df) > 0:
                st.markdown("---")
                st.markdown("**Detailed View**")

                selected_idx = st.selectbox(
                    "Select row to view details",
                    range(len(filtered_df)),
                    format_func=lambda x: f"Row {x+1}: {filtered_df.iloc[x].get('model', 'N/A')} - {filtered_df.iloc[x].get('test_case_id', 'N/A')}"
                )

                if selected_idx is not None:
                    row = filtered_df.iloc[selected_idx]

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**Input**")
                        st.text_area("Prompt", value=row.get("input", "N/A"), height=150, disabled=True)

                    with col2:
                        st.markdown("**Output**")
                        st.text_area("Response", value=row.get("output", "N/A"), height=150, disabled=True)

                    # Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Cost", f"${row.get('cost', 0):.4f}")
                    col2.metric("Latency", f"{row.get('latency', 0):.2f}s")
                    col3.metric("Pass", "✅" if row.get("pass") else "❌")
                    col4.metric("Success", "✅" if row.get("success") else "❌")

    with tab3:
        st.markdown("### Performance by Model")

        if model_summary is not None:
            st.dataframe(model_summary, use_container_width=True)

            # Model comparison chart
            if len(model_summary) > 0:
                fig = go.Figure()

                fig.add_trace(go.Bar(
                    name="Total Cost",
                    x=model_summary.index,
                    y=model_summary["Total Cost"],
                    yaxis="y",
                    offsetgroup=1
                ))

                fig.add_trace(go.Bar(
                    name="Pass Rate",
                    x=model_summary.index,
                    y=model_summary["Pass Rate"],
                    yaxis="y2",
                    offsetgroup=2
                ))

                fig.update_layout(
                    title="Model Comparison: Cost vs Pass Rate",
                    xaxis=dict(title="Model"),
                    yaxis=dict(title="Total Cost ($)", side="left"),
                    yaxis2=dict(title="Pass Rate", side="right", overlaying="y", tickformat=".0%"),
                    barmode="group",
                    height=500
                )

                st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.markdown("### Performance by Prompt")

        if prompt_summary is not None:
            st.dataframe(prompt_summary, use_container_width=True)

            # Prompt comparison
            if len(prompt_summary) > 0 and "Pass Rate" in prompt_summary.columns:
                fig = px.bar(
                    prompt_summary.reset_index(),
                    x="prompt_id",
                    y="Pass Rate",
                    title="Prompt Performance Comparison",
                    color="Pass Rate",
                    color_continuous_scale="RdYlGn",
                    labels={"prompt_id": "Prompt", "Pass Rate": "Pass Rate"}
                )
                fig.update_traces(texttemplate='%{y:.1%}', textposition='outside')
                fig.update_layout(yaxis_tickformat='.0%')
                st.plotly_chart(fig, use_container_width=True)

    # Download section
    st.markdown("---")
    st.markdown("## 📥 Export Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if results_df is not None:
            csv_data = results_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"{selected_file.stem}.csv",
                mime="text/csv",
                use_container_width=True
            )

    with col2:
        with open(selected_file, 'rb') as f:
            st.download_button(
                label="Download Excel",
                data=f.read(),
                file_name=selected_file.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    with col3:
        if results_df is not None:
            json_data = results_df.to_json(orient="records", indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"{selected_file.stem}.json",
                mime="application/json",
                use_container_width=True
            )

    with col4:
        if st.button("📧 Email Results", use_container_width=True):
            st.session_state.show_email_dialog = True

    # Email dialog
    if st.session_state.get("show_email_dialog", False):
        with st.form("email_results_form"):
            st.markdown("### 📧 Email Results")

            recipient = st.text_input(
                "Send to",
                value=st.session_state.get("smtp_username", ""),
                placeholder="recipient@example.com"
            )

            include_attachment = st.checkbox(
                "Include Excel file as attachment",
                value=True
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.form_submit_button("Send Email", type="primary", use_container_width=True):
                    if not st.session_state.get("smtp_username"):
                        st.error("❌ Email not configured. Go to Settings to set up SMTP.")
                    elif not recipient:
                        st.error("❌ Please enter recipient email")
                    else:
                        with st.spinner("Sending email..."):
                            try:
                                sys.path.insert(0, str(Path(__file__).parent.parent.parent))
                                from evaluator.email_notify import EmailNotifier

                                # Get summary stats
                                summary = {
                                    "total_evaluations": len(results_df),
                                    "pass_rate": results_df["pass"].mean() if "pass" in results_df.columns else 0,
                                    "total_cost": results_df["cost"].sum() if "cost" in results_df.columns else 0,
                                    "avg_latency": results_df["latency"].mean() if "latency" in results_df.columns else 0
                                }

                                # Determine best model
                                best_model = None
                                if "model" in results_df.columns and "pass" in results_df.columns:
                                    model_perf = results_df.groupby("model")["pass"].mean()
                                    best_model = model_perf.idxmax()

                                notifier = EmailNotifier(
                                    smtp_server=st.session_state.get("smtp_server"),
                                    smtp_port=st.session_state.get("smtp_port"),
                                    username=st.session_state.get("smtp_username"),
                                    password=st.session_state.get("smtp_password"),
                                    from_email=st.session_state.get("from_email", "ai@synapmarketing.com"),
                                    from_name=st.session_state.get("from_name", "LLM Evaluator")
                                )

                                success = notifier.send_evaluation_complete(
                                    to_email=recipient,
                                    experiment_name=selected_file.stem.replace("results_", ""),
                                    total_evaluations=summary["total_evaluations"],
                                    pass_rate=summary["pass_rate"],
                                    total_cost=summary["total_cost"],
                                    avg_latency=summary["avg_latency"],
                                    best_model=best_model,
                                    results_file=str(selected_file) if include_attachment else None
                                )

                                if success:
                                    st.success(f"✅ Results emailed to {recipient}!")
                                    st.session_state.show_email_dialog = False
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to send email")

                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")

            with col2:
                if st.form_submit_button("Cancel", use_container_width=True):
                    st.session_state.show_email_dialog = False
                    st.rerun()


if __name__ == "__main__":
    show()
