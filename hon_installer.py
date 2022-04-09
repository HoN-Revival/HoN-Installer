import gdown
import os
from packaging import version
import shutil
import tkinter as tk
import zipfile

HON_64_PATH = 'C:\Program Files\Heroes of Newerth x64'
HON_32_PATH = 'C:\Program Files (x86)\Heroes of Newerth'

GDRIVE_32_BIT_ID = '1xTq9CLaZpuunZU3Dr3MtpU8gUwEnSI15'
GDRIVE_64_BIT_ID = '16CUMIiT-U1JJfmXSNl7UFPNSe0ZcvW-y'

architecture_options = [
    "32-Bit (i686)",
    "64-Bit (x86_64)",
]

def download(architecture):
  gdrive_id = GDRIVE_32_BIT_ID if architecture == architecture_options[0] else GDRIVE_64_BIT_ID
  return gdown.download_folder(id=gdrive_id)

def extract_all(architecture):
  print('Unzipping files...', flush=True)
  filenames = os.listdir(architecture)
  root_path = os.path.join(os.getcwd(), architecture)
  for filename in filenames:
    path = os.path.join(root_path, filename)
    print(path, flush=True)
    with zipfile.ZipFile(path) as zf:
      zf.extractall(root_path)
    os.remove(path)
  
  for root, dirs, files in os.walk(root_path):
    for name in files:
      file_path = os.path.join(root, name)
      if not file_path.endswith('.zip'):
        continue
      print(file_path, flush=True)
      with zipfile.ZipFile(file_path) as zf:
        zf.extractall(root)
      os.remove(file_path)
  print('Unzipping complete', flush=True)

def copy_files(architecture, path, target_version):
  print('Copying files to: ' + path, flush=True)
  root_path = os.path.join(os.getcwd(), architecture)
  for dir_name in sorted(os.listdir(root_path), key=lambda x: [int(i) if i.isdigit() else i for i in x.split('.')]):
    if version.parse(dir_name) <= version.parse(target_version):
      dir_path = os.path.join(root_path, dir_name)
      print('>> Copying version: ' + dir_name, flush=True)
      for root, dirs, files in os.walk(dir_path):
        for file in files:
          rel_dir = os.path.relpath(root, dir_path)
          target_path = os.path.join(path, rel_dir)
          if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)
          target_file = os.path.join(root, file)
          print('Copying: ' + target_file + ' to ' + target_path, flush=True)
          shutil.copy(target_file, target_path)
      shutil.rmtree(dir_path)
          
  print('Copying complete', flush=True)

def zipdir(path, zf):
  cwd = os.getcwd()
  os.chdir(path)
  for root, dirs, files in os.walk('.'):
    for file in files:
      zf.write(os.path.join(root, file), 
               os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
  os.chdir(cwd)

def archive_files(path):
  processed = []
  cwd = os.getcwd()
  for root, dirs, files in os.walk(path):
    for dir in dirs:
      dir_path = os.path.join(root, dir)
      if not dir_path.endswith('.s2z'):
        continue
      if dir_path in processed:
        continue
      split = os.path.split(dir_path)
      parent_dir = split[0]
      dir_name = split[1]
      os.chdir(parent_dir)
      processed.append(dir_path)
      print(f'Zipping {os.path.split(parent_dir)[1] + "/" + dir_name}', flush=True)
      with zipfile.ZipFile(dir_name + '.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
        zipdir(dir_name, zf)
        shutil.rmtree(dir_name)
      os.rename(dir_name + '.zip', dir_name)  
  os.chdir(cwd)
  print('\nArchiving complete', flush=True)

def install(architecture, target_version, path):
  print('\n\n==================== Downloading files ====================', flush=True)
  download(architecture)
  print('\n\n==================== Extracting files ====================', flush=True)
  extract_all(architecture)
  print('\n\n==================== Installing files ====================', flush=True)
  copy_files(architecture, path, target_version)
  print('\n\n==================== Archiving files ====================', flush=True)
  archive_files(path)
  print('\n\n===========================================================', flush=True)
  print('==================== Install Complete! ====================', flush=True)
  print('===========================================================', flush=True)


 
versions_32 = [
    "0.3.3",
    "1.0.0.1",
    "1.0.1",
    "1.0.2",
    "1.0.3",
    "1.0.4",
    "1.0.5",
    "1.0.6",
    "1.0.7",
    "1.0.8",
    "1.0.9",
    "1.0.10",
    "1.0.11",
    "1.0.12",
    "1.0.12.1",
    "1.0.13",
    "1.0.13.1",
    "1.0.14",
    "1.0.16",
    "1.0.17",
    "1.0.18",
    "1.0.19",
    "1.0.19.1",
    "1.0.20",
    "2.0.0.1",
    "2.0.1",
    "2.0.2",
    "2.0.3"
]

versions_64 = [
    "4.9.0",
    "4.9.2.1",
    "4.9.3",
    "4.9.3.1",
    "4.9.4",
    "4.9.5",
    "4.10.0",
    "4.10.0.1"
] 

versions_drop_down = None
target_version = None

def architecture_changed(*args):
  if (args[0] == target_version.get()):
    return
  target_version.set('')
  versions_drop_down['menu'].delete(0, 'end')
  update_options = versions_32 if args[0] == architecture_options[0] else versions_64
  for option in update_options:
    versions_drop_down['menu'].add_command(label=option, command=tk._setit(target_version, option))
  target_version.set(update_options[-1])
  
  if install_path.get() == HON_32_PATH or install_path.get() == HON_64_PATH:
    updated_path = HON_32_PATH if args[0] == architecture_options[0] else HON_64_PATH
    install_path.set(updated_path)

window = tk.Tk()
window.title("HoN Installer")
window.geometry( "400x200" )

tk.Button(window, text="Exit", command=lambda: terminate())

# Archeticture selection
architecture_label = tk.Label(text="Select your architecture:")
architecture_label.pack()

# datatype of menu text
architecture = tk.StringVar()
  
# initial menu text
architecture.set(architecture_options[1])

# Create Dropdown menu
architecture_drop_down = tk.OptionMenu( window , architecture , *architecture_options, command=architecture_changed)
architecture_drop_down.pack()

# Version selection
version_label = tk.Label(text="Select your target version:")
version_label.pack()

# datatype of menu text
target_version = tk.StringVar()
target_version.set(versions_64[-1])

# Create Dropdown menu
versions_drop_down = tk.OptionMenu( window , target_version , *versions_64)
versions_drop_down.pack()

# Path
install_path_label = tk.Label(text="Select the install directory:")
install_path_label.pack()

install_path = tk.StringVar()
install_path.set(HON_64_PATH)
install_path_entry = tk.Entry(window, width=50, textvariable=install_path)
install_path_entry.pack()

install_button = tk.Button(text="Install", command=lambda: install(architecture.get(), target_version.get(), install_path.get()))
install_button.pack()

window.mainloop()