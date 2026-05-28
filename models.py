"""Local model management for GGUF models."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


class ModelManager:
    """Manage local GGUF models."""

    def __init__(self, models_dir: str = "./models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def get_model_path(self, model_name: str) -> Optional[Path]:
        """Find model file by name.
        
        Args:
            model_name: Model filename (e.g. 'model.gguf') or model ID (e.g. 'phi-3-mini')
        
        Returns:
            Path to model file if found, None otherwise.
        """
        # Try direct filename first
        model_path = self.models_dir / model_name
        if model_path.exists() and model_path.suffix == ".gguf":
            return model_path

        # Try with .gguf extension
        if not model_name.endswith(".gguf"):
            model_path = self.models_dir / f"{model_name}.gguf"
            if model_path.exists():
                return model_path

        # Search in subdirectories
        for gguf_file in self.models_dir.rglob("*.gguf"):
            if model_name in str(gguf_file):
                return gguf_file

        return None

    def list_models(self) -> list[str]:
        """List all available GGUF models."""
        models = []
        for gguf_file in self.models_dir.rglob("*.gguf"):
            models.append(str(gguf_file.relative_to(self.models_dir)))
        return sorted(models)

    def verify_model_exists(self, model_name: str) -> bool:
        """Check if model exists."""
        return self.get_model_path(model_name) is not None
