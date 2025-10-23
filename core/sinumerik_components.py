import math
import numpy as np
import config

class Filter:
    def __init__(self, application, activate_param, type_param, time_constant_param, fn_param, dn_param, fz_param, dz_param):
        self.application = application # Can be "current_setpoint", "speed_setpoint" or "actual_speed"
        self.activate_param = activate_param # Only for actual speed filter
        self.type_param = type_param
        self.time_constant_param = time_constant_param
        self.fn_param = fn_param
        self.dn_param = dn_param
        self.fz_param = fz_param
        self.dz_param = dz_param

        self.actual_speed_filter_active = None  # Only for actual speed filter
        self.type = None
        self.fn = None
        self.dn = None
        self.fz = None
        self.dz = None
        self.time_constant = None

        # === Calculated values ===

        # Variables for PT2 filter
        self.f_res = None
        self.damping = None

        # Variables for Generic 2nd order filter
        self.f_block = None
        self.attenuation = None
        self.f_band = None
        self.notch_depth = None

        # UI variables
        self.color = [0, 0, 0]  # Default to black
        self.show_param = False
        self.show_bode_plot = True

    def init_default_values(self):
        if self.application == "current_setpoint" or self.application == "actual_speed":
            self.set_sinumerik_values(type=1, time_constant=None, fn=config.FREQ_DEFAULT, dn=config.DAMPING_DEFAULT, fz=config.FREQ_DEFAULT, dz=config.DAMPING_DEFAULT)
        elif self.application == "speed_setpoint":
            self.set_sinumerik_values(type=0, time_constant=config.TIME_CONSTANT_DEFAULT, fn=None, dn=None, fz=None, dz=None)
        else:
            print(f"❌ Unknown application type: {self.application}. Cannot initialize default values.")

    def calculate_type2_sinumerik_filter_values(self):

        if self.f_block is None or self.f_band is None or self.attenuation is None or self.notch_depth is None:
            print("❌ Filter parameters (f_block, f_band, attenuation, notch_depth) are not set. \
                  Cannot calculate Sinumerik filter values.")
            return

        self.fn = float(self.f_block * 10**(self.attenuation / 40))
        self.dn = float(self.f_band / (2 * self.f_block * (10 ** (self.attenuation / 40))))
        self.fz = float(self.f_block)
        self.dz = float((10 ** (self.notch_depth / 20)) * 0.5 * math.sqrt((1 - (1 / 10 ** (self.attenuation / 20))) ** 2 + ((self.f_band ** 2) / ((self.f_block ** 2) * (10 ** (self.notch_depth / 10))))))

    def set_sinumerik_values(self, type=None, time_constant=None, fn=None, dn=None, fz=None, dz=None, actual_speed_filter_active=None):

        if type is not None:
            self.type = np.int16(type)

        if time_constant is not None:
            self.time_constant = float(time_constant)

        if fn is not None:
            self.fn = float(fn)

        if dn is not None:
            self.dn = float(dn)

        if fz is not None:
            self.fz = float(fz)

        if dz is not None:
            self.dz = float(dz)

        if actual_speed_filter_active is not None:
            self.actual_speed_filter_active = np.uint16(actual_speed_filter_active)

        if self.type not in [0, None]:
            self.calculate_filter_values()

    def set_filter_values(self, f_res=None, damping=None, f_block=None, f_band=None, attenuation=None, notch_depth=None):
        set_type1 = False
        if f_res is not None:
            self.f_res = float(f_res)
            set_type1 = True
        if damping is not None:
            self.damping = float(damping)
            set_type1 = True

        # If parameters for type 1 filter are set, calculate the values
        if set_type1:
            self.set_sinumerik_values(fn=f_res, dn=damping)

        calc_type2 = False
        if f_block is not None:
            self.f_block = float(f_block)
            calc_type2 = True
        if f_band is not None:
            self.f_band = float(f_band)
            calc_type2 = True
        if attenuation is not None:
            self.attenuation = float(attenuation)
            calc_type2 = True
        if notch_depth is not None:
            self.notch_depth = float(notch_depth)
            calc_type2 = True
        
        # If parameters for type 2 filter are set, calculate the values
        if calc_type2:
            self.calculate_type2_sinumerik_filter_values()

    def set_type(self, type):
        self.type = np.int16(type) if type is not None else None

    def calculate_filter_values(self):
        # If the filter is for current setpoint, only PT2 (type 1) and Geneirc 2nd order (type 2) filters are supported
        if self.application == "current_setpoint" or self.application == "actual_speed":
            if self.type not in [1, 2]:
                print(f"❌ Unsupported filter type {self.type} for {self.application} application. Only PT2 and Generic 2nd order filters are supported.")
                return
            
        # If the filter is for speed setpoint, low-pass PT1 (type 0) is also allowed
        elif self.application == "speed_setpoint":
            if self.type not in [0, 1, 2]:
                print(f"❌ Unsupported filter type {self.type} for {self.application} application. Only (0) Low-pass PT1, (1) Low-pass PT2 and (2) Generic 2nd order filters are supported.")
                return
        
        if self.type == 0:  # Low-pass PT1 filter
            # No additional calculations needed for PT1 filter
            pass
        if self.type == 1:  # Low-pass PT2 filter
            self.f_res = self.fn
            self.damping = self.dn

        elif self.type == 2:  # Generic 2nd order filter
            # If one of the values needed for this filter is not init., do not calculate
            if self.fz is None or self.dz is None or self.fn is None or self.dn is None:
                return
            
            self.f_block = self.fz
            self.attenuation = self.calculate_attenuation(self.fn, self.fz)
            self.f_band = self.calculate_fband(self.dn, self.fz, self.attenuation)
            self.notch_depth = self.calculate_notch_depth(self.dz, self.f_band, self.f_block, self.attenuation)

        else:
            print(f"❌ Unknown filter type: {self.type} in filter {self}. Cannot calculate filter values.")

    # Calculate band-stop frequency fband from dn, fz, and attenuation
    def calculate_fband(self, dn, fz, attenuation_db):
        return dn / (2 * fz * (10 ** (attenuation_db / 40)))

    # Calculate notch depth (Absenkung) from dz, fband, fsperr, and attenuation
    def calculate_notch_depth(self, dz, fband, fsperr, attenuation_db):
        term1 = (1 - (1 / (10 ** (attenuation_db / 20)))) ** 2
        term2 = (fband ** 2) / (fsperr ** 2 * (10 ** (attenuation_db / 10)))
        denominator = 0.5 * math.sqrt(term1 + term2)
        return 20 * math.log10(dz / denominator)

    # Calculate attenuation (Daempfung) from fn and fz
    def calculate_attenuation(self, fn, fz):
        return 40 * math.log10(fn / fz)

    def __str__(self):
        if self.type == 0:
            return f"Filter(type=Low-pass PT1, fn={self.fn}, dn={self.dn})"
        
        elif self.type == 1:
            return (f"Filter(type=Low-pass PT2, "
                    f"fn={self.fn}, dn={self.dn})")
        
        elif self.type == 2:
            return (f"Filter(type=General second-order, "
                    f"fn={self.fn}, dn={self.dn}, "
                    f"fz={self.fz}, dz={self.dz}, "
                    f"f_block={self.f_block}, "
                    f"attenuation={self.attenuation}, "
                    f"f_band={self.f_band}, "
                    f"notch_depth={self.notch_depth})")
        
        else:
            return (f"Filter(type={self.type} (Unknown), "
                    f"fn={self.fn}, dn={self.dn}, "
                    f"fz={self.fz}, dz={self.dz})")


class Drive:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.num_active_current_setpoint_filters = 0
        self.current_setpoint_filters = []
        self.speed_setpoint_filters = []
        self.actual_speed_filters = []
        self.controllers = []

        # Variables used for retrieving original data. These are set at parsing
        self.original_num_current_setpoint_filters = None
        self.original_num_speed_setpoint_filters = None
        self.original_num_actual_speed_filters = None

    def set_original_filter_amounts(self):
        self.original_num_current_setpoint_filters = self.num_active_current_setpoint_filters
        self.original_num_speed_setpoint_filters = len(self.speed_setpoint_filters)
        self.original_num_actual_speed_filters = len(self.actual_speed_filters)

    def __str__(self):
        return f"Drive(name={self.name}, path={self.path})"


class ParameterContainer:
    def __init__(self, name_dict, param_list, default_lang="ger"):
        # Save the dictionary with the names in different languages
        # Example of name_dict: {"ger": "Stromregelkreis", "eng": "Current Control Loop"}
        self.name_dict = name_dict

        # Save the list of ControllerParam objects
        self.param_list: list[Parameter | ParamBitconfig | AdaptationPlotParams] = param_list

        # Save the default language for the container names
        self.default_lang = default_lang

        # Extract the name in the default language
        self.name = self.name_dict[self.default_lang] if self.default_lang in self.name_dict else "Unknown Container"


class Parameter:
    def __init__(self, param_str, meaning_dict, min, max, default_value, step, decimals, var_type_str, default_lang='ger'):
        self.param_type = "normal"  # Type of the parameter, can be "normal" or "bitconfig"
        
        self.param_str = param_str
        # Example of param_meaning_dict: {"ger": "Abtastzeit Stromregelkreis [µs]", "eng": "Sampling time current control loop [µs]"}
        self.meaning_dict = meaning_dict
        self.value = None 
        self.og_value = None  # Original value read from archive
        self.min = min
        self.max = max
        self.default_value = default_value # Default value from docs
        self.step = step
        self.decimals = decimals
        self.var_type_str = var_type_str
        self.default_lang = default_lang

        self.meaning = self.meaning_dict[self.default_lang] if self.default_lang in self.meaning_dict else "Unknown Meaning"

    def set_value(self, value, original=False):
        # Handle string type parameters
        if self.var_type_str == "str":
            if not isinstance(value, str):
                print(f"❌ Value '{value}' is not a string and cannot be set for parameter {self.param_str}.")
                return False
            if original:
                self.og_value = value
            self.value = value
            return True

        # Convert string input to the correct type if necessary
        if isinstance(value, str):
            try:
                if self.var_type_str == "float32":
                    value = float(value)
                elif self.var_type_str == "int32":
                    value = int(value)
                elif self.var_type_str == "uint16":
                    value = np.uint16(value)
                else:
                    print(f"❌ Unsupported variable type: {self.var_type_str}. Cannot set value.")
                    return False
            except (ValueError, TypeError):
                print(f"❌ Value '{value}' could not be converted to {self.var_type_str} for parameter {self.param_str}.")
                return False

        # Check bounds for numeric types (unless original value)
        if original or (self.min <= value <= self.max):
            try:
                if self.var_type_str == "float32":
                    value = float(value)
                elif self.var_type_str == "int32":
                    value = int(value)
                elif self.var_type_str == "uint16":
                    value = np.uint16(value)
                elif self.var_type_str == "bool":
                    value = int(value)
                else:
                    print(f"❌ Unsupported variable type: {self.var_type_str}. Cannot set value.")
                    return False
            except (ValueError, TypeError):
                print(f"❌ Value {value} is not a valid {self.var_type_str} for parameter {self.param_str}.")
                return False

            if original:
                self.og_value = value
            self.value = value
            return True
        else:
            print(f"❌ Value {value} is out of bounds for parameter {self.param_str}. Must be between {self.min} and {self.max}.")
            return False
        

class ParamBitconfig:
    def __init__(self, param_str, meaning_dict, og_value, bit_meanings_dict, default_lang='ger'):
        self.param_type = "bitconfig"  # Type of the parameter
        self.var_type_str = "uint32"

        self.param_str = param_str # e.g. "p0000[0]"
        self.meaning_dict = meaning_dict # e.g. {"ger": "Abtastzeit Stromregelkreis [µs]"}
        self.og_value = og_value
        self.bit_meanings_dict = bit_meanings_dict  # Dictionary of bit meanings {'en': ["Bit 0 meaning", "Bit 1 meaning"], 'ger': ["Bit 0 Bedeutung", "Bit 1 Bedeutung"]}
        self.default_lang = default_lang

        self.value = self.og_value  # Current value of the parameter
        self.meaning = self.meaning_dict[self.default_lang] if self.default_lang in self.meaning_dict else "Unknown Meaning"
        self.bit_meanings_list = self.bit_meanings_dict[self.default_lang]
        self.bit_values_list = [0 for _ in range(len(self.bit_meanings_list))]  # Initialize with 0

    def set_bit(self, bit_index, value):
        if bit_index < 0 or bit_index >= len(self.bit_values_list):
            print(f"❌ Invalid bit index: {bit_index}. Must be between 0 and {len(self.bit_values_list) - 1}.")
            return False

        if value not in [0, 1]:
            print(f"❌ Invalid value: {value}. Must be 0 or 1.")
            return False

        self.bit_values_list[bit_index] = value
        return True
    
    def calculate_value(self):
        """
        Calculate the integer value from the bit values list.
        Each bit is represented as a power of 2, where the least significant bit is at index 0.
        """
        value = 0
        for i, bit in enumerate(self.bit_values_list):
            if bit == 1:
                value += 2 ** i
        
        self.value = value

    def reset_bits(self):
        self.bit_values_list = [0 for _ in range(len(self.bit_meanings_list))]
        self.calculate_value()

    
class AdaptationPlotParams:
    """
    Placeholder class for the 3-Zones plot with two Y-axes.
    Used in my_app/config.py
    """

    def __init__(self, name1_dict, name2_dict, y1_param: str, y1_adapt_factor_param: str, 
                 y2_param: str, y2_adapt_factor_param: str, x1_param: str, x2_param: str, default_lang="ger"):
        self.param_type = "adaptation_plot"

        self.name1_dict = name1_dict  # Dictionary with names in different languages for the first graph
        self.name2_dict = name2_dict  # Dictionary with names in different languages for the second graph
        self.y1_param = y1_param
        self.y1_adapt_factor_param = y1_adapt_factor_param
        self.y2_param = y2_param
        self.y2_adapt_factor_param = y2_adapt_factor_param
        self.x1_param = x1_param
        self.x2_param = x2_param

        self.name1 = self.name1_dict[default_lang] if default_lang in self.name1_dict else "Unknown Name 1"
        self.name2 = self.name2_dict[default_lang] if default_lang in self.name2_dict else "Unknown Name 2"


class Archive:
    def __init__(self, path):

        # Determine the type of archive based on the file extension
        if path.endswith('.arc'):
            self.type = "ARC"
        elif path.endswith('.dsf'):
            self.type = "DSF"
        else:
            print(f"❌ File {path.split('/')[-1]} is not a valid archive type.")
            self.type = "UNKNOWN"

        self.name = path.split('/')[-1]
        self.path = path
        self.is_binary = False

        self.ncu_path = ""
        self.drv_path = ""
        self.drives = []
        self.is_innit = False # Flag to check if the archive has been initialized
        self.original_copy: Archive  # To keep a copy of the original archive for comparison

        self.md_path = ""
        self.kinematic_tree: KinematicTree | None = None

        # UI variables
        self.show_more_drive_info = False

    def add_ncu_path(self, ncu_path):
        self.ncu_path = ncu_path

    def add_drv_path(self, drv_path):
        self.drv_path = drv_path

    def set_archive_innit_status(self, is_innit):
        self.is_innit = is_innit


class KinematicNode:
    # Kinematic Node can only be initialized with the index and name at least.
    def __init__(self, index, name):  
        # Initialize all attributes with default values  
        self.index = index
        self.name = name
        self.next = ""
        self.parallel = ""
        self.type = ""
        self.off_dir_x = 0.0
        self.off_dir_y = 0.0
        self.off_dir_z = 0.0
        self.axis = ""
        self.a_off = 0.0
        self.switch_index = -1
        self.switch_pos = 0
        self.switch = None

        # Position related attributes
        self.position_calculated = False
        self.position = [0.0, 0.0, 0.0]  

    def __repr__(self):
        return (f"Kinematic Node \"{self.name}\" (Index: {self.index})")
    
    def __str__(self):
        return (f"Kinematic Node \"{self.name}\" (Index: {self.index})\n"
                f"  Next: {self.next}\n"
                f"  Parallel: {self.parallel}\n"
                f"  Type: {self.type}\n"
                f"  Offset Direction: ({self.off_dir_x}, {self.off_dir_y}, {self.off_dir_z})\n"
                f"  Axis: {self.axis}\n"
                f"  A_Offset: {self.a_off}\n"
                f"  Switch Index: {self.switch_index}\n"
                f"  Switch Position: {self.switch_pos}\n"
                f"  Switch: {self.switch}")

    def update(self, next=None, parallel=None, type=None, 
               off_dir_x=None, off_dir_y=None, off_dir_z=None, axis=None, a_off=None,
               switch_index=None, switch_pos=None, switch=None,
               position_calculated=None, position=None): 
        if next is not None:
            self.next = next
        if parallel is not None:
            self.parallel = parallel
        if type is not None:
            self.type = type
        if off_dir_x is not None:
            self.off_dir_x = off_dir_x
        if off_dir_y is not None:
            self.off_dir_y = off_dir_y
        if off_dir_z is not None:
            self.off_dir_z = off_dir_z
        if axis is not None:
            self.axis = axis
        if a_off is not None:
            self.a_off = a_off
        if switch_index is not None:
            self.switch_index = switch_index
        if switch_pos is not None:
            self.switch_pos = switch_pos
        if switch is not None:
            self.switch = switch    
        if position_calculated is not None:
            self.position_calculated = position_calculated
        if position is not None:
            if isinstance(position, list) and len(position) == 3:
                self.position = position
            else:
                print(f"Warning: Invalid position format for node {self.name}. Expected a list of three floats.") 


class KinematicTree:
    def __init__(self, node_dict):
        self.PRINT_ROOT_NODES = True  # Set to True to print root nodes in the console

        self.node_dict = node_dict
        
        # Calculate root nodes
        self.root_nodes = self.find_root_nodes()

    def find_root_nodes(self):
        """Identify root nodes from a dictionary of kinematic nodes.
        
        Args:
            node_dict: Dictionary mapping node names to KinematicNodeClass objects with:
                - name: String identifier (should match dictionary key)
                - next: Name of child node or empty string
        
        Returns:
            List of root node objects
        """
        if not self.node_dict:
            return []

        root_nodes = []
        all_nodes = list(self.node_dict.values())
        child_nodes = set()

        # First pass: Collect all child references
        for node in all_nodes:
            if node.parallel not in (None, ""):
                child_nodes.add(node.parallel)
            if node.next not in (None, ""):
                child_nodes.add(node.next)

        # Second pass: Identify roots
        for node in all_nodes:
            # A root must:
            # 1. Not be someone's child (not in child_nodes)
            # 2. Have at least one child (node.next exists)
            if node.name not in child_nodes and node.next:
                root_nodes.append(node)

        if self.PRINT_ROOT_NODES:
            print("\nRoot Nodes:")
            for root in root_nodes:
                print(root)

        return root_nodes