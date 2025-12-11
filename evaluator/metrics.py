"""
Evaluation metrics for LLM outputs
"""

import re
from typing import Dict, Any, List, Optional, Callable
from difflib import SequenceMatcher


class EvaluationMetrics:
    """Calculate various evaluation metrics for LLM outputs"""

    @staticmethod
    def exact_match(output: str, expected: str) -> bool:
        """Check if output exactly matches expected"""
        return output.strip() == expected.strip()

    @staticmethod
    def contains_keyword(output: str, keyword: str, case_sensitive: bool = False) -> bool:
        """Check if output contains a specific keyword"""
        if not case_sensitive:
            output = output.lower()
            keyword = keyword.lower()
        return keyword in output

    @staticmethod
    def contains_all_keywords(output: str, keywords: List[str], case_sensitive: bool = False) -> bool:
        """Check if output contains all keywords"""
        return all(
            EvaluationMetrics.contains_keyword(output, kw, case_sensitive)
            for kw in keywords
        )

    @staticmethod
    def similarity_score(output: str, expected: str) -> float:
        """Calculate similarity score between 0 and 1"""
        return SequenceMatcher(None, output.strip(), expected.strip()).ratio()

    @staticmethod
    def word_count(output: str) -> int:
        """Count words in output"""
        return len(output.split())

    @staticmethod
    def char_count(output: str) -> int:
        """Count characters in output"""
        return len(output)

    @staticmethod
    def has_valid_json(output: str) -> bool:
        """Check if output contains valid JSON"""
        import json
        try:
            json.loads(output)
            return True
        except:
            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```json\n(.*?)\n```', output, re.DOTALL)
            if json_match:
                try:
                    json.loads(json_match.group(1))
                    return True
                except:
                    pass
            return False

    @staticmethod
    def has_valid_code(output: str, language: Optional[str] = None) -> bool:
        """Check if output contains code"""
        if language:
            pattern = f'```{language}.*?```'
        else:
            pattern = r'```.*?```'
        return bool(re.search(pattern, output, re.DOTALL))

    @staticmethod
    def sentiment_score(output: str) -> str:
        """Simple sentiment analysis (positive/negative/neutral)"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'poor', 'disappointing']

        output_lower = output.lower()
        positive_count = sum(1 for word in positive_words if word in output_lower)
        negative_count = sum(1 for word in negative_words if word in output_lower)

        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

    @staticmethod
    def evaluate(
        output: str,
        test_case: Dict[str, Any],
        custom_metrics: Optional[Dict[str, Callable]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate output against test case

        Args:
            output: LLM output to evaluate
            test_case: Test case containing expected values and evaluation criteria
            custom_metrics: Optional custom evaluation functions

        Returns:
            Dictionary of metric results
        """
        results = {}

        # Standard metrics
        if "expected_output" in test_case:
            results["exact_match"] = EvaluationMetrics.exact_match(
                output, test_case["expected_output"]
            )
            results["similarity"] = EvaluationMetrics.similarity_score(
                output, test_case["expected_output"]
            )

        if "required_keywords" in test_case:
            results["has_required_keywords"] = EvaluationMetrics.contains_all_keywords(
                output, test_case["required_keywords"]
            )

        if "min_words" in test_case:
            word_count = EvaluationMetrics.word_count(output)
            results["word_count"] = word_count
            results["meets_min_words"] = word_count >= test_case["min_words"]

        if "max_words" in test_case:
            word_count = results.get("word_count", EvaluationMetrics.word_count(output))
            results["word_count"] = word_count
            results["meets_max_words"] = word_count <= test_case["max_words"]

        if "expect_json" in test_case and test_case["expect_json"]:
            results["valid_json"] = EvaluationMetrics.has_valid_json(output)

        if "expect_code" in test_case:
            language = test_case.get("code_language")
            results["has_code"] = EvaluationMetrics.has_valid_code(output, language)

        if "check_sentiment" in test_case and test_case["check_sentiment"]:
            results["sentiment"] = EvaluationMetrics.sentiment_score(output)

        # Custom metrics
        if custom_metrics:
            for metric_name, metric_func in custom_metrics.items():
                try:
                    results[f"custom_{metric_name}"] = metric_func(output, test_case)
                except Exception as e:
                    results[f"custom_{metric_name}"] = f"Error: {str(e)}"

        # Overall pass/fail
        # Consider it a pass if exact match OR similarity > 0.8 OR has required keywords
        if "exact_match" in results:
            results["pass"] = results["exact_match"]
        elif "similarity" in results:
            results["pass"] = results["similarity"] > 0.8
        elif "has_required_keywords" in results:
            results["pass"] = results["has_required_keywords"]
        else:
            results["pass"] = True  # Default to pass if no specific criteria

        return results
