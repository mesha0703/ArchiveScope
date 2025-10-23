import os
import numpy as np

from PySide6.QtWidgets import QMessageBox, QApplication
import sys

import core.sinumerik_components as sinumerik_components
from core.read_dif import read_file_from_zip, copy_zip_with_changes
from core.manage_archive_content import change_params_in_content
import config

def export_archive(archive, original_archive, export_path):

    if not os.path.isfile(archive.path):
        error_message = f"Archive file does not exist: {archive.path}"
        print(error_message)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Export Error")
        msg_box.setText(error_message)
        msg_box.exec_()
        return

    if os.path.abspath(export_path) == os.path.abspath(archive.path):
        error_message = "Export path cannot be the same as the archive path."
        print(error_message)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Export Error")
        msg_box.setText(error_message)
        msg_box.exec_()
        return

    print("\n----------------------------------------")
    print(f"Exporting archive \"{archive.name}\" to \"{export_path}\"...\n")

    # Dict where all changes for each path will be stored
    patches = {}

    # Find which archive parameters have been changed
    for i, drive in enumerate(archive.drives):

        # Dictionary to keep track of changed parameters in the drive content
        params_change_dict = {}

        # List to keep track of drive errors. If they are any error, they will be shown in a qt warning dialog
        error_log = []

        # Open the drive file
        drive_content_raw = read_file_from_zip(archive.path, drive.path)

        if drive_content_raw is None:
            error_log.append(f"Failed to read drive file: {drive.path}")
            print(error_log[-1])
            continue
        
        # Check number of active current setpoint filters
        num_active_current_setpoint_filters = drive.num_active_current_setpoint_filters
        og_num_active_current_setpoint_filters = original_archive.drives[i].num_active_current_setpoint_filters
        if num_active_current_setpoint_filters != og_num_active_current_setpoint_filters:
            print(f"Drive {drive.name} has changed number of active current setpoint filters.")
            print(f"Original: {og_num_active_current_setpoint_filters}, New: {num_active_current_setpoint_filters}")

            # Change the parameter in the drive content
            if num_active_current_setpoint_filters <= 4:
                # Change the parameter for num of active filters 1-4
                num_active_current_setpoint_filters_bin = ""
                for i in range(num_active_current_setpoint_filters):
                    num_active_current_setpoint_filters_bin = "1" + num_active_current_setpoint_filters_bin

                num_active_current_setpoint_filters_dec = int(num_active_current_setpoint_filters_bin, 2)
                num_active_current_setpoint_filters_hex = format(num_active_current_setpoint_filters_dec, "X")
                params_change_dict[config.PARAM_NUM_ACTIVATED_FILTERS_1_4] = f"'H{num_active_current_setpoint_filters_hex}'"

            else:
                # Change the parameter for num of active filters 1-4 to 4 
                params_change_dict[config.PARAM_NUM_ACTIVATED_FILTERS_5_10] = "'HF'"

                num_active_current_setpoint_filters_5_10 = num_active_current_setpoint_filters - 4
                
                if num_active_current_setpoint_filters_5_10 < 0:
                    error_log.append(f"Invalid number of active current setpoint filters 5-10 \
                                     for param {config.PARAM_NUM_ACTIVATED_FILTERS_5_10}: \
                                        {num_active_current_setpoint_filters_5_10}. It must be >= 0.")
                    print(error_log[-1])
                    continue

                elif num_active_current_setpoint_filters_5_10 > 6:
                    error_log.append(f"Invalid number of active current setpoint filters 5-10 \
                                     for param {config.PARAM_NUM_ACTIVATED_FILTERS_5_10}: \
                                        {num_active_current_setpoint_filters_5_10}. It must be <= 6.")
                    print(error_log[-1])
                    continue

                else:
                    # Convert value into right format
                    num_active_current_setpoint_filters_5_10_bin = ""
                    for i in range(num_active_current_setpoint_filters_5_10):
                        num_active_current_setpoint_filters_5_10_bin = "1" + num_active_current_setpoint_filters_5_10_bin
                    num_active_current_setpoint_filters_5_10_dec = int(num_active_current_setpoint_filters_5_10_bin, 2)
                    num_active_current_setpoint_filters_5_10_hex = format(num_active_current_setpoint_filters_5_10_dec, "X")

                    # Change the parameter for num of active filters 5-10
                    params_change_dict[config.PARAM_NUM_ACTIVATED_FILTERS_5_10] = f"'H{num_active_current_setpoint_filters_5_10_hex}'"

        # ===== Exporting the drive content =====

        # Check each filter in the drive
        filter_lists = [
            ("current_setpoint_filters", drive.current_setpoint_filters, original_archive.drives[i].current_setpoint_filters),
            ("speed_setpoint_filters", drive.speed_setpoint_filters, original_archive.drives[i].speed_setpoint_filters),
            ("actual_speed_filters", drive.actual_speed_filters, original_archive.drives[i].actual_speed_filters)
        ]

        for filter_name, filter_list, og_filter_list in filter_lists:
            for j, filter in enumerate(filter_list):
                # If the filter is not initialized in the original archive, define it as None
                if j >= len(og_filter_list):
                    og_filter = None
                else:
                    og_filter = og_filter_list[j]
            for j, filter in enumerate(filter_list):
                # If the filter is not initialized in the original archive, define it as None
                if j >= len(og_filter_list):
                    og_filter = None
                else:
                    og_filter = og_filter_list[j]

                # Check if the filter type has changed
                if (og_filter is None and filter.type is not None)\
                    or (og_filter is not None and values_differ(filter.type, og_filter.type)):
                    print(f"Filter {j+1} in drive {drive.name} has changed type to {filter.type}.")
                    params_change_dict[filter.type_param] = f"{np.int16(filter.type)}"

                if (og_filter is None and filter.time_constant is not None)\
                    or (og_filter is not None and values_differ(filter.time_constant, og_filter.time_constant)):
                    print(f"Filter {j+1} in drive {drive.name} has changed time constant to {filter.time_constant}.")
                    params_change_dict[filter.time_constant_param] = format_float32(filter.time_constant)

                if (og_filter is None and filter.fn is not None)\
                    or (og_filter is not None and values_differ(filter.fn, og_filter.fn)):
                    print(f"Filter {j+1} in drive {drive.name} has changed fn to {filter.fn}.")
                    params_change_dict[filter.fn_param] = format_float32(filter.fn)

                if (og_filter is None and filter.dn is not None)\
                    or (og_filter is not None and values_differ(filter.dn, og_filter.dn)):
                    print(f"Filter {j+1} in drive {drive.name} has changed dn to {filter.dn}.")
                    params_change_dict[filter.dn_param] = format_float32(filter.dn)

                if (og_filter is None and filter.fz is not None)\
                    or (og_filter is not None and values_differ(filter.fz, og_filter.fz)):
                    print(f"Filter {j+1} in drive {drive.name} has changed fz to {filter.fz}.")
                    params_change_dict[filter.fz_param] = format_float32(filter.fz)

                if (og_filter is None and filter.dz is not None)\
                    or (og_filter is not None and values_differ(filter.dz, og_filter.dz)):
                    print(f"Filter {j+1} in drive {drive.name} has changed dz to {filter.dz}.")
                    params_change_dict[filter.dz_param] = format_float32(filter.dz)

                if (og_filter is None and filter.actual_speed_filter_active is not None)\
                    or (og_filter is not None and values_differ(filter.actual_speed_filter_active, og_filter.actual_speed_filter_active)):
                    print(f"Filter {j+1} in drive {drive.name} has changed activation to {filter.actual_speed_filter_active}.")
                    params_change_dict[filter.activate_param] = f"{np.int16(filter.actual_speed_filter_active)}"
         
        # ===== Exporting the controller content =====
        for controller in drive.controllers:

            for param in controller.param_list:
                
                if param.param_type == "adaptation_plot":
                    # Skip adaptation plot parameters, they are only used for visualization
                    continue
                
                # Check if the parameter has changed
                if param.value != param.og_value:
                    print(f"Parameter {param.param_str} in drive {drive.name} has changed from {param.og_value} to {param.value}.")
                    if param.var_type_str == "float32":
                        params_change_dict[param.param_str] = format_float32(param.value)
                    elif param.var_type_str == "int32":
                        params_change_dict[param.param_str] = f"{np.int32(param.value)}"
                    elif param.var_type_str == "uint16":
                        params_change_dict[param.param_str] = f"{np.uint16(param.value)}"
                    elif param.var_type_str == "bool":
                        params_change_dict[param.param_str] = f"{np.int16(param.value)}"
                    elif param.var_type_str == "uint32":
                        params_change_dict[param.param_str] = f"{np.uint32(param.value)}"
                    else:
                        print(f"Unknown parameter type for {param.param_str} in drive {drive.name}. Skipping export.")

        # ===== Change parameters in the drive content ====
        if params_change_dict:

            # Change the parameters in the drive content
            new_content, successfully_changed_dict = change_params_in_content(drive_content_raw, params_change_dict)
            
            # Check whether all parameters were successfully changed
            for param in successfully_changed_dict:
                if successfully_changed_dict[param] == False:
                    error_log.append(f"Failed to change parameter {param} in drive {drive.name}.")
                    print(error_log[-1])

            # If there are errors in the error log, show a Qt warning dialog
            if error_log:
                error_message = "\n".join(error_log)
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Warning)
                msg_box.setWindowTitle("Export Errors")
                msg_box.setText("The following errors occurred during the export process:")
                msg_box.setInformativeText(error_message)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Abort | QMessageBox.StandardButton.Ignore)
                msg_box.setDefaultButton(QMessageBox.StandardButton.Abort)

                user_response = msg_box.exec_()

                if user_response == QMessageBox.StandardButton.Abort:
                    print("User chose to abort the export process.")
                    return
                else:
                    print("User chose to continue despite the errors.")

            # Save in patch dict
            patches[drive.path] = new_content

    # ===== Exporting the archive content =====
    if patches:
        print("Changes detected, exporting archive...")

        # Copy the original archive and apply changes
        copy_zip_with_changes(archive.path, export_path, patches, encoding="utf-8", create_missing=False)

        QMessageBox.information(
            None,
            "Export Successful",
            f"Archive exported successfully to:\n{export_path}",
            QMessageBox.StandardButton.Ok
        )
        
        print(f"Archive exported successfully to: {export_path}")

    else:
        print("No changes detected, nothing to export.")
        QMessageBox.information(
            None,
            "No Changes Detected",
            "No changes were detected in the archive. Nothing to export.",
            QMessageBox.StandardButton.Ok
        )
        return

        
def format_float32(value, decimals=8):
    """Format a float32 value as a string with fixed decimals."""
    if value is None:
        return "None"
    return f"{np.float32(value):.{decimals}f}"


def values_differ(a, b, tol=1e-6):
    """Return True if values differ beyond tolerance."""
    # Both None → no change
    if a is None and b is None:
        return False

    # One None, one not → change
    if (a is None) != (b is None):
        return True

    # Floats: compare with tolerance
    try:
        if isinstance(a, float) or isinstance(b, float):
            return abs(float(a) - float(b)) > tol
    except (ValueError, TypeError):
        pass

    # Fallback: direct compare
    return a != b