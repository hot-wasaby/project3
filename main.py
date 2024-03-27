import os
import datetime
import threading
import time

class File:
    def __init__(self, name, extension, created_time, updated_time):
        self.name = name
        self.extension = extension
        self.created_time = created_time
        self.updated_time = updated_time

    def __eq__(self, other):
        return isinstance(other, File) and self.name == other.name

class TextFile(File):
    def __init__(self, name, extension, created_time, updated_time, line_count, word_count, char_count):
        super().__init__(name, extension, created_time, updated_time)
        self.line_count = line_count
        self.word_count = word_count
        self.char_count = char_count

class ImageFile(File):
    def __init__(self, name, extension, created_time, updated_time, image_size):
        super().__init__(name, extension, created_time, updated_time)
        self.image_size = image_size

class ProgramFile(File):
    def __init__(self, name, extension, created_time, updated_time, line_count, class_count, method_count):
        super().__init__(name, extension, created_time, updated_time)
        self.line_count = line_count
        self.class_count = class_count
        self.method_count = method_count

class FolderMonitor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.files = self.scan_folder()
        self.snapshot_time = datetime.datetime.now()  # Initial snapshot time
        self.last_commit_time = datetime.datetime.now()  # Initialize last commit time
        self.log_file = "Log.txt"
        self.create_log_file_if_not_exists()

    def scan_folder(self):
        files = []
        for filename in os.listdir(self.folder_path):
            filepath = os.path.join(self.folder_path, filename)
            if os.path.isfile(filepath):
                created_time = datetime.datetime.fromtimestamp(os.path.getctime(filepath))
                updated_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
                if filename.endswith('.txt'):
                    with open(filepath, 'r') as f:
                        line_count = sum(1 for line in f)
                        f.seek(0)
                        word_count = sum(len(line.split()) for line in f)
                        f.seek(0)
                        char_count = sum(len(line) for line in f)
                    files.append(TextFile(filename, 'txt', created_time, updated_time, line_count, word_count, char_count))
                elif filename.endswith(('.jpg', '.png')):
                    image_size = os.path.getsize(filepath)
                    files.append(ImageFile(filename, filename.split('.')[-1], created_time, updated_time, image_size))
                elif filename.endswith(('.py', '.java')):
                    with open(filepath, 'r') as f:
                        line_count = sum(1 for line in f)
                        f.seek(0)
                        class_count = sum(1 for line in f if 'class ' in line)
                        f.seek(0)
                        method_count = sum(1 for line in f if 'def ' in line)
                    files.append(ProgramFile(filename, filename.split('.')[-1], created_time, updated_time, line_count, class_count, method_count))
        return files

    def detect_changes(self):
        while True:
            time.sleep(5)  # Check every 5 seconds
            current_time = datetime.datetime.now()
            if (current_time - self.snapshot_time).total_seconds() > 5:  # Change detection since the last snapshot
                current_files = self.scan_folder()
                added_files = [file for file in current_files if file not in self.files]
                deleted_files = [file for file in self.files if file not in current_files]
                for file in current_files:
                    old_file = next((f for f in self.files if f == file), None)
                    if old_file and file.updated_time > old_file.updated_time:
                        if file.name != self.log_file:  # Skip logging if the file is the log file
                            message = f"File '{file.name}' changed."
                            print(message)
                            self.log_event(message)
                for file in added_files:
                    if file.name != self.log_file:  # Skip logging if the file is the log file
                        message = f"File '{file.name}' added."
                        print(message)
                        self.log_event(message)
                for file in deleted_files:
                    if file.name != self.log_file:  # Skip logging if the file is the log file
                        message = f"File '{file.name}' deleted."
                        print(message)
                        self.log_event(message)
                self.files = current_files
                self.snapshot_time = current_time  # Update snapshot time

    def log_event(self, message):
        with open(self.log_file, "a") as log:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log.write(f"[{timestamp}] {message}\n")

    def create_log_file_if_not_exists(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as log:
                pass  # Creates an empty log file if it doesn't exist

    def find_file(self, filename):
        for file in self.files:
            if file.name.lower() == filename.lower():
                return file
        return None

    def print_status(self):
        if self.last_commit_time:
            print(f"Last commit time: {self.last_commit_time}")
            print("Changes since last commit:")
            for file in self.files:
                status = "changed" if file.updated_time > self.last_commit_time else "no changes"
                print(f"{file.name} - {status}")
        else:
            print("No commits have been made yet.")

    def commit_snapshot(self):
        snapshot_time = datetime.datetime.now()

        current_files = self.scan_folder()

        added_files = [file for file in current_files if file not in self.files]
        deleted_files = [file for file in self.files if file not in current_files]
        changed_files = [file for file in current_files if file in self.files and file.updated_time > self.last_commit_time]

        with open(self.log_file, "a") as log:
            log.write(f"Snapshot time: {snapshot_time}\n")
            log.write("Added files:\n")
            for file in added_files:
                log.write(f"{file.name} - {file.updated_time}\n")
            log.write("Deleted files:\n")
            for file in deleted_files:
                log.write(f"{file.name} - {file.updated_time}\n")
            log.write("Changed files:\n")
            for file in changed_files:
                log.write(f"{file.name} - {file.updated_time}\n")

        self.files = current_files
        self.last_commit_time = snapshot_time

if __name__ == "__main__":
    folder_path = "C:\\Users\\pc\\Desktop\\project3"
    folder_monitor = FolderMonitor(folder_path)

    change_detection_thread = threading.Thread(target=folder_monitor.detect_changes)
    change_detection_thread.daemon = True
    change_detection_thread.start()

    while True:
        print("input one of comands : commit, info filename , status")
        command = input(">")
        if command == "commit":
            folder_monitor.commit_snapshot()
            print("Snapshot updated.")
        elif command.startswith("info"):
            filename = command.split()[1]
            file = folder_monitor.find_file(filename)
            if file:
                print(f"File: {file.name}")
                print(f"Extension: {file.extension}")
                print(f"Created Time: {file.created_time}")
                print(f"Updated Time: {file.updated_time}")
                if isinstance(file, TextFile):
                    print(f"Line Count: {file.line_count}")
                    print(f"Word Count: {file.word_count}")
                    print(f"Character Count: {file.char_count}")
                elif isinstance(file, ProgramFile):
                    print(f"Line Count: {file.line_count}")
                    print(f"Class Count: {file.class_count}")
                    print(f"Method Count: {file.method_count}")
                elif isinstance(file, ImageFile):
                    print(f"Image Size: {file.image_size}")
            else:
                print("File not found.")
        elif command == "status":
            folder_monitor.print_status()
        elif command == "exit":
            break

