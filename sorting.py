import os
import pathlib as Path
import fnmatch as Match
import shutil
import logging_sort

# target folder path
folder_path = Path.Path.home() / 'downloads'

# important lists
foldernames = []
extension_list = []
stray_file_list = []

# changes the target folder path
def change_folder_path(new_path):
    global folder_path
    if Path.Path.exists(new_path):
        folder_path = new_path
    else:
        pass

# makes an instance of the logging class
log = logging_sort.logs(folder_path)

# makes the script account for special files
def special_condition(flag: bool = False ,video_extentions:list = None, image_extensions:list = None,
                         doc_extensions:list = None, audio_extensions:list = None, compressed_extensions:list = None):
    global conditions_extensions
    global condition_folder_names
    global condition_flags

    video_extention_list = video_extentions
    image_extension_list = image_extensions
    doc_extension_list = doc_extensions
    audio_extension_list = audio_extensions
    compressed_extensions_list = compressed_extensions
    
    # incase there is a need to add more special files
    #add them to the list, and make sure the index is the same in all three lists
    conditions_extensions = [image_extension_list, video_extention_list, doc_extension_list, audio_extension_list
                             , compressed_extensions_list]
    condition_folder_names = ["Image_files","Video_files","documents","audio_files","compressed_files"]
    condition_flags = [False, False, False, False, False]

# checks all the files in the target folder, and creates a list of stray files and folder names
def check_all_files():
    log.call_to_check_all(folder_path)
    global foldernames
    global stray_file_list
    global conditions_extensions
    global condition_folder_names

    foldernames = []
    extension_list = []
    stray_file_flag = False

    for file in os.listdir(folder_path):
        flag = True
        filename, extension = os.path.splitext(file)
        if extension != '':
            stray_file_list.append(f"{filename}{extension}")
            for index, condition in enumerate(conditions_extensions):
                if extension in condition:
                    extension_list.append(condition_folder_names[index])
                    condition_flags[index] = True
                    flag = False
            if flag:
                extension = extension.split('.')
                extension_list.append(extension[-1])
    foldernames = list(set(extension_list))
    if len(stray_file_list) > 0:
        stray_file_flag = True
    log.stary_files_logs(stray_file_list)
    return stray_file_flag, foldernames

# creates the necessary folders in the target folder
def create_folder(folder_names: list = None):
    if folder_names == None:
        global foldernames
        folder_names = foldernames
    global folder_path

    for name in folder_names:
        new_path = folder_path / name
        new_path.mkdir(exist_ok=True)
        log.on_folder_create(new_path)

# renames and moves the files to the appropriate folders in case of a name conflict
def rename(call_id, file, name):

    filename, extension = os.path.splitext(file)
    number = 1

    # numbers till it finds a name that doesn't exist
    try:
        while f'{filename}_{number}{extension}' in os.listdir(folder_path/name):
            if f'{filename}_{number}{extension}' in os.listdir(folder_path):
                number = number + 1
                continue
            number = number + 1
    except (FileExistsError, FileNotFoundError):
        log.other(f"RENAME_ERROR: FileExistsError/FileNotFoundError: {folder_path/name}")
        return
    
    new_name = f"{filename}_{number}{extension}"
    old_name = folder_path / file
    renamed = folder_path / new_name

    # if the file exists, it commits the rename and moves the file
    if old_name.exists():
        log.on_rename(31, old_name, new_name)
        old_name.rename(renamed)
        try:
            shutil.move(str(renamed), str(folder_path / name))
            log.on_move(21, renamed, (folder_path / name))
        except (shutil.Error, FileNotFoundError, FileExistsError):
            log.other(f"MOVE_ERROR in rename: file: {renamed}")
    else:
        log.other(f"Rename: File not found: {old_name} --- call id: {call_id}")

# sorts special files into their respective folders
def sort_condition(file):
    global foldernames
    global conditions_extensions
   
    filename, extention = os.path.splitext(file)
    folder_names = condition_folder_names
    # goes through the list of condition lists
    for index, condition in enumerate(conditions_extensions):
        # checks if the list is not empty and if the files extension is in the list
        if condition and extention in condition:
            # checks if the file already exists in the folder and calls rename if it does
            if Path.Path.exists(folder_path / folder_names[index] / file) and Path.Path.exists(folder_path / file):
                rename(11, file, folder_names[index])
            # moves the file to it's respective folder
            else:
                try:
                    shutil.move(os.path.join(folder_path, file), folder_path / folder_names[index])
                    path = str(folder_path/file)
                    log.on_move(22, path, (folder_path / folder_names[index]))
                except (shutil.Error, FileNotFoundError, FileExistsError):
                    log.other(f"Exception raised: sort_condition: file: {file}")
                    pass
            return

# sorts all the files in the target folder
def sort_it():
    global foldernames
    global stray_file_list

    # goes through the list of stray files
    for file in stray_file_list:
    
        # checks if it needs to account for special files
        if is_special(file):
            sort_condition(file)
            continue
        
        # goes through the list of folder names
        for name in foldernames:
            
            # checks if the file has an extension that matches the folder name
            if Match.fnmatch(file, f'*.{name}') and Path.Path.exists(folder_path / name):
                # checks if the file already exists in the folder and calls rename if it does
                if Path.Path.exists(folder_path / name / file) and Path.Path.exists(folder_path / file):
                    rename(12, file, name)
                # moves the file to it's respective folder
                else:
                    try:
                        shutil.move(os.path.join(folder_path, file), folder_path / name)
                        path = str(folder_path/file)
                        log.on_move(23, path, (folder_path / name))
                    except (shutil.Error, FileNotFoundError, FileExistsError):
                        log.other(f"Exception raised: sort_it: file: {file}")
                        pass
                break
    stray_file_list = []

# checks if the file is part of the exceptions
def is_special(file):
    ext = file.split('.')[-1].lower()
    for condition in conditions_extensions:
        if "."+ext in condition:
            return True
    return False

# one time sort
if __name__ == "__main__":
    videos = [".mp4",".mkv"]
    images = [".png",".jpg",".jpeg",".webp"]
    documents = [".docx",".doc",".pdf",".ppt",".pptx",".txt"]
    audios = [".mp3",".flac"]
    compressed_files = [".rar",".xz",".zip",".tar",".7z"]
    account_for_special_files = True
    special_condition(flag= account_for_special_files, video_extentions= videos, image_extensions= images,
                doc_extensions= documents,audio_extensions= audios, compressed_extensions= compressed_files)
    check_all_files()
    create_folder()
    sort_it()
