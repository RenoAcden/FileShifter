import os
from os import scandir, makedirs
from os.path import splitext, exists, join, dirname, abspath
from pathlib import Path
from shutil import move
from time import sleep
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Optional local .env configuration loader
_script_dir = Path(__file__).resolve().parent
_env_path = _script_dir / ".env"
if _env_path.exists():
    try:
        with open(_env_path, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip())
    except Exception:
        pass

# Determine source downloads directory:
# 1. Environment variable DOWNLOADS_DIR (or from .env)
# 2. Defaults to standard user Downloads folder (e.g. C:\Users\<Username>\Downloads)
_default_downloads = str(Path.home() / "Downloads")
source_dir = os.getenv("DOWNLOADS_DIR", _default_downloads)

dest_dir_sfx = join(source_dir, "SFX's")
dest_dir_music = join(source_dir, "Music")
dest_dir_video = join(source_dir, "Videos")
dest_dir_image = join(source_dir, "Images")
dest_dir_documents = join(source_dir, "Documents")
dest_dir_applications = join(source_dir, "Applications")
dest_dir_zip = join(source_dir, "Zips")

# ? Temporary or incomplete download extensions to ignore
ignored_extensions = {".crdownload", ".tmp", ".part", ".download", ".partial"}

# ? Supported image types
image_extensions = {
    ".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp",
    ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp",
    ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf",
    ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"
}

# ? Supported video types
video_extensions = {
    ".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4",
    ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"
}

# ? Supported audio types (fixed missing dot in .mp3)
audio_extensions = {".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"}

# ? Supported document types
document_extensions = {
    ".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv"
}

# ? Supported application types
application_extensions = {".exe", ".msi", ".iso"}

# ? Supported zip / archive types
zip_extensions = {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"}

# Build extension to destination directory mapping
extension_map = {}
for ext in image_extensions:
    extension_map[ext] = dest_dir_image
for ext in video_extensions:
    extension_map[ext] = dest_dir_video
for ext in document_extensions:
    extension_map[ext] = dest_dir_documents
for ext in application_extensions:
    extension_map[ext] = dest_dir_applications
for ext in zip_extensions:
    extension_map[ext] = dest_dir_zip


def get_unique_path(dest, name):
    """
    Generate a unique destination path without modifying or renaming
    any pre-existing files in the target directory.
    """
    filename, extension = splitext(name)
    dest_path = join(dest, name)
    counter = 1
    while exists(dest_path):
        dest_path = join(dest, f"{filename}({counter}){extension}")
        counter += 1
    return dest_path


def move_file(dest, entry, name):
    """
    Safely move a file to its destination directory, creating the directory
    if needed and retrying if the file is locked by a browser or system process.
    """
    if not exists(dest):
        makedirs(dest, exist_ok=True)

    dest_path = get_unique_path(dest, name)
    max_retries = 5
    for attempt in range(max_retries):
        try:
            source_path = entry.path if hasattr(entry, 'path') else entry
            move(source_path, dest_path)
            return True
        except (PermissionError, OSError) as e:
            if attempt < max_retries - 1:
                sleep(1)
            else:
                logging.warning(f"Could not move {name} (file may be in use): {e}")
                return False


def get_destination(entry, name):
    """Determine the appropriate destination directory for a file based on its extension and metadata."""
    _, ext = splitext(name)
    ext = ext.lower()

    if not ext or ext in ignored_extensions:
        return None

    # Audio files: split between SFX and Music based on size and name
    if ext in audio_extensions:
        try:
            size = entry.stat().st_size
        except OSError:
            size = 0
        if size < 10_000_000 or "SFX" in name.upper():
            return dest_dir_sfx
        return dest_dir_music

    return extension_map.get(ext)


def process_entry(entry):
    """Inspect and move a single filesystem entry if it matches a handled file type."""
    try:
        # Ignore subdirectories (e.g. existing destination folders)
        if not entry.is_file():
            return

        name = entry.name
        dest = get_destination(entry, name)
        if dest:
            if move_file(dest, entry, name):
                logging.info(f"Moved: {name} -> {dest}")
    except Exception as e:
        logging.error(f"Error processing {entry.name}: {e}")


def organize_existing_files():
    """Initial pass to sort any existing files currently in the source folder on startup."""
    logging.info("Scanning and organizing existing files in downloads...")
    with scandir(source_dir) as entries:
        for entry in entries:
            process_entry(entry)


class MoverHandler(FileSystemEventHandler):
    # Runs when changes occur in source_dir
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                process_entry(entry)


if __name__ == "__main__":
    log_file = join(dirname(abspath(__file__)), "file_organizer.log")
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.FileHandler(log_file, encoding='utf-8'),
                            logging.StreamHandler()
                        ])

    # 1. Organize files that are already in downloads
    organize_existing_files()

    # 2. Watch for new files (recursive=False to avoid loops in subdirectories)
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    logging.info(f"Monitoring started for: {source_dir}")

    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()