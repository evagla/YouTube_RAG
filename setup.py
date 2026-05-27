"""
Creating the environment based on the project.ymal file information.
"""

import subprocess
import yaml
import os
from pathlib import Path


def run(cmd):
    print(f">>> {cmd}")
    subprocess.run(cmd, shell=True, check=True)


# Läs YAML
with open("project.yaml") as f:
    config = yaml.safe_load(f)

deps = config.get("dependencies", [])
templates = config.get("templates", {})

# 1. Skapa venv om den inte finns
if not Path(".venv").exists():
    run("uv venv")
else:
    print("Virtuell miljö finns redan")

# 2. Installera dependencies
if deps:
    run("uv pip install " + " ".join(deps))

# 3. Spara requirements.txt
run("uv pip freeze > requirements.txt")

# 4. Skapa filer från templates
for filepath, content in templates.items():
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Skapade fil: {filepath}")

print("\nMiljön och filerna är klara!")
