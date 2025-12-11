"""
Model Comparison page - Side-by-side model analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def show():
    """Display model comparison page"""

    st.title("🔄 Model Comparison")
    st.markdown("Compare LLM models side-by-side across multiple dimensions")

    st.markdown("---")

    # Load results
    results_dir = Path(__file__).parent.parent.parent
    result_files = sorted(
        results_dir.glob("results_*.xlsx"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    if not result_files:
        st.info("Run evaluations to see model comparisons!")
        return

    # File selector
    selected_file = st.selectbox(
        "Select Experiment",
        result_files,
        format_func=lambda x: x.name
    )

    try:
        df = pd.read_excel(selected_file, sheet_name="Results")
    except:
        st.error("Error loading results")
        return

    if "model" not in df.columns:
        st.warning("No model data available")
        return

    # Model selector
    models = df["model"].unique().tolist()

    st.markdown("### Select Models to Compare")

    selected_models = st.multiselect(
        "Choose 2-5 models",
        models,
        default=models[:min(3, len(models))],
        max_selections=5
    )

    if len(selected_models) < 2:
        st.warning("Please select at least 2 models to compare")
        return

    # Filter data
    comparison_df = df[df["model"].isin(selected_models)]

    st.markdown("---")

    # Comparison metrics
    st.markdown("## 📊 Performance Comparison")

    metrics = comparison_df.groupby("model").agg({
        "pass": ["mean", "count"],
        "cost": ["sum", "mean"],
        "latency": ["mean", "median"],
        "success": "mean"
    }).round(4)

    metrics.columns = [
        "Pass Rate", "Total Evals",
        "Total Cost", "Avg Cost",
        "Avg Latency", "Median Latency",
        "Success Rate"
    ]

    st.dataframe(
        metrics.style.format({
            "Pass Rate": "{:.1%}",
            "Total Cost": "${:.2f}",
            "Avg Cost": "${:.4f}",
            "Avg Latency": "{:.2f}s",
            "Median Latency": "{:.2f}s",
            "Success Rate": "{:.1%}"
        }).background_gradient(subset=["Pass Rate"], cmap="RdYlGn"),
        use_container_width=True
    )

    st.markdown("---")

    # Radar chart
    st.markdown("### 📡 Multi-Dimensional Comparison")

    # Normalize metrics for radar chart
    radar_data = comparison_df.groupby("model").agg({
        "pass": "mean",
        "cost": "mean",
        "latency": "mean",
        "success": "mean"
    })

    # Invert cost and latency (lower is better)
    radar_data["cost"] = 1 / (radar_data["cost"] + 0.0001)
    radar_data["latency"] = 1 / (radar_data["latency"] + 0.1)

    # Normalize to 0-1
    for col in radar_data.columns:
        radar_data[col] = (radar_data[col] - radar_data[col].min()) / (radar_data[col].max() - radar_data[col].min())

    fig = go.Figure()

    categories = ["Quality (Pass Rate)", "Cost Efficiency", "Speed", "Reliability"]

    for model in selected_models:
        if model in radar_data.index:
            values = [
                radar_data.loc[model, "pass"],
                radar_data.loc[model, "cost"],
                radar_data.loc[model, "latency"],
                radar_data.loc[model, "success"]
            ]
            values.append(values[0])  # Close the polygon

            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=model
            ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Model Performance Radar"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Detailed comparisons
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💰 Cost Comparison")

        cost_data = comparison_df.groupby("model")["cost"].agg(["sum", "mean", "min", "max"])

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name="Total Cost",
            x=cost_data.index,
            y=cost_data["sum"],
            text=cost_data["sum"].apply(lambda x: f"${x:.2f}"),
            textposition="outside"
        ))
        fig2.update_layout(title="Total Cost by Model", yaxis_title="Cost ($)")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown("### ⚡ Latency Comparison")

        fig3 = go.Figure()
        for model in selected_models:
            model_data = comparison_df[comparison_df["model"] == model]["latency"]
            fig3.add_trace(go.Box(
                y=model_data,
                name=model,
                boxmean="sd"
            ))
        fig3.update_layout(title="Latency Distribution", yaxis_title="Latency (seconds)")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # Winner analysis
    st.markdown("### 🏆 Winner Analysis")

    winners = {
        "Highest Pass Rate": metrics["Pass Rate"].idxmax(),
        "Lowest Cost": metrics["Total Cost"].idxmin(),
        "Fastest (Avg)": metrics["Avg Latency"].idxmin(),
        "Most Reliable": metrics["Success Rate"].idxmax(),
        "Best Value": (metrics["Pass Rate"] / metrics["Avg Cost"]).idxmax()
    }

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**🎯 Quality Leader**")
        st.success(f"**{winners['Highest Pass Rate']}**")
        st.caption(f"{metrics.loc[winners['Highest Pass Rate'], 'Pass Rate']:.1%} pass rate")

    with col2:
        st.markdown("**💰 Cost Leader**")
        st.success(f"**{winners['Lowest Cost']}**")
        st.caption(f"${metrics.loc[winners['Lowest Cost'], 'Total Cost']:.2f} total")

    with col3:
        st.markdown("**⚡ Speed Leader**")
        st.success(f"**{winners['Fastest (Avg)']}**")
        st.caption(f"{metrics.loc[winners['Fastest (Avg)'], 'Avg Latency']:.2f}s avg")

    st.markdown("---")

    # Recommendation
    st.markdown("### 💡 Recommendation")

    best_value = winners["Best Value"]
    best_quality = winners["Highest Pass Rate"]

    st.markdown(f"""
    <div class="success-box">
    <strong>Best Overall Value: {best_value}</strong><br>
    {best_value} offers the best balance of quality and cost.<br><br>

    <strong>Recommendations:</strong><br>
    • For maximum quality: Use <strong>{best_quality}</strong><br>
    • For cost efficiency: Use <strong>{winners['Lowest Cost']}</strong><br>
    • For speed: Use <strong>{winners['Fastest (Avg)']}</strong><br>
    • For best value: Use <strong>{best_value}</strong>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show()
