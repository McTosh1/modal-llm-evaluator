"""
Cost Tracker page - Analyze spending across evaluations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def show():
    """Display cost tracker page"""

    st.title("💰 Cost Tracker")
    st.markdown("Monitor and analyze your LLM evaluation spending")

    st.markdown("---")

    # Find all result files
    results_dir = Path(__file__).parent.parent.parent
    result_files = list(results_dir.glob("results_*.xlsx"))

    if not result_files:
        st.info("""
        ### 🔍 No Cost Data Available

        Run evaluations to see cost tracking here!

        Cost tracking includes:
        - Total spend across experiments
        - Cost by model and provider
        - Cost per evaluation trends
        - Budget utilization
        """)
        return

    # Load all results
    all_results = []
    for file in result_files:
        try:
            df = pd.read_excel(file, sheet_name="Results")
            df["experiment"] = file.stem
            all_results.append(df)
        except:
            continue

    if not all_results:
        st.warning("No valid results found")
        return

    combined_df = pd.concat(all_results, ignore_index=True)

    # Overall metrics
    st.markdown("## 📊 Overall Spending")

    col1, col2, col3, col4 = st.columns(4)

    total_cost = combined_df["cost"].sum() if "cost" in combined_df.columns else 0
    total_evals = len(combined_df)
    avg_cost_per_eval = total_cost / total_evals if total_evals > 0 else 0
    num_experiments = combined_df["experiment"].nunique()

    col1.metric("Total Spend", f"${total_cost:.2f}")
    col2.metric("Total Evaluations", f"{total_evals:,}")
    col3.metric("Avg Cost/Eval", f"${avg_cost_per_eval:.4f}")
    col4.metric("Experiments", num_experiments)

    st.markdown("---")

    # Cost breakdown
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💸 Cost by Model")

        if "model" in combined_df.columns and "cost" in combined_df.columns:
            model_costs = combined_df.groupby("model")["cost"].sum().sort_values(ascending=False)

            fig1 = px.bar(
                model_costs.reset_index(),
                x="model",
                y="cost",
                title="Total Cost by Model",
                labels={"cost": "Total Cost ($)", "model": "Model"},
                color="cost",
                color_continuous_scale="Reds"
            )
            fig1.update_traces(texttemplate='$%{y:.2f}', textposition='outside')
            st.plotly_chart(fig1, use_container_width=True)

            # Data table
            st.dataframe(
                model_costs.reset_index().rename(columns={"cost": "Total Cost ($)"}),
                use_container_width=True,
                hide_index=True
            )

    with col2:
        st.markdown("### 📈 Cost by Provider")

        if "provider" in combined_df.columns and "cost" in combined_df.columns:
            provider_costs = combined_df.groupby("provider")["cost"].sum()

            fig2 = px.pie(
                provider_costs.reset_index(),
                values="cost",
                names="provider",
                title="Cost Distribution by Provider"
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Data table
            st.dataframe(
                provider_costs.reset_index().rename(columns={"cost": "Total Cost ($)"}),
                use_container_width=True,
                hide_index=True
            )

    st.markdown("---")

    # Cost over time
    st.markdown("### 📅 Cost Over Time")

    if "timestamp" in combined_df.columns:
        combined_df["date"] = pd.to_datetime(combined_df["timestamp"]).dt.date

        daily_costs = combined_df.groupby("date")["cost"].sum().reset_index()

        fig3 = px.line(
            daily_costs,
            x="date",
            y="cost",
            title="Daily Spending",
            labels={"cost": "Daily Cost ($)", "date": "Date"},
            markers=True
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Cost per experiment
    st.markdown("---")
    st.markdown("### 🧪 Cost by Experiment")

    exp_costs = combined_df.groupby("experiment").agg({
        "cost": "sum",
        "test_case_id": "count"
    }).rename(columns={"test_case_id": "Evaluations", "cost": "Total Cost"})

    exp_costs["Avg Cost/Eval"] = exp_costs["Total Cost"] / exp_costs["Evaluations"]

    st.dataframe(
        exp_costs.style.format({
            "Total Cost": "${:.2f}",
            "Avg Cost/Eval": "${:.4f}"
        }),
        use_container_width=True
    )

    # Cost efficiency analysis
    st.markdown("---")
    st.markdown("### ⚡ Cost Efficiency Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Most Cost-Effective Models**")

        if "model" in combined_df.columns and "pass" in combined_df.columns:
            efficiency = combined_df.groupby("model").agg({
                "cost": "mean",
                "pass": "mean"
            })
            efficiency["efficiency_score"] = efficiency["pass"] / efficiency["cost"]
            efficiency = efficiency.sort_values("efficiency_score", ascending=False)

            st.dataframe(
                efficiency.style.format({
                    "cost": "${:.4f}",
                    "pass": "{:.1%}",
                    "efficiency_score": "{:.2f}"
                }).background_gradient(subset=["efficiency_score"], cmap="RdYlGn"),
                use_container_width=True
            )

    with col2:
        st.markdown("**Cost vs Quality Trade-off**")

        if "model" in combined_df.columns and "cost" in combined_df.columns and "pass" in combined_df.columns:
            model_stats = combined_df.groupby("model").agg({
                "cost": "mean",
                "pass": "mean"
            }).reset_index()

            fig4 = px.scatter(
                model_stats,
                x="cost",
                y="pass",
                text="model",
                title="Cost vs Pass Rate",
                labels={"cost": "Avg Cost per Eval ($)", "pass": "Pass Rate"},
                size=[10] * len(model_stats)
            )
            fig4.update_traces(textposition="top center")
            fig4.update_layout(yaxis_tickformat=".0%")
            st.plotly_chart(fig4, use_container_width=True)

    # Budget recommendations
    st.markdown("---")
    st.markdown("### 💡 Budget Recommendations")

    if total_evals > 0:
        st.markdown(f"""
        <div class="info-box">
        <strong>Based on your {total_evals:,} evaluations:</strong><br><br>
        • Average cost per evaluation: <strong>${avg_cost_per_eval:.4f}</strong><br>
        • For 1,000 evaluations, budget: <strong>${avg_cost_per_eval * 1000:.2f}</strong><br>
        • For 10,000 evaluations, budget: <strong>${avg_cost_per_eval * 10000:.2f}</strong><br><br>
        💡 Tip: Use cheaper models (Haiku, GPT-4o-mini) for testing, then upgrade to premium models for production.
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    show()
