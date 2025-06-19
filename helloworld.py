from diffusers import DiffusionPipeline
import torch
import imageio
import os

# Define prompt file paths
base_path = os.path.expanduser("~/Documents/alp/utubed")
character_path = os.path.join(base_path, "character_prompt.txt")
video1_path = os.path.join(base_path, "video1_prompt.txt")
video2_path = os.path.join(base_path, "video2_prompt.txt")

# Load prompt texts
def read_prompt(path):
    with open(path, "r") as f:
        return f.read().strip()

character = read_prompt(character_path)
video1 = read_prompt(video1_path)
video2 = read_prompt(video2_path)

# Compose full prompts
prompt1 = f"{character}, {video1}"
prompt2 = f"{character}, {video2}"

# Load model
pipe = DiffusionPipeline.from_pretrained(
    "cerspense/zeroscope_v2_576w",
    torch_dtype=torch.float16,
)
pipe.to("mps")

# Output directory
os.makedirs("outputs", exist_ok=True)

# Function to generate and save video
def generate_video(prompt, filename):
    print(f"Generating video for: {prompt}")
    result = pipe(prompt)
    frames = result.frames[0]
    output_path = f"outputs/{filename}"
    imageio.mimsave(output_path, frames, fps=6)
    print(f"Saved: {output_path}")

# Generate videos
generate_video(prompt1, "child_getting_on_bus.mp4")
generate_video(prompt2, "child_in_bus_window.mp4")
