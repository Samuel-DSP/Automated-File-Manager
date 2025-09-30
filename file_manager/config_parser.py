# import yaml

# class Config:
#     def __init__(self, path: str):
#         with open(path, "r") as f:
#             data = yaml.safe_load(f)
#         self.sources = data.get("sources", [])
#         self.destinations = data.get("destinations", {})
#         self.categories = data.get("categories", {})
#         self.archive_after_days = data.get("archive_after_days", 30)
#         self.db_path = data.get("db_path", "filemanager.db")
#         self.scan_recursive = data.get("scan_recursive", True)




import yaml

# Class to load and store configuration from a YAML file
class Config:
    # Function to initialize configuration from a YAML file
    def __init__(self, path: str):
        # Open the YAML file at the specified path
        with open(path, "r") as f:
            # Load YAML data safely
            data = yaml.safe_load(f)
        
        # List of source directories to monitor
        self.sources = data.get("sources", [])
        # Dictionary of destination directories by file type
        self.destinations = data.get("destinations", {})
        # Dictionary of file categories (e.g., images, audio, video)
        self.categories = data.get("categories", {})
        # Number of days after which files are archived
        self.archive_after_days = data.get("archive_after_days", 30)
        # Path to the SQLite database file
        self.db_path = data.get("db_path", "filemanager.db")
        # Whether to scan directories recursively
        self.scan_recursive = data.get("scan_recursive", True)
