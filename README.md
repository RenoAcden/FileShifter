# Automated Downloads Organizer

A Python-based background service that monitors your Downloads folder in real-time and automatically sorts incoming files into category folders (Documents, Images, Videos, Music, SFX, Applications, and Archives).

## Features

- **Real-time Monitoring:** Uses `watchdog` to detect newly downloaded files instantly.
- **Initial Organization:** Automatically sorts any pre-existing unorganized files upon launch.
- **Duplicate Handling:** Renames conflicting files automatically (e.g. `file(1).pdf`) without overwriting existing files.
- **Background Execution:** Includes VBS and PowerShell scripts to run silently in the background on Windows without keeping a command prompt open.
- **Startup Integration:** Configurable Windows startup shortcut to run automatically on system boot.

## Categories

| Category | Destination Folder | Handled Extensions |
| :--- | :--- | :--- |
| **Images** | `Images/` | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`, `.ico`, etc. |
| **Videos** | `Videos/` | `.mp4`, `.mkv`, `.avi`, `.mov`, `.flv`, `.webm`, etc. |
| **Music / Audio** | `Music/` or `SFX's/` | `.mp3`, `.wav`, `.flac`, `.m4a`, `.aac`, etc. |
| **Documents** | `Documents/` | `.pdf`, `.docx`, `.doc`, `.xlsx`, `.pptx`, `.txt`, `.csv`, etc. |
| **Applications** | `Applications/` | `.exe`, `.msi`, `.iso` |
| **Archives** | `Zips/` | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, etc. |

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Source Directory (Optional):**
   By default, the script monitors your user profile's standard `Downloads` folder (`C:\Users\<User>\Downloads`).
   If your downloads are stored in a custom folder or drive, create a `.env` file in the project root:
   ```ini
   DOWNLOADS_DIR=D:\YourCustomDownloadsPath
   ```
   *(See `.env.example` for reference. The `.env` file is ignored by Git to protect your local paths).*

## Running the Organizer

- **Run in foreground (console):**
  ```bash
  python automates-files.py
  ```

- **Run silently in background:**
  Double-click `start_background.vbs`.

- **Stop background process:**
  Double-click `stop_background.bat`.

- **Enable automatic run on Windows startup:**
  Right-click `setup_startup.ps1` and choose **Run with PowerShell** (or run `powershell -ExecutionPolicy Bypass -File .\setup_startup.ps1`).

## Logs

Runtime activity and processed files are recorded in `file_organizer.log` (automatically ignored by Git).
