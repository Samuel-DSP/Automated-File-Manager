# Automated-File-Manager
Automated File Organiser is a Python-based tool that monitors your directories in real-time and automatically organizes downloaded files into categories. It provides a Flask API to view recent file activity and category statistics, backed by SQLite.

# Features

  - **Real-time File Monitoring**: Uses Watchdog to track changes in source directories and automatically move files to the appropriate destination.
  - **Categorisation**: Supports images, videos, audio, documents, and GIFs with configurable categories via YAML.
  - **Duplicate Handling**: Ensures unique filenames when duplicates exist.
  - **Logging**: Structured logging for all file movements.
  - **Flask API**: Provides endpoints to monitor system health, recent file activity, and category statistics.
  - **Portable Configuration**: YAML file allows flexible setup across different environments.

# Installation
1. Clone the repository
<pre>git clone '://github.com/Samuel_DSP/Automated-File-Organiser.git</pre>
2. Install dependencies
<pre>pip install -r requirements.txt
</pre>


# Configuration
Edit `config.yaml` to set:
  - `sources` – List of directories to monitor.
  - `destinations` – Map categories to destination folders.
  - `categories` – File extensions for each category.
  - `archive_after_days` – Optional archiving delay.
  - `db_path` – Path to SQLite database.
  - `scan_recursive` – Set to `true` to monitor subdirectories.

Example:
<pre>yaml 
  sources:
  - C:/Users/username/Downloads

destinations:
  Images: C:/Users/username/Desktop/Downloaded Images
  Videos: C:/Users/username/Desktop/Downloaded Videos
  Music: C:/Users/username/Desktop/Downloaded Music

categories:
  Images: [".jpg", ".png", ".jpeg"]
  Videos: [".mp4", ".avi"]
  Music: [".mp3", ".wav"]

archive_after_days: 30
db_path: ./filemanager.database
scan_recursive: true
</pre>

# Usage
Run the file organiser with:
<pre>python main.py</pre>
- It will monitor your `sources` folders and move files automatically.
- Open the Flask dashboard at http://127.0.0.1:5000 to see:
  - /health – API status
  - /recent – Last 10 moved files
  - /stats – File counts per category
 
# Scan Existing Files
To process files already in the source folders when starting the app:
<pre>python
from filemanager.mover import scan_existing_files
scan_existing_files(config, db_session)
</pre>

# Project Structure
<pre>
File_Manager/
├── filemanager/              # Core python files containing all logic
│   ├── __init__.py
│   ├── database.py           # SQLite setup and SQLAlcehemy ORM
│   ├── api.py                # Flask API and dashboard
│   ├── config_parser.py      # YAML configuration parser
│   └── file_mover.py         # File monitoring and moving logic 
├── templates/                # HTML templates for Flask
│   └── dashboard.html        # Dashboard template for recent files and stats
├── static/                   # Static files for Flask
│   └── style.css             # Styles for Dashboard
├── main.py                   # Entry point to run the File Manager
└── config.yaml               # User configuration file
</pre>

# Logging
Logs are printed to the console with timestamps for all file movements:
<pre>
2025-09-26 18:36:54 - Moving C:/Users/username/Downloads/file.jpg → C:/Users/username/Desktop/Downloaded Images/file.jpg
2025-09-26 18:36:54 - Moved file.jpg → Images
</pre>
