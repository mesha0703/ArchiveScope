# my_app/core/manipulate_arc.py

from copy import deepcopy
from core.sinumerik_components import Archive, Drive, KinematicTree
from core.manage_archive_content import search_params_in_content, extract_filter_data_from_content, extract_controller_data_from_content

MAX_PARAM_INDEX = 100 # Safe limit to avoid infinite loops.

def get_drive_file_content(archive_content: str, bus_nr: int, slave_nr: int, ps_nr: int) -> tuple[bool, str]:
    """
    Each drive file has its start and end marker/tag.
    """
    start_tag1 = f"\\_NC_ACT.DIR\\_N_PS0000{ps_nr:02d}_TEAPS0000{ps_nr:02d}.TEA"
    start_tag2 = f"/_N_SYSTEM_DRV/_N_BUS{bus_nr}_DIR/_N_SLAVE{slave_nr}_DIR/\\SYSTEM.DRV\\BUS{bus_nr}.DIR\\SLAVE{slave_nr}.DIR\\[SINUMERIK_HEADER]"
    end_tag = f"@@_N_ADRV_SINAMICS_{bus_nr}_{slave_nr}_PS0000{ps_nr:02d}"

    is_valid = True
    start_line = -1
    end_line = -1

    for i, line in enumerate(archive_content.splitlines()):
        if start_tag1 in line and start_tag2 in line:
            start_line = i
            break

    # If the start tags havent been found, return false flage and empty content
    if start_line == -1:
        is_valid = False
        print(f"❌ Start tags ({start_tag1} AND {start_tag2}) not found in archive file")
        return is_valid, ""

    file_content_lines = []
    for i, line in enumerate(archive_content.splitlines()[start_line:], start=start_line):
        if end_tag in line:
            end_line = i
            break
        file_content_lines.append(line)

    # If the end tag hasn't been found, return false flag and empty content
    if end_line == -1:
        is_valid = False
        print(f"❌ End tag ({end_tag}) not found in archive file")
        return is_valid, ""

    # Join the file content lines into a single string
    file_content = "\n".join(file_content_lines)

    return is_valid, file_content

def get_archive_content(file_path: str) -> str:
    print(f"Reading content from: {file_path}")
    try:
        # Read the entire file.  Use latin‑1 decoding with replacement to
        # tolerate binary islands and control characters.  The ASCII export
        # occasionally inserts null bytes which we remove explicitly.
        with open(file_path, "rb") as f:
            raw_bytes = f.read()
        content = raw_bytes.decode("latin1", errors="replace")
        content = content.replace("\x00", "")
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        content = ""
    return content

def get_files_list(content: str) -> list[str]:
    content_lines = content.splitlines()

    # The files or so called "components" are listed under a
    # comment ";---components" until an empty line
    components = []
    is_component_section = False
    for line in content_lines:
        if line.startswith(";---components"):
            is_component_section = True
            continue
        if is_component_section and line.strip() == "":
            break
        if is_component_section:
            components.append(line.strip())
    return components

def parse_filters_from_arc(archive: Archive):

    # Check if the archive is initialized
    if archive.is_innit:
        print("Archive is already initialized. Skipping parsing.")
        return None
    
    # Check whether the archive type is ARC
    if archive.type != 'ARC':
        print("❌ Archive type is not ARC. Skipping parsing.")
        return None

    # Tags and parameters used for parsing
    drv_folder_tag = '\\SYSTEM.DRV'
    drive_specific_param = 'p1657'

    class BusSlaveCombination:
        # Create a PS-File-Component instance by passing a path of a PS (.TEA) file, which contains Drive-parameters
        def __init__(self, ps_path: str):
            self.is_valid: bool = True

            # Check whether the path begins correctly
            if not ps_path.startswith(drv_folder_tag) or len(ps_path.split('\\')) < 5:
                print("❌ Invalid DRV folder path. Cannot create valid BusSlaveCombination.")
                self.is_valid = False

            # Initialize bus and slave number variables
            self.bus_nr: int = -1
            self.slave_nr: int = -1
            self.ps_nr: int = -1

            # Extract bus, slave, and PS numbers
            self.is_valid, self.bus_nr, self.slave_nr, self.ps_nr = self._extract_bus_slave_ps(ps_path)

            # Save PS number in a list
            self.ps_list: list[int] = []
            if self.ps_nr != -1: self.ps_list.append(self.ps_nr)

            # Save the file path in a list
            self.file_paths: list[str] = []
            if self.ps_nr != 1: self.file_paths.append(ps_path)

        def _extract_bus_slave_ps(self, ps_path) -> tuple[bool, int, int, int]:
            path_parts = ps_path.split('\\')
            valid_bus_slave_ps: bool = True

            # Extract bus and slave numbers from the path
            bus_nr_str = path_parts[2].replace('BUS', '').replace('.DIR', '')
            slave_nr_str = path_parts[3].replace('SLAVE', '').replace('.DIR', '')
            ps_nr_str = path_parts[4].replace('PS', '').replace('.TEA', '')

            # Check whether there are .ACX files in the archive. If there are, the archive is in binary format
            if ".ACX" in ps_nr_str:
                print("❌ The given ARC Archive is in binary format and cannot be read.")
                archive.is_binary = True
                return False, -1, -1, -1

            # Initialize bus, slave, and PS numbers
            bus_nr: int = -1
            slave_nr: int = -1
            ps_nr: int = -1

            # Validate bus and slave numbers
            try:
                bus_nr = int(bus_nr_str)
                slave_nr = int(slave_nr_str)
                ps_nr = int(ps_nr_str)
            except ValueError:
                print(f"❌ Invalid BUS, SLAVE or PS number: {bus_nr_str}, {slave_nr_str}, {ps_nr_str}")
                valid_bus_slave_ps = False

            # Check whether the bus and slave numbers are valid
            if bus_nr == -1 or slave_nr == -1 or ps_nr == -1:
                print(f"❌ Invalid BUS, SLAVE or PS number: {bus_nr_str}, {slave_nr_str}, {ps_nr_str}")
                valid_bus_slave_ps = False

            return valid_bus_slave_ps, bus_nr, slave_nr, ps_nr

        def get_bus_slave(self) -> tuple[int, int]:
            return self.bus_nr, self.slave_nr
        
        def add_ps(self, ps_path) -> bool:
            # Check whether the PS path is valid (correct bus and slave)
            ps_valid, bus_nr, slave_nr, ps_nr = self._extract_bus_slave_ps(ps_path)

            if not ps_valid:
                print(f"❌ Invalid PS path: {ps_path}. Cannot add to BusSlaveCombination on bus {self.bus_nr} and slave {self.slave_nr}.")
                return False

            # If valid, add the PS number to the list
            self.ps_list.append(ps_nr)
            self.file_paths.append(ps_path)
            print(f"Added PS file: {ps_path} to {self}.")

            return True
        
        def __str__(self):
            return f"BusSlaveCombination(bus={self.bus_nr}, slave={self.slave_nr})"

    class BusSlaveCombinationList:
        def __init__(self):
            self.components: list[BusSlaveCombination] = []

        def add_component_by_ps_path(self, ps_path: str):

            # Create a new BusSlaveCombination
            component = BusSlaveCombination(ps_path)

            # Check whether the component is valid
            if not component.is_valid:
                print(f"❌ Invalid BusSlaveCombination: {component}. Not adding to list.")
                return

            # Check whether a BusSlaveCombination with the given bus / slave number already exists
            for existing_component in self.components:
                if existing_component.get_bus_slave() == component.get_bus_slave():

                    # If the component on given bus and slave already exist, add the ps file to the existing component
                    existing_component.add_ps(ps_path)
                    return

            # If no existing component was found, add the new component
            print(f"Adding new BusSlaveCombination: {component} to the list.")
            self.components.append(component)

    # Get archive content
    archive_content = get_archive_content(archive.path)
    if archive_content == "":
        print("❌ Failed to read archive content.")
        return None

    # Get the list of files (components) from the archive content
    components = get_files_list(archive_content)
    if not components:
        print("❌ No components found.")
        return None

    print(f"Found {len(components)} components in the archive.")

    # ===== Extracting DRIVE components =====

    # Create a BusSlaveCombinationList object, which will manage all BusSlaveCombination components
    bus_slave_combination_list = BusSlaveCombinationList()

    # Iterate trough all components and check whether the drv tag is present
    for component in components:
        if drv_folder_tag in component:
            print(f"\nFound DRV folder in component: {component}")

            # Add the ps path to the BusSlaveCombinationList
            bus_slave_combination_list.add_component_by_ps_path(component)

    # Iterate through all BusSlaveCombinations and extract parameters that are defined config.py
    for bus_slave_combination in bus_slave_combination_list.components:

        # Iterate trough each PS file
        for p, ps_nr in enumerate(bus_slave_combination.ps_list):
            # Get file content
            content_is_valid, file_content = get_drive_file_content(archive_content,\
                                                    bus_slave_combination.bus_nr, bus_slave_combination.slave_nr, ps_nr)

            # Check whether the content is valid
            if not content_is_valid:
                print(f"❌ Invalid PS file content for {bus_slave_combination} (PS{ps_nr}): {file_content}")
                continue

            # Check if the parameter, that is only in drive files can be found in the file
            drive_param = search_params_in_content(file_content, drive_specific_param)

            if drive_param is None:
                print(f"PS file {ps_nr} in {bus_slave_combination} does not contain the drive-specific parameter {drive_specific_param}. Skipping...")
                continue

            # If the drive parameter is found, we can process it
            print(f"Found drive-specific parameter in PS file {ps_nr} of {bus_slave_combination}: {drive_param}")

            # Initialize all variables that are needed for the drive object "Drive" from sinumerik_components.py
            drive_name: str = ""
            drive_path: str = bus_slave_combination.file_paths[p]

            # Create a Drive object
            drive = Drive(name=drive_name, path=drive_path)
            print(f"\nCreated Drive object: {drive}")

            # Extract filter data
            data_extracted_successfully = extract_filter_data_from_content(file_content, drive_path, drive)
            if not data_extracted_successfully:
                print(f"❌ Could not extract filter data from {drive_path}.")

            # Extract controller data
            data_extracted_successfully = extract_controller_data_from_content(file_content, drive_path, drive)
            if not data_extracted_successfully:
                print(f"❌ Could not extract controller data from {drive_path}.")

            archive.drives.append(drive)

    archive.set_archive_innit_status(True)
    archive.original_copy = deepcopy(archive)  # Keep a copy of the original archive

    # Kinematic tree cannot be extracted from an ARC Archive, so add an empty Tree
    archive.kinematic_tree = KinematicTree({})

    print("✅ Archive parsing completed successfully.")
    return True






