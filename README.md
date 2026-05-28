# Ai-code-free-agent

**100% Free Local AI Agent** — Run code assistance with local GGUF models, no API keys required.

## Features

✅ **Fully local & free** — No OpenAI API, no cloud services  
✅ **GGUF format support** — Lightweight, fast quantized models  
✅ **Easy model management** — Auto-download from Hugging Face  
✅ **Project configuration** — Per-project settings via JSON  
✅ **GPU acceleration** — Optional CUDA support via llama-cpp-python  

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Models

Download recommended free models (Phi-3-mini, Neural-Chat, Mistral):

```bash
python download_models.py --popular
```

Or download a specific model:

```bash
python download_models.py --model-id TheBloke/Phi-3-mini-4k-instruct-GGUF \
  --filename phi-3-mini-4k-instruct.Q4_K_M.gguf
```

### 3. Run Agent

```bash
python agent.py "Write a Python function to calculate Fibonacci numbers"
```

List available models:

```bash
python agent.py --list-models
```

## Project Configuration

Create `agent.config.json` in your project:

```json
{
  "model": "phi-3-mini-4k-instruct.Q4_K_M.gguf",
  "models_dir": "./models",
  "n_ctx": 2048,
  "n_threads": 4,
  "n_gpu_layers": 0
}
```

| Setting | Description |
|---------|-------------|
| `model` | Model filename (searches in models_dir) |
| `models_dir` | Directory containing GGUF models |
| `n_ctx` | Context window size (tokens) |
| `n_threads` | CPU threads for inference |
| `n_gpu_layers` | GPU layers (0 = CPU only) |

## Usage Examples

### Basic usage with config

```bash
python agent.py "Explain closures in Python"
```

### Override model

```bash
python agent.py --model mistral-7b "Write a sorting algorithm"
```

### Customize inference

```bash
python agent.py --threads 8 --temperature 0.5 --gpu-layers 20 \
  "Generate a test for user authentication"
```

### List available models

```bash
python agent.py --list-models
```

## Recommended Models

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| **Phi-3-mini** | ~2.3 GB | ⚡ Fastest | Good |
| **Neural-Chat-7B** | ~4.3 GB | 🚀 Fast | Excellent |
| **Mistral-7B** | ~4.3 GB | 🚀 Fast | Excellent |

## Architecture

```
agent.py         - Main agent & CLI
models.py        - Model management (find, list GGUF files)
download_models.py - Download from Hugging Face
agent.config.json - Project configuration
models/          - Local GGUF models directory
```

## API Usage

```python
from agent import LocalAIAgent

# Initialize with a GGUF model
agent = LocalAIAgent(
    model_path="./models/phi-3-mini-4k-instruct.Q4_K_M.gguf",
    n_threads=4,
    n_ctx=2048,
)

# Get response
response = agent.ask("Write a sorting function")
print(response)
```

## Performance Tips

- **Use Q4_K_M quantization** — Best speed/quality balance (~4 bits)
- **Increase n_threads** — Match your CPU core count
- **Enable GPU layers** — If you have CUDA: `--gpu-layers 20`
- **Adjust temperature** — Lower = more focused (0.0-0.2), higher = creative (0.7-1.0)

## Troubleshooting

### Model not found
```bash
python agent.py --list-models
# Download missing models
python download_models.py --popular
```

### Memory issues
- Use smaller models (Phi-3-mini)
- Reduce `n_ctx` (e.g., 1024 instead of 2048)
- Enable GPU acceleration

### Slow inference
- Use CPU: ensure `n_threads` = your core count
- Use GPU: install CUDA-enabled llama-cpp-python
- Switch to faster quantization (Q4 instead of Q5)

## Free Model Resources

- **TheBloke GGUF Models** — https://huggingface.co/TheBloke
- **Llama.cpp** — https://github.com/ggerganov/llama.cpp
- **Ollama** — Alternative local model runtime

## License

MIT

