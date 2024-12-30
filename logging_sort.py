import os
from datetime import datetime

# class to log all the events
class logs:
    def __init__(self, folder_path):
        self.log_folder = folder_path / '__logging_sort__'
        os.makedirs(self.log_folder, exist_ok=True)
        self.log_file = 'download_sorting_logs.txt'
        self.log_text_file = os.path.join(self.log_folder, self.log_file)
        t = timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.log_text_file, 'w') as L:
            L.write(f"Logging start --- [{t}]\n")
            L.write(f"monitoring: {folder_path} --- {t}\n")
            L.write("----------------\n")
            L.write("\n")
            
    # logs the path to the folder that has been checked
    def call_to_check_all(self, path):
        t = timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_text_file, 'a') as L:
            L.write(f"Checked: {path} --- [{t}]\n")
            L.write("\n")

    # logs the stray files found in the folder
    def stary_files_logs(self, stray_file_list: list):
        t = timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_text_file, 'a') as L:
            L.write(f"Stray files: {stray_file_list} --- [{t}]\n")
            L.write("\n")

    # logs the moved files, berfore and after location
    def on_move(self, id, old_location, new_location):
        t = timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_text_file, 'a') as L:
            L.write(f"Moved: {old_location} --> {new_location} ---  call id: {id} --- [{t}]\n")
            L.write("\n")

    # logs the created folders
    def on_folder_create(self, path):
        t = timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_text_file, 'a') as L:
            L.write(f"Created: {path} --- [{t}]\n")
            L.write("\n")

    # logs the renaming of files, old name and new name
    def on_rename(self, id, old_name, new_name):
        t = timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_text_file, 'a') as L:
            L.write(f"Renamed: {old_name} to {new_name} --- call id: {id} --- [{t}]\n")
            L.write("\n")

    # incase of a specific loggin event (errors and the like)
    def other(self, text):
        t = timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_text_file, 'a') as L:
            L.write(f"{text} --- [{t}]\n")
            L.write("\n")



