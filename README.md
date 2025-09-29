# Automated-File-Organiser

Automated File Organiser is a Python-based tool that monitors your directories in real-time and automatically organizes downloaded files into categories. It provides a Flask API to view recent file activity and category statistics, backed by SQLite.

Features

Real-time File Monitoring: Uses Watchdog to track changes in source directories and automatically move files to the appropriate destination.

Categorisation: Supports images, videos, audio, documents, and GIFs with configurable categories via YAML.

Duplicate Handling: Ensures unique filenames when duplicates exist.

Logging: Structured logging for all file movements.

Flask API: Provides endpoints to monitor system health, recent file activity, and category statistics.

Portable Configuration: YAML file allows flexible setup across different environments.

Tech Stack

Python 3.10+

Watchdog – Real-time file system monitoring

Flask – API backend and dashboard

SQLAlchemy – SQLite database ORM

YAML – Configuration

Logging – Structured logs for tracking file movements

Installation

Clone the repository:

git clone https://github.com/yourusername/file-organiser.git
cd file-organiser


Install dependencies:

pip install -r requirements.txt

Configuration

Edit config.yaml to set:

sources – List of directories to monitor.

destinations – Map categories to destination folders.

categories – File extensions for each category.

archive_after_days – Optional archiving delay.

db_path – Path to SQLite database.

scan_recursive – Set to true to monitor subdirectories.

Example:

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

Usage

Run the file organiser with:

python cli.py


It will monitor your sources folder(s) and move files automatically.

Open the Flask dashboard at http://127.0.0.1:5000
 to see:

/health – API status

/recent – Last 10 moved files

/stats – File counts per category

Scan Existing Files

To process files already in the source folders when starting the app:

from filemanager.mover import scan_existing_files
scan_existing_files(config, db_session)

Project Structure
filemanager/
│
├── api.py         # Flask API and dashboard
├── cli.py         # Entry point
├── config.py      # YAML configuration parser
├── db.py          # SQLite setup and ORM
├── mover.py       # File monitoring and moving logic
├── __init__.py
└── config.yaml    # User configuration file

Logging

Logs are printed to the console with timestamps for all file movements:

2025-09-26 18:36:54 - Moving C:/Users/username/Downloads/file.jpg → C:/Users/username/Desktop/Downloaded Images/file.jpg
2025-09-26 18:36:54 - Moved file.jpg → Images

Contributing

Fork the repo

Create a feature branch

Submit a pull request with detailed description

License

MIT License – feel free to use, modify, and distribute.
