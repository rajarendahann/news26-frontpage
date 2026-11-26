"""Main entry point script to copy the generated newspaper front-page entry image
to the designated output directory for make.fun evaluation.
"""

import os
import shutil
from pathlib import Path

def main():
    """Copy entry.png from the workspace root directory to the target output directory."""
    # Retrieve target output directory from environment (defaulting to 'out')
    output_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    bot_dir_env = os.environ.get("MAKEFUN_BOT_DIR", ".")
    
    source_image_path = Path(bot_dir_env) / "entry.png"
    output_directory_path = Path(output_dir_env)
    
    # Ensure the output destination directory exists
    output_directory_path.mkdir(parents=True, exist_ok=True)
    
    destination_image_path = output_directory_path / "entry.png"
    
    if source_image_path.exists():
        shutil.copyfile(source_image_path, destination_image_path)
        print(f"Successfully copied {source_image_path} to {destination_image_path}")
    else:
        print(f"Error: Source image not found at {source_image_path}")

if __name__ == "__main__":
    main()
