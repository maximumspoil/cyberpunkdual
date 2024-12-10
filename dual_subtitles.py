import os
import shutil
import subprocess
import chardet
import json

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

base_language_combo = None
target_language_combo = None
folder_entry = None

# Wrapper function to replace subprocess.run()
def run_with_redirect(*args, **kwargs):
    # Capture the output of subprocess
    result = subprocess.run(*args, **kwargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Redirect the captured output to stdout and stderr
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)

    return result

def detect_encoding(source_file):
    # Read a sample of the file to detect the encoding
    with open(source_file, 'rb') as raw_file:
        raw_data = raw_file.read(4096)  # Reads the first 4 KB of the file

    # Detect encoding
    detected_encoding = chardet.detect(raw_data)['encoding']
    print("File :" + source_file)
    print("Encoding: " + detected_encoding) 
    return detected_encoding;

# Create a function to redirect the print output to the Text widget
def redirect_output(text_widget, window):
    class CustomStream:
        def __init__(self, text_widget, window):
            self.text_widget = text_widget
            self.window = window

        def write(self, text):
            self.text_widget.insert(tk.END, text)
            self.text_widget.see(tk.END)  # Auto-scroll to the end
            self.window.update()  # Force widget update

        def flush(self):
            pass

    sys.stdout = CustomStream(text_widget, window)
    sys.stderr = CustomStream(text_widget, window)  # Redirect stderr as well

def apply():
    global base_language_combo
    global target_language_combo
    global folder_entry
    global folder2_entry
    # Get selected values from comboboxes
    base_language = base_language_combo.get()
    target_language = target_language_combo.get()
    selected_folder = folder_entry.get()
    kit_folder = folder2_entry.get()

    # Perform your actions with the selected values

    process_files(target_language, base_language, selected_folder, kit_folder)
    print("Modified Language:", base_language)
    print("Translation Language (added):", target_language)
    print("Selected Folder:", selected_folder)
    print("Selected Wolvenkit Folder:", kit_folder)
    print("--- DONE !       ---")
    print("--- You can exit ---")
    print("To restore defaults, use the same source and base languages.")
    
def open_ui_dialog():
    global base_language_combo
    global target_language_combo
    global folder_entry
    global folder2_entry
    global progress_bar
    # Create the main dialog window
    window = tk.Tk()
    window.title("Cyberpunk 2077 Dual Subtitles Mod")
    window.configure(bg="light green")
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
      
 
    top_label = tk.Label(window, text="Language to Translate -> Translation Language")
    top_label.grid(row=0, column=0, columnspan=2)
    
    # Create combobox for Base Language
    base_language_combo = ttk.Combobox(window, values=["ar", "br", "cn", "cz", "de", "en", "enpc", "es", "esmx", "fr", "hu", "it", "pl", "ru", "plpc", "tr", "zh"])
    base_language_combo.set("pl")
    base_language_combo.grid(row=1, column=0)

    # Create combobox for Target Language
    target_language_combo = ttk.Combobox(window, values=["ar", "br", "cn", "cz", "de", "en", "enpc", "es", "esmx", "fr", "hu", "it", "pl", "ru", "plpc", "tr", "zh"])
    target_language_combo.set("fr")
    target_language_combo.grid(row=1, column=1)

    # Create a button to open a folder selection dialog
    def select_folder():
        folder_path = filedialog.askdirectory()
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

    # Create a button to open a folder selection dialog
    def select_folder2():
        folder_path2 = filedialog.askdirectory()
        folder2_entry.delete(0, tk.END)
        folder2_entry.insert(0, folder_path2)

    folder_button = tk.Button(window, text="Select Game Folder", command=select_folder)
    folder_button.grid(row=2, column=0)

    folder2_button = tk.Button(window, text="Select WolvenKit.Console Folder", command=select_folder2)
    folder2_button.grid(row=3, column=0)
  

    # Create an editable textbox for selected folder
    folder_entry = tk.Entry(window)
    folder_entry.insert(0, r"E:\SteamLibrary\steamapps\common\Cyberpunk 2077")
    folder_entry.grid(row=2, column=1)

    folder2_entry = tk.Entry(window)
    folder2_entry.insert(0, r"C:\Users\kurza\Downloads\WolvenKit")
    folder2_entry.grid(row=3, column=1)

    # Create an Apply button to call the apply() function
    apply_button = tk.Button(window, text="Apply", command=apply)
    apply_button.grid(row=4, column=0, columnspan=2)

    # Create a label with a link to your YouTube channel
    youtube_label = tk.Label(window, text="Check out my YouTube channel:")
    youtube_label.grid(row=5, column=0, columnspan=2)

    youtube_link = tk.Label(window, text="https://www.youtube.com/@maximumspoil2500", fg="blue", cursor="hand2")
    youtube_link.grid(row=6, column=0, columnspan=2)
    youtube_link.bind("<Button-1>", lambda e: window.clipboard_append("https://www.youtube.com/@maximumspoil2500"))

    progress_bar = ttk.Progressbar(window, orient="horizontal", length=200, mode="indeterminate")
    progress_bar.grid(row=7, column=0, columnspan=2)
    progress_bar["value"] = 0  # Reset to zero after loading
    
    # Create a Text widget to display console output
    output_text = tk.Text(window, wrap=tk.WORD, height=20, width=60)
    output_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    # Redirect print output to the Text widget
    redirect_output(output_text, window)

     # Calculate the window position for centering
    window_width = 500  # Change this to the desired window width
    window_height = 500  # Change this to the desired window height
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the window's geometry to center it on the screen
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Start the GUI main loop
    window.mainloop()

def merge_content(source_file, target_file, should_merge):
    # Read the source file
    
    enc = detect_encoding(source_file);
    with open(source_file, "r", encoding="utf-8") as source:
        source_lines = source.readlines()
    
    enc = detect_encoding(target_file);
    # Read the target file
    with open(target_file, "r", encoding="utf-8") as target:
        target_lines = target.readlines()
    
    # Create a dictionary to store the source lines
    source_dict = {}
    for line in source_lines:
        line_parts = line.split("||")
        line_parts2 = line.split("|")
        if (len(line_parts2) > 0):
            key = line_parts2[0].strip()
            if (len(line_parts) > 1):
                value = line_parts[1].strip()
                source_dict[key] = value
    
    # Merge content into the target lines
    merged_lines = []
    for line in target_lines:
        line_parts = line.split("||")
        line_parts2 = line.split("|")
        merged_line = line
        if (len(line_parts2) > 0 and should_merge):
            key = line_parts2[0].strip()
            key_uns = line_parts2[0]
            if (len(line_parts) > 1):
                value = line_parts[1].strip()
                
                if key in source_dict:
                    delim = " ~ "
                    if (len(value) > 20):
                        delim = "<br>~ "
                    merged_value = value + delim + source_dict[key] 
                    merged_line = f"{key_uns}|{line_parts2[1]}||{merged_value}\n"
            
        merged_lines.append(merged_line)
    
    return merged_lines

def merge_json_translations_with_separator(folder1: str, folder2: str):
    """
    Merges translations from JSON files in folder2 into JSON files in folder1,
    separating content from both files with the given separator.
    
    Args:
        folder1 (str): Path to the first folder containing JSON files.
        folder2 (str): Path to the second folder containing JSON files.
        separator (str): String used to separate content from the two files.
    """

    sep1 = " \\n"
    sep2 = ""

    for filename in os.listdir(folder1):
        if filename.endswith(".json.json"):
            file1_path = os.path.join(folder1, filename)
            file2_path = os.path.join(folder2, filename)
            
            # Ensure the corresponding file exists in the second folder
            if not os.path.exists(file2_path):
                print(f"Matching file not found for {filename} in {folder2}")
                continue
            
            # Load both JSON files
            with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
                json1 = json.load(file1)
                json2 = json.load(file2)
            
            # Extract entries from both files
            entries1 = json1["Data"]["RootChunk"]["root"]["Data"]["entries"]
            entries2 = json2["Data"]["RootChunk"]["root"]["Data"]["entries"]
            
            # Create a mapping for quick access to entries in the second file
            entries2_map = {}
            for entry in entries2:
                # First check primaryKey and secondaryKey
                primary_key = entry.get("primaryKey", "")
                secondary_key = entry.get("secondaryKey", "")
                key = (primary_key, secondary_key or None)
                
                # If no primary or secondary key, fall back to stringId
                if "stringId" in entry:
                    entries2_map[entry["stringId"]] = entry
                else:
                    entries2_map[key] = entry
            
            # Merge translations from file2 into file1 with separator
            for entry1 in entries1:
                # Determine the key for lookup
                primary_key = entry1.get("primaryKey", "")
                secondary_key = entry1.get("secondaryKey", "")
                string_id = entry1.get("stringId", None)
                
                # Key lookup in the map, first try primaryKey + secondaryKey, then fall back to stringId
                key = (primary_key, secondary_key or None)
                if string_id and string_id in entries2_map:
                    entry2 = entries2_map[string_id]
                elif key in entries2_map:
                    entry2 = entries2_map[key]
                else:
                    continue
                
                # Merge translations for femaleVariant and maleVariant
                # Combine femaleVariant if it exists in entry1
                if "femaleVariant" in entry1 and entry1["femaleVariant"]:
                    translation1 = entry1["femaleVariant"]
                    translation2 = entry2.get("femaleVariant", "")
                    if translation2 == "":
                        translation2 = entry2.get("maleVariant", "")

                    if (translation1 != translation2):
                        entry1["femaleVariant"] = f"{translation1}{sep1}{translation2}{sep2}"
                    else:
                        entry1["femaleVariant"] = f"{translation1}"
                
                # Combine maleVariant if it exists in entry1
                if "maleVariant" in entry1 and entry1["maleVariant"]:
                    translation1 = entry1["maleVariant"]
                    translation2 = entry2.get("maleVariant", "")
                    if translation2 == "":
                        translation2 = entry2.get("femaleVariant", "")

                    if (translation1 != translation2):
                        entry1["maleVariant"] = f"{translation1}{sep1}{translation2}{sep2}"
                    else:
                        entry1["maleVariant"] = f"{translation1}"
            
            # Write the updated JSON back to the file in folder1
            with open(file1_path, 'w', encoding='utf-8') as file1:
                json.dump(json1, file1, ensure_ascii=False, indent=2)
            
            print(f"Merged translations for {filename}")

def move_and_override_files(src_folder: str):
    """
    Moves files from the given folder into subfolders within a 'base' subfolder, 
    overriding files with the same name.

    Args:
        src_folder (str): Path to the source folder containing files and the 'base' subfolder.
    """
    # Define the base subfolder path
    base_folder = os.path.join(src_folder, "base")
    
    # Ensure the base folder exists
    if not os.path.exists(base_folder):
        print(f"'base' folder not found in {src_folder}.")
        return
    
    # Iterate over files in the source folder
    for item in os.listdir(src_folder):
        item_path = os.path.join(src_folder, item)
        
        # Skip the base folder and non-files
        if item == "base" or not os.path.isfile(item_path):
            continue
        
        # Search for matching files in subfolders of the base folder
        for root, _, files in os.walk(base_folder):
            if item in files:
                target_path = os.path.join(root, item)
                
                # Move and override the file
                shutil.move(item_path, target_path)
                print(f"Moved and overridden: {item_path} -> {target_path}")
                break  # Stop searching once the file is moved
        else:
            print(f"No matching file found for: {item}")

def convert_json_to_cr2w(folder_path, kit_folder):

    print(f"Converting back all .json files in {folder_path} to .json format.")
    exe_path = os.path.join(kit_folder, "WolvenKit.CLI.exe")

    # Create the target converted folder
    converted_folder = folder_path + "_converted"
    if not os.path.exists(converted_folder):
        os.makedirs(converted_folder)
        print(f"Created converted folder: {converted_folder}")
    # Run the WolvenKit CLI command to convert all files in the folder (batch)
    command = [
        exe_path,
        "cr2w",
        "-d", converted_folder,  # Source folder
        "-o", folder_path  # Output folder for the converted files
    ]
    
    try:
        run_with_redirect(command, check=True)
        print(f"Batch conversion completed. Files saved to {converted_folder}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run WolvenKit CLI: {e}")
        return
    except FileNotFoundError:
        print("Error: WolvenKit CLI not found. Ensure it's installed and in your PATH.")
        return

def convert_cr2w_to_json2(folder_path, kit_folder):
    """
    Converts all .json files in a given folder and its subfolders (CR2W format) to .json2 using WolvenKit CLI.
    Creates a target folder 'folder_path_converted', performs batch conversion, 
    and moves the generated files to match the original folder structure.

    Parameters:
    folder_path (str): Path to the folder containing the .json files.
    kit_folder (str): Path to the folder containing WolvenKit.CLI.exe.
    """
    print(f"Converting all .json files in {folder_path} to .json2 format.")
    exe_path = os.path.join(kit_folder, "WolvenKit.CLI.exe")

    # Ensure the folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
        return

    # Create the target converted folder
    converted_folder = folder_path + "_converted"
    if not os.path.exists(converted_folder):
        os.makedirs(converted_folder)
        print(f"Created converted folder: {converted_folder}")
    
    # Run the WolvenKit CLI command to convert all files in the folder (batch)
    command = [
        exe_path,
        "cr2w",
        "-s", folder_path,  # Source folder
        "-o", converted_folder  # Output folder for the converted files
    ]
    
    try:
        run_with_redirect(command, check=True)
        print(f"Batch conversion completed. Files saved to {converted_folder}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run WolvenKit CLI: {e}")
        return
    except FileNotFoundError:
        print("Error: WolvenKit CLI not found. Ensure it's installed and in your PATH.")
        return
    
    print(f"Conversion and file organization complete.")

def extract_archives(source_lang, target_lang, location, content_suffix , kit_folder):
    """
    Extracts the specified language archives for Cyberpunk 2077.

    Args:
        source_lang (str): The language code for the source archive (e.g., 'en', 'ko').
        target_lang (str): The language code for the target archive (e.g., 'ru', 'jp').
        location (str): The root folder of Cyberpunk 2077.

    Returns:
        None
    """
    print(f"Extracting {source_lang} and {target_lang} archives at {location}")

    # Define paths
    archive_dir = os.path.join(location, "archive", "pc", content_suffix)
    extracted_dir = os.path.join(location, "extracted_archives", content_suffix)
    source_output_dir = os.path.join(extracted_dir, f"lang_{source_lang}_text")
    target_output_dir = os.path.join(extracted_dir, f"lang_{target_lang}_text")

    if os.path.exists(extracted_dir):
        shutil.rmtree(extracted_dir)

    # Ensure the archive directory exists
    if not os.path.exists(archive_dir):
        print(f"Error: Archive directory {archive_dir} does not exist.")
        return

    # Ensure the extracted directory exists (create if necessary)
    os.makedirs(extracted_dir, exist_ok=True)

    # Archive file names
    source_archive = f"lang_{source_lang}_text.archive"
    target_archive = f"lang_{target_lang}_text.archive"

    # Full paths to archives
    source_archive_path = os.path.join(archive_dir, source_archive)
    target_archive_path = os.path.join(archive_dir, target_archive)

    # Copy the files to the backup location
    if not os.path.exists(f"{source_archive_path}_backup"):
        shutil.copyfile(source_archive_path, f"{source_archive_path}_backup")
    else:
        shutil.copyfile(f"{source_archive_path}_backup", source_archive_path)

    if not os.path.exists(f"{target_archive_path}_backup"):
        shutil.copyfile(target_archive_path, f"{target_archive_path}_backup")
    else:
        shutil.copyfile(f"{target_archive_path}_backup", target_archive_path)

    exe_path = os.path.join(kit_folder, "WolvenKit.CLI.exe")

    if (source_lang == target_lang):
        return

    # Check if both archives exist
    if not os.path.exists(source_archive_path):
        print(f"Error: Source archive {source_archive} not found in {archive_dir}.")
        return

    if not os.path.exists(target_archive_path):
        print(f"Error: Target archive {target_archive} not found in {archive_dir}.")
        return

    # Check if source archive is already extracted
    if os.path.exists(source_output_dir):
        print(f"Source archive {source_archive} is already extracted in {source_output_dir}. Skipping extraction.")
    else:
        # Extract source archive
        print(f"Extracting {source_archive}... with {exe_path}")
        run_with_redirect([exe_path, "extract", source_archive_path, "-o", source_output_dir], check=True)

    convert_cr2w_to_json2(source_output_dir, kit_folder)

    # Check if target archive is already extracted
    if os.path.exists(target_output_dir):
        print(f"Target archive {target_archive} is already extracted in {target_output_dir}. Skipping extraction.")
    else:
        # Extract target archive
        print(f"Extracting {target_archive}... with {exe_path}")
        run_with_redirect([exe_path, "extract", target_archive_path, "-o", target_output_dir], check=True)
    
    convert_cr2w_to_json2(target_output_dir, kit_folder)

    print(f"Extraction complete. Extracted files are located in {extracted_dir}.")

    merge_json_translations_with_separator(target_output_dir + "_converted", source_output_dir + "_converted")

    convert_json_to_cr2w(target_output_dir, kit_folder)

    move_and_override_files(target_output_dir)

    print(f"Archiving {target_output_dir} into {archive_dir}...")
    run_with_redirect([exe_path, "pack", "-p", target_output_dir, "-o", archive_dir], check=True)



def process_files(source_lang, target_lang, location, kit_folder):
    global progress_bar
    progress_bar.start()
    # Track if the merging process has been done
    should_merge = source_lang != target_lang
    merged = False
    print("Starting " + source_lang + " " + target_lang + " " + location) 

    extract_archives(source_lang, target_lang, location, "content", kit_folder);
    extract_archives(source_lang, target_lang, location, "ep1", kit_folder);

    progress_bar.stop()
   
"""
def parse_localization(file_content):
    pattern = re.compile(r'(\w+)-(\w+-\w+-\w+-\w+).*?[\x0e\x0f]\s+(.*?)\s+', re.DOTALL)
    matches = pattern.findall(file_content)
    
    localization_map = {}
    for match in matches:
        secondary_key = match[1].strip()
        localized_text = match[2].strip()
        localization_map[secondary_key] = localized_text
    return localization_map

def compare_localizations(file1_content, file2_content):

    loc1 = parse_localization(file1_content)
    loc2 = parse_localization(file2_content)

    mapping = {}
    for key in loc1:
        if key in loc2:
            mapping[key] = (loc1[key], loc2[key])  # Pair (File1Text, File2Text)
    return mapping

with open(r"E:\SteamLibrary\steamapps\common\Cyberpunk 2077\extracted_archives\lang_fr_text\base\localization\fr-fr\onscreens\onscreens.json", "r", encoding="latin1") as f1, open(r"E:\SteamLibrary\steamapps\common\Cyberpunk 2077\extracted_archives\lang_pl_text\base\localization\pl-pl\onscreens\onscreens.json", "r", encoding="latin1") as f2:
    file1_content = f1.read()
    file2_content = f2.read()

translations = compare_localizations(file1_content, file2_content)
for key, (text1, text2) in translations.items():
    print(f"{key}:\n  File 1: {text1}\n  File 2: {text2}\n")
"""
"""
def print_file_bytes(filepath, n=6000):

    try:
        with open(filepath, "rb") as f:
            data = f.read(n)
            hex_output = " ".join(f"{byte:02x}" for byte in data)
            print(f"First {n} bytes of the file in hex:")
            print(hex_output)
    except Exception as e:
        print(f"Error reading file: {e}")
# Get command line arguments

"""

"""
# Example usage
file_path =(r"E:\SteamLibrary\steamapps\common\Cyberpunk 2077\extracted_archives\lang_fr_text\base\localization\fr-fr\onscreens\onscreens.json");
 
def parse_binary_locale_file(file_path):
    # Define delimiters
    key_delimiter = b'\x0E\x00\x0D'           # 'SO', 'NUL', 'CR'
    translation_delimiter = b'\x00\x00\x00\x0A'  # 'NUL', 'NUL', 'NUL', 'LF'

    with open(file_path, "rb") as binary_file:
        # Read all binary data
        data = binary_file.read()

    # Split data using the translation delimiter
    sections = data.split(translation_delimiter)

    # Discard the first entry as it's junk
    sections = sections[1:]

    # List to store key-translation pairs
    entries = []

    for section in sections:
        # Split by the key delimiter to separate key and translation
        parts = section.split(key_delimiter)

        if len(parts) >= 2:
            # The last part is the translation
            translation = parts[-1]
            # The part before the last one contains the key and junk
            key_and_junk = parts[-2]

            # Split by CR (0x0D) to remove the junk before the key
            key_parts = key_and_junk.split(b'\x0D')

            # The actual key is the last part after splitting by CR
            key = key_parts[-1]

            # If translation exists, we assume the first two bytes represent the length
            translation_length = 0
            if len(translation) > 1:
                # First byte is the high byte, second byte is the low byte
                translation_length = translation[0] * 256 + translation[1]  # High byte * 256 + Low byte
                translation = translation[2:]  # Remove the length bytes from the translation data

            # Decode the translation, handle any non-UTF-8 characters gracefully
            translation_decoded = translation.decode('utf-8', errors='replace').strip()

            # Clean up unwanted characters from the start of the translation
            translation_decoded = re.sub(r"^[^\w]+", "", translation_decoded)

            # Add entry with key and translation information
            entries.append((key, translation_length, translation_decoded))

    return entries


entries = parse_binary_locale_file(file_path)

# Display parsed entries
for key, translation_length, translation in entries:
    print(f"Key: {key}")
    print(f"Translation Length: {translation_length}, Translation: {translation}\n")


"""


import sys

if len(sys.argv) < 4:
    print("Running UI mode.")
    print("Usage: python script.py <source_lang> <target_lang> <location>")
    open_ui_dialog()
else:
    print("Running batch mode.")
    print("To restore defaults, use the same source and base languages.")
    source_lang = sys.argv[1]
    target_lang = sys.argv[2]
    location = sys.argv[3]
    kit_folder = sys.argv[4]
    process_files(source_lang, target_lang, location, kit_folder)
 

