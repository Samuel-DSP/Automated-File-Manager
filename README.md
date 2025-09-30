# Automated-File-Organiser
Automated File Organiser is a Python-based tool that monitors your directories in real-time and automatically organizes downloaded files into categories. It provides a Flask API to view recent file activity and category statistics, backed by SQLite.

___
# Features

  - Real-time File Monitoring: Uses Watchdog to track changes in source directories and automatically move files to the appropriate destination.
  - Categorisation: Supports images, videos, audio, documents, and GIFs with configurable categories via YAML.
  - Duplicate Handling: Ensures unique filenames when duplicates exist.
  - Logging: Structured logging for all file movements.
  - Flask API: Provides endpoints to monitor system health, recent file activity, and category statistics.
  - Portable Configuration: YAML file allows flexible setup across different environments.
