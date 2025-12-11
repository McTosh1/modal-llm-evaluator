"""
Basic tests for Modal LLM Evaluator

These are simple tests to ensure CI passes.
Add more comprehensive tests as the project grows.
"""

import sys
from pathlib import Path


def test_python_version():
    """Test that Python version is 3.11 or higher"""
    assert sys.version_info >= (3, 11), "Python 3.11+ required"


def test_basic_math():
    """Basic sanity check test"""
    assert 1 + 1 == 2, "Basic arithmetic works"
    assert True is True, "Boolean logic works"


def test_project_structure():
    """Test that project structure exists"""
    project_root = Path(__file__).parent.parent

    # Check for main directories
    assert project_root.exists(), "Project root should exist"
    assert (project_root / "evaluator").exists(), "Evaluator package should exist"
    assert (project_root / "streamlit_app").exists(), "Streamlit app should exist"
    assert (project_root / "examples").exists(), "Examples directory should exist"


def test_example_files_exist():
    """Test that example files exist"""
    project_root = Path(__file__).parent.parent
    examples_dir = project_root / "examples"

    # Check for specific example files
    assert (examples_dir / "prompts_simple.json").exists(), "Simple prompts example should exist"
    assert (examples_dir / "test_cases_simple.json").exists(), "Simple test cases should exist"
    assert (examples_dir / "README.md").exists(), "Examples README should exist"


def test_documentation_exists():
    """Test that key documentation files exist"""
    project_root = Path(__file__).parent.parent

    # Check for documentation
    assert (project_root / "README.md").exists(), "README should exist"
    assert (project_root / "LICENSE").exists(), "LICENSE should exist"
    assert (project_root / "CONTRIBUTING.md").exists(), "CONTRIBUTING guide should exist"
    assert (project_root / "CODE_OF_CONDUCT.md").exists(), "Code of Conduct should exist"


def test_requirements_file():
    """Test that requirements.txt exists and is readable"""
    project_root = Path(__file__).parent.parent
    req_file = project_root / "requirements.txt"

    assert req_file.exists(), "requirements.txt should exist"

    # Check that it's not empty
    content = req_file.read_text()
    assert len(content) > 0, "requirements.txt should not be empty"
    assert "modal" in content.lower(), "requirements should include modal"
