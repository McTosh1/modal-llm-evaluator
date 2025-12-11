"""
Example 2: Prompt Optimization for Product Descriptions

Test different prompt templates to find the best one for generating product descriptions.
This is highly relevant for your SynapMarketing business!
"""

import modal
import json

# Prompt templates to test
PROMPT_TEMPLATES = {
    "basic": """Generate a product description for: {product_name}

Product details:
- Category: {category}
- Features: {features}
- Price: {price}""",

    "marketing": """You are an expert copywriter. Create a compelling product description that will drive sales.

Product: {product_name}
Category: {category}
Key Features: {features}
Price Point: {price}

Write a description that highlights benefits and creates desire.""",

    "seo_optimized": """Create an SEO-optimized product description for e-commerce.

Product Name: {product_name}
Category: {category}
Features: {features}
Price: {price}

Include relevant keywords naturally while making it compelling for customers.""",

    "storytelling": """Use storytelling to make this product irresistible to customers.

Product: {product_name}
Category: {category}
What it does: {features}
Price: {price}

Tell a story about how this product solves a problem or improves someone's life.""",

    "bullet_points": """Create a structured product description with clear bullet points.

{product_name}
Category: {category}

Key Features:
{features}

Price: {price}

Format: Short intro paragraph + 5 benefit-focused bullet points + call to action."""
}

# Test products
TEST_PRODUCTS = [
    {
        "id": "prod1",
        "product_name": "Wireless Noise-Cancelling Headphones",
        "category": "Electronics",
        "features": "40-hour battery, active noise cancellation, comfortable over-ear design, premium sound quality",
        "price": "$199",
        "min_words": 100,
        "required_keywords": ["headphones", "noise", "battery"]
    },
    {
        "id": "prod2",
        "product_name": "Organic Green Tea Set",
        "category": "Food & Beverage",
        "features": "100% organic, antioxidant-rich, 20 premium tea bags, sourced from Japan",
        "price": "$24.99",
        "min_words": 80,
        "required_keywords": ["organic", "tea", "antioxidant"]
    }
]

# Models to test
MODELS = [
    "claude-3-5-haiku-20241022",  # Fast and cheap
    "claude-3-5-sonnet-20241022",  # Balanced
    "gpt-4o-mini"  # OpenAI comparison
]

if __name__ == "__main__":
    print("🎯 Example 2: Prompt Optimization for Product Descriptions\n")
    print(f"Testing {len(PROMPT_TEMPLATES)} prompt templates")
    print(f"Across {len(TEST_PRODUCTS)} products")
    print(f"Using {len(MODELS)} models")
    print(f"Total evaluations: {len(PROMPT_TEMPLATES) * len(TEST_PRODUCTS) * len(MODELS)}\n")

    # Save test config
    with open("examples/prompt_optimization_config.json", "w") as f:
        json.dump({
            "prompts": PROMPT_TEMPLATES,
            "test_cases": TEST_PRODUCTS,
            "models": MODELS
        }, f, indent=2)

    print("✅ Test configuration saved to: examples/prompt_optimization_config.json")
    print("\nTo run this evaluation:")
    print("python -m modal run main.py \\")
    print("  --experiment-name='product-description-optimization' \\")
    print("  --prompts-file='examples/prompt_optimization_config.json' \\")
    print("  --budget-limit=5.00")
