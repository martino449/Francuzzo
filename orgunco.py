import random
import re
from datetime import datetime
import os
import shutil
import json
from datetime import datetime
language = "it"
from config import destinations, patterns


import os
import shutil

class FileOrganizer:
    def __init__(self, source_folder=None):
        if source_folder is None:
            self.source_folder = self.get_source_folder()
        else:
            self.source_folder = source_folder

        self.destinations = destinations

    def get_source_folder(self):
        current_dir = os.getcwd()
        return current_dir

    def create_destination_folders(self, folders):
        for folder in folders:
            folder_path = os.path.join(self.source_folder, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def move_file(self, filename, folder):
        file_path = os.path.join(self.source_folder, filename)
        destination_path = os.path.join(self.source_folder, folder, filename)
        shutil.move(file_path, destination_path)
        print(f"Moved: {filename} -> {folder}")
        log_action(f"Moved file: {filename} to {folder}")

    def organize_by_name_pattern(self):
        if not os.path.exists(self.source_folder):
            print(f"The folder {self.source_folder} does not exist.")
            return
        self.create_destination_folders(patterns.values())
        for filename in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, filename)
            if os.path.isdir(file_path):
                continue
            for pattern, folder in patterns.items():
                if pattern in filename:
                    self.move_file(filename, folder)
                    break

    def organize(self):
        if not os.path.exists(self.source_folder):
            print(f"The folder {self.source_folder} does not exist.")
            return
        self.create_destination_folders(self.destinations.keys())
        for filename in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, filename)
            if os.path.isdir(file_path):
                continue
            _, extension = os.path.splitext(filename)
            for folder, extensions in self.destinations.items():
                if extension.lower() in extensions:
                    self.move_file(filename, folder)
                    break








#Fine del codice
# ---------------------------------------------
# Copyright (c) 2024 Mario Pisano
#
# Questo programma è distribuito sotto la licenza EUPL, Versione 1.2 o – non appena 
# saranno approvate dalla Commissione Europea – versioni successive della EUPL 
# (la "Licenza");
# Puoi usare, modificare e/o ridistribuire il programma sotto i termini della 
# Licenza. 
# 
# Puoi trovare una copia della Licenza all'indirizzo:
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
