import os
from app.config import UPLOAD_DIRECTORY
file_name = "Group 419.png"
file_names = os.listdir(UPLOAD_DIRECTORY)
files = dict()
for f in file_names:
    files[f] = os.path.getsize(f"{UPLOAD_DIRECTORY}/{f}")

if file_name in files:
    print("yes")
if ".stl" in file_name.lower():
    print("yes")
print(files)