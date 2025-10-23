import numpy as np
import config
from copy import deepcopy
from core import read_dif, sinumerik_components
from core.manage_archive_content import search_params_in_content, extract_filter_data_from_content, extract_controller_data_from_content

MAX_PARAM_INDEX = 100 # Safe limit to avoid infinite loops.

def parse_filters_from_dsf(archive):
    """
    Parse drive and filter parameters from the archive into the archive object.

    Path of a file in the archive that contains the Drive data.
    Here is an example of the path for a example Drive "DRIVE_3.15:3": 'NCU_NCU1/DRV/3/15/PS000003.TEA'
    First folder always begins with "NCU".
    The next folder always begins with "DRV"
    The next folders are numbered according to the first number of the Drive name. The folder 'DESC/' can be skipped.
    The next folder is numbered according to the second number of the Drive name.
    The last folder is always named "PS00000X.TEA" where X is the number of the Drive pin.
    The PS00000X.TEA files can also be from other components, like Control-Unit. 
    Only way to know if the file is from a Drive is to check the content of the file and
    read parameter p199 and search for p1657, which only Drives have.
    """

    if archive.is_innit:
        print("Archive is already initialized. Skipping parsing.")
        return

    ncu_folder_tag = 'NCU'
    drv_folder_tag = 'DRV'
    nck_folger_tag = 'NCK'
    desc_folder_tag = 'DESC/'
    drive_specific_param = 'p1657'

    # Drive name is defined by the parameter p199[n] where n is from 0 to 24.
    drive_name_param = config.drive_name_param
    drive_name_param_max_index = 24

    # Get first part of the path
    ls_dsf = read_dif.list_zip_subpath(archive.path)

    # Find the NCU path in the archive
    ncu_path = ""
    for item in ls_dsf:
        if item.startswith(ncu_folder_tag):
            ncu_path = item
            print(f"Found NCU path: {ncu_path}")
            break
    
    # If no NCU path is found, there is something wrong with the archive
    if not ncu_path:
        print("❌ No NCU path found in the archive.")
        return None
    
    # Add the NCU path to the archive object
    archive.add_ncu_path(ncu_path)
    
    ls_ncu = read_dif.list_zip_subpath(archive.path, ncu_path)

    # Find the DRV path in the archive
    drv_item = ""
    nck_item = ""
    for item in ls_ncu:
        if item.startswith(drv_folder_tag):
            drv_item = item
            print(f"Found DRV folder: {drv_item}")
        
        elif item.startswith(nck_folger_tag):
            nck_item = item
            print(f"Found NCK folder: {nck_item}")

    drv_path = ncu_path + drv_item if drv_item else ""
    nck_path = ncu_path + nck_item if nck_item else ""

    # ===== Going trough DRV path =====
    # If no DRV path is found, there is something wrong with the archive
    if not drv_path:
        print("❌ No DRV path found in the archive.")
        return None
    
    # Add the DRV path to the archive object
    archive.add_drv_path(drv_path)
    
    # Go to the DRV path
    ls_drv = read_dif.list_zip_subpath(archive.path, drv_path)

    if ls_drv is None:
        print("❌ No DRV path found in the archive.")
        return None
    
    if ls_drv == []:
        print("❌ DRV folder is empty.")
        return None

    for drv_item in ls_drv:
        if desc_folder_tag in drv_item:
            # Skip the DESC folder
            continue

        # Check each folder in the DRV path
        if drv_item.endswith('/'):
            
            drv_item_path = drv_path + drv_item
            ls_drv_n1 = read_dif.list_zip_subpath(archive.path, drv_item_path, print_items=True)

            if ls_drv_n1 is None:
                print(f"❌ No subfolders found in {drv_item_path}.")
                continue

            for drv_n1_item in ls_drv_n1:
                if drv_n1_item.endswith('/'):
                    # Check the second level folder
                    drv_n2_item_path = drv_item_path + drv_n1_item
                    ls_drv_n2 = read_dif.list_zip_subpath(archive.path, drv_n2_item_path, print_items=True)

                    for drv_n2_item in ls_drv_n2:
                        if drv_n2_item.endswith('.TEA'):
                            # Found a Component file - time to check if it is a Drive
                            # Read the content of the file and check for a specific parameter, that only Drives have
                            full_path = drv_n2_item_path + drv_n2_item
                            content = read_dif.read_file_from_zip(archive.path, full_path)

                            if content == None:
                                print(f"❌ Could not read file {full_path}.")
                                continue
                            
                            drive_specific_param_value = search_params_in_content(content, drive_specific_param)
                            if drive_specific_param_value is None:
                                continue

                            print(f"Found Drive file: {full_path}")

                            # Create a Drive object and add it to the archive
                            drive = sinumerik_components.Drive("", full_path)

                            # Extract filter data
                            data_extracted_successfully = extract_filter_data_from_content(content, full_path, drive)
                            if not data_extracted_successfully:
                                print(f"❌ Could not extract filter data from {full_path}.")

                            # Extract controller data
                            data_extracted_successfully = extract_controller_data_from_content(content, full_path, drive)
                            if not data_extracted_successfully:
                                print(f"❌ Could not extract controller data from {full_path}.")

                            archive.drives.append(drive)

    # ===== Find MD params =====

    kin_path = nck_path + 'cfg/ncdata/kin.ini'

    # Read the KIN file from the archive
    kin_content = read_dif.read_file_from_zip(archive.path, kin_path)

    if kin_content is None or kin_content == -1:
        # If there is no kinematic content available, create empty tree
        archive.kinematic_tree = sinumerik_components.KinematicTree({})
        print(f"❌ Could not read KIN file from {kin_path}.")
    else:
        # ===== Extract KIN data =====

        # Split the KIN file into lines. Each line contains a kinematic node setting.
        kin_file_lines = kin_content.split("\n")

        # Dict for storing kinematic nodes
        node_dict = {}

        for line in kin_file_lines:

            # Here is an example of a KIN (Kinematic-File) line: $NK_NAME[0]="ROOT" '38c0
            # $NK_NAME is the parameter name, [0] is the index, "ROOT" is the value, 
            # '38c0 is a checksum which can be ignored for reading purposes.
            # Offset parameter has multiple indices - $NK_OFF_DIR[n,i]=1
            # Where n is the node index and i is the X (i==0), Y (i==1) or Z (i==2) direction
            # i is going to be saved in the off_dir_xyz list of the KinematicNode class.
            settings = line.split(" ")[0].split("=")

            for kin_par in config.kin_parameters:

                # Check if the needed kinematic parameter is in the line
                if kin_par not in settings[0]:
                    continue
                    
                # Extract the index of the kinematic node from the parameter name
                index_str = settings[0].split("[")[1].split("]")[0]

                # Extract the value from the settings
                value_str = settings[1].strip('"')

                # Variable to check if the node was found
                node_found = False

                if kin_par == "$NK_NAME":
                    # Create a new KinematicNode with the extracted name
                    node_dict[value_str] = sinumerik_components.KinematicNode(index=index_str, name=value_str)
                    node_found = True

                elif kin_par == "$NK_NEXT":
                    # Check if the node with the given index exists

                    for node in node_dict.values():
                        if node.index == index_str:
                            # Update the next of the current node
                            node.update(next=value_str)
                            node_found = True
                            break
            
                elif kin_par == "$NK_PARALLEL":
                    # Check if the node with the given index exists
                    for node in node_dict.values():
                        if node.index == index_str:
                            # Update the parallel flag of the current node
                            node.update(parallel=value_str)
                            node_found = True
                            break
                    
                elif kin_par == "$NK_TYPE":
                    # Check if the node with the given index exists
                    for node in node_dict.values():
                        if node.index == index_str:
                            # Update the type of the current node
                            node.update(type=value_str)
                            node_found = True
                            break
                    
                elif kin_par == "$NK_OFF_DIR":
                    # Seperate node index and direction
                    if ',' in index_str:
                        node_index, direction = index_str.split(',')
                        # Convert direction to integer
                        direction = int(direction)
                    else:
                        print(f"Warning: Invalid index format for parameter {kin_par} in line: {line}. \n\
                            Expected format is '$NK_OFF_DIR[n,i]'. Skipping this parameter.")
                        continue

                    # Check if the node with the given index exists
                    for node in node_dict.values():
                        if node.index == node_index:
                            node_found = True
                            
                            # Convert the value to a float
                            try:
                                dir_value = float(value_str)
                            except ValueError:
                                print(f"Warning: Invalid value '{value_str}' for parameter {kin_par} in line: {line}. \n\
                                    Expected an integer. Skipping this parameter.")
                                continue

                            # Update the off_dir_i of the current node (i is the direction)
                            match direction:
                                case 0:
                                    node.update(off_dir_x=dir_value)
                                case 1:
                                    node.update(off_dir_y=dir_value )
                                case 2:
                                    node.update(off_dir_z=dir_value)
                                case _:
                                    print(f"Warning: Invalid direction {direction} for parameter {kin_par} in line: {line}. \n\
                                        Expected direction is 0 (X), 1 (Y) or 2 (Z). Skipping this parameter.")
                                    continue
                                
                elif kin_par == "$NK_AXIS":
                    # Check if the node with the given index exists
                    for node in node_dict.values():
                        if node.index == index_str:
                            # Update the axis of the current node
                            node.update(axis=value_str)
                            node_found = True
                            break

                elif kin_par == "$NK_A_OFF":
                    # Check if the node with the given index exists
                    for node in node_dict.values():
                        if node.index == index_str:
                            # Convert value to a float
                            try:
                                a_off = float(value_str)
                            except ValueError:
                                print(f"Warning: Invalid value '{value_str}' for parameter {kin_par} in line: {line}. \n\
                                    Expected an integer. Skipping this parameter.")
                                continue

                            # Update the a_off of the current node
                            node.update(a_off=a_off)
                            node_found = True
                            break
            
                elif kin_par == "$NK_SWITCH_INDEX":
                    # Check if the node with the given index exists
                    for node in node_dict.values():
                        if node.index == index_str:
                            # Update the switch_index of the current node
                            node.update(switch_index=value_str)
                            node_found = True
                            break
                    
                elif kin_par == "$NK_SWITCH_POS":
                    # Check if the node with the given index exists
                    for node in node_dict.values():
                        if node.index == index_str:
                            # Update the switch_pos of the current node
                            node.update(switch_pos=value_str)
                            node_found = True
                            break

                elif kin_par == "$NK_SWITCH":
                    # Check if the node with the given index exists
                    for node in node_dict.values():
                        if node.index == index_str:
                            # Update the switch of the current node
                            node.update(switch=value_str)
                            node_found = True
                            break

                if not node_found:
                    print(f"Warning: Node with index {index_str} not found for parameter {kin_par}. Skipping this parameter.")
    
        # Create a KinematicTree object with the node_dict
        archive.kinematic_tree = sinumerik_components.KinematicTree(node_dict)

    archive.set_archive_innit_status(True)
    archive.original_copy = deepcopy(archive)  # Keep a copy of the original archive
    print("✅ Archive parsing completed successfully.")

    return True
                                
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import config

    # Example usage
    dsf_path = (
        "/Users/meho.kitovnica/Desktop/Bachelorarbeit T3300/Archiv/Archiv-Formate/DSF/"
        "DSF Archiv Beispiele/Backup_NPD_2025-04-08_CONTAINERGROSS_NCU1.dsf"
    )
