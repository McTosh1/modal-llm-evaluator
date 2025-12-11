"""
Modal LLM Evaluator - Main orchestration engine

This is the core Modal app that runs evaluations in parallel across multiple models and prompts.
"""

import modal
import os
from typing import List, Dict, Any, Optional
from evaluator.providers import get_provider
from evaluator.metrics import EvaluationMetrics
from evaluator.cost_tracker import CostTracker
from evaluator.storage import ResultsStorage

# Create Modal app
app = modal.App("llm-evaluator")

# Create Modal image with all dependencies
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "anthropic>=0.39.0",
    "openai>=1.54.0",
    "google-generativeai>=0.8.0",
    "pandas>=2.0.0",
    "sqlalchemy>=2.0.0",
    "openpyxl>=3.1.0"
)


@app.function(
    image=image,
    secrets=[
        modal.Secret.from_name("anthropic-key"),
        modal.Secret.from_name("openai-key"),
        modal.Secret.from_name("google-api-key"),
    ],
    retries=2,
    timeout=300  # 5 minutes per evaluation
)
def evaluate_single(
    prompt: str,
    model: str,
    test_case: Dict[str, Any],
    prompt_id: str,
    test_case_id: str,
    max_tokens: int = 1024
) -> Dict[str, Any]:
    """
    Evaluate a single prompt + model + test case combination

    This function runs in parallel on Modal's infrastructure.
    """
    # Get the appropriate provider
    provider = get_provider(model)

    # Generate response
    response = provider.generate(prompt, max_tokens=max_tokens)

    # Calculate cost
    cost = provider.calculate_cost(response)

    # Evaluate the output
    metrics = {}
    if response["success"] and response["output"]:
        metrics = EvaluationMetrics.evaluate(response["output"], test_case)

    # Combine all results
    result = {
        "prompt_id": prompt_id,
        "test_case_id": test_case_id,
        "model": model,
        "provider": response["provider"],
        "input": prompt,
        "output": response["output"],
        "success": response["success"],
        "error": response["error"],
        "input_tokens": response["input_tokens"],
        "output_tokens": response["output_tokens"],
        "latency": response["latency"],
        "cost": cost,
        **metrics  # Add all evaluation metrics
    }

    return result


@app.local_entrypoint()
def main(
    experiment_name: str = "test_experiment",
    prompts_file: Optional[str] = None,
    test_cases_file: Optional[str] = None,
    models: Optional[List[str]] = None,
    budget_limit: Optional[float] = None,
    export_format: str = "excel",  # json, csv, excel, or database
    database_url: Optional[str] = None
):
    """
    Main entry point for LLM evaluation experiments

    Args:
        experiment_name: Name for this experiment
        prompts_file: Path to file containing prompts (one per line or JSON)
        test_cases_file: Path to JSON file containing test cases
        models: List of model names to test
        budget_limit: Maximum spend limit in dollars
        export_format: Output format (json, csv, excel, database)
        database_url: Database connection string for Power BI export
    """
    import json

    # Default test data if not provided
    if prompts_file is None:
        prompts = {
            "prompt1": "You are a helpful assistant. {question}",
            "prompt2": "You are an expert in the field. Answer this question: {question}",
        }
    else:
        with open(prompts_file) as f:
            prompts = json.load(f)

    if test_cases_file is None:
        test_cases = [
            {
                "id": "test1",
                "question": "What is the capital of France?",
                "expected_output": "Paris",
                "required_keywords": ["Paris"]
            },
            {
                "id": "test2",
                "question": "Explain quantum computing in simple terms.",
                "min_words": 50,
                "required_keywords": ["quantum", "computing"]
            }
        ]
    else:
        with open(test_cases_file) as f:
            test_cases = json.load(f)

    if models is None:
        models = [
            "claude-3-5-sonnet-20241022",
            "gpt-4o-mini",
            "gemini-2.0-flash-exp"
        ]

    # Initialize trackers
    cost_tracker = CostTracker(budget_limit=budget_limit)
    storage = ResultsStorage(experiment_name)

    print(f"\n🚀 Starting LLM Evaluation: {experiment_name}")
    print(f"📝 Prompts: {len(prompts)}")
    print(f"🧪 Test Cases: {len(test_cases)}")
    print(f"🤖 Models: {len(models)}")
    print(f"📊 Total Evaluations: {len(prompts) * len(test_cases) * len(models)}")
    if budget_limit:
        print(f"💰 Budget Limit: ${budget_limit:.2f}")
    print("\n" + "=" * 60)

    # Generate all evaluation tasks
    tasks = []
    for prompt_id, prompt_template in prompts.items():
        for test_case in test_cases:
            # Format prompt with test case data
            formatted_prompt = prompt_template.format(**test_case)

            for model in models:
                tasks.append({
                    "prompt": formatted_prompt,
                    "model": model,
                    "test_case": test_case,
                    "prompt_id": prompt_id,
                    "test_case_id": test_case["id"]
                })

    print(f"⚡ Running {len(tasks)} evaluations in parallel on Modal...\n")

    # Run evaluations in parallel using Modal
    results = list(evaluate_single.starmap([
        (
            task["prompt"],
            task["model"],
            task["test_case"],
            task["prompt_id"],
            task["test_case_id"]
        )
        for task in tasks
    ]))

    print(f"✅ Completed {len(results)} evaluations\n")

    # Process results
    for result in results:
        # Track costs
        if result["success"]:
            cost_tracker.add_entry(
                model=result["model"],
                provider=result["provider"],
                input_tokens=result["input_tokens"],
                output_tokens=result["output_tokens"],
                cost=result["cost"],
                prompt_id=result["prompt_id"],
                test_case_id=result["test_case_id"]
            )

        # Store result
        storage.add_result(result)

        # Check budget
        if cost_tracker.is_budget_exceeded():
            print(f"⚠️  Budget limit exceeded! Stopping evaluation.")
            break

    # Print summaries
    storage.print_summary()
    cost_tracker.print_summary()

    # Export results
    print("💾 Exporting results...")

    if export_format == "json":
        output_file = storage.save_json()
        print(f"✅ Saved to {output_file}")

    elif export_format == "csv":
        output_file = storage.save_csv()
        print(f"✅ Saved to {output_file}")

    elif export_format == "excel":
        output_file = storage.save_excel()
        print(f"✅ Saved to {output_file}")

    elif export_format == "database" and database_url:
        storage.export_to_powerbi_database(database_url)
        print("✅ Exported to Power BI database")

    # Also save as Excel for local viewing
    if export_format != "excel":
        excel_file = storage.save_excel()
        print(f"📊 Also saved Excel summary: {excel_file}")

    print("\n✨ Evaluation complete!")

    return storage.get_summary()


# Example: Run a quick test
@app.function(image=image)
def quick_test():
    """Quick test to verify everything works"""
    from evaluator.providers import AnthropicProvider

    print("Testing Anthropic provider...")
    provider = AnthropicProvider("claude-3-5-sonnet-20241022")
    result = provider.generate("Say 'Hello, Modal!' in a creative way.")

    print(f"\n✅ Test successful!")
    print(f"Output: {result['output']}")
    print(f"Cost: ${provider.calculate_cost(result):.6f}")
    print(f"Latency: {result['latency']:.2f}s")

    return result
