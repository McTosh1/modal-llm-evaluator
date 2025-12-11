"""
Example 1: Simple Prompt Comparison

Compare how different models respond to the same prompts.
"""

import modal
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app, evaluate_single

# Test prompts
prompts = {
    "direct": "What is 2+2?",
    "conversational": "Hey! Quick math question - what's 2+2?",
    "formal": "Please calculate the sum of 2 and 2.",
}

# Models to compare
models = [
    "claude-3-5-sonnet-20241022",
    "gpt-4o-mini",
    "gemini-2.0-flash-exp"
]

# Simple test case
test_case = {
    "id": "math_test",
    "expected_output": "4",
    "required_keywords": ["4"]
}

if __name__ == "__main__":
    print("🧪 Example 1: Simple Prompt Comparison\n")
    print("Testing 3 prompt styles across 3 models (9 evaluations total)\n")

    with app.run():
        results = []

        for prompt_id, prompt in prompts.items():
            print(f"\nPrompt '{prompt_id}': {prompt}")

            for model in models:
                result = evaluate_single.remote(
                    prompt=prompt,
                    model=model,
                    test_case=test_case,
                    prompt_id=prompt_id,
                    test_case_id="math_test"
                )

                print(f"  {model}: {result['output'][:50]}... (${result['cost']:.6f})")
                results.append(result)

        # Summary
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)

        total_cost = sum(r["cost"] for r in results)
        avg_latency = sum(r["latency"] for r in results) / len(results)

        print(f"Total Cost: ${total_cost:.4f}")
        print(f"Avg Latency: {avg_latency:.2f}s")
        print(f"Success Rate: {sum(1 for r in results if r['success'])}/{len(results)}")
