# Automated-File-Organiser
Automated File Organiser is a Python-based tool that monitors your directories in real-time and automatically organizes downloaded files into categories. It provides a Flask API to view recent file activity and category statistics, backed by SQLite.

# Features

  - **Real-time File Monitoring**: Uses Watchdog to track changes in source directories and automatically move files to the appropriate destination.
  - **Categorisation**: Supports images, videos, audio, documents, and GIFs with configurable categories via YAML.
  - **Duplicate Handling**: Ensures unique filenames when duplicates exist.
  - **Logging**: Structured logging for all file movements.
  - **Flask API**: Provides endpoints to monitor system health, recent file activity, and category statistics.
  - **Portable Configuration**: YAML file allows flexible setup across different environments.

# Installation



# Configuration
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
db_path: ./filemanager.db
scan_recursive: true
</pre>

# Usage
Run the file organiser with:
<pre>python cli.py</pre>
- It will monitor your sources folder(s) and move files automatically.
- Open the Flask dashboard at http://127.0.0.1:5000 to see:
  - /health – API status
  - /recent – Last 10 moved files
/stats – File counts per category
