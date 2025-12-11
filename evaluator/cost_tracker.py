"""
Cost tracking and budget management for LLM evaluations
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CostEntry:
    """Single cost entry"""
    timestamp: datetime
    model: str
    provider: str
    input_tokens: int
    output_tokens: int
    cost: float
    prompt_id: str
    test_case_id: str


class CostTracker:
    """Track costs across all evaluations"""

    def __init__(self, budget_limit: Optional[float] = None):
        self.budget_limit = budget_limit
        self.entries: List[CostEntry] = []
        self.total_cost = 0.0

    def add_entry(
        self,
        model: str,
        provider: str,
        input_tokens: int,
        output_tokens: int,
        cost: float,
        prompt_id: str,
        test_case_id: str
    ):
        """Add a cost entry"""
        entry = CostEntry(
            timestamp=datetime.now(),
            model=model,
            provider=provider,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            prompt_id=prompt_id,
            test_case_id=test_case_id
        )
        self.entries.append(entry)
        self.total_cost += cost

    def is_budget_exceeded(self) -> bool:
        """Check if budget limit is exceeded"""
        if self.budget_limit is None:
            return False
        return self.total_cost >= self.budget_limit

    def get_remaining_budget(self) -> Optional[float]:
        """Get remaining budget"""
        if self.budget_limit is None:
            return None
        return max(0, self.budget_limit - self.total_cost)

    def get_cost_breakdown(self) -> Dict[str, Dict[str, float]]:
        """Get cost breakdown by model and provider"""
        breakdown = {}

        for entry in self.entries:
            key = f"{entry.provider}/{entry.model}"
            if key not in breakdown:
                breakdown[key] = {
                    "total_cost": 0.0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "num_calls": 0
                }

            breakdown[key]["total_cost"] += entry.cost
            breakdown[key]["input_tokens"] += entry.input_tokens
            breakdown[key]["output_tokens"] += entry.output_tokens
            breakdown[key]["num_calls"] += 1

        return breakdown

    def get_summary(self) -> Dict[str, any]:
        """Get cost summary"""
        return {
            "total_cost": self.total_cost,
            "budget_limit": self.budget_limit,
            "remaining_budget": self.get_remaining_budget(),
            "total_evaluations": len(self.entries),
            "breakdown": self.get_cost_breakdown()
        }

    def print_summary(self):
        """Print formatted cost summary"""
        summary = self.get_summary()

        print("\n" + "=" * 60)
        print("💰 COST SUMMARY")
        print("=" * 60)
        print(f"Total Cost: ${summary['total_cost']:.4f}")

        if summary['budget_limit']:
            print(f"Budget Limit: ${summary['budget_limit']:.2f}")
            print(f"Remaining: ${summary['remaining_budget']:.2f}")

        print(f"Total Evaluations: {summary['total_evaluations']}")
        print("\nBreakdown by Model:")
        print("-" * 60)

        for model, stats in summary['breakdown'].items():
            print(f"\n{model}:")
            print(f"  Cost: ${stats['total_cost']:.4f}")
            print(f"  Calls: {stats['num_calls']}")
            print(f"  Input Tokens: {stats['input_tokens']:,}")
            print(f"  Output Tokens: {stats['output_tokens']:,}")

        print("=" * 60 + "\n")
