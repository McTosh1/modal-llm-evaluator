"""
Setup verification script

Run this to check if your Modal LLM Evaluator is configured correctly.
"""

import sys

def check_modal():
    """Check if Modal is installed and configured"""
    print("[*] Checking Modal installation...")
    try:
        import modal
        print(f"  [OK] Modal version: {modal.__version__}")
        return True
    except ImportError:
        print("  [FAIL] Modal not installed")
        print("     Fix: pip install modal")
        return False


def check_dependencies():
    """Check if all dependencies are installed"""
    print("\n[*] Checking dependencies...")
    required = {
        "anthropic": "Anthropic API client",
        "openai": "OpenAI API client",
        "google.generativeai": "Google Gemini client",
        "pandas": "Data processing",
        "sqlalchemy": "Database export"
    }

    all_installed = True
    for package, description in required.items():
        try:
            __import__(package)
            print(f"  [OK] {description}")
        except ImportError:
            print(f"  [FAIL] {description} ({package})")
            all_installed = False

    if not all_installed:
        print("\n     Fix: pip install -r requirements.txt")

    return all_installed


def check_modal_auth():
    """Check if Modal is authenticated"""
    print("\n[*] Checking Modal authentication...")
    try:
        import subprocess
        result = subprocess.run(
            ["python", "-m", "modal", "token", "current"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("  [OK] Modal is authenticated")
            return True
        else:
            print("  [FAIL] Modal not authenticated")
            print("     Fix: python -m modal setup")
            return False
    except Exception as e:
        print(f"  [WARN] Could not verify: {e}")
        return False


def check_api_keys():
    """Check if API keys are configured"""
    print("\n[*] Checking API keys (Modal secrets)...")
    print("  [INFO] To check secrets, run: python -m modal secret list")
    print("\n  Required secrets:")
    print("    - anthropic-key (for Claude)")
    print("    - openai-key (for GPT)")
    print("    - google-api-key (for Gemini)")
    print("\n  Create with:")
    print("    python -m modal secret create anthropic-key ANTHROPIC_API_KEY=sk-ant-...")
    return True


def main():
    print("=" * 60)
    print("  Modal LLM Evaluator - Setup Verification")
    print("=" * 60)

    checks = [
        check_modal(),
        check_dependencies(),
        check_modal_auth(),
        check_api_keys()
    ]

    print("\n" + "=" * 60)
    if all(checks[:-1]):  # Exclude API keys check from all()
        print("[SUCCESS] All checks passed! You're ready to run evaluations.")
        print("\nNext steps:")
        print("  1. Make sure you've created Modal secrets for API keys")
        print("  2. Run: python -m modal run main.py")
        print("  3. Check out QUICKSTART.md for examples")
    else:
        print("[WARNING] Some checks failed. Please fix the issues above.")
    print("=" * 60)


if __name__ == "__main__":
    main()
