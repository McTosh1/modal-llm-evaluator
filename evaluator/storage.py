"""
Results storage and Power BI export functionality
"""

import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import sqlalchemy


class ResultsStorage:
    """Store and export evaluation results"""

    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results: List[Dict[str, Any]] = []

    def add_result(self, result: Dict[str, Any]):
        """Add a single evaluation result"""
        result["experiment_name"] = self.experiment_name
        result["timestamp"] = datetime.now().isoformat()
        self.results.append(result)

    def add_results(self, results: List[Dict[str, Any]]):
        """Add multiple evaluation results"""
        for result in results:
            self.add_result(result)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert results to pandas DataFrame"""
        if not self.results:
            return pd.DataFrame()

        df = pd.DataFrame(self.results)

        # Ensure consistent column ordering
        priority_cols = [
            "experiment_name", "timestamp", "prompt_id", "test_case_id",
            "model", "provider", "input", "output", "success",
            "latency", "cost", "pass"
        ]

        # Add priority columns that exist, then add remaining columns
        existing_priority = [col for col in priority_cols if col in df.columns]
        other_cols = [col for col in df.columns if col not in priority_cols]
        df = df[existing_priority + other_cols]

        return df

    def save_json(self, output_path: Optional[str] = None) -> str:
        """Save results as JSON"""
        if output_path is None:
            output_path = f"results_{self.experiment_name}_{self.timestamp}.json"

        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

        return output_path

    def save_csv(self, output_path: Optional[str] = None) -> str:
        """Save results as CSV"""
        if output_path is None:
            output_path = f"results_{self.experiment_name}_{self.timestamp}.csv"

        df = self.to_dataframe()
        df.to_csv(output_path, index=False)

        return output_path

    def save_excel(self, output_path: Optional[str] = None) -> str:
        """Save results as Excel with multiple sheets"""
        if output_path is None:
            output_path = f"results_{self.experiment_name}_{self.timestamp}.xlsx"

        df = self.to_dataframe()

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Main results sheet
            df.to_excel(writer, sheet_name='Results', index=False)

            # Summary by model
            if 'model' in df.columns and 'cost' in df.columns:
                model_summary = df.groupby('model').agg({
                    'cost': 'sum',
                    'latency': 'mean',
                    'pass': 'mean',
                    'test_case_id': 'count'
                }).round(4)
                model_summary.columns = ['Total Cost', 'Avg Latency', 'Pass Rate', 'Num Tests']
                model_summary.to_excel(writer, sheet_name='Model Summary')

            # Summary by prompt
            if 'prompt_id' in df.columns:
                prompt_summary = df.groupby('prompt_id').agg({
                    'cost': 'sum',
                    'latency': 'mean',
                    'pass': 'mean',
                    'test_case_id': 'count'
                }).round(4)
                prompt_summary.columns = ['Total Cost', 'Avg Latency', 'Pass Rate', 'Num Tests']
                prompt_summary.to_excel(writer, sheet_name='Prompt Summary')

        return output_path

    def export_to_powerbi_database(
        self,
        connection_string: str,
        table_name: str = "llm_evaluation_results"
    ) -> bool:
        """
        Export results to SQL database for Power BI

        Args:
            connection_string: SQLAlchemy database connection string
                             Example: "postgresql://user:pass@localhost/dbname"
                             Example: "mssql+pyodbc://user:pass@server/db?driver=ODBC+Driver+17+for+SQL+Server"
            table_name: Name of the table to create/append to

        Returns:
            True if successful
        """
        try:
            df = self.to_dataframe()
            engine = sqlalchemy.create_engine(connection_string)

            # Write to database
            df.to_sql(
                table_name,
                engine,
                if_exists='append',  # Append to existing data
                index=False
            )

            print(f"✅ Exported {len(df)} results to database table '{table_name}'")
            return True

        except Exception as e:
            print(f"❌ Failed to export to database: {str(e)}")
            return False

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics"""
        df = self.to_dataframe()

        if df.empty:
            return {"error": "No results to summarize"}

        summary = {
            "experiment_name": self.experiment_name,
            "total_evaluations": len(df),
            "successful_calls": df["success"].sum() if "success" in df.columns else 0,
            "failed_calls": (~df["success"]).sum() if "success" in df.columns else 0,
        }

        if "cost" in df.columns:
            summary["total_cost"] = df["cost"].sum()
            summary["avg_cost_per_call"] = df["cost"].mean()

        if "latency" in df.columns:
            summary["avg_latency"] = df["latency"].mean()
            summary["min_latency"] = df["latency"].min()
            summary["max_latency"] = df["latency"].max()

        if "pass" in df.columns:
            summary["pass_rate"] = df["pass"].mean()
            summary["passed"] = df["pass"].sum()
            summary["failed"] = (~df["pass"]).sum()

        if "model" in df.columns:
            summary["models_tested"] = df["model"].nunique()
            summary["best_model_by_pass_rate"] = (
                df.groupby("model")["pass"].mean().idxmax()
                if "pass" in df.columns else None
            )

        if "prompt_id" in df.columns:
            summary["prompts_tested"] = df["prompt_id"].nunique()

        return summary

    def print_summary(self):
        """Print formatted summary"""
        summary = self.get_summary()

        print("\n" + "=" * 60)
        print(f"📊 EVALUATION SUMMARY: {summary['experiment_name']}")
        print("=" * 60)
        print(f"Total Evaluations: {summary['total_evaluations']}")

        if "successful_calls" in summary:
            print(f"Successful: {summary['successful_calls']}")
            print(f"Failed: {summary['failed_calls']}")

        if "total_cost" in summary:
            print(f"\nTotal Cost: ${summary['total_cost']:.4f}")
            print(f"Avg Cost per Call: ${summary['avg_cost_per_call']:.4f}")

        if "avg_latency" in summary:
            print(f"\nAvg Latency: {summary['avg_latency']:.2f}s")
            print(f"Min/Max Latency: {summary['min_latency']:.2f}s / {summary['max_latency']:.2f}s")

        if "pass_rate" in summary:
            print(f"\nPass Rate: {summary['pass_rate']*100:.1f}%")
            print(f"Passed: {summary['passed']} / Failed: {summary['failed']}")

        if "models_tested" in summary:
            print(f"\nModels Tested: {summary['models_tested']}")
            if summary.get("best_model_by_pass_rate"):
                print(f"Best Model: {summary['best_model_by_pass_rate']}")

        if "prompts_tested" in summary:
            print(f"Prompts Tested: {summary['prompts_tested']}")

        print("=" * 60 + "\n")
