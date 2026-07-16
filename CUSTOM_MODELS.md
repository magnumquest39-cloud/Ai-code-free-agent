# Custom Models Integration Guide

## Adding Your Own Fine-Tuned Models

### Option 1: Local Directory

Place your GGUF model files in the `models/` directory:

```bash
models/
├── phi-3-mini-4k-instruct.Q4_K_M.gguf
├── my-custom-model.gguf
└── my-finetuned-codegen.gguf
```

Then use it:

```bash
python agent.py --model my-custom-model.gguf "Your prompt"
```

### Option 2: Subdirectories

Organize models by type:

```bash
models/
├── general/
│   └── mistral-7b.gguf
├── coding/
│   └── my-code-specialist.gguf
└── custom/
    └── domain-specific.gguf
```

Reference with path:

```bash
python agent.py --model coding/my-code-specialist.gguf "Write Python code"
```

### Option 3: External Locations

Download your model from external sources and move to `models/`:

```bash
# Example: Download from Hugging Face (custom model)
python download_models.py \
  --model-id your-username/my-custom-model-GGUF \
  --filename custom.gguf
```

### Option 4: Project-Specific Configuration

Update `agent.config.json`:

```json
{
  "model": "my-finetuned-model.gguf",
  "models_dir": "./models",
  "n_ctx": 4096,
  "n_threads": 8,
  "n_gpu_layers": 10
}
```

## Converting Models to GGUF

If you have a model in other formats (SafeTensors, PyTorch), convert to GGUF:

### Using llama.cpp

```bash
# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Convert model to GGUF
python convert.py /path/to/your/model

# Quantize (optional, for smaller files)
./quantize /path/to/model.gguf /path/to/model.Q4_K_M.gguf Q4_K_M
```

### Using AutoGGUF

```bash
pip install auto-gptq

# Convert PyTorch → GGUF
python -m llama_cpp.scripts.convert /path/to/model
```

## Performance Tuning for Custom Models

### Recommended Quantization Levels

| Level | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| Q2_K | 20% | ⚡⚡⚡ | Poor | Mobile/edge |
| Q3_K | 30% | ⚡⚡ | Fair | Light use |
| **Q4_K_M** | 42% | 🚀 | Good | **Recommended** |
| Q5_K_M | 52% | ⚡ | Excellent | Quality |
| Q6_K | 62% | Medium | Excellent | High quality |
| Q8_0 | 82% | Slow | Perfect | Reference |

### Optimize n_ctx for Your Model

```bash
# Small models (3-7B), limited RAM: 1024-2048
python agent.py --model my-small-model.gguf "prompt"

# Large models (13B+), more RAM: 2048-4096
python agent.py --model my-large-model.gguf \
  --config agent.config.json "prompt"
```

### Enable GPU Acceleration

If you have CUDA:

```bash
# Install CUDA-enabled version
pip uninstall llama-cpp-python
CMAKE_ARGS="-DLLAMA_CUDA=on" pip install llama-cpp-python

# Use GPU layers
python agent.py --gpu-layers 20 "prompt"
```

## Supported Model Architectures

Models that work well with llama-cpp-python (GGUF format):

- ✅ Llama/Llama-2/Llama-3
- ✅ Mistral
- ✅ Phi (1, 2, 3)
- ✅ Neural-Chat
- ✅ OpenHermes
- ✅ WizardCoder
- ✅ CodeLlama
- ✅ Vicuna
- ✅ Dolphin
- ✅ Orca

## Creating Your Own Fine-Tuned Model

### Quick Example: LoRA Fine-Tuning

```python
# Fine-tune on your data with unsloth or peft
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/phi-2-unsloth-gguf",
    load_in_4bit=True,
)

# ... train your model ...

# Save and convert to GGUF
model.save_pretrained_merged("./my-finetuned-model")

# Then convert to GGUF using llama.cpp
```

## Troubleshooting Custom Models

### Model not loading
```
Error: Model not found
Solution: Place model in models/ directory and use correct filename
```

### Out of memory
```
Solution: Reduce n_ctx or use a more quantized version (Q2_K vs Q8_0)
```

### Slow inference
```
Solution: 
- Use Q4_K_M quantization
- Enable GPU with --gpu-layers
- Reduce context size
```

## Resources

- **Llama.cpp** — https://github.com/ggerganov/llama.cpp
- **TheBloke's Models** — https://huggingface.co/TheBloke
- **GGUF Specification** — https://github.com/ggerganov/ggml
- **Model Hub** — https://huggingface.co/models?library=ggml
