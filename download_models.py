import sys
import subprocess
import requests
import os

# 函式: 用於下載文件
def download_file(url, save_path="./models/"):
    # 從URL中獲取文件名
    local_filename = url.split('/')[-1]
    full_path = os.path.join(save_path, local_filename)
    
    # 使用requests來下載文件
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(full_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded {local_filename} to {save_path}")

# 檢查是否提供了足夠的參數
if len(sys.argv) < 3:
    print("Insufficient arguments provided. At least two arguments are required.")
    sys.exit(1)

# 檢查是否有 "essential" 參數並進行相應的操作
if sys.argv[1] == "essential":
    print("Downloading Essential Models (EfficientNet, Stage A, Previewer)")
    essential_models = [
        "https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_a.safetensors",
        "https://huggingface.co/stabilityai/StableWurst/resolve/main/previewer.safetensors",
        "https://huggingface.co/stabilityai/StableWurst/resolve/main/effnet_encoder.safetensors"
    ]
    for model_url in essential_models:
        download_file(model_url)
    sys.argv.pop(1)  # 移除 "essential" 參數，使得後續參數向前移動

# 解析參數
second_argument = sys.argv[1]
binary_decision = sys.argv[2] if len(sys.argv) > 2 else "bfloat16"

# 下載模型
model_urls = {
    "big-big": [
        ("https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_b_bf16.safetensors", "https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_c_bf16.safetensors") if binary_decision == "bfloat16" else 
        ("https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_b.safetensors", "https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_c.safetensors")
    ],
    "big-small": [
        ("https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_b_bf16.safetensors", "https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_c_lite_bf16.safetensors") if binary_decision == "bfloat16" else 
        ("https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_b.safetensors", "https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_c_lite.safetensors")
    ],
    "small-big": [
        ("https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_b_lite_bf16.safetensors", "https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_c_bf16.safetensors") if binary_decision == "bfloat16" else 
        ("https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_b_lite.safetensors", "https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_c.safetensors")
    ],
    "small-small": [
        ("https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_b_lite_bf16.safetensors", "https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_c_lite_bf16.safetensors") if binary_decision == "bfloat16" else 
        ("https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_b_lite.safetensors", "https://huggingface.co/stabilityai/StableWurst/resolve/main/stage_c_lite.safetensors")
    ]
}

for url_tuple in model_urls[second_argument]:
    for url in url_tuple:  # 遍歷元組中的每個URL
        download_file(url)  # 現在傳遞的是字符串而不是元組
else:
    print("Invalid second argument. Please provide a valid argument: big-big, big-small, small-big, or small-small.")
    sys.exit(2)
