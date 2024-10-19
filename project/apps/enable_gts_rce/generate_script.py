import json
import os

BUILD_PATH = "./build"
BASE_SCRIPT_PATH = "./data/base_script.json"
OUTPUT_SCRIPT_PATH = os.path.join(BUILD_PATH, "script.json")

BUILD_FILES = [
    os.path.join(BUILD_PATH, "inject_overlay_payload.bin"),
    os.path.join(BUILD_PATH, "overlay_payload.bin"),
]

def generate_memory_section(file_path):
    """
    Reads a binary file and returns a dictionary representing
    the memory editor section with the hex content of the file.
    Hexadecimal values are zero-padded to two digits.
    """
    data = {"type": "memory_editor"}

    with open(file_path, "rb") as f:
        data["memory"] = ["0x" + f"{byte:02x}".upper() for byte in f.read()]

    return data

def generate_script(files, base_script_path, output_script_path):
    """
    Reads the base script, appends memory sections from the provided files,
    and writes the updated script to the output file.
    """
    with open(base_script_path, "r") as f:
        base_script = json.load(f)[0]

    for file in files:
        base_script["input_fields"].append(generate_memory_section(file))

    with open(output_script_path, "w") as f:
        json.dump(base_script, f, indent=4)

if __name__ == "__main__":
    generate_script(BUILD_FILES, BASE_SCRIPT_PATH, OUTPUT_SCRIPT_PATH)
