"""Examples of using the Ai-code-free-agent."""

from api import AICodeAgentAPI


def example_1_basic():
    """Basic usage with default configuration."""
    print("=== Example 1: Basic Usage ===\n")

    api = AICodeAgentAPI()

    prompt = "Write a Python function to reverse a list"
    response = api.ask(prompt)

    print(f"Prompt: {prompt}\n")
    print(f"Response:\n{response}\n")


def example_2_multiple_prompts():
    """Ask multiple questions with the same model."""
    print("=== Example 2: Multiple Prompts ===\n")

    api = AICodeAgentAPI()

    prompts = [
        "Explain what a closure is in Python",
        "How do decorators work?",
        "What are list comprehensions?",
    ]

    for prompt in prompts:
        print(f"Q: {prompt}")
        response = api.ask(prompt, temperature=0.3)
        print(f"A: {response}\n")


def example_3_custom_model():
    """Use a different model."""
    print("=== Example 3: Custom Model ===\n")

    api = AICodeAgentAPI()

    # List available models
    available = api.list_models()
    print(f"Available models: {available}\n")

    if available:
        model = available[0]
        prompt = "Write a unit test for a sorting function"
        response = api.ask(prompt, model=model, temperature=0.2)

        print(f"Using model: {model}")
        print(f"Prompt: {prompt}\n")
        print(f"Response:\n{response}\n")


def example_4_code_generation():
    """Generate code for specific tasks."""
    print("=== Example 4: Code Generation ===\n")

    api = AICodeAgentAPI()

    tasks = [
        "Create a simple REST API endpoint for user registration",
        "Write a decorator that logs function calls",
        "Implement a binary search algorithm",
    ]

    for task in tasks:
        print(f"Task: {task}")
        response = api.ask(task, temperature=0.2, max_tokens=512)
        print(f"Generated code:\n{response}\n")
        print("-" * 80 + "\n")


def example_5_conversation_context():
    """Maintain conversation context with system prompts."""
    print("=== Example 5: Code Review ===\n")

    api = AICodeAgentAPI()

    code_snippet = """
def calculate_factorial(n):
    result = 1
    for i in range(n):
        result *= i + 1
    return result
"""

    prompt = f"Review this code for bugs and improvements:\n\n{code_snippet}"
    response = api.ask(prompt, temperature=0.2)

    print(f"Code to review:\n{code_snippet}")
    print(f"\nReview:\n{response}\n")


if __name__ == "__main__":
    print("AI Code Agent - Usage Examples\n")
    print("=" * 80)

    try:
        example_1_basic()
        print("=" * 80)
        # Uncomment to run more examples:
        # example_2_multiple_prompts()
        # example_3_custom_model()
        # example_4_code_generation()
        # example_5_conversation_context()

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nFirst, download models with: python download_models.py --popular")
