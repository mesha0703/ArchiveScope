# my_app/core/manage_archive_content.py

import numpy as np
from copy import deepcopy
import config
from core.sinumerik_components import Drive, Filter, Parameter, ParamBitconfig, AdaptationPlotParams

MAX_PARAM_INDEX = 100  # Maximum number of parameters with [*n*] wildcard

def search_params_in_content(content, param_tag):
    """
    Searches for the specified parameter tags in the content and returns their values.
    """

    for line in content.split('\n'):
        if param_tag in line:
            # Extract the value after the tag
            value = line.split('=')[1].strip()

            return value

    return None

def change_params_in_content(content, params_dict):
    """
    Changes the values of the specified parameter tags in the content.
    Returns the modified content and a dictionary indicating which parameters were successfully changed.
    """

    # Dictionary to keep track of successfully changed parameters
    successfully_changed_dict = {}
    for param_tag in params_dict.keys():
        successfully_changed_dict[param_tag] = False

    for line in content.split('\n'):
        for param_tag, new_value in params_dict.items():
            if param_tag in line:
                # Change the value after the tag
                new_line = f"{param_tag}={new_value}"
                content = content.replace(line, new_line)

                successfully_changed_dict[param_tag] = True

    # Calculate checksum and change it in the content
    # COMING SOON...

    return content, successfully_changed_dict

def extract_filter_data_from_content(content, path, drive: Drive):
    drive_name = ""
    default_drive_name = "Drive"
    drive_name_param_max_index = 24

    # Get drive name
    for i in range(drive_name_param_max_index):
        param = f'{config.drive_name_param}[{i}]'
        value_str = search_params_in_content(content, param)

        # If the value is None or 0, stop reading the name
        if value_str is None or value_str == "0":
            break

        # Convert the value to an integer
        try:
            value = int(value_str)
        except ValueError:
            print(f"❌ Could not convert value '{value_str}' for {param} to int.")
            continue
        
        # The value is an ascii number which needs to be converted to a character
        if 32 <= value <= 126:  # ASCII printable range
            drive_name += chr(value)
        else:
            # If the value is not in the printable ASCII range, just append the number
            # This can happen if the value is a number or a special character
            drive_name += ' '

    # Safe default
    if drive_name == "":
        print(f"❌ Drive name could not be determined. Setting drive name as '{default_drive_name}'")
        drive_name = default_drive_name

    # Set drive name
    drive.name = drive_name

    # ===== Read FILTER params in config.py from the archive file =====

    # Read number of activated filter (1-4) is defined by the parameter p1656
    activated_filters_hex = search_params_in_content(content, config.PARAM_NUM_ACTIVATED_FILTERS_1_4)
    if activated_filters_hex is None:
        print(f"❌ Could not find {config.PARAM_NUM_ACTIVATED_FILTERS_1_4} in the file {path}.")
        return None

    # Hex numbers in parameters contain H at the beginning and '' around it, so we need to remove it
    activated_filters_hex = activated_filters_hex.replace('H', '').replace("'", "").strip()

    try:
        activated_filters_1_4_hex = int(activated_filters_hex, 16)
        activated_filters_1_4_bitconfig = [(activated_filters_1_4_hex >> i) & 1 for i in range(4)]
        activated_filters_1_4 = 0
        for i in activated_filters_1_4_bitconfig:
            if i == 1: activated_filters_1_4 += 1
    except ValueError:
        print(f"❌ Could not convert {activated_filters_hex} to int.")
        return None

    # Read number of activated filters (5-10)
    activated_filters_5_10_hex = search_params_in_content(content, config.PARAM_NUM_ACTIVATED_FILTERS_5_10)
    if activated_filters_5_10_hex is not None:
        activated_filters_5_10_hex = activated_filters_5_10_hex.replace('H', '').replace("'", "").strip()
        try:
            activated_filters_5_10_hex = int(activated_filters_5_10_hex, 16)
            activated_filters_5_10_bitconfig = [(activated_filters_5_10_hex >> i) & 1 for i in range(6)]
            activated_filters_5_10 = 0
            for i in activated_filters_5_10_bitconfig:
                if i == 1: activated_filters_5_10 += 1
        except ValueError:
            print(f"❌ Could not convert {activated_filters_5_10_hex} to int.")
            activated_filters_5_10 = 0
    else:
        print("No additional filters (5-10) activated.")
        activated_filters_5_10 = 0

    activated_filters = activated_filters_1_4 + activated_filters_5_10
    
    # Set the number of activated filters in the Drive object
    drive.num_active_current_setpoint_filters = activated_filters

    print(f"Activated filters: {activated_filters}")

    # Create a list of ALL filters
    filter_list = config.current_setpoint_filter_list[:activated_filters]
    filter_list += config.speed_setpoint_filter_list
    filter_list.append(config.actual_speed_filter)

    # Read the CURRENT SETPOINT filter parameters
    for filter_setting in filter_list:

        # Get application (current_setpoint, speed_setpoint, actual_speed)
        if filter_setting in config.current_setpoint_filter_list:
            application = "current_setpoint"
        elif filter_setting in config.speed_setpoint_filter_list:
            application = "speed_setpoint"
        else:
            application = "actual_speed"

        # Create a filter objects for CURRENT SETPOINT FILTERS with parameters from the config
        filter = Filter(
            application=application,
            activate_param=filter_setting['activate_param'] if 'activate_param' in filter_setting else None,
            type_param=filter_setting['type_param'],
            time_constant_param=filter_setting['time_constant_param'] if 'time_constant_param' in filter_setting else None,
            fn_param=filter_setting['fn_param'],
            dn_param=filter_setting['dn_param'],
            fz_param=filter_setting['fz_param'],
            dz_param=filter_setting['dz_param']
        )

        # ===== Check filter type and read needed parameters =====

        # If the application is "actual_speed", the activate_param is needed
        if filter.application == "actual_speed":
            activate_str = search_params_in_content(content, filter.activate_param) if filter.activate_param else None
            if activate_str is None:
                print(f"❌ Could not find {filter.activate_param} in the file {path}.")
                continue

            # Remove 'H' and '' from the string
            activate_str = activate_str.replace('H', '').replace("'", "").strip()

            # Convert activate_str to uint16
            try:
                filter.set_sinumerik_values(actual_speed_filter_active=np.uint16(activate_str))
            except Exception as e:
                print(f"❌ Could not convert {activate_str} to {np.uint16}. Error: {e}")
                continue

        # Read type parameter
        filter_type_str = search_params_in_content(content, filter.type_param)

        # Check whether filter_type_str has been found
        if filter_type_str is None:
            print(f"❌ Could not find {filter.type_param} in the file {path}.")
            continue

        # Convert type to int and check if it is valid
        try:
            filter_type = np.int16(filter_type_str)

        except Exception as e:
            print(f"❌ Could not convert {filter_type_str} to {np.int16}. Error: {e}")
            continue

        if filter_type == 0:
            # for PT1 filters, only time constant is needed
            time_constant_str = search_params_in_content(content, filter.time_constant_param)

            if time_constant_str is None:
                print(f"❌ Could not find {filter.time_constant_param} in the file {path}.")
                continue

            try:
                time_constant = float(time_constant_str)
            except ValueError:
                print(f"❌ Could not convert {filter.time_constant_param} to float in the file {path}.")
                continue

            # Change the values in the filter object
            filter.set_sinumerik_values(type=filter_type, time_constant=time_constant,\
                                fn=None, dn=None, fz=None, dz=None)

        elif filter_type == 1:
            # fn (nat. Freq. denom.) and dn (damping denom.) are needed for PT2 (type 1)
            fn_str = search_params_in_content(content, filter.fn_param)
            dn_str = search_params_in_content(content, filter.dn_param)

            if fn_str is None or dn_str is None:
                print(f"❌ Could not find {filter.fn_param} or {filter.dn_param} in the file {path}.")
                continue

            # Convert the values to floats
            try:
                fn = float(fn_str)
                dn = float(dn_str)
            except ValueError:
                print(f"❌ Could not convert {filter.fn_param} or {filter.dn_param} to float in the file {path}.")
                continue

            filter.set_sinumerik_values(type=filter_type, time_constant=None,\
                                fn=fn, dn=dn, fz=fn, dz=dn)
            
            print(f"Filter {filter.type_param} is a PT2 filter with fn={fn} and dn={dn}.")

        elif filter_type == 2:
            # fn, dn, fz (nat. Freq. numerator) and dz (damping numerator) 
            # are needed for Generic second-order (type 2) filters
            fn_str = search_params_in_content(content, filter.fn_param)
            dn_str = search_params_in_content(content, filter.dn_param)
            fz_str = search_params_in_content(content, filter.fz_param)
            dz_str = search_params_in_content(content, filter.dz_param)



            if fn_str is None or dn_str is None or fz_str is None or dz_str is None:
                print(f"❌ Could not find {filter.fn_param}, {filter.dn_param}, {filter.fz_param} or\
                    {filter.dz_param} in the file {path}.")
                continue

            # Convert the values to floats
            try:
                fn = float(fn_str)
                dn = float(dn_str)
                fz = float(fz_str)
                dz = float(dz_str)
            except ValueError:
                print(f"❌ Could not convert {filter.fz_param} or {filter.dz_param} to float in the file {path}.")
                continue

            # Change the values in the filter object
            filter.set_sinumerik_values(type=filter_type, time_constant=None, fn=fn, dn=dn, fz=fz, dz=dz)

        # Add the filter to the Drive object
        if application == "current_setpoint":
            drive.current_setpoint_filters.append(filter)
        elif application == "speed_setpoint":
            drive.speed_setpoint_filters.append(filter)
        elif application == "actual_speed":
            drive.actual_speed_filters.append(filter)
        else:
            print(f"❌ Unknown application {application} for filter {filter.type_param}.")
            continue

        # Save original filter num data
        drive.set_original_filter_amounts()

    return True

def extract_controller_data_from_content(content, path, drive: Drive):
    # ===== Read CONTROLLER params in config.py from the archive file =====

    # Create Controller Objects
    controllers = config.drive_controllers_list

    for controller in controllers:
        controller = deepcopy(controller)  # Create a copy of the controller object

        # Create a new parameter list, which will have [*n*] replaced with the actual index
        new_param_list = []

        # Read the parameters for the controller
        for param in controller.param_list:
            
            if param.param_type == "normal" and isinstance(param, Parameter):
                if "[*n*]" in param.param_str:
                    template_str = param.param_str           # preserve the wildcard template
                    base_param = param                       # preserve the original object

                    for n in range(MAX_PARAM_INDEX):
                        key = template_str.replace("[*n*]", f"[{n}]")

                        value = search_params_in_content(content, key)
                        if value is None:
                            break

                        p = deepcopy(base_param)
                        p.param_str = key
                        p.set_value(value, original=True)
                        new_param_list.append(p)

                else:
                    # Read the parameter value
                    value = search_params_in_content(content, param.param_str)
                    if value is None:
                        print(f"❌ Could not find {param.param_str} in the file {path}.")
                        continue

                    # Work on a per-drive copy to avoid shared state
                    p = deepcopy(param)
                    p.set_value(value, original=True)
                    new_param_list.append(p)
            
            elif param.param_type == "bitconfig" and isinstance(param, ParamBitconfig):
                # Read the parameter value
                value = search_params_in_content(content, param.param_str)
                if value is None:
                    print(f"❌ Could not find {param.param_str} in the file {path}.")
                    continue

                # Convert to integer and build bit list using a per-drive copy
                try:
                    raw_int = int(value.replace('H', '').replace("'", "").strip(), 16)
                except ValueError:
                    print(f"❌ Could not convert {param.param_str} value '{value}' to bit list in the file {path}.")
                    continue

                p = deepcopy(param)
                p.og_value = raw_int
                p.value = raw_int
                bit_count = len(p.bit_meanings_list)

                # If the param class supports it, reset bits before setting
                if hasattr(p, 'reset_bits') and callable(getattr(p, 'reset_bits')):
                    p.reset_bits()

                for b in range(bit_count):
                    p.set_bit(b, (raw_int >> b) & 1)

                new_param_list.append(p)

            elif param.param_type == "adaptation_plot" and isinstance(param, AdaptationPlotParams):
                new_param_list.append(param)  # Keep the adaptation plot param as is
            else:
                print(f"❌ Unknown parameter type {param.param_type}.")

        # Replace the old parameter list with the new one
        controller.param_list = new_param_list
        drive.controllers.append(controller)

    return True