# import logging
# from time import sleep
# from threading import Thread
# from watchdog.observers import Observer
# from filemanager.config_parser import Config
# from filemanager.database import init_db
# from filemanager.file_mover import MoverHandler
# from filemanager.api import create_app
# import os  # <-- needed for scan_existing_files

# def scan_existing_files(config, db_session):
#     """Scan all source folders for existing files and categorize them."""
#     for src in config.sources:
#         for entry in os.scandir(src):
#             if entry.is_file():
#                 mover = MoverHandler(config, db_session)
#                 mover.categorise(entry.path)

# # --- MAIN ---
# def main():
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(message)s',
#         datefmt='%Y-%m-%d %H:%M:%S'
#     )

#     # Load config + DB
#     config = Config("config.yaml")
#     db_session = init_db(config.db_path)

#     # --- Initial scan of existing files ---
#     scan_existing_files(config, db_session)

#     # Start Flask API in a thread
#     app = create_app(db_session)
#     Thread(target=lambda: app.run(port=5000, debug=False, use_reloader=False), daemon=True).start()

#     # Start watchdog mover
#     event_handler = MoverHandler(config, db_session)
#     observer = Observer()
#     for src in config.sources:
#         observer.schedule(event_handler, src, recursive=config.scan_recursive)

#     observer.start()
#     logging.info(f"Watching folder(s): {config.sources} (recursive={config.scan_recursive})")

#     try:
#         while True:
#             sleep(5)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()


# if __name__ == "__main__":
#     main()



import os
import logging
from time import sleep
from threading import Thread
from watchdog.observers import Observer
from filemanager.config_parser import Config
from filemanager.database import init_db
from filemanager.file_mover import MoverHandler
from filemanager.api import create_app

# Scan all source folders for existing files and categorize them
def scan_existing_files(config, db_session):
    for src in config.sources:
        for entry in os.scandir(src):
            if entry.is_file():
                # Initialize mover handler for each file
                mover = MoverHandler(config, db_session)
                # Categorize and move the file
                mover.categorise(entry.path)

def main():
    # Configure logging with timestamps
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Load configuration from YAML
    config = Config("config.yaml")
    # Initialize database session
    db_session = init_db(config.db_path)

    # Perform an initial scan of existing files in source directories
    scan_existing_files(config, db_session)

    # Start Flask API in a separate daemon thread
    app = create_app(db_session)
    Thread(
        target=lambda: app.run(port=5000, debug=False, use_reloader=False),
        daemon=True
    ).start()

    # Initialize watchdog event handler for monitoring new files
    event_handler = MoverHandler(config, db_session)
    observer = Observer()
    # Schedule observer for all source directories
    for src in config.sources:
        observer.schedule(event_handler, src, recursive=config.scan_recursive)

    # Start observer
    observer.start()
    logging.info(f"Watching folder(s): {config.sources} (recursive={config.scan_recursive})")

    # Keep the program running, checking for new events
    try:
        while True:
            sleep(5)
    except KeyboardInterrupt:
        # Stop observer on user interruption
        observer.stop()
    observer.join()

# Run main() if script is executed directly
if __name__ == "__main__":
    main()
