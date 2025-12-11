# Contributing to Modal LLM Evaluator

First off, thank you for considering contributing to Modal LLM Evaluator! It's people like you that make this tool better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Community](#community)

---

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to hello@gtmvp.com.

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Found a bug? Help us fix it!

**Before submitting a bug report:**
- Check the [existing issues](https://github.com/GTMVP/modal-llm-evaluator/issues) to see if it's already reported
- Try the latest version to see if the bug still exists
- Collect information about the bug (error messages, steps to reproduce, environment)

**How to submit a good bug report:**
1. Use the bug report template
2. Provide a clear, descriptive title
3. Include steps to reproduce the behavior
4. Describe what you expected to happen
5. Include screenshots if applicable
6. Note your environment (OS, Python version, Modal version)
7. Include relevant logs or error messages

### 💡 Suggesting Enhancements

Have an idea to make this better? We'd love to hear it!

**Before submitting an enhancement:**
- Check if it's already been suggested in [issues](https://github.com/GTMVP/modal-llm-evaluator/issues)
- Consider if it fits the project scope
- Think about how it benefits the broader community

**How to submit a good enhancement:**
1. Use the feature request template
2. Provide a clear, descriptive title
3. Explain the problem this enhancement solves
4. Describe your proposed solution
5. List any alternatives you've considered
6. Include mockups or examples if applicable

### 📖 Improving Documentation

Documentation improvements are always welcome!
- Fix typos or clarify confusing sections
- Add examples or use cases
- Improve installation instructions
- Translate documentation

### 🔧 Contributing Code

Ready to contribute code? Awesome!

**Good first issues:**
- Look for issues labeled `good first issue` or `help wanted`
- These are great for getting familiar with the codebase

**Areas we need help:**
- Additional LLM provider integrations (Cohere, Together AI, etc.)
- New evaluation metrics
- Performance optimizations
- Test coverage improvements
- UI/UX enhancements
- Documentation

---

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Modal account ([sign up free](https://modal.com))
- Git
- At least one LLM API key (Anthropic, OpenAI, or Google)

### Setup Steps

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/GTMVP/modal-llm-evaluator.git
   cd modal-llm-evaluator
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set up Modal**
   ```bash
   python -m modal setup
   ```

5. **Configure API keys**
   ```bash
   # Create Modal secrets for your API keys
   python -m modal secret create anthropic-key ANTHROPIC_API_KEY=sk-ant-...
   python -m modal secret create openai-key OPENAI_API_KEY=sk-...
   python -m modal secret create google-api-key GOOGLE_API_KEY=...
   ```

6. **Create a development branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=evaluator

# Run specific test file
pytest tests/test_providers.py

# Run Streamlit UI locally
streamlit run streamlit_app/app.py
```

### Project Structure

```
modal-llm-evaluator/
├── evaluator/              # Core evaluation engine
│   ├── providers.py        # LLM provider implementations
│   ├── metrics.py          # Evaluation metrics
│   ├── cost_tracker.py     # Cost calculation
│   └── email_notify.py     # Email notifications
├── streamlit_app/          # Web UI
│   ├── app.py             # Main Streamlit app
│   └── pages/             # UI pages
├── tests/                  # Test suite
├── examples/               # Example configurations
├── docs/                   # Additional documentation
└── main.py                # Modal entry point
```

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Imports**: Use absolute imports, grouped by standard library, third-party, local
- **Docstrings**: Use Google-style docstrings
- **Type hints**: Use type hints for all function signatures

**Example:**

```python
from typing import List, Dict, Optional
import anthropic


def evaluate_prompt(
    prompt: str,
    model: str,
    test_cases: List[Dict],
    max_tokens: int = 1024
) -> Dict:
    """Evaluate a prompt against multiple test cases.

    Args:
        prompt: The prompt template to evaluate
        model: Model identifier (e.g., 'claude-3-5-sonnet-20241022')
        test_cases: List of test case dictionaries
        max_tokens: Maximum tokens in response

    Returns:
        Dictionary containing evaluation results with metrics and costs

    Raises:
        ValueError: If prompt is empty or model is not supported
    """
    # Implementation here
    pass
```

### Code Quality Tools

We use these tools to maintain code quality:

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8

# Type checking
mypy evaluator/

# Security check
bandit -r evaluator/
```

All pull requests must pass these checks.

### Testing Requirements

- All new features must include tests
- Bug fixes should include a test that would have caught the bug
- Aim for >80% code coverage
- Tests should be fast and reliable

**Test structure:**

```python
import pytest
from evaluator.providers import AnthropicProvider


class TestAnthropicProvider:
    """Test suite for Anthropic provider."""

    def test_generate_basic(self):
        """Test basic text generation."""
        provider = AnthropicProvider(model="claude-3-5-sonnet-20241022")
        result = provider.generate("Say hello")
        assert "output" in result
        assert len(result["output"]) > 0

    def test_cost_calculation(self):
        """Test cost calculation accuracy."""
        provider = AnthropicProvider(model="claude-3-5-sonnet-20241022")
        cost = provider.calculate_cost(input_tokens=1000, output_tokens=500)
        expected = (1000 * 3.00 / 1_000_000) + (500 * 15.00 / 1_000_000)
        assert abs(cost - expected) < 0.0001
```

---

## Pull Request Process

### Before Submitting

1. **Update your fork**
   ```bash
   git remote add upstream https://github.com/GTMVP/modal-llm-evaluator.git
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all checks**
   ```bash
   black .
   isort .
   flake8
   pytest
   ```

3. **Update documentation**
   - Add docstrings to new functions
   - Update README if adding features
   - Add examples if relevant

4. **Test thoroughly**
   - Test your changes locally
   - Test in Modal environment
   - Test the Streamlit UI if applicable

### Submitting the PR

1. **Push your changes**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to GitHub and create a pull request
   - Use the PR template
   - Link any related issues

3. **PR Checklist**
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Comments added for complex code
   - [ ] Documentation updated
   - [ ] Tests added/updated
   - [ ] All tests pass
   - [ ] No merge conflicts

### PR Review Process

1. **Automated checks** run (tests, linting, coverage)
2. **Maintainer review** (usually within 48 hours)
3. **Address feedback** if changes are requested
4. **Approval** from at least one maintainer
5. **Merge** by maintainer

### After Your PR is Merged

1. **Delete your branch**
   ```bash
   git branch -d feature/your-feature-name
   git push origin --delete feature/your-feature-name
   ```

2. **Update your fork**
   ```bash
   git checkout main
   git pull upstream main
   ```

3. **Celebrate!** You've contributed to open source!

---

## Commit Message Guidelines

Write clear, meaningful commit messages:

**Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**

```
feat: Add Cohere LLM provider support

- Implement CoherePr provider class
- Add pricing information
- Include tests for Cohere integration
- Update documentation

Closes #123
```

```
fix: Resolve cost calculation error for GPT-4o mini

The pricing was using the wrong tier. Updated to use
correct input/output token pricing from OpenAI docs.

Fixes #456
```

---

## Community

### Getting Help

- **Documentation**: Check [docs/](docs/) first
- **Issues**: Search [existing issues](https://github.com/GTMVP/modal-llm-evaluator/issues)
- **Discussions**: Use [GitHub Discussions](https://github.com/GTMVP/modal-llm-evaluator/discussions)
- **Email**: hello@gtmvp.com

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community discussion
- **Pull Requests**: Code contributions

### Recognition

Contributors are recognized in:
- README.md Contributors section
- Release notes for significant contributions
- Annual contributor spotlight

---

## Development Tips

### Working with Modal

```python
# Test Modal functions locally
@app.function()
def my_function():
    return "Hello"

# Run locally without deploying
if __name__ == "__main__":
    with app.run():
        result = my_function.remote()
        print(result)
```

### Debugging Streamlit

```python
# Add debug info
import streamlit as st
st.write("Debug:", st.session_state)

# Run with debugging
streamlit run streamlit_app/app.py --logger.level=debug
```

### Testing Email Integration

```python
# Use test SMTP server
# Set up a test account at https://ethereal.email for testing
```

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

Don't hesitate to ask! We're here to help:
- Open a [Discussion](https://github.com/GTMVP/modal-llm-evaluator/discussions)
- Email us at hello@gtmvp.com
- Tag @GTMVP in issues

**Thank you for contributing to Modal LLM Evaluator!**

Together, we're making LLM evaluation better for everyone.
