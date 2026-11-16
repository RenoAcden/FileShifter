import os
from pathlib import Path

# Quick helper / inspection script
src_dir = Path.home() / "Downloads"

if src_dir.exists():
    with os.scandir(src_dir) as entries:
        for entry in entries:
            print(entry.name)

    