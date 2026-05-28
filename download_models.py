"""Download GGUF models from Hugging Face."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Optional


def download_from_huggingface(
    model_id: str,
    model_filename: str = "model.gguf",
    output_dir: str = "./models",
    token: Optional[str] = None,
) -> Path:
    """Download GGUF model from Hugging Face Hub.
    
    Args:
        model_id: Hugging Face model ID (e.g., 'TheBloke/Phi-3-mini-GGUF')
        model_filename: Model filename in the repo (e.g., 'model.gguf')
        output_dir: Directory to save the model
        token: Hugging Face API token (optional, for private models)
    
    Returns:
        Path to downloaded model.
    """
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        raise ImportError(
            "huggingface_hub is required. Install with: pip install huggingface-hub"
        )

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {model_id}/{model_filename}...")
    local_path = hf_hub_download(
        repo_id=model_id,
        filename=model_filename,
        cache_dir=str(output_path),
        token=token,
    )

    print(f"✓ Downloaded to: {local_path}")
    return Path(local_path)


def download_popular_models(output_dir: str = "./models") -> None:
    """Download recommended free GGUF models.
    
    Models:
    - Phi-3-mini: Lightweight, fast (~2GB)
    - Neural-Chat: General purpose (~7GB)
    - Mistral: High quality (~7GB)
    """
    models = [
        {
            "id": "TheBloke/Phi-3-mini-4k-instruct-GGUF",
            "file": "phi-3-mini-4k-instruct.Q4_K_M.gguf",
            "description": "Phi-3-mini (4B parameters, ~2.3GB)",
        },
        {
            "id": "TheBloke/neural-chat-7B-v3-1-GGUF",
            "file": "neural-chat-7b-v3-1.Q4_K_M.gguf",
            "description": "Neural-Chat (7B parameters, ~4.3GB)",
        },
        {
            "id": "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
            "file": "mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            "description": "Mistral (7B parameters, ~4.3GB)",
        },
    ]

    for i, model in enumerate(models, 1):
        try:
            print(f"\n[{i}/{len(models)}] {model['description']}")
            download_from_huggingface(
                model_id=model["id"],
                model_filename=model["file"],
                output_dir=output_dir,
            )
        except Exception as e:
            print(f"✗ Failed to download {model['id']}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download GGUF models from Hugging Face"
    )
    parser.add_argument(
        "--popular",
        action="store_true",
        help="Download recommended free models (Phi-3, Neural-Chat, Mistral)",
    )
    parser.add_argument(
        "--model-id",
        help="Hugging Face model ID (e.g., 'TheBloke/Phi-3-mini-GGUF')",
    )
    parser.add_argument(
        "--filename",
        default="model.gguf",
        help="Model filename in the repo (default: model.gguf)",
    )
    parser.add_argument(
        "--output",
        default="./models",
        help="Output directory (default: ./models)",
    )
    parser.add_argument(
        "--token",
        help="Hugging Face API token (optional, for private models)",
    )

    args = parser.parse_args()

    if args.popular:
        download_popular_models(output_dir=args.output)
    elif args.model_id:
        download_from_huggingface(
            model_id=args.model_id,
            model_filename=args.filename,
            output_dir=args.output,
            token=args.token,
        )
    else:
        print("Use --popular to download recommended models")
        print("Or use --model-id to download a specific model")
        parser.print_help()


if __name__ == "__main__":
    main()
