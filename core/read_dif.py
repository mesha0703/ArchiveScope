import zipfile
import os
from pathlib import Path


# Flag to control whether content should be printed
PRINT_CONTENT = False


def list_zip_structure(zip_path):
    """
    Prints the full folder structure of a ZIP file as a tree.
    """
    if not zipfile.is_zipfile(zip_path):
        print("The specified file is not a valid ZIP file.")
        return

    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        # Get the list of all file paths in the ZIP archive
        file_list = zip_file.namelist()

        # Build a nested dictionary (tree) to represent the folder structure
        tree = {}
        for path in file_list:
            parts = path.strip('/').split('/')
            current = tree
            for part in parts:
                current = current.setdefault(part, {})

        # Recursive function to print the tree with indentation
        def print_tree(d, indent=0):
            for key, val in sorted(d.items()):
                # Folder if val is a dict, file otherwise
                print(('  ' * indent + '📁 ' + key) if val else ('  ' * indent + '📄 ' + key))
                if val:
                    print_tree(val, indent + 1)

        # Print the top-level message and the structure
        print(f"Contents of {os.path.basename(zip_path)}:")
        print_tree(tree)


def list_zip_subpath(zip_path, inner_path="", print_items=PRINT_CONTENT):
    """
    Lists only the top-level files/folders inside a specified subpath of the ZIP.
    Similar to the 'ls' command.
    """
    if not zipfile.is_zipfile(zip_path):
        print("❌ The specified file is not a valid ZIP file.")
        return []

    # Clean up input path (remove leading/trailing slashes)
    inner_path = inner_path.strip("/")

    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        all_files = zip_file.namelist()
        listed_items = set()

        # Loop through all files in the archive
        for file in all_files:
            if inner_path:
                # Skip files not in the specified folder
                if not file.startswith(inner_path + "/"):
                    continue
                # Remove the subpath prefix to work with relative paths
                relative = file[len(inner_path) + 1:]
            else:
                relative = file

            # Extract the top-level directory or file
            top_level = relative.split('/', 1)[0]
            # Append '/' to indicate folders
            listed_items.add(top_level + ('/' if '/' in relative else ''))

        # Sort the result alphabetically
        result = sorted(list(listed_items))

        # Optional output
        if print_items:
            print(f"Contents of '{inner_path}' in {os.path.basename(zip_path)}:")
            for item in result:
                print(("📁 " + item[:-1]) if item.endswith('/') else ("📄 " + item))

        return result


def read_file_from_zip(zip_path, internal_file_path):
    """
    Reads the content of a specific file inside a ZIP archive.
    If it's a text file, prints and returns the content.
    If it's binary or not found, returns None.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        # Check if the file exists in the archive
        if internal_file_path in zip_file.namelist():
            with zip_file.open(internal_file_path) as file:
                content = file.read()
                try:
                    # Attempt to decode as UTF-8 text
                    content = content.decode('utf-8')
                    if PRINT_CONTENT:
                        print("📄 File content:\n", content)
                    return content
                except UnicodeDecodeError:
                    print("📂 File is not a text file (binary or not UTF-8).")
                    return None
        else:
            print(f"❌ File '{internal_file_path}' was not found in the archive.")
            return None

def copy_zip_with_changes(src_zip, dst_zip, patch, *, encoding="utf-8", create_missing=False):
    """
    Make a copy of src_zip at dst_zip, replacing whole file contents for any
    member listed in `patch = { member_path: new_content }`.

    - member_path: str, exact path inside the zip (case-sensitive, uses '/')
    - new_content: str (encoded as UTF-8) or bytes
    - create_missing: if True, members in patch not present in src are added

    Returns: (replaced:list[str], added:list[str], skipped_missing:list[str])
    """
    src_zip = Path(src_zip)
    dst_zip = Path(dst_zip)

    replaced, added, skipped = [], [], []

    with zipfile.ZipFile(src_zip, "r") as zin, zipfile.ZipFile(dst_zip, "w") as zout:
        # Preserve archive-level comment
        zout.comment = zin.comment

        names = set(zin.namelist())

        # Copy all members; replace those present in patch
        for src_info in zin.infolist():
            name = src_info.filename
            if name in patch:
                data = patch[name]
                if isinstance(data, str):
                    data = data.encode(encoding)
                else:
                    data = bytes(data)

                # Write replacement preserving metadata/compression
                dst_info = zipfile.ZipInfo(name, date_time=src_info.date_time)
                dst_info.compress_type = src_info.compress_type
                dst_info.external_attr = src_info.external_attr
                dst_info.create_system = src_info.create_system
                dst_info.flag_bits = src_info.flag_bits
                zout.writestr(dst_info, data)
                replaced.append(name)
            else:
                # verbatim copy
                zout.writestr(src_info, zin.read(name))

        # Add new files (optional)
        if create_missing:
            for name, payload in patch.items():
                if name not in names:
                    data = payload.encode(encoding) if isinstance(payload, str) else bytes(payload)
                    info = zipfile.ZipInfo(name)
                    info.compress_type = zipfile.ZIP_DEFLATED
                    zout.writestr(info, data)
                    added.append(name)
        else:
            skipped = [name for name in patch.keys() if name not in names]

    return replaced, added, skipped

if __name__ == "__main__":
    # Path to the .dsf (ZIP-like) file to be analyzed
    dsf_path = (
        "/Users/meho.kitovnica/Desktop/Bachelorarbeit T3300/Archiv/Archiv-Formate/DSF/"
        "DSF Archiv Beispiele/Backup_NPD_2025-04-08_CONTAINERGROSS_NCU1.dsf"
    )

    # Uncomment to print full ZIP structure as a tree
    # list_zip_structure(dsf_path)

    # List top-level files/folders inside a specific path of the ZIP
    list_zip_subpath(dsf_path, "NCU_NCU1/DRV")