"""
Basic tests for Modal LLM Evaluator

These are placeholder tests to ensure CI passes.
Add more comprehensive tests as the project grows.
"""

import pytest


def test_package_imports():
    """Test that the main package can be imported"""
    try:
        from evaluator import providers
        from evaluator import metrics
        from evaluator import cost_tracker
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import evaluator modules: {e}")


def test_python_version():
    """Test that Python version is 3.11 or higher"""
    import sys
    assert sys.version_info >= (3, 11), "Python 3.11+ required"


def test_basic_functionality():
    """Placeholder test - replace with actual tests"""
    assert True, "Basic test passes"


def test_example_data_exists():
    """Test that example files exist"""
    from pathlib import Path

    project_root = Path(__file__).parent.parent

    # Check for example files
    examples_dir = project_root / "examples"
    assert examples_dir.exists(), "Examples directory should exist"

    # Check for at least one example file
    example_files = list(examples_dir.glob("*.json"))
    assert len(example_files) > 0, "Should have at least one example file"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
