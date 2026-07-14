"""Local AI agent using GGUF models."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

from models import ModelManager


class LocalAIAgent:
    """Run inference using local GGUF models with llama-cpp-python."""

    def __init__(
        self,
        model_path: str | Path,
        n_ctx: int = 2048,
        n_threads: int = 4,
        n_gpu_layers: int = 0,
    ):
        """Initialize agent with a GGUF model.
        
        Args:
            model_path: Path to GGUF model file.
            n_ctx: Context window size.
            n_threads: Number of threads for CPU inference.
            n_gpu_layers: Number of layers to offload to GPU (0 = CPU only).
        """
        try:
            from llama_cpp import Llama
        except ImportError:
            raise ImportError(
                "llama-cpp-python is required. Install with: pip install llama-cpp-python"
            )

        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        print(f"Loading model: {model_path}")
        self.llm = Llama(
            model_path=str(model_path),
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_gpu_layers=n_gpu_layers,
            verbose=False,
        )

    def ask(self, prompt: str, temperature: float = 0.2, max_tokens: int = 512) -> str:
        """Get response from model.
        
        Args:
            prompt: User prompt.
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative).
            max_tokens: Maximum response length.
        
        Returns:
            Model response.
        """
        system_prompt = (
            "You are a helpful AI code assistant. "
            "Provide clear, concise answers focused on code and programming."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        response = self.llm.create_chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response["choices"][0]["message"]["content"].strip()


def load_project_config(config_path: str = "agent.config.json") -> dict:
    """Load project configuration.
    
    Args:
        config_path: Path to agent.config.json
    
    Returns:
        Configuration dictionary.
    """
    default_config = {
        "model": "model.gguf",
        "models_dir": "./models",
        "n_ctx": 2048,
        "n_threads": 4,
        "n_gpu_layers": 0,
    }

    config_path = Path(config_path)
    if config_path.exists():
        with open(config_path) as f:
            loaded = json.load(f)
            default_config.update(loaded)

    return default_config


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the Ai-code-free-agent with local GGUF models."
    )
    parser.add_argument("prompt", nargs="+", help="Prompt text to send to the agent.")
    parser.add_argument(
        "--model", help="Model filename or name (searches in models_dir)."
    )
    parser.add_argument(
        "--models-dir",
        default="./models",
        help="Directory containing GGUF models (default: ./models)",
    )
    parser.add_argument(
        "--config",
        default="agent.config.json",
        help="Project configuration file (default: agent.config.json)",
    )
    parser.add_argument(
        "--threads",
        type=int,
        help="Number of threads for inference (default: 4)",
    )
    parser.add_argument(
        "--gpu-layers",
        type=int,
        default=0,
        help="Number of layers to offload to GPU (default: 0 = CPU only)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature (default: 0.2)",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models in models_dir",
    )

    args = parser.parse_args()

    # Load project config
    config = load_project_config(args.config)

    # Override with command-line arguments
    if args.model:
        config["model"] = args.model
    if args.models_dir:
        config["models_dir"] = args.models_dir
    if args.threads:
        config["n_threads"] = args.threads

    models_mgr = ModelManager(config["models_dir"])

    # List models if requested
    if args.list_models:
        available_models = models_mgr.list_models()
        if available_models:
            print("Available GGUF models:")
            for model in available_models:
                print(f"  - {model}")
        else:
            print(f"No GGUF models found in {config['models_dir']}")
        return

    # Find model
    model_path = models_mgr.get_model_path(config["model"])
    if not model_path:
        print(f"Error: Model '{config['model']}' not found in {config['models_dir']}")
        print("Available models:")
        for model in models_mgr.list_models():
            print(f"  - {model}")
        print("\nDownload models with: python download_models.py")
        return

    # Run agent
    try:
        agent = LocalAIAgent(
            model_path=model_path,
            n_ctx=config.get("n_ctx", 2048),
            n_threads=config.get("n_threads", 4),
            n_gpu_layers=args.gpu_layers,
        )

        prompt_text = " ".join(args.prompt)
        answer = agent.ask(prompt_text, temperature=args.temperature)

        print("\n--- Agent response ---\n")
        print(answer)

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
