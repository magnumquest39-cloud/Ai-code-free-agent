"""API interface for using the agent as a library."""

from __future__ import annotations

from agent import LocalAIAgent, load_project_config
from models import ModelManager
from pathlib import Path
from typing import Optional


class AICodeAgentAPI:
    """Simple API for using the agent as a Python library."""

    def __init__(
        self,
        config_path: str = "agent.config.json",
        models_dir: Optional[str] = None,
    ):
        """Initialize the agent API.
        
        Args:
            config_path: Path to agent.config.json
            models_dir: Override models directory
        """
        config = load_project_config(config_path)
        
        if models_dir:
            config["models_dir"] = models_dir
        
        self.model_mgr = ModelManager(config["models_dir"])
        self.config = config
        self.agent: Optional[LocalAIAgent] = None

    def load_model(self, model_name: Optional[str] = None) -> LocalAIAgent:
        """Load a model and initialize the agent.
        
        Args:
            model_name: Model filename (overrides config)
        
        Returns:
            Initialized LocalAIAgent
        """
        model = model_name or self.config.get("model")
        model_path = self.model_mgr.get_model_path(model)
        
        if not model_path:
            raise FileNotFoundError(
                f"Model '{model}' not found in {self.config['models_dir']}\n"
                f"Available: {self.model_mgr.list_models()}"
            )
        
        self.agent = LocalAIAgent(
            model_path=model_path,
            n_ctx=self.config.get("n_ctx", 2048),
            n_threads=self.config.get("n_threads", 4),
            n_gpu_layers=self.config.get("n_gpu_layers", 0),
        )
        return self.agent

    def ask(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 512,
    ) -> str:
        """Ask the agent a question.
        
        Args:
            prompt: User prompt
            model: Model to use (loads if not already loaded)
            temperature: Sampling temperature
            max_tokens: Maximum response length
        
        Returns:
            Model response
        """
        if not self.agent or (model and self.config.get("model") != model):
            self.load_model(model)
        
        return self.agent.ask(
            prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def list_models(self) -> list[str]:
        """List available models."""
        return self.model_mgr.list_models()


# Example usage
if __name__ == "__main__":
    import sys

    # Initialize API
    api = AICodeAgentAPI()

    # List available models
    print("Available models:")
    for model in api.list_models():
        print(f"  - {model}")

    if len(api.list_models()) == 0:
        print("\nNo models found. Download with: python download_models.py --popular")
        sys.exit(1)

    # Ask a question
    print("\n--- Running example ---\n")
    response = api.ask("Write a quick hello world function in Python")
    print(response)
