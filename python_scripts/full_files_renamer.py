#!/usr/bin/env python3
import os 
import datetime 

folder_path = "directory" 
if not os.path.exists(folder_path):
    print(f"Dir {folder_path} not found.")
    exit()

for filename in os.listdir(folder_path): 
    old_path = os.path.join(folder_path, filename) 
    if os.path.isfile(old_path):  
        file_name, file_ext = os.path.splitext(filename) 
        date_str = datetime.datetime.now().strftime("%Y-%m-%d") 
        new_name = f"{file_name.replace(' ', '_')}_{date_str}{file_ext}" 
        new_path = os.path.join(folder_path, new_name) 
        try:
            os.rename(old_path, new_path)
        except Exception as e:
            print(f"Errow while renaming {filename}: {e}")
