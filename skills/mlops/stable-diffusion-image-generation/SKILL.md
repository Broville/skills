---
name: stable-diffusion-image-generation
description: Local text-to-image generation with Stable Diffusion models — text-to-image, image-to-image, inpainting, ControlNet, LoRA adapters, all running on local GPU inference
version: 1.0.0
author: Broville
license: MIT
platforms: [linux]
trigger:
  - User asks to generate an image from a text description
  - User wants image-to-image transformation or style transfer
  - User needs inpainting or outpainting on an existing image
  - User asks about running Stable Diffusion locally
  - User wants to use ControlNet for spatial conditioning or LoRA style adapters
related_skills:
  - meme-generation
  - chroma
---

# Stable Diffusion Image Generation — Local Inference

## Description

Comprehensive guide to generating images locally with Stable Diffusion models using the Diffusers library. All inference runs on your hardware — no cloud API calls, no data leaves your machine. Supports text-to-image, image-to-image, inpainting, ControlNet conditioning, LoRA style adapters, and multiple model variants (SD 1.5, SDXL, SD 3.0, Flux).

## Prerequisites

- Python 3.8+
- NVIDIA GPU with CUDA support recommended (CPU works but is 10-20× slower)
- `pip install diffusers transformers accelerate torch`
- Optional: `pip install xformers` for memory-efficient attention
- Model weights are downloaded on first use (~4-10 GB depending on model)

## Steps

### 1. Basic text-to-image generation

```python
from diffusers import DiffusionPipeline
import torch

pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe.to("cuda")

image = pipe(
    "A serene mountain landscape at sunset, highly detailed",
    num_inference_steps=50,
    guidance_scale=7.5
).images[0]

image.save("output.png")
```

### 2. Higher quality with SDXL

```python
from diffusers import AutoPipelineForText2Image
import torch

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.enable_model_cpu_offload()  # Memory optimization

image = pipe(
    prompt="A futuristic city with flying cars, cinematic lighting",
    height=1024,
    width=1024,
    num_inference_steps=30
).images[0]

image.save("output_xl.png")
```

### 3. Image-to-image transformation

```python
from diffusers import AutoPipelineForImage2Image
from PIL import Image
import torch

pipe = AutoPipelineForImage2Image.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

init_image = Image.open("input.jpg").resize((512, 512))

image = pipe(
    prompt="A watercolor painting of the scene",
    image=init_image,
    strength=0.75,  # How much to transform (0-1)
    num_inference_steps=50
).images[0]

image.save("output_img2img.png")
```

### 4. Inpainting (fill masked regions)

```python
from diffusers import AutoPipelineForInpainting
from PIL import Image
import torch

pipe = AutoPipelineForInpainting.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16
).to("cuda")

image = Image.open("photo.jpg")
mask = Image.open("mask.png")  # White = region to fill

result = pipe(
    prompt="A red car parked on the street",
    image=image,
    mask_image=mask,
    num_inference_steps=50
).images[0]

result.save("output_inpaint.png")
```

### 5. ControlNet for spatial conditioning

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import torch

controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_canny",
    torch_dtype=torch.float16
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16
).to("cuda")

# Use Canny edge image as control
control_image = get_canny_image(input_image)

image = pipe(
    prompt="A beautiful house in the style of Van Gogh",
    image=control_image,
    num_inference_steps=30
).images[0]
```

### 6. LoRA style adapters

```python
# Load LoRA weights onto existing pipeline
pipe.load_lora_weights("path/to/lora", weight_name="style.safetensors")

image = pipe("A portrait in the trained style").images[0]

# Adjust LoRA strength
pipe.fuse_lora(lora_scale=0.8)

# Unload when done
pipe.unload_lora_weights()
```

### 7. Memory optimization (essential for low-VRAM GPUs)

```python
# Model CPU offload — moves unused models to RAM
pipe.enable_model_cpu_offload()

# Sequential CPU offload — more aggressive, slower
pipe.enable_sequential_cpu_offload()

# Attention slicing — reduces memory by computing attention in chunks
pipe.enable_attention_slicing()

# VAE slicing for large images
pipe.enable_vae_slicing()
pipe.enable_vae_tiling()
```

### 8. Fast scheduler swapping

```python
from diffusers import DPMSolverMultistepScheduler

# Swap for faster generation with fewer steps
pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config
)

image = pipe(prompt, num_inference_steps=20).images[0]
```

### 9. Reproducible generation

```python
generator = torch.Generator(device="cuda").manual_seed(42)

image = pipe(
    prompt="A cat wearing a top hat",
    generator=generator,
    num_inference_steps=50
).images[0]
```

## Pitfalls

1. **CUDA out of memory** — SDXL and large models need ≥8 GB VRAM. Enable `pipe.enable_model_cpu_offload()` and `pipe.enable_attention_slicing()` to reduce peak usage. For SD 1.5 on 4 GB GPUs, use `float16` with CPU offload.
2. **Model download size** — First run downloads 4–10 GB of weights. Set `HF_HOME` or `TRANSFORMERS_CACHE` environment variable to control where models are cached if disk space is limited.
3. **Black/noise images from safety checker** — The safety checker can over-trigger on artistic prompts. Bypass with `pipe.safety_checker = None` if appropriate, but ensure responsible use.
4. **Wrong dimensions cause artifacts** — Image dimensions must be multiples of 8. SD 1.5 works best at 512×512, SDXL at 1024×1024. Arbitrary sizes produce visible artifacts.
5. **Long generation times on CPU** — CPU inference for SD 1.5 takes minutes per image. Use GPU (`pipe.to("cuda")`) for practical generation, or use the `turbo` model for faster results.

## Verification

1. **Basic generation works**: Run the text-to-image example from Step 1 and confirm it saves a valid PNG file at `output.png` that visually matches the prompt.
2. **Memory optimization works**: Enable `pipe.enable_model_cpu_offload()` and confirm the same prompt still generates correctly without CUDA OOM.
3. **Model is cached locally**: After first generation, check that model weights are cached in `~/.cache/huggingface/` (or your `HF_HOME` directory).