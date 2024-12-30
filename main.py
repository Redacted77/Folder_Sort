import pathlib as Path
from download_watchdog import run
from sorting import change_folder_path, special_condition

# default path = Path.Path.home() / 'Downloads'
folder_path = Path.Path.home() / 'Downloads'

# special files
videos = [".mp4",".mkv"]
images = [".png",".jpg",".jpeg",".webp"]
documents = [".docx",".doc",".pdf",".ppt",".pptx",".txt"]
audios = [".mp3",".flac"]
compressed_files = [".rar",".xz",".zip",".tar",".7z"]
account_for_special_files = True
change_folder_path(folder_path)
special_condition(flag= account_for_special_files, video_extentions= videos, image_extensions= images,
                   doc_extensions= documents,audio_extensions= audios, compressed_extensions= compressed_files)

# start the script
run()