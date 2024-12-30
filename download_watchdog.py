import threading
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from sorting import folder_path, create_folder, check_all_files, sort_it

# if the flag is true the program will start sorting the files in the folder
start_real_work_flag = False
debounce_timer = None
debounce_time = 2

# calls the functions (check_all_files, get_folder_ncreate_folders) in order
def order_of_opreation():
    global start_real_work_flag
    stray_file_flag, foldernames = check_all_files()
    # only create folders if there are stray files
    if stray_file_flag:
        create_folder(foldernames)
        stray_file_flag = not stray_file_flag
        start_real_work_flag = True

# calls sort_it to start the sorting process
def start_sort():
    global start_real_work_flag
    sort_it()
    start_real_work_flag = False

# watchdog event handler
class WatchHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        global start_real_work_flag
    
    def debounce_timer(self):
        global debounce_timer
        if debounce_timer:
            debounce_timer.cancel()  # Reset timer if event fires again
        # Start a new debounce timer
        debounce_timer = threading.Timer(debounce_time, self.start_sort_on_timer)
        debounce_timer.start()
    def start_sort_on_timer(self):
        order_of_opreation()
        if start_real_work_flag:
            start_sort()
    def on_created(self, event):
        self.debounce_timer()
    def on_moved(self, event):
        self.debounce_timer()
    def on_deleted(self, event):
        self.debounce_timer()

# starts an initial check and sort of the files in the folder
def before_start():
   order_of_opreation()
   if start_real_work_flag:
       start_sort()

# starts the watchdog observer and watches the folder for changes
def start_watching():
    event_handler = WatchHandler()
    watch = Observer()
    watch.schedule(event_handler, folder_path, recursive=False)
    watch.start()

    try:
        watch.join()
    except KeyboardInterrupt:
        watch.stop()

# starts all process in order (before_start, start_watching) and inisializes the watching thread
def run():
    before_start()
    watching_thread = threading.Thread(target=start_watching, daemon=True)
    watching_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        exit()