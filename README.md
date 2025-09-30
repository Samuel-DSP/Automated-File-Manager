# Automated-File-Organiser
Automated File Organiser is a Python-based tool that monitors your directories in real-time and automatically organizes downloaded files into categories. It provides a Flask API to view recent file activity and category statistics, backed by SQLite.

___
# Features

  - **Real-time File Monitoring**: Uses Watchdog to track changes in source directories and automatically move files to the appropriate destination.
  - **Categorisation**: Supports images, videos, audio, documents, and GIFs with configurable categories via YAML.
  - **Duplicate Handling**: Ensures unique filenames when duplicates exist.
  - **Logging**: Structured logging for all file movements.
  - **Flask API**: Provides endpoints to monitor system health, recent file activity, and category statistics.
  - **Portable Configuration**: YAML file allows flexible setup across different environments.

___
# Installation



___
# Configuration
<pre>python sources:
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
