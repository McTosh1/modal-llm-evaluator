"""
Screenshot automation helper for Modal LLM Evaluator

This script helps automate taking screenshots of the Streamlit UI.
Requires: playwright, pillow

Install: pip install playwright pillow
Setup: playwright install chromium
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

# Screenshot configuration
SCREENSHOTS = [
    {
        "name": "screenshot-home.png",
        "url": "http://localhost:8501",
        "viewport": {"width": 1920, "height": 1080},
        "wait_for": 3000,  # Wait 3 seconds for page to load
        "description": "Home page"
    },
    {
        "name": "screenshot-results.png",
        "url": "http://localhost:8501",
        "click_sidebar": "Results",
        "viewport": {"width": 1920, "height": 1080},
        "wait_for": 3000,
        "description": "Results dashboard"
    },
    {
        "name": "screenshot-comparison.png",
        "url": "http://localhost:8501",
        "click_sidebar": "Model Comparison",
        "viewport": {"width": 1920, "height": 1080},
        "wait_for": 3000,
        "description": "Model comparison view"
    },
    {
        "name": "screenshot-cost.png",
        "url": "http://localhost:8501",
        "click_sidebar": "Cost Tracker",
        "viewport": {"width": 1920, "height": 1080},
        "wait_for": 3000,
        "description": "Cost tracking page"
    }
]

async def take_screenshots():
    """Take all configured screenshots"""

    # Output directory
    output_dir = Path(__file__).parent
    output_dir.mkdir(exist_ok=True)

    print("🎬 Starting screenshot automation...")
    print(f"📁 Saving to: {output_dir}")
    print()

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)  # headless=False to see what's happening
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        for i, config in enumerate(SCREENSHOTS, 1):
            try:
                print(f"📸 [{i}/{len(SCREENSHOTS)}] Taking screenshot: {config['description']}")

                # Navigate to URL
                await page.goto(config["url"])
                await page.wait_for_timeout(config["wait_for"])

                # Click sidebar item if specified
                if "click_sidebar" in config:
                    print(f"   Clicking: {config['click_sidebar']}")
                    # Try to find and click the sidebar item
                    try:
                        await page.click(f"text={config['click_sidebar']}")
                        await page.wait_for_timeout(2000)  # Wait for page to load
                    except Exception as e:
                        print(f"   ⚠️  Could not click {config['click_sidebar']}: {e}")

                # Take screenshot
                screenshot_path = output_dir / config["name"]
                await page.screenshot(path=str(screenshot_path), full_page=False)

                print(f"   ✅ Saved: {config['name']}")
                print()

            except Exception as e:
                print(f"   ❌ Error: {e}")
                print()

        await browser.close()

    print("🎉 Screenshot automation complete!")
    print()
    print("Next steps:")
    print("1. Review screenshots in docs/images/")
    print("2. Optimize images (compress to <500KB each)")
    print("3. Update README.md to use local images instead of placeholders")
    print("4. Commit and push to GitHub")


def main():
    """Main entry point"""
    print("=" * 70)
    print("  Modal LLM Evaluator - Screenshot Automation")
    print("=" * 70)
    print()

    # Check if Streamlit is running
    print("⚠️  IMPORTANT: Make sure Streamlit is running!")
    print("   Run this in another terminal:")
    print("   streamlit run streamlit_app/app.py")
    print()

    input("Press Enter when Streamlit is ready...")
    print()

    # Run async screenshot function
    asyncio.run(take_screenshots())


if __name__ == "__main__":
    main()
