import time
import os
import logging
from os.path import splitext, exists, join
from shutil import move
from os import rename
from watchdog.events import FileSystemEventHandler
from .database import FileLog

# Function to ensure a unique filename in the destination folder
def make_unique(dest, name):
    counter = 1
    filename, extension = splitext(name)
    
    # Keep incrementing counter until a unique filename is found
    while exists(join(dest, name)):
        name = f"{filename}({counter}){extension}"
        counter += 1
    return name

# Function to move a file to the destination folder
# Handles duplicate files by renaming the existing file to a unique name
def move_file(dest, entry, name):
    if exists(join(dest, name)):
        # Generate a unique name for existing file
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        # Rename existing file to unique name
        rename(oldName, newName)
    # Move the new file to destination
    move(entry, dest)

# Function to wait until a file exists and is ready to be accessed
def wait_for_file(path, timeout=5):
    """Wait until the file exists and is accessible."""
    start = time.time()
    while True:
        if os.path.exists(path):
            try:
                # Try opening the file for reading to ensure it's not locked
                with open(path, "rb"):
                    return True
            except:
                pass
        # Timeout check
        if time.time() - start > timeout:
            return False
        time.sleep(0.1)

# Watchdog event handler class for monitoring file creation
class MoverHandler(FileSystemEventHandler):
    # Constructor for the handler
    def __init__(self, config, db_session):
        self.config = config          # YAML config object
        self.db_session = db_session  # SQLAlchemy session factory

    # Event triggered when a new file is created
    def on_created(self, event):
        if not event.is_directory:
            self.categorise(event.src_path)

    # Function to categorise and move the file based on its extension
    def categorise(self, path):
        # Wait for file to be fully ready
        if not wait_for_file(path):
            logging.warning(f"File not ready or missing: {path}")
            return
        
        name = os.path.basename(path)

        # Ignore incomplete download files (.crdownload, .part, .tmp, etc.)
        if name.endswith((".crdownload", ".part", ".tmp")):
            logging.info(f"Ignoring temporary download file: {name}")
            return
        
        # Check which category the file belongs to based on extensions
        for category, exts in self.config.categories.items():
            if any(name.lower().endswith(ext) for ext in exts):
                dest = self.config.destinations.get(category)
                if dest:
                    logging.info(f"Moving {path} → {join(dest, name)}")
                    # Move the file to the destination folder
                    move_file(dest, path, name)
                    logging.info(f"Moved {name} → {category}")
                    # Log the move in the database
                    self.log_to_db(name, path, join(dest, name), category)
                return

    # Function to log the file movement to the database
    def log_to_db(self, filename, src, dest, category):
        session = self.db_session()
        log = FileLog(filename=filename, src=src, dest=dest, category=category)
        session.add(log)
        session.commit()








# import time
# import os
# import logging
# from os.path import splitext, exists, join
# from shutil import move
# from os import rename
# from watchdog.events import FileSystemEventHandler
# from .database import FileLog

# # Function to ensure a unique filename in the destination folder
# def make_unique(dest, name):
#     counter = 1
#     filename, extension = splitext(name)
    
#     # Keep incrementing counter until a unique filename is found
#     while exists(join(dest, name)):
#         name = f"{filename}({counter}){extension}"
#         counter += 1
#     return name

# # Function to move a file to the destination folder
# # Handles duplicate files by renaming the existing file to a unique name
# def move_file(dest, entry, name):
#     if exists(join(dest, name)):
#         # Generate a unique name for existing file
#         unique_name = make_unique(dest, name)
#         oldName = join(dest, name)
#         newName = join(dest, unique_name)
#         # Rename existing file to unique name
#         rename(oldName, newName)
#     # Move the new file to destination
#     move(entry, dest)

# # Function to wait until a file exists, is ready to be accessed, and its size is stable
# def wait_for_file(path, timeout=15, stable_time=2):
#     # start time for timeout
#     start = time.time()
#     last_size = -1
#     stable_since = None

#     while True:
#         if os.path.exists(path):
#             try:
#                 current_size = os.path.getsize(path)
#                 # If size hasn't changed since last check
#                 if current_size == last_size:
#                     if stable_since is None:
#                         stable_since = time.time()
#                     elif time.time() - stable_since >= stable_time:
#                         # File is stable long enough
#                         return True
#                 else:
#                     # Size changed -> reset stability timer
#                     stable_since = None
#                     last_size = current_size
#             except OSError:
#                 pass

#         if time.time() - start > timeout:
#             return False

#         time.sleep(0.5)  # check twice per second


# # Watchdog event handler class for monitoring file creation
# class MoverHandler(FileSystemEventHandler):
#     # Constructor for the handler
#     def __init__(self, config, db_session):
#         self.config = config          # YAML config object
#         self.db_session = db_session  # SQLAlchemy session factory

#     # Event triggered when a new file is created
#     def on_created(self, event):
#         if not event.is_directory:
#             self.categorise(event.src_path)

#     # Function to categorise and move the file based on its extension
#     def categorise(self, path):
#         name = os.path.basename(path)

#         # Ignore incomplete download files (.crdownload, .part, .tmp, etc.)
#         if name.endswith((".crdownload", ".part", ".tmp")):
#             logging.info(f"Ignoring temporary download file: {name}")
#             return
        
#         # Wait until file is complete and stable
#         if not wait_for_file(path):
#             logging.warning(f"File not ready or missing: {path}")
#             return
        
#         # Check which category the file belongs to based on extensions
#         for category, exts in self.config.categories.items():
#             if any(name.lower().endswith(ext) for ext in exts):
#                 dest = self.config.destinations.get(category)
#                 if dest:
#                     logging.info(f"Moving {path} → {join(dest, name)}")
#                     # Move the file to the destination folder
#                     move_file(dest, path, name)
#                     logging.info(f"Moved {name} → {category}")
#                     # Log the move in the database
#                     self.log_to_db(name, path, join(dest, name), category)
#                 return

#     # Function to log the file movement to the database
#     def log_to_db(self, filename, src, dest, category):
#         session = self.db_session()
#         log = FileLog(filename=filename, src=src, dest=dest, category=category)
#         session.add(log)
#         session.commit()
