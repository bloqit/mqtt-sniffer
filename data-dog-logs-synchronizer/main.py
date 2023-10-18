from logger import Logger
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

log_dir = "logs"
app_log_file = 'synchronizer_log_file.json'

logger = Logger("logger", log_dir, app_log_file, 15, 1)

class BackupLogFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            # sniffer_log_file.json.1 is always the latest backup file
            file_to_sync = "sniffer_log_file.json.1"
            if os.path.isfile(os.path.join(log_dir, file_to_sync)):
                logger.info(f"Syncing file {file_to_sync} ...")

                logger.info(f"File {file_to_sync} has been synced.")

if __name__ == "__main__":
    # Log
    logger.info("Application has been started.")
    logger.info(f"Watching {log_dir} folder ...")

    event_handler = BackupLogFileHandler()

    observer = Observer()
    observer.schedule(event_handler, path=log_dir, recursive=False)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    logger.info("Application has been stopped.")
    