from PySide6 import QtWidgets as qtw
from PySide6.QtCore import QSize, Qt, Signal, QEvent
from PySide6.QtCore import QModelIndex
from ui.drag_and_drop_surface import Ui_Form as Ui_ArchiveDragAndDrop
from ui.drive_info import Ui_Form as Ui_ArchiveDriveInfo
from ui.cw_filter import Ui_Form as Ui_CwFilter
from ui.single_controller_frame import Ui_fr_controller as Ui_ControllerFrame
from ui.all_controllers_info_frame import Ui_Frame as Ui_ControllerInfoFrame
from ui.bode_plot_widget import BodePlotWidget
from ui.param_frame import Ui_fr_param as Ui_ParamFrame
from ui.param_frame_bitconfig import Ui_fr_param as Ui_ParamFrameBitconfig
from ui.bitconfig_single_bit import Ui_Frame as Ui_BitconfigSingleBit
from ui.adaptation_plot import GraphParams as AdaptationGraphParams
from ui.adaptation_plot import TwoAxisZonesPlot as Adaptationplot
from ui.cw_kinematic_tree import Ui_Frame as Ui_CwKinematicTree

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon, QPalette, QColor, QPainter, QFontMetrics, QCursor, QStandardItemModel, QStandardItem

from core import sinumerik_components
from core.manipulate_dsf import parse_filters_from_dsf
from core.manipulate_arc import parse_filters_from_arc
import config
from copy import deepcopy
import math
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from core.kinematics import KinematicModel, AXIS_LIN, AXIS_ROT

class ArchiveDragAndDropSurface(qtw.QWidget, Ui_ArchiveDragAndDrop):
    # Setup a signal which emits when an archive is added
    archive_added_signal = Signal(sinumerik_components.Archive)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect the button to open file dialog
        self.pb_browseFiles.clicked.connect(self.open_file_dialog)

        self.fr_dragAndDropZone.fileDropped.connect(self.handle_dropped_file)

    def handle_dropped_file(self, file_path: str):
        print(f"📦 Handling dropped file: {file_path}")
        archive = sinumerik_components.Archive(file_path)

        if archive.type == "UNKNOWN":
            qtw.QMessageBox.critical(self, "Kein Archiv.", "Die eingefügte Datei ist kein gültiges Archiv.")
            print("❌ Invalid dropped archive.")
            return

        self.archive_added_signal.emit(archive)

        # Hide Drop Widget
        self.w_addArchive.hide()
        self.hide()

    def open_file_dialog(self):
        file_path, _ = qtw.QFileDialog.getOpenFileName(
            self,
            "Choose a File",
            "",                      # Start directory ("" = current)
            "Archive Files (*.dsf *.arc);;All Files (*)"
        )

        if file_path:
            print(f"Selected file: {file_path}")

            archive = sinumerik_components.Archive(file_path)

            # Check if the archive is valid
            if archive.type == "UNKNOWN":
                # Show an error message if the archive is invalid
                qtw.QMessageBox.critical(
                    self,
                    "Kein Archiv.",
                    "Die ausgewählte Datei ist kein gültiges Archiv."
                )

                print("Invalid archive file.")
                return

            self.archive_added_signal.emit(archive)

            # Hide Drag & Drop surface - this widget can be used again when this archive has been freed
            self.w_addArchive.hide()

            # Hide this widget and emit signal to notify that an archive has been added
            self.hide()

        else:
            print("No file selected.")


class CwArchiveDriveInfo(qtw.QWidget, Ui_ArchiveDriveInfo):
    def __init__(self, application):
        super().__init__()
        self.setupUi(self)

        self._updating_drive_ui = False

        self.archive = None  # This will hold the current archive
        self.application = application  # Can be "current_setpoint", "speed_setpoint" or "actual_speed"
        self.current_drive = None
        self.current_drive_index = 0
        self.num_active_current_setpoint_filters = 0
        self.filter_list = []
            
        # Initialize layout for the filters
        self.filters_layout = qtw.QVBoxLayout(self.w_filters)
        self.plot_layout = qtw.QVBoxLayout(self.w_plot)

        # Connect the combo box for drive names to update the UI when a different drive is selected
        self.cb_driveNames.currentIndexChanged.connect(self.update_drive_ui)
        
        # Connect "more info" button to toggle visibility of the "more info" section
        self.pb_moreInfo.clicked.connect(self.pb_moreInfo_clicked)

        # Hide the "more info" section initially
        self.w_moreInfo.hide()

        # Hide reset num of filters button
        self.pb_numActiveFilters.hide()

    def activate_compare_mode(self, compare_archive_widget):

        if self.archive is None or compare_archive_widget is None:
            print("❌ Cannot activate compare mode. One of the archives is not set.")
            self.compare_mode = False
            qtw.QMessageBox.critical(self, "Vergleichsmodus Fehler.", "Eins der Archive wurde nicht initalisiert.")
            return

        # Connect scrollbars
        self.sa_main.verticalScrollBar().valueChanged.connect(compare_archive_widget.sa_main.verticalScrollBar().setValue)
        self.sa_main.verticalScrollBar().setValue(0)

    def deactivate_compare_mode(self, compare_archive_widget):

        # Disconnect scrollnars
        self.sa_main.verticalScrollBar().valueChanged.disconnect(compare_archive_widget.sa_main.verticalScrollBar().setValue)

    def update_archive(self, archive):
        """
        Initialize the widget with the given archive.
        This method should be called after an archive is added.
        """
        self.archive = archive

        # Set the Archive name in the label
        self.lbl_archiveNameValue.setText(f"{archive.name}")

        # Parse filters from the archive, if archive is not innitialized
        if not archive.is_innit:
            if archive.type == "DSF":
                parse_filters_from_dsf(archive)
            elif archive.type == "ARC":
                parse_filters_from_arc(archive)
            else:
                print(f"❌ Unknown archive type: {archive.type}")

        # Populate drive names without emitting signals during changes
        self.cb_driveNames.blockSignals(True)
        self.cb_driveNames.clear()
        for drive in self.archive.drives:
            self.cb_driveNames.addItem(drive.name)
        self.cb_driveNames.blockSignals(False)

        # Update the UI with the parsed filters
        update_drive_ui_success = self.update_drive_ui(0)
        if update_drive_ui_success:
            # Show the widget, if the updating was successful
            self.show()

            # Connect once; avoid duplicates & disconnect warnings
            self.cb_numActiveFilters.currentIndexChanged.connect(self.filter_amount_changed, Qt.ConnectionType.UniqueConnection)
        else:
            print("❌ Failed to update UI with filters.")

    def update_drive_ui(self, drive_index):
        """
        Update the UI elements with the filters parsed from the archive.
        This method should be called after parsing filters from the archive.
        """

        # Prevent re-entrant calls while we are updating UI programmatically
        if self._updating_drive_ui:
            return False
        self._updating_drive_ui = True

        if not self.archive:
            print(f"❌ Cannot update drive UI. No archive loaded for tab {self.application}.")
            qtw.QMessageBox.critical(self, "Archiv Fehler", "Archiv wurde nicht initalisiert.")
            self._updating_drive_ui = False
            return False

        if not self.archive.drives:
            print(f"❌ No drives available for tab {self.application}.")
            # Avoid recursive currentIndexChanged while we set a placeholder item
            self.cb_driveNames.blockSignals(True)
            self.cb_driveNames.clear()
            self.cb_driveNames.addItem("No drives available.")
            self.cb_driveNames.blockSignals(False)
            self._updating_drive_ui = False
            self.pb_moreInfo.hide()
            self.w_activeFiltersNum.hide()
            return False

        if drive_index < 0 or drive_index >= len(self.archive.drives):
            print(f"❌ Invalid drive index: {drive_index} in tab {self.application}.")
            self._updating_drive_ui = False
            return False

        self.current_drive = self.archive.drives[drive_index]
        self.current_drive_index = drive_index
        self.num_active_current_setpoint_filters = self.current_drive.num_active_current_setpoint_filters

        # Update "more info"
        self.lbl_driveMoreInfoLeft.setText("Speicherort im Archiv:")
        self.lbl_driveMoreInfoRight.setText(self.current_drive.path)

        # Initialize filter list based on the application type
        if self.application == "current_setpoint":
            self.filter_list = self.current_drive.current_setpoint_filters
            MAX_ACTIVE_FILTERS = config.MAX_ACTIVE_CURRENT_SETPOINT_FILTERS
        elif self.application == "speed_setpoint":
            self.filter_list = self.current_drive.speed_setpoint_filters
            MAX_ACTIVE_FILTERS = config.MAX_ACTIVE_SPEED_SETPOINT_FILTERS
        elif self.application == "actual_speed":
            self.filter_list = self.current_drive.actual_speed_filters
            MAX_ACTIVE_FILTERS = config.MAX_ACTIVE_ACTUAL_SPEED_FILTERS
        else:
            print(f"❌ Unknown application type: {self.application}")
            self._updating_drive_ui = False
            return False

        self.cb_numActiveFilters.blockSignals(True)
        self.cb_numActiveFilters.clear()
        for i in range(0, MAX_ACTIVE_FILTERS + 1):
            self.cb_numActiveFilters.addItem(str(i))
        self.cb_numActiveFilters.blockSignals(False)

        # If the application is current_setpoint, read the number of active filters from the parameters
        update_filters_ui_result = False
        if self.application == "current_setpoint":
            n = self.num_active_current_setpoint_filters
            if n is None or n < 0 or n > MAX_ACTIVE_FILTERS: n = 0
            self.current_drive.num_active_current_setpoint_filters = n
            self.cb_numActiveFilters.setCurrentIndex(n)

            # Update filters UI with the current drive's filters
            update_filters_ui_result = self.update_filters_ui()
        
        elif self.application == "speed_setpoint":
            # For speed setpoint, we always have 2 filters
            self.cb_numActiveFilters.setCurrentIndex(2)
            update_filters_ui_result = self.update_filters_ui()

        elif self.application == "actual_speed":
            # For actual speed, we always have 1 filter
            self.cb_numActiveFilters.setCurrentIndex(1)
            update_filters_ui_result = self.update_filters_ui()

        else:
            print("Compare mode is off. Using default palette.")

        if not update_filters_ui_result:
            print("❌ Failed to update filters UI.")
            self._updating_drive_ui = False
            return False
        
        # Update bode plot after drive and its filters are loaded
        self.update_bode_plot()
        self._updating_drive_ui = False
        return True
    
    def update_bode_plot(self):
        if not self.current_drive:
            print("❌ No current drive selected.")
            return
        
        filter_list = [f for f in self.filter_list if ((f.application == self.application) and f.show_bode_plot)]

        # Remove existing widgets from the plot layout
        for i in reversed(range(self.plot_layout.count())):
            widget = self.plot_layout.itemAt(i).widget()
            if widget is not None:
                widget.hide()
                self.plot_layout.removeWidget(widget)
                # Delete the widget to free up memory
                widget.deleteLater()

        # Update Bode plot
        self.main_plot_widget = BodePlotWidget(filter_list)
        self.plot_layout.addWidget(self.main_plot_widget)

    def update_filters_ui(self):
        """
        Update the filters UI based on the selected drive and filter index.
        """

        if self.archive is None:
            print("❌ Cannot update filters UI. No archive loaded.")
            return False

        if self.current_drive is None:
            print("❌ Cannot update filters UI. No drive found in the archive.")
            return False
        
        # Clear the existing filters in the layout
        for i in reversed(range(self.filters_layout.count())):
            widget = self.filters_layout.itemAt(i).widget()
            if widget is not None:
                widget.hide()
                self.filters_layout.removeWidget(widget)
                # Delete the widget to free up memory
                widget.deleteLater()

        # Load filters into the UI
        for i, filter in enumerate(self.filter_list):
            # Load custom widget for each filter
            cw_filter = CwFilter(filter, self.application)

            # Set filter number
            cw_filter.lbl_filterN.setText(f"Filter {i+1}")

            # Add filter widget to the layout
            self.filters_layout.addWidget(cw_filter)

            # Connect changing visibility of the filter to the Bode plot
            cw_filter.cb_showFilter.stateChanged.connect(self.update_bode_plot)

            # ===== Color square widget =====

            # If the filter does not have a color, assign a standard color from the config
            if filter.color == [0, 0, 0]:
                filter.color = config.STANDARD_FILTER_COLORS[i % len(config.STANDARD_FILTER_COLORS)]

            # Change the color of the color square widget
            cw_filter.w_colorSquare.change_color(QColor(*filter.color))

            # Connect the update bode signal to the update_bode_plot method
            cw_filter.update_bode_signal.connect(self.update_bode_plot)

            # ===== Add Sinumerik parameters =====
            cw_filter.update_sinumerik_parameters_ui()

        return True

    def pb_moreInfo_clicked(self):
        """
        Toggle the visibility of the "more info" section.
        """

        # Check if the archive is loaded
        if not self.archive:
            print("❌ Cannot toggle more drive info visibility. No archive loaded.")
            return
        
        self.archive.show_more_drive_info = not self.archive.show_more_drive_info
        if self.archive.show_more_drive_info:
            self.w_moreInfo.show()
            self.pb_moreInfo.setIcon(QIcon(":/resources/arrow_drop_down_24dp.svg"))
        else:
            self.w_moreInfo.hide()
            self.pb_moreInfo.setIcon(QIcon(":/resources/arrow_right_24dp.svg"))

    def filter_amount_changed(self, index):
        """
        Handle changes in the filter amount (number of active filters).
        """

        print(f"Filter amount changed: {index}")

        if not self.archive or not self.current_drive:
            print("❌ Cannot change filter amount. No archive or drive found.")
            return
        
        # Update the number of active filters in the current drive
        if self.application == "current_setpoint":
            old_filter_count = self.current_drive.num_active_current_setpoint_filters
            print(f"Old filter count: {old_filter_count}, New filter count: {index}")

            # If the number of old filters is the same, do nothing
            if old_filter_count == index:
                return
            
            # If the number of old filters is smaller, remove the excess filters
            elif old_filter_count > index:
                self.filter_list = self.filter_list[:index]

            # Create new filters if the number of active filters is increased
            elif old_filter_count < index:
                print(f"Creating new current setpoint filters from index {old_filter_count} to {index}.")

                for i in range(old_filter_count, index):
                    # Create a new filter object based on the current application
                    new_filter = sinumerik_components.Filter(
                        application=self.application,
                        activate_param=None,
                        type_param=config.current_setpoint_filter_list[i]['type_param'],
                        time_constant_param=None,
                        fn_param= config.current_setpoint_filter_list[i]['fn_param'],
                        dn_param=config.current_setpoint_filter_list[i]['dn_param'],
                        fz_param=config.current_setpoint_filter_list[i]['fz_param'],
                        dz_param=config.current_setpoint_filter_list[i]['dz_param'],
                    )

                    # Initialize default values from config
                    new_filter.init_default_values()

                    # Add the new filter to the current drive's filter list
                    self.filter_list.append(new_filter)

            # Update the number of active filters in the current drive
            self.current_drive.num_active_current_setpoint_filters = index
        
        elif self.application == "speed_setpoint":
            old_filter_count = len(self.filter_list)

            if old_filter_count == index:
                return # No change needed

            elif old_filter_count > index:
                # Remove the excess filters
                self.filter_list = self.filter_list[:index]

            elif old_filter_count < index:
                # Create new filters
                print(f"Creating new speed setpoint filters from index {old_filter_count} to {index}.")
                for i in range(old_filter_count, index):
                    new_filter = sinumerik_components.Filter(
                        application=self.application,
                        activate_param=None,
                        type_param=config.speed_setpoint_filter_list[i]['type_param'],
                        time_constant_param=config.speed_setpoint_filter_list[i]['time_constant_param'],
                        fn_param=config.speed_setpoint_filter_list[i]['fn_param'],
                        dn_param=config.speed_setpoint_filter_list[i]['dn_param'],
                        fz_param=config.speed_setpoint_filter_list[i]['fz_param'],
                        dz_param=config.speed_setpoint_filter_list[i]['dz_param'],
                    )

                    # Initialize default values from config
                    new_filter.init_default_values()

                    # Add the new filter to the current drive's filter list
                    self.filter_list.append(new_filter)

        elif self.application == "actual_speed":
            old_filter_count = len(self.filter_list)

            if old_filter_count == index:
                return  # No change needed
            
            # There is only max one actual speed filter
            elif index == 0:
                self.filter_list = []

            elif index == 1:
                # Recover the actual speed filter from the original archive if possible
                if self.archive.original_copy and self.archive.original_copy.drives[self.current_drive_index].actual_speed_filters:
                    self.filter_list = [self.archive.original_copy.drives[self.current_drive_index].actual_speed_filters[0]]
                    print("Recovered actual speed filter from the original archive.")
                else:
                    # Create a new actual speed filter
                    new_filter = sinumerik_components.Filter(
                        application=self.application,
                        activate_param=config.actual_speed_filter['activate_param'],
                        type_param=config.actual_speed_filter['type_param'],
                        time_constant_param=None,  # Actual speed filter does not have a time constant
                        fn_param=config.actual_speed_filter['fn_param'],
                        dn_param=config.actual_speed_filter['dn_param'],
                        fz_param=config.actual_speed_filter['fz_param'],
                        dz_param=config.actual_speed_filter['dz_param'],
                    )

                    # Initialize default values from config
                    new_filter.init_default_values()

                    # Add the new filter to the current drive's filter list
                    self.filter_list = [new_filter]

                    print("Created a new actual speed filter.")

        # Check if the value differs from the original
        og_filter_amount = 0
        if self.application == "current_setpoint": og_filter_amount = self.current_drive.original_num_current_setpoint_filters
        elif self.application == "speed_setpoint": og_filter_amount = self.current_drive.original_num_speed_setpoint_filters
        elif self.application == "actual_speed": og_filter_amount = self.current_drive.original_num_actual_speed_filters
        if len(self.filter_list) != og_filter_amount:
            # Change color
            palette = self.cb_numActiveFilters.palette()
            palette.setColor(QPalette.ColorRole.Text, QColor(*config.VALUE_CHANGED_TEXT_COLOR))
            self.cb_numActiveFilters.setPalette(palette)

            # Show reset button
            self.pb_numActiveFilters.clicked.connect(self.reset_num_active_filters, Qt.ConnectionType.UniqueConnection)
            self.pb_numActiveFilters.show()
        
        else:
            # Set to default color
            palette = self.cb_numActiveFilters.palette()
            palette.setColor(QPalette.ColorRole.Text, QColor(*config.DEFAULT_TEXT_COLOR))
            self.cb_numActiveFilters.setPalette(palette)

            self.pb_numActiveFilters.hide()

        # Update UI
        self.update_filters_ui()

        # Update Bode plot
        self.update_bode_plot()

    def reset_num_active_filters(self):
        if self.current_drive:
            if self.application == "current_setpoint":
                self.cb_numActiveFilters.setCurrentIndex(self.current_drive.original_num_current_setpoint_filters)
            elif self.application == "speed_setpoint":
                self.cb_numActiveFilters.setCurrentIndex(self.current_drive.original_num_speed_setpoint_filters)
            elif self.application == "actual_speed":
                self.cb_numActiveFilters.setCurrentIndex(self.current_drive.original_num_actual_speed_filters)

        self.pb_numActiveFilters.hide()


class CwFilter(qtw.QWidget, Ui_CwFilter):
    update_bode_signal = Signal()

    def __init__(self, filter_obj, application, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.filter = filter_obj
        self.original_filter = deepcopy(filter_obj)  # Keep a copy of the original filter
        self.application = application

        self.filter_type0 = "Tiefpass PT1"
        self.filter_type1 = "Tiefpass PT2"
        self.filter_type2 = "Allg. 2. Ordnung"
        self.filter_type_unknown = "Unbekannt"

        # ===== Initialize the filter settings in the UI =====

        # Set the filter type string using a mapping
        type_map = {
            0: self.filter_type0,
            1: self.filter_type1,
            2: self.filter_type2
        }
        self.type_str = type_map.get(filter_obj.type, self.filter_type_unknown)

        # Set the filter type in the UI
        self.cb_filterType.clear()
        if self.type_str != self.filter_type_unknown:
            # Only Current Setpoint and Actual Speed applications have the filter type 0 (Low-pass PT1)
            if self.application != "current_setpoint" and self.application != "actual_speed":
                self.cb_filterType.addItem(self.filter_type0)
            self.cb_filterType.addItem(self.filter_type1)
            self.cb_filterType.addItem(self.filter_type2)
            self.cb_filterType.setCurrentText(self.type_str)

        # Change the filter type using the change_filter_type method
        self.change_filter_type(self.type_str)

        self.param_objects = {
            "type": ParamObject("type", type_map[self.filter.type], type_map[self.original_filter.type], None, None),
            "time_constant": ParamObject("timeConstant", self.filter.time_constant, config.TIME_CONSTANT_DEFAULT, config.MIN_TIME_CONSTANT, config.MAX_TIME_CONSTANT),
            "res_freq": ParamObject("resFreq", self.filter.f_res, config.FREQ_DEFAULT, config.MIN_FREQ, config.MAX_FREQ),
            "damping": ParamObject("damping", self.filter.damping, config.DAMPING_DEFAULT, config.MIN_DAMPING, config.MAX_DAMPING),
            "block_freq": ParamObject("blockFreq", self.filter.f_block, config.FREQ_DEFAULT, config.MIN_BLOCK_FREQ, config.MAX_BLOCK_FREQ),
            "band_freq": ParamObject("bandFreq", self.filter.f_band, config.DEFAULT_BAND_FREQ, config.MIN_BAND_FREQ, config.MAX_BAND_FREQ),
            "notch_depth": ParamObject("notchDepth", self.filter.notch_depth, config.DEFAULT_NOTCH_DEPTH, config.MIN_NOTCH_DEPTH, config.MAX_NOTCH_DEPTH),
            "attenuation": ParamObject("attenuation", self.filter.attenuation, config.DEFAULT_ATTENUATION, config.MIN_ATTENUATION, config.MAX_ATTENUATION),
        }

        # Bind widgets to update method
        self.dsb_timeConstant.setValue(self.param_objects["time_constant"].current_value)
        self.dsb_timeConstant.valueChanged.connect(lambda val: self.on_param_change("time_constant", val))
        self.pb_time_constant = self.pb_timeConstant
        self.pb_time_constant.hide()
        self.pb_time_constant.clicked.connect(lambda: self.reset_param("time_constant", self.dsb_timeConstant, self.pb_time_constant))

        self.dsb_resFreq.setValue(self.param_objects["res_freq"].current_value)
        self.dsb_resFreq.valueChanged.connect(lambda val: self.on_param_change("res_freq", val))
        self.pb_res_freq = self.pb_resFreq
        self.pb_res_freq.hide()
        self.pb_res_freq.clicked.connect(lambda: self.reset_param("res_freq", self.dsb_resFreq, self.pb_res_freq))

        self.dsb_damping.setValue(self.param_objects["damping"].current_value)
        self.dsb_damping.valueChanged.connect(lambda val: self.on_param_change("damping", val))
        self.pb_damping = self.pb_damping
        self.pb_damping.hide()
        self.pb_damping.clicked.connect(lambda: self.reset_param("damping", self.dsb_damping, self.pb_damping))

        self.dsb_blockFreq.setValue(self.param_objects["block_freq"].current_value)
        self.dsb_blockFreq.valueChanged.connect(lambda val: self.on_param_change("block_freq", val))
        self.pb_block_freq = self.pb_blockFreq
        self.pb_block_freq.hide()
        self.pb_block_freq.clicked.connect(lambda: self.reset_param("block_freq", self.dsb_blockFreq, self.pb_block_freq))

        self.dsb_bandFreq.setValue(self.param_objects["band_freq"].current_value)
        self.dsb_bandFreq.valueChanged.connect(lambda val: self.on_param_change("band_freq", val))
        self.pb_band_freq = self.pb_bandFreq
        self.pb_band_freq.hide()
        self.pb_band_freq.clicked.connect(lambda: self.reset_param("band_freq", self.dsb_bandFreq, self.pb_band_freq))

        self.dsb_notchDepth.setValue(self.param_objects["notch_depth"].current_value)
        self.dsb_notchDepth.valueChanged.connect(lambda val: self.on_param_change("notch_depth", val))
        self.pb_notch_depth = self.pb_notchDepth
        self.pb_notch_depth.hide()
        self.pb_notch_depth.clicked.connect(lambda: self.reset_param("notch_depth", self.dsb_notchDepth, self.pb_notch_depth))

        self.dsb_attenuation.setValue(self.param_objects["attenuation"].current_value)
        self.dsb_attenuation.valueChanged.connect(lambda val: self.on_param_change("attenuation", val))
        self.pb_attenuation.hide()
        self.pb_attenuation.clicked.connect(lambda: self.reset_param("attenuation", self.dsb_attenuation, self.pb_attenuation))

        # Ensure spin boxes do not show thousands group separators
        for sb in [
            self.dsb_timeConstant,
            self.dsb_resFreq,
            self.dsb_damping,
            self.dsb_blockFreq,
            self.dsb_bandFreq,
            self.dsb_notchDepth,
            self.dsb_attenuation,
        ]:
            if hasattr(sb, 'setGroupSeparatorShown'):
                sb.setGroupSeparatorShown(False)

        self.pb_type.hide()
        self.pb_type.clicked.connect(lambda: self.reset_param("type", self.cb_filterType, self.pb_type))

        # Connect the filter type combo box to the change_filter_type method
        self.cb_filterType.currentTextChanged.connect(self.change_filter_type)

        # Make sure the check box is active
        self.cb_showFilter.setChecked(filter_obj.show_bode_plot)

        # Connect the check box to the on_cb_showFilter_change method
        self.cb_showFilter.stateChanged.connect(self.on_cb_showFilter_change)

        # Init color square widget
        self.w_colorSquare = ColorSquare(initial_color=QColor())

        # Add color square to the layout
        self.w_color_layout = qtw.QVBoxLayout(self.w_colorPlaceholder)
        self.w_color_layout.setContentsMargins(0, 0, 0, 0)
        self.w_color_layout.setSpacing(0)
        self.w_color_layout.addWidget(self.w_colorSquare)

        # Connect the color square's color changed signal to the color_square_color_changed method
        self.w_colorSquare.color_changed_signal.connect(self.colorSquare_color_changed)

        # Connect the button to show Sinumerik parameters
        self.pb_showParam.clicked.connect(self.pb_showParam_clicked)

        # Initlially hide the Sinumerik parameters
        self.filter.show_param = False
        self.w_param.hide()

        # Connect all spin boxes to the value_changed method in a loop
        for spinbox in [
            self.dsb_timeConstant,
            self.dsb_resFreq,
            self.dsb_damping,
            self.dsb_blockFreq,
            self.dsb_bandFreq,
            self.dsb_notchDepth,
            self.dsb_attenuation,
        ]:
            spinbox.valueChanged.connect(self.value_changed)
    
    def on_param_change(self, name, value):
        print(f"Parameter '{name}' changed to {value}")

        param = self.param_objects[name]
        param.set_value(value)

        if not param.is_valid():
            print(f"❌ Invalid value for {name}")
            return

        # Update internal filter model
        if name == "time_constant":
            self.filter.set_sinumerik_values(time_constant=value)
        elif name == "res_freq":
            self.filter.set_sinumerik_values(fn=value)  # Update the filter's frequency
            self.filter.set_sinumerik_values(fz=value)
        elif name == "damping":
            self.filter.set_sinumerik_values(dn=value)
            self.filter.set_sinumerik_values(dz=value)
        elif name == "block_freq":
            self.filter.set_filter_values(f_block=value)  # Update the filter's block frequency
        elif name == "band_freq":
            self.filter.set_filter_values(f_band=value)  # Update the filter's band frequency
        elif name == "notch_depth":
            self.filter.set_filter_values(notch_depth=value)  # Update the filter's notch depth
        elif name == "attenuation":
            self.filter.set_filter_values(attenuation=value)  # Update the filter's attenuation
        else:
            print(f"❌ Unknown parameter name: {name}")
            return
        
        # UI feedback
        spinbox = getattr(self, f"dsb_{''.join([part[0].upper() + part[1:] if i > 0 else part for i, part in enumerate(name.split('_'))])}", None)
        if spinbox is None:
            # fallback: try lowercase
            spinbox = getattr(self, f"dsb_{name}", None)
        if spinbox:
            line_edit = spinbox.findChild(qtw.QLineEdit)
            if line_edit:
                palette = line_edit.palette()
                color = QColor(*config.VALUE_CHANGED_TEXT_COLOR if param.changed else config.DEFAULT_TEXT_COLOR)
                palette.setColor(QPalette.ColorRole.Text, color)
                line_edit.setPalette(palette)

        # Show/hide reset button logic
        reset_button = getattr(self, f"pb_{name}", None)
        if reset_button:
            if param.changed:
                reset_button.show()
            else:
                reset_button.hide()

        self.update_sinumerik_parameters_ui()
        self.update_bode_signal.emit()

    def reset_param(self, name, widget, button):
        param = self.param_objects[name]
        param.reset()
        
        # Handle QDoubleSpinBox
        if isinstance(widget, qtw.QDoubleSpinBox):
            widget.setValue(param.default_value)
            
            # Reset text color
            line_edit = widget.findChild(qtw.QLineEdit)
            if line_edit:
                palette = line_edit.palette()
                palette.setColor(QPalette.ColorRole.Text, QColor(*config.DEFAULT_TEXT_COLOR))
                line_edit.setPalette(palette)

        # Handle QComboBox
        elif isinstance(widget, qtw.QComboBox):
            # Try to match by value as string
            found = False
            for i in range(widget.count()):
                if str(widget.itemText(i)) == str(param.default_value):
                    widget.setCurrentIndex(i)
                    found = True
                    print(f"✅ Reset combo box {widget.objectName()} to value '{param.default_value}'")
                    break
            
            if not found:
                print(f"❌ Default value '{param.default_value}' not found in combo box {widget.objectName()}")

            # Reset text color
            palette = widget.palette()
            palette.setColor(QPalette.ColorRole.Text, QColor(*config.DEFAULT_TEXT_COLOR))
            widget.setPalette(palette)

        # Hide reset button
        button.hide()

        # Update internal filter model
        if name != "type":
            self.on_param_change(name, param.default_value)

    def change_filter_type(self, cb_chosen_str):
        """
        Change the filter type and update the UI accordingly.
        This method is connected to the filter type combo box.
        """

        if cb_chosen_str == self.filter_type0:
            new_type = 0
        elif cb_chosen_str == self.filter_type1:
            new_type = 1
        elif cb_chosen_str == self.filter_type2:
            new_type = 2
        else:
            print(f"❌ Unsupported filter type: {cb_chosen_str}")
            return

        self.filter.set_type(new_type)

        # If the new type is not the original one, make it different color and show a reset button
        palette = self.cb_filterType.palette()
        if new_type != self.original_filter.type:
            palette.setColor(QPalette.ColorRole.Text, QColor(*config.VALUE_CHANGED_TEXT_COLOR))
            self.pb_type.show()
        else:
            palette.setColor(QPalette.ColorRole.Text, QColor(*config.DEFAULT_TEXT_COLOR))  # reset to black text
            self.pb_type.hide()
        self.cb_filterType.setPalette(palette)

        if new_type == 0:
            # Low-pass PT1 filter
            self.w_PT2Filter.hide()
            self.w_otherFilterTypes.hide()
            self.w_PT1Filter.show()

            # Set the filter parameters in the UI

            # Read the time constant from the filter object
            time_constant = self.filter.time_constant
            if time_constant is None or time_constant < config.MIN_TIME_CONSTANT or time_constant > config.MAX_TIME_CONSTANT:
                time_constant = config.TIME_CONSTANT_DEFAULT  # Set to default if invalid
            self.dsb_timeConstant.setValue(time_constant)

        elif new_type == 1:
            # Low-pass PT2 filter
            self.w_PT1Filter.hide()
            self.w_otherFilterTypes.hide()
            self.w_PT2Filter.show()

            # Set the filter parameters
            fn = self.filter.fn
            dn = self.filter.dn

            if fn is None or fn < config.MIN_FREQ or fn > config.MAX_FREQ:
                fn = config.FREQ_DEFAULT  # Set to default if invalid
                self.filter.set_sinumerik_values(fn=fn)
            if dn is None or dn < config.MIN_DAMPING or dn > config.MAX_DAMPING:
                dn = config.DAMPING_DEFAULT  # Set to default if invalid
                self.filter.set_sinumerik_values(dn=dn)

            self.filter.f_res = self.filter.fn
            self.filter.damping = self.filter.dn

            self.dsb_resFreq.setValue(self.filter.f_res)
            self.dsb_damping.setValue(self.filter.damping)

        elif new_type == 2:
            # General second-order filter
            self.w_PT1Filter.hide()
            self.w_PT2Filter.hide()
            self.w_otherFilterTypes.show()

            # Set the filter parameters in the UI
            fn = self.filter.fn
            dn = self.filter.dn
            fz = self.filter.fz
            dz = self.filter.dz

            if fn is None or fn < config.MIN_FREQ or fn > config.MAX_FREQ:
                fn = config.FREQ_DEFAULT  # Set to default if invalid
                self.filter.set_sinumerik_values(fn=fn)
            if dn is None or dn < config.MIN_DAMPING or dn > config.MAX_DAMPING:
                dn = config.DAMPING_DEFAULT  # Set to default if invalid
                self.filter.set_sinumerik_values(dn=dn)
            if fz is None or fz < config.MIN_FREQ or fz > config.MAX_FREQ:
                fz = config.FREQ_DEFAULT  # Set to default if invalid
                self.filter.set_sinumerik_values(fz=fz)
            if dz is None or dz < config.MIN_DAMPING or dz > config.MAX_DAMPING:
                dz = config.DAMPING_DEFAULT  # Set to default if invalid
                self.filter.set_sinumerik_values(dz=dz)

            # Calculate the filter values
            self.filter.calculate_filter_values()

            # Set the values in the UI
            self.dsb_blockFreq.setValue(self.filter.f_block)
            self.dsb_bandFreq.setValue(self.filter.f_band)
            self.dsb_notchDepth.setValue(self.filter.notch_depth)
            self.dsb_attenuation.setValue(self.filter.attenuation)

        else:
            print(f"❌ Unsupported filter type {new_type}. Only PT1, PT2 and General second-order filters are supported.")
            return
        
        # Update UI
        self.update_sinumerik_parameters_ui()

        # Update Bode plot after changing the filter type
        self.update_bode_signal.emit()

    def value_changed(self):

        print(f"Filter type: {self.filter.type}, application: {self.application}")

        # Get all double spin boxes in the widget
        if self.filter.type == 0:  # Low-pass PT1 filter
            time_constant_value = self.dsb_timeConstant.value()
            if time_constant_value < config.MIN_TIME_CONSTANT or time_constant_value > config.MAX_TIME_CONSTANT:
                print(f"❌ Invalid time constant value: {time_constant_value}. Must be between {config.MIN_TIME_CONSTANT} and {config.MAX_TIME_CONSTANT}.")
                return
            
            # Update sinumerik parameters
            self.filter.set_sinumerik_values(time_constant=time_constant_value)

        elif self.filter.type == 1:  # Low-pass PT2 filter
            resFreq_value = self.dsb_resFreq.value()
            damping_value = self.dsb_damping.value()

            if resFreq_value < config.MIN_FREQ or resFreq_value > config.MAX_FREQ:
                print(f"❌ Invalid resonance frequency value: {resFreq_value}. Must be between {config.MIN_FREQ} and {config.MAX_FREQ}.")
                return
            if damping_value < config.MIN_DAMPING or damping_value > config.MAX_DAMPING:
                print(f"❌ Invalid damping value: {damping_value}. Must be between {config.MIN_DAMPING} and {config.MAX_DAMPING}.")
                return
            
            # Update filter parameters
            self.filter.f_res = resFreq_value
            self.filter.damping = damping_value

            # Update sinumerik parameters
            self.filter.set_sinumerik_values(fn=resFreq_value, dn=damping_value)

        elif self.filter.type == 2:  # Speed setpoint filter
            blockFreq_value = self.dsb_blockFreq.value()
            bandFreq_value = self.dsb_bandFreq.value()
            notchDepth_value = self.dsb_notchDepth.value()
            attenuation_value = self.dsb_attenuation.value()

            if blockFreq_value < config.MIN_BLOCK_FREQ or blockFreq_value > config.MAX_BLOCK_FREQ:
                print(f"❌ Invalid block frequency value: {blockFreq_value}. Must be between {config.MIN_BLOCK_FREQ} and {config.MAX_BLOCK_FREQ}.")
                return
            if bandFreq_value < config.MIN_BAND_FREQ or bandFreq_value > config.MAX_BAND_FREQ:
                print(f"❌ Invalid band frequency value: {bandFreq_value}. Must be between {config.MIN_BAND_FREQ} and {config.MAX_BAND_FREQ}.")
                return
            if notchDepth_value < config.MIN_NOTCH_DEPTH or notchDepth_value > config.MAX_NOTCH_DEPTH:
                print(f"❌ Invalid notch depth value: {notchDepth_value}. Must be between {config.MIN_NOTCH_DEPTH} and {config.MAX_NOTCH_DEPTH}.")
                return
            if attenuation_value < config.MIN_ATTENUATION or attenuation_value > config.MAX_ATTENUATION:
                print(f"❌ Invalid attenuation value: {attenuation_value}. Must be between {config.MIN_ATTENUATION} and {config.MAX_ATTENUATION}.")
                return
            
            # Update filter parameters
            self.filter.set_filter_values(
                f_block=blockFreq_value,
                f_band=bandFreq_value,
                notch_depth=notchDepth_value,
                attenuation=attenuation_value
            )

            print(f"Filter parameters updated: f_block={blockFreq_value}, f_band={bandFreq_value}, notch_depth={notchDepth_value}, attenuation={attenuation_value}")

            # Update sinumerik fn, dn, fz, dz parameters
            self.filter.calculate_type2_sinumerik_filter_values()

        # Update Bode plot
        self.update_bode_signal.emit()

        # Update Sinumerik parameters in the filter object
        self.update_sinumerik_parameters_ui()

    def colorSquare_color_changed(self, red, green, blue):
        # Update the filter color with the selected RGB values
        self.filter.color = [red, green, blue]

        # Send signal to update the Bode plot
        self.update_bode_signal.emit()

    def on_cb_showFilter_change(self, state):
        checked = self.cb_showFilter.isChecked()
        self.filter.show_bode_plot = checked

        # If the filter is checked, show the color widget, in which the user can select the color
        if checked:
            self.w_color.show()
        else:
            self.w_color.hide()

    def update_sinumerik_parameters_ui(self):
        """
        Update the Sinumerik (p...) parameters in the filter object.
        This method is called when the user changes the filter type or parameters and the values in the filter object are updated.
        """
        if not self.filter:
            print("❌ Cannot update Sinumerik parameters. Filter object not loaded.")
            return
        
        # Firstly hide all parameter labels and values
        self.lbl_param1.hide()
        self.lbl_param2.hide()
        self.lbl_param3.hide()
        self.lbl_param4.hide()
        self.lbl_param5.hide()

        self.lbl_param1Value.hide()
        self.lbl_param2Value.hide()
        self.lbl_param3Value.hide()
        self.lbl_param4Value.hide()
        self.lbl_param5Value.hide()

        # Update the filter parameters based on the current filter type
        if self.filter.type == 0: # Low-pass PT1 filter
            self.lbl_param1.setText(f"{self.filter.type_param} Typ")
            self.lbl_param2.setText(f"{self.filter.time_constant_param} Zeitkonstante")
            self.lbl_param1.show()
            self.lbl_param2.show()

            self.lbl_param1Value.setText(f"{self.filter.type}")
            self.lbl_param2Value.setText(f"{float(self.filter.time_constant):.4f}")
            self.lbl_param1Value.show()
            self.lbl_param2Value.show()
        
        elif self.filter.type == 1: # Low-pass PT2 filter
            self.lbl_param1.setText(f"{self.filter.type_param} Typ")
            self.lbl_param2.setText(f"{self.filter.fn_param} Nenner-Frequenz")
            self.lbl_param3.setText(f"{self.filter.dn_param} Nenner-Dämpfung")
            self.lbl_param1.show()
            self.lbl_param2.show()
            self.lbl_param3.show()

            self.lbl_param1Value.setText(f"{self.filter.type}")
            self.lbl_param2Value.setText(f"{float(self.filter.fn):.4f}")
            self.lbl_param3Value.setText(f"{float(self.filter.dn):.4f}")
            self.lbl_param1Value.show()
            self.lbl_param2Value.show()
            self.lbl_param3Value.show()

        elif self.filter.type == 2: # General second-order filter
            self.lbl_param1.setText(f"{self.filter.type_param} Typ")
            self.lbl_param2.setText(f"{self.filter.fn_param} Nenner-Frequenz")
            self.lbl_param3.setText(f"{self.filter.dn_param} Nenner-Dämpfung")
            self.lbl_param4.setText(f"{self.filter.fz_param} Zähler-Bandbreite")
            self.lbl_param5.setText(f"{self.filter.dz_param} Zähler-Kerbtiefe")
            self.lbl_param1.show()
            self.lbl_param2.show()
            self.lbl_param3.show()
            self.lbl_param4.show()
            self.lbl_param5.show()

            self.lbl_param1Value.setText(f"{self.filter.type}")
            self.lbl_param2Value.setText(f"{float(self.filter.fn):.4f}")
            self.lbl_param3Value.setText(f"{float(self.filter.dn):.4f}")
            self.lbl_param4Value.setText(f"{float(self.filter.fz):.4f}")
            self.lbl_param5Value.setText(f"{float(self.filter.dz):.4f}")
            self.lbl_param1Value.show()
            self.lbl_param2Value.show()
            self.lbl_param3Value.show()
            self.lbl_param4Value.show()
            self.lbl_param5Value.show()

        else:
            print(f"❌ Unsupported filter type {self.filter.type}. Only PT1, PT2 and General second-order filters are supported.")
            return


    def pb_showParam_clicked(self):
        """
        Show the Sinumerik parameters for the selected drive.
        This method is connected to the "> Parameters" button.
        """

        if not self.filter:
            print("❌ Show parameters does not work. Filter object not loaded.")
            return
        
        # Toggle the visibility of the Sinumerik parameters
        self.filter.show_param = not self.filter.show_param

        if self.filter.show_param:
            self.w_param.show()
            self.pb_showParam.setIcon(QIcon(":/resources/arrow_drop_down_24dp.svg"))
        else:
            self.w_param.hide()
            self.pb_showParam.setIcon(QIcon(":/resources/arrow_right_24dp.svg"))


class ParamObject:
    def __init__(self, name, archive_value=None, default_value=None, min_value=None, max_value=None):
        self.name = name
        self.archive_value = archive_value
        self.default_value = archive_value if archive_value is not None else (default_value if default_value is not None else 0)
        self.current_value = self.default_value
        self.min = min_value
        self.max = max_value
        self.changed = False

    def set_value(self, value):
        self.current_value = value
        self.changed = (value != self.default_value)

    def reset(self):
        self.set_value(self.default_value)

    def is_valid(self):
        if self.min is None and self.max is None:
            return True
        return (self.min is None or self.current_value >= self.min) and \
               (self.max is None or self.current_value <= self.max)


class CwControllerInfo(qtw.QWidget, Ui_ControllerInfoFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.archive = None  # This will hold the current archive
        self.current_drive = None
        self.current_drive_index = 0

        # Create layout in the w_controllers widget
        self.w_controllers_layout = qtw.QVBoxLayout(self.w_controllers)
        self.w_controllers.setLayout(self.w_controllers_layout)

        # --- Adaptation plot live-update bookkeeping ---
        self._adaptation_plots = []
        self._param_to_adaptation_plots = {}

    def update_drive_ui(self, drive_index):
        """
        Update the UI with the drive information based on the selected drive index.
        This method should be called when the user selects a different drive from the combo box.
        """
        if not self.archive or not self.archive.drives:
            print("❌ No archive or drives available to update.")
            return

        # Update current drive index
        self.current_drive_index = drive_index
        self.current_drive = self.archive.drives[self.current_drive_index]

        # Make sure the index is correct
        self.cb_driveNames.blockSignals(True)
        self.cb_driveNames.setCurrentIndex(self.current_drive_index)
        self.cb_driveNames.blockSignals(False)

         # Set more info
        self.lbl_driveMoreInfoLeft.setText(f"Speicherort im Archiv:")
        self.lbl_driveMoreInfoRight.setText(f"{self.current_drive.path}")
        self.w_moreInfo.hide() # Hide more info section initially

        # Clear the current controllers layout
        for i in reversed(range(self.w_controllers_layout.count())):
            widget = self.w_controllers_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        # Clear previous adaptation-plot bookkeeping
        self._adaptation_plots.clear()
        self._param_to_adaptation_plots.clear()

        for controller in self.current_drive.controllers:
            # Create frame for each controller
            controller_frame = ControllerFrame(self)
            self.w_controllers_layout.addWidget(controller_frame)

            # Set the controller name
            controller_frame.lbl_controller_name.setText(controller.name)

            # Get the frame where the parameter will be added
            param_frame = controller_frame.fr_controllerParams

            # Create a vertical layout for the controller parameters
            controller_layout = qtw.QVBoxLayout(param_frame)

            # Build a quick index for lookups of referenced params
            param_by_key = {p.param_str: p for p in controller.param_list if hasattr(p, 'param_str')}

            adaptation_graph_list = []

            for param in controller.param_list:
                if param.param_type == "normal":
                    param_frame = ControllerParamFrame(param, parent=controller_frame)
                    # When this param changes, update any adaptation plots that depend on it
                    param_frame.value_changed_signal.connect(
                        lambda p=param: self._update_adaptation_plots_for_param(p)
                    )
                elif param.param_type == "bitconfig":
                    param_frame = ControllerParamFrameBitconfig(param, parent=controller_frame)
                elif param.param_type == "adaptation_plot":
                    required_attrs = [
                        'y1_param', 'y1_adapt_factor_param',
                        'y2_param', 'y2_adapt_factor_param',
                        'x1_param', 'x2_param',
                        'name1', 'name2'
                    ]
                    if not all(hasattr(param, a) for a in required_attrs):
                        print(f"❌ Missing adaptation graph parameters for {getattr(param, 'param_str', '<unnamed>')}. Skipping.")
                        continue

                    # Lookup referenced params
                    y1_obj  = param_by_key.get(param.y1_param)
                    y1f_obj = param_by_key.get(param.y1_adapt_factor_param)
                    y2_obj  = param_by_key.get(param.y2_param)
                    y2f_obj = param_by_key.get(param.y2_adapt_factor_param)
                    x1_obj  = param_by_key.get(param.x1_param)
                    x2_obj  = param_by_key.get(param.x2_param)

                    referenced = [y1_obj, y1f_obj, y2_obj, y2f_obj, x1_obj, x2_obj]
                    if any(o is None for o in referenced):
                        missing = [name for name, o in zip(['y1','y1_factor','y2','y2_factor','x1','x2'], referenced) if o is None]
                        print(f"❌ Adaptation plot: missing referenced params {missing} in controller {controller.name}. Skipping.")
                        continue

                    if y1_obj is None or y2_obj is None or y1f_obj is None or y2f_obj is None or x1_obj is None or x2_obj is None:
                        print(f"❌ Adaptation plot: missing y1, y2, y1_factor, y2_factor, x1 or x2 for {getattr(param, 'param_str', '<unnamed>')}. Skipping.")
                        continue

                    # Initial values
                    try:
                        y1 = float(y1_obj.value)
                        y1_factor = float(y1f_obj.value)
                        y2 = float(y2_obj.value)
                        y2_factor = float(y2f_obj.value)
                        x1 = float(x1_obj.value)
                        x2 = float(x2_obj.value)
                    except Exception as e:
                        print(f"❌ Adaptation plot: failed to read values: {e}")
                        continue

                    graph1_params = AdaptationGraphParams(
                        y1=y1, y2=y1*y1_factor,
                        x=(0.0, x1, x2, x1+x2),
                        color="tab:blue",
                        label="",
                        ylabel=param.name1,
                        y_min=None, y_max=None
                    )

                    graph2_params = AdaptationGraphParams(
                        y1=y2, y2=y2*y2_factor,
                        x=(0.0, x1, x2, x1+x2),
                        color="tab:orange",
                        label="",
                        ylabel=param.name2,
                        y_min=None, y_max=None
                    )

                    # Create widget and register it
                    adaptation_plot_widget = Adaptationplot(graph1_params, graph2_params, parent=controller_frame)
                    adaptation_plot_widget.setMinimumHeight(300)

                    # Bookkeeping entry
                    entry = {
                        "widget": adaptation_plot_widget,
                        "y1_obj": y1_obj,  "y1f_obj": y1f_obj,
                        "y2_obj": y2_obj,  "y2f_obj": y2f_obj,
                        "x1_obj": x1_obj,  "x2_obj": x2_obj,
                        "name1": param.name1,
                        "name2": param.name2,
                    }
                    self._adaptation_plots.append(entry)
                    for o in [y1_obj, y1f_obj, y2_obj, y2f_obj, x1_obj, x2_obj]:
                        self._param_to_adaptation_plots.setdefault(o, []).append(entry)

                    # for layout consistency
                    param_frame = adaptation_plot_widget

                else:
                    print(f"❌ Unsupported parameter type: {param.param_type}")
                    continue

                controller_layout.addWidget(param_frame)

        # Connect more info button to toggle visibility
        self.pb_moreInfo.clicked.connect(self.pb_moreInfo_clicked)

    def update_archive(self, archive):
        """
        Initialize the widget with the given archive.
        This method should be called after an archive is added.
        """
        self.archive = archive
        self.current_drive = self.archive.drives[self.current_drive_index] if self.archive and self.archive.drives else None
        
        # Set the Archive name in the label
        self.lbl_archiveNameValue.setText(f"{archive.name}")

        if self.current_drive is None:
            print("❌ No drives available in the archive.")
            self.cb_driveNames.blockSignals(True)
            self.cb_driveNames.clear()
            self.cb_driveNames.addItem("No drives available.")
            self.cb_driveNames.blockSignals(False)
            self._updating_drive_ui = False
            self.w_moreInfo.hide()
            self.pb_moreInfo.hide()
            return False

        if not self.archive:
            print(f"❌ Cannot update drive UI. No archive loaded for tab CwControllerInfo")
            qtw.QMessageBox.critical(self, "Archiv Fehler", "Archiv wurde nicht initalisiert.")
            self._updating_drive_ui = False
            return False

        if not self.archive.drives:
            print(f"❌ No drives available for tab CwControllerInfo.")

        # Parse filters from the archive, if archive is not innitialized
        if not archive.is_innit:
            if archive.type == "DSF":
                parse_filters_from_dsf(archive)
            elif archive.type == "ARC":
                parse_filters_from_arc(archive)
            else:
                print(f"❌ Unknown archive type: {archive.type}")

        # Populate drive names without emitting signals during changes
        self.cb_driveNames.blockSignals(True)
        self.cb_driveNames.clear()
        for drive in self.archive.drives:
            self.cb_driveNames.addItem(drive.name)
        self.cb_driveNames.blockSignals(False)

        # Update drive UI
        self.update_drive_ui(self.current_drive_index)

        # Connect combo box for drive selection to the update_drive_ui method
        self.cb_driveNames.currentIndexChanged.connect(self.update_drive_ui)

    def activate_compare_mode(self, compare_archive_widget):
        if self.archive is None or compare_archive_widget is None:
            print("❌ Cannot activate compare mode. One of the archives is not set.")
            self.compare_mode = False
            qtw.QMessageBox.critical(self, "Vergleichsmodus Fehler.", "Eins der Archive wurde nicht initalisziert.")
            return

        # Connect scrollbars
        self.sa_main.verticalScrollBar().valueChanged.connect(compare_archive_widget.sa_main.verticalScrollBar().setValue)
        self.sa_main.verticalScrollBar().setValue(0)

    def deactivate_compare_mode(self, compare_archive_widget):

        # Disconnect scrollbars
        self.sa_main.verticalScrollBar().valueChanged.disconnect(compare_archive_widget.sa_main.verticalScrollBar().setValue)

    def _update_adaptation_plots_for_param(self, changed_param_obj):
        """Recompute and update any adaptation plot widgets that depend on the given param object."""
        entries = self._param_to_adaptation_plots.get(changed_param_obj)
        if not entries:
            return
        for entry in entries:
            try:
                gp_a, gp_b = self._build_graph_params_from_entry(entry)
                # TwoAxisZonesPlot signature:
                # update_params(self, params_a: Optional[GraphParams] = None,
                #               params_b: Optional[GraphParams] = None)
                entry["widget"].update_params(params_a=gp_a, params_b=gp_b)
            except Exception as e:
                print(f"❌ Adaptation plot update failed: {e}")

    def _build_graph_params_from_entry(self, entry):
        """Build current GraphParams for both axes from the entry's referenced params."""
        y1  = float(entry["y1_obj"].value)
        y1f = float(entry["y1f_obj"].value)
        y2  = float(entry["y2_obj"].value)
        y2f = float(entry["y2f_obj"].value)
        x1  = float(entry["x1_obj"].value)
        x2  = float(entry["x2_obj"].value)

        gp1 = AdaptationGraphParams(
            y1=y1, y2=y1*y1f,
            x=(0.0, x1, x2, x1+x2),
            color="tab:blue",
            label="",
            ylabel=entry["name1"],
            y_min=None, y_max=None
        )
        gp2 = AdaptationGraphParams(
            y1=y2, y2=y2*y2f,
            x=(0.0, x1, x2, x1+x2),
            color="tab:orange",
            label="",
            ylabel=entry["name2"],
            y_min=None, y_max=None
        )
        return gp1, gp2

    def pb_moreInfo_clicked(self):
        """
        Toggle the visibility of the "more info" section.
        """

        # Check if the archive is loaded
        if not self.archive:
            print("❌ Cannot toggle more drive info visibility. No archive loaded.")
            return
        
        self.archive.show_more_drive_info = not self.archive.show_more_drive_info
        if self.archive.show_more_drive_info:
            self.w_moreInfo.show()
            self.pb_moreInfo.setIcon(QIcon(":/resources/arrow_drop_down_24dp.svg"))
        else:
            self.w_moreInfo.hide()
            self.pb_moreInfo.setIcon(QIcon(":/resources/arrow_right_24dp.svg"))


class ControllerFrame(qtw.QFrame, Ui_ControllerFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class ControllerParamFrame(qtw.QFrame, Ui_ParamFrame):
    value_changed_signal = Signal()

    def __init__(self, param_obj, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.param_obj = param_obj  # Store the parameter object

        # Set the parameter string and meaning in the UI
        self.lbl_param_str.setText(self.param_obj.param_str)
        self.lbl_meaning.setText(self.param_obj.meaning)
        self.dsb_value.setMinimum(self.param_obj.min)
        self.dsb_value.setMaximum(self.param_obj.max)
        self.dsb_value.setSingleStep(self.param_obj.step)
        self.dsb_value.setDecimals(self.param_obj.decimals)
        self.dsb_value.setValue(self.param_obj.value)

        # Hide the reset button initially
        self.pb_reset.hide()

        # Connect double spin box value change to the value_changed method
        self.dsb_value.valueChanged.connect(self.value_changed)

        # Connect reset button to the reset_clicked method
        self.pb_reset.clicked.connect(self.reset_clicked)

    def value_changed(self, new_value):
        """
        This method is called when the value of the double spin box changes.
        """

        # Check if the original value is set, if not, set it to the default value
        if self.param_obj.og_value is None:
            print(f"Original value for {self.param_obj.param_str} is not set. Setting factory default value.")
            self.param_obj.og_value = self.param_obj.default_value

        # Check whether the new value is same as the original value
        if new_value == self.param_obj.og_value:

            # Change color text to standard color
            line_edit = self.dsb_value.findChild(qtw.QLineEdit)
            if line_edit:
                palette = line_edit.palette()
                palette.setColor(QPalette.ColorRole.Text, QColor(*config.DEFAULT_TEXT_COLOR))
                line_edit.setPalette(palette)

            # Hide the reset button
            self.pb_reset.hide()

        else:
            # Change color text to "value changed"-color
            line_edit = self.dsb_value.findChild(qtw.QLineEdit)
            if line_edit:
                palette = line_edit.palette()
                palette.setColor(QPalette.ColorRole.Text, QColor(*config.VALUE_CHANGED_TEXT_COLOR))
                line_edit.setPalette(palette)

            # Show reset button
            self.pb_reset.show()

        # Update the parameter object with the new value
        self.param_obj.set_value(new_value)

        self.value_changed_signal.emit()  # Emit the value changed signal to notify other components

    def reset_clicked(self):
        if self.param_obj.og_value is not None:
            self.dsb_value.setValue(self.param_obj.og_value)
            self.value_changed(self.param_obj.og_value)
        else:
            self.dsb_value.setValue(self.param_obj.default_value)
            self.value_changed(self.param_obj.default_value)
        print(f"Reset {self.param_obj.param_str} to original value: {self.param_obj.og_value}")
         

class BitconfigSingleBit(qtw.QFrame, Ui_BitconfigSingleBit):
    def __init__(self, bit_index, meaning, value, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.bit_index = bit_index
        self.meaning = meaning  # Meaning of the bit
        self.default_value = value
        self.value = value
        
        # Set the bit information in the UI with elided text and tooltip on hover if elided
        self._max_meaning_width = 350
        fm = QFontMetrics(self.lbl_meaning.font())
        elided_text = fm.elidedText(self.meaning, Qt.TextElideMode.ElideRight, self._max_meaning_width)
        self.lbl_meaning.setText(elided_text)
        self._meaning_elided = (elided_text != self.meaning)

        # Enable hover/mouse tracking to support tooltip display
        self.lbl_meaning.setMouseTracking(True)
        self.lbl_meaning.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.lbl_meaning.installEventFilter(self)

        # Set the check box state based on the bit value
        self.checkBox.setCheckState(Qt.CheckState.Checked if self.value else Qt.CheckState.Unchecked)

        # Hook up interactions for bit value and reset
        self.pb_reset.hide()
        self.checkBox.stateChanged.connect(self.check_state_changed)
        self.pb_reset.clicked.connect(self.reset_clicked)

    def eventFilter(self, obj, event):
        # Show full meaning as a tooltip when the text is elided and the user hovers the label
        if obj is self.lbl_meaning:
            if event.type() in (QEvent.Type.Enter, QEvent.Type.HoverMove):
                if getattr(self, "_meaning_elided", False):
                    qtw.QToolTip.showText(QCursor.pos(), self.meaning, self.lbl_meaning)
                else:
                    qtw.QToolTip.hideText()
            elif event.type() == QEvent.Type.Leave:
                qtw.QToolTip.hideText()
        return super().eventFilter(obj, event)

    def check_state_changed(self, state):
        """
        This method is called when the check box state changes.
        """

        if state == 2: # 2 means checked
            self.value = True
        else:
            self.value = False

        if self.value == self.default_value:
            self.pb_reset.hide()
        else:
            self.pb_reset.show()

    def reset_clicked(self):
        """
        Reset the bit value to the default value.
        This method is called when the reset button is clicked.
        """

        self.value = self.default_value
        self.checkBox.setCheckState(Qt.CheckState.Checked if self.value else Qt.CheckState.Unchecked)
        self.pb_reset.hide()


class ControllerParamFrameBitconfig(qtw.QFrame, Ui_ParamFrameBitconfig):
    def __init__(self, bitconfig_param_obj, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.show_bitconfig = False

        self.bitconfig_param_obj = bitconfig_param_obj
        self.param_str = bitconfig_param_obj.param_str
        self.meaning = bitconfig_param_obj.meaning
        self.default_lang = bitconfig_param_obj.default_lang

        # Create layout for the widget where bits appear
        self.w_bit_config_layout = qtw.QVBoxLayout(self.w_bit_config)
        self.w_bit_config_layout.setContentsMargins(16, 0, 0, 0)
        self.w_bit_config_layout.setSpacing(0)

        # List for holding bit frame widgets
        self.bit_frames_list = []

        # Read each bitconfig parameter and set the UI
        for b in range(len(self.bitconfig_param_obj.bit_meanings_list)):

            # Create a frame for the single bit
            bit_frame = BitconfigSingleBit(b,
                                           self.bitconfig_param_obj.bit_meanings_list[b],
                                           self.bitconfig_param_obj.bit_values_list[b],
                                           parent=self)
            bit_frame.setObjectName(f"bit_frame_{b}")

            self.bit_frames_list.append(bit_frame)
            
            # Connect the bit frame's check state changed signal to the bitconfig_changed method
            bit_frame.checkBox.stateChanged.connect(self.bitconfig_changed)

            self.w_bit_config_layout.addWidget(bit_frame)
            # Hide if the bit meaning is empty
            if not self.bitconfig_param_obj.bit_meanings_list[b]:
                bit_frame.hide()

        # Set the parameter string and meaning in the UI
        self.pb_param.setText(self.param_str)
        self.lbl_meaning.setText(self.meaning)

        # Show the value by triggering the bitconfig_changed method
        self.bitconfig_changed()

        # Connect the show bitconfig button to the show_bitconfig_clicked method
        self.pb_param.clicked.connect(self.show_bitconfig_clicked)

        # Hide w_bit_config initially
        self.w_bit_config.hide()

    def show_bitconfig_clicked(self):
        self.show_bitconfig = not self.show_bitconfig
        if self.show_bitconfig:
            self.w_bit_config.show()
            self.pb_param.setIcon(QIcon(":/resources/arrow_drop_down_24dp.svg"))
        else:
            self.w_bit_config.hide()
            self.pb_param.setIcon(QIcon(":/resources/arrow_right_24dp.svg"))

    def bitconfig_changed(self):
        """
        This method is called when the bit configuration changes.
        It updates the bit values in the parameter object.
        """

        # Update the bit values in the parameter object
        bit_values_list = [0 for _ in range(len(self.bitconfig_param_obj.bit_meanings_list))]
        for bit in self.bit_frames_list:
            if bit.checkBox.isChecked():
                bit_values_list[bit.bit_index] = 1

        self.bitconfig_param_obj.bit_values_list = bit_values_list

        # Calculate the new value based on the bit values
        self.bitconfig_param_obj.calculate_value()

        # Update the label with the new value
        # Display the value in hexadecimal format (e.g., 0x1A)
        self.lbl_value.setText(f"0x{self.bitconfig_param_obj.value:X}")


class ColorSquare(qtw.QWidget):
    color_changed_signal = Signal(int, int, int)

    def __init__(self, initial_color=QColor("red"), parent=None):
        super().__init__(parent)
        self.color = initial_color
        self.setFixedSize(QSize(16, 16))

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        selected_color = qtw.QColorDialog.getColor(self.color, self, "Choose color")
        if selected_color.isValid():
            self.color = selected_color
            self.color_changed_signal.emit(selected_color.red(), selected_color.green(), selected_color.blue())
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(self.color)
        painter.drawRect(self.rect())

    def change_color(self, new_color):
        if isinstance(new_color, QColor):
            self.color = new_color
            self.update()

            self.color_changed_signal.emit(new_color.red(), new_color.green(), new_color.blue())


class KinematicTreeView(qtw.QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.kinematic_tree: sinumerik_components.KinematicTree

    def setup_model(self, kinematic_tree):
        self.kinematic_tree = kinematic_tree
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Kinematic Tree"])
        
        def add_tree_items(parent_item, node):
            item = QStandardItem(node.name)
            parent_item.appendRow(item)

            if node.parallel is not None and node.parallel != "":
                # Parallel items come BEFORE the current node, that is why the parent_item is given as next
                add_tree_items(parent_item, self.kinematic_tree.node_dict[node.parallel])
            if node.next is not None and node.next != "":
                add_tree_items(item, self.kinematic_tree.node_dict[node.next])

        # Create the root item for the model
        root_item = model.invisibleRootItem()
        # Add each root node to the model
        for root_node in self.kinematic_tree.root_nodes:
            add_tree_items(root_item, root_node)

        self.setModel(model)
        self.expandAll()
        # Autosize height to show all expanded rows (no inner scrollbar)
        self._resize_to_contents()


    def _resize_to_contents(self):
        """Set minimum/maximum height so all expanded rows are visible (let outer scroll area handle overflow)."""
        model = self.model()
        if model is None:
            return
        # ensure expanded so row count reflects visible nodes
        self.expandAll()
        # count visible rows recursively
        def count_rows(parent_index):
            total = 0
            rc = model.rowCount(parent_index)
            for r in range(rc):
                idx = model.index(r, 0, parent_index)
                total += 1  # this row
                if self.isExpanded(idx):
                    total += count_rows(idx)
            return total
        rows = count_rows(QModelIndex())
        row_h = self.sizeHintForRow(0) if rows > 0 else self.fontMetrics().height() + 6
        header_h = 0 if self.isHeaderHidden() else self.header().height()
        margins = 4
        total_h = header_h + rows * row_h + margins
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMinimumHeight(total_h)
        self.setMaximumHeight(total_h)


class CwKinematicTree(qtw.QFrame, Ui_CwKinematicTree):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)

        # === Layout: Tree (top) → 3D Plot → hover label → Sliders (bottom) ===
        # 1) Kinematic Tree (existing view)
        self.kinematic_tree_widget = KinematicTreeView(self)
        self.kinematic_tree_widget.setObjectName("kinematic_tree")
        self.kinematic_tree_widget.setHeaderHidden(True)
        self.sa_mainContents_layout.addWidget(self.kinematic_tree_widget)

        # 2) 3D Visualisation (Matplotlib)
        self.plot = KinematicPlotWidget(self)
        self.plot.setMinimumHeight(500)
        self.plot.setMinimumWidth(500)
        self.sa_mainContents_layout.addWidget(self.plot)

        # Hover info label under the plot
        self.info_label = qtw.QLabel("Hover über Knoten/Axis für Details …")
        self.info_label.setStyleSheet("color: #666;")
        self.plot.hoverTextChanged.connect(self.info_label.setText)
        self.sa_mainContents_layout.addWidget(self.info_label)

        # 3) Sliders container (ALL axes) directly in layout (no inner scroll)
        self.controls_container = qtw.QWidget()
        self.controls_container.setSizePolicy(qtw.QSizePolicy.Policy.Preferred, qtw.QSizePolicy.Policy.Maximum)
        self.controls_layout = qtw.QVBoxLayout(self.controls_container)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        self.controls_layout.setSpacing(6)
        self.controls_layout.addStretch(1)
        self.sa_mainContents_layout.addWidget(self.controls_container)

        # State
        self.archive = None
        self.kinematic_tree = None
        self.model: KinematicModel | None = None
        self.axis_controls: dict[str, AxisControlWidget] = {}

    def update_archive(self, archive):
        if archive is None:
            print("❌ Cannot initialize kinematic tree. Archive is None.")
            return
        
        self.archive = archive 
        
        """Bind new archive (tree + math model) and refresh GUI."""
        self.archive_name = archive.name
        self.kinematic_tree = archive.kinematic_tree

        if not self.kinematic_tree:
            print("❌ Cannot initialize kinematic tree. Kinematic tree cannot be found.")
            return

        try:
            self.lbl_archiveNameValue.setText(self.archive_name)
            self.kinematic_tree_widget.setup_model(self.kinematic_tree)
            # ensure the tree view resizes to fit all items
            if hasattr(self.kinematic_tree_widget, "_resize_to_contents"):
                self.kinematic_tree_widget._resize_to_contents()

            # Build math model (pure core) and bind to plot
            self.model = KinematicModel.from_tree(self.kinematic_tree)
            self.plot.set_model(self.model)

            # Remove existing controls (keep the final stretch item)
            for i in reversed(range(self.controls_layout.count() - 1)):
                w = self.controls_layout.itemAt(i).widget()
                if w:
                    w.setParent(None)
            self.axis_controls.clear()

            # Create sliders for ALL axes (LIN + ROT), no dropdown
            for axis_name in self.model.get_axis_names():
                node = self.model.nodes[axis_name]
                def on_val_changed(x: float, axis=axis_name):
                    if self.model is not None:
                        self.model.set_axis_value(axis, x)
                        self.plot.update_scene()
                ctrl = AxisControlWidget(
                    axis_name=axis_name,
                    axis_type=(node.type or ""),
                    initial_value=float(node.a_off),
                    on_value_changed=on_val_changed
                )
                self.controls_layout.insertWidget(self.controls_layout.count() - 1, ctrl)
                self.axis_controls[axis_name] = ctrl

            # Resize sliders container to fit children (no inner scrolling)
            self.controls_container.adjustSize()
            self.controls_container.setMinimumHeight(self.controls_container.sizeHint().height())
            self.controls_container.setMaximumHeight(self.controls_container.sizeHint().height())

            # First render
            self.plot.update_scene()
        except Exception as e:
            print(f"❌ Cannot initialize kinematic tree: {e}")
            return
        
    def activate_compare_mode(self, compare_archive_widget):

        if self.archive is None or compare_archive_widget is None:
            print("❌ Cannot activate compare mode. One of the archives is not set.")
            self.compare_mode = False
            qtw.QMessageBox.critical(self, "Vergleichsmodus Fehler", "Eins der Archive wurde nicht initalisiert.")
            return

        # Connect scrollbars
        self.sa_main.verticalScrollBar().valueChanged.connect(compare_archive_widget.sa_main.verticalScrollBar().setValue)
        self.sa_main.verticalScrollBar().setValue(0)

    def deactivate_compare_mode(self, compare_archive_widget):

        # Disconnect scrollnars
        self.sa_main.verticalScrollBar().valueChanged.disconnect(compare_archive_widget.sa_main.verticalScrollBar().setValue)



class KinematicPlotWidget(qtw.QWidget):
    hoverTextChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._model: KinematicModel | None = None

        self._fig = Figure(figsize=(6, 5))
        self._canvas = FigureCanvas(self._fig)
        self._ax = self._fig.add_subplot(111, projection="3d")
        self._ax.set_xlabel("X"); self._ax.set_ylabel("Y"); self._ax.set_zlabel("Z")
        try:
            self._ax.mouse_init()
        except Exception:
            pass

        lay = qtw.QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._canvas)

        try:
            self._ax.set_box_aspect((1, 1, 1))
        except Exception:
            pass

        self._hover_items: list[tuple[object, dict]] = []
        self._canvas.mpl_connect("motion_notify_event", self._on_motion)

    def _on_motion(self, event):
        if event.inaxes != self._ax:
            self.hoverTextChanged.emit(" ")
            return
        for artist, meta in reversed(self._hover_items):
            contains, _ = artist.contains(event)
            if contains:
                self.hoverTextChanged.emit(meta.get("label", ""))
                return
        self.hoverTextChanged.emit(" ")

    def set_model(self, model: KinematicModel):
        self._model = model
        self.update_scene()

    def update_scene(self):
        if self._model is None:
            return

        self._ax.cla()
        self._ax.set_xlabel("X"); self._ax.set_ylabel("Y"); self._ax.set_zlabel("Z")
        self._hover_items.clear()

        # Recompute chain and get segments
        segments = self._model.calculate_positions()

        # 1) Links
        for (p0, p1) in segments:
            xs = [p0[0], p1[0]]; ys = [p0[1], p1[1]]; zs = [p0[2], p1[2]]
            line, = self._ax.plot(xs, ys, zs, linewidth=2, picker=5)
            self._hover_items.append((line, {"label": "Segment"}))

        # 2) Nodes
        for node in self._model.nodes.values():
            p = np.array(node.position, dtype=float)
            pt = self._ax.scatter(p[0], p[1], p[2], s=20, picker=True)
            label = f"Knoten: {node.name}  |  Typ: {node.type}"
            if getattr(node, "axis", ""):
                label += f"  |  Axis: {node.axis}"
            self._hover_items.append((pt, {"label": label}))

        # 3) Axis visuals
        for node in self._model.nodes.values():
            tpe = (node.type or "").upper()
            p = np.array(node.position, dtype=float)
            d = np.array([float(node.off_dir_x), float(node.off_dir_y), float(node.off_dir_z)], dtype=float)
            nrm = np.linalg.norm(d)
            if nrm > 0: d = d / nrm

            if "AXIS_LIN" in tpe:
                start = p
                end = start + d * 0.1
                ax_line, = self._ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], picker=5)
                self._hover_items.append((ax_line, {"label": f"Achse: {node.name}  |  Transformation: Translation (AXIS_LIN)"}))

            elif "AXIS_ROT" in tpe and nrm > 0:
                n = d
                center = p
                if np.allclose(n, np.array([0, 0, 1])):
                    tangent = np.array([1, 0, 0])
                else:
                    tangent = np.cross(n, np.array([0, 0, 1])); tangent = tangent / np.linalg.norm(tangent)
                bitang = np.cross(n, tangent)
                r = 0.1
                angles = np.linspace(0, 2 * np.pi, 64)
                circ = np.array([center + r * (math.cos(a) * tangent + math.sin(a) * bitang) for a in angles])
                rot_circle, = self._ax.plot(circ[:, 0], circ[:, 1], circ[:, 2], picker=5)
                self._hover_items.append((rot_circle, {"label": f"Achse: {node.name}  |  Transformation: Rotation (AXIS_ROT)"}))

        # Auto scale
        all_pts = np.array([np.array(n.position, dtype=float) for n in self._model.nodes.values()])
        mins = np.min(all_pts, axis=0); maxs = np.max(all_pts, axis=0)
        span = np.maximum(maxs - mins, 1e-3)
        center = (maxs + mins) / 2.0
        half = float(np.max(span) * 0.6 + 0.2)
        self._ax.set_xlim(center[0] - half, center[0] + half)
        self._ax.set_ylim(center[1] - half, center[1] + half)
        self._ax.set_zlim(center[2] - half, center[2] + half)
        try:
            self._ax.set_box_aspect((1, 1, 1))
        except Exception:
            pass

        # Ensure the 3D view remains visible and expands
        self.setMinimumHeight(400)
        self._canvas.setMinimumHeight(400)
        self.setSizePolicy(qtw.QSizePolicy.Policy.Preferred, qtw.QSizePolicy.Policy.Expanding)
        self._canvas.setSizePolicy(qtw.QSizePolicy.Policy.Preferred, qtw.QSizePolicy.Policy.Expanding)

        self._canvas.draw()


class AxisControlWidget(qtw.QGroupBox):
    def __init__(self, axis_name: str, axis_type: str, initial_value: float, on_value_changed, parent=None):
        super().__init__(parent)
        self._axis_name = axis_name
        self._axis_type = axis_type
        self._on_value_changed = on_value_changed
        self.setTitle(f"{axis_name}  —  {'Translation [m]' if 'AXIS_LIN' in axis_type else 'Rotation [deg]'}")

        # sensible defaults
        if "AXIS_LIN" in axis_type:
            min_default, max_default, step_default = -1.0, 1.0, 0.01
        else:
            min_default, max_default, step_default = -180.0, 180.0, 1.0

        self.spin_min = qtw.QDoubleSpinBox(); self.spin_min.setRange(-1e6, 1e6); self.spin_min.setDecimals(6); self.spin_min.setValue(min_default)
        self.spin_max = qtw.QDoubleSpinBox(); self.spin_max.setRange(-1e6, 1e6); self.spin_max.setDecimals(6); self.spin_max.setValue(max_default)
        self.spin_step = qtw.QDoubleSpinBox(); self.spin_step.setRange(1e-6, 1e6); self.spin_step.setDecimals(6); self.spin_step.setValue(step_default)

        self.slider = qtw.QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0); self.slider.setMaximum(1000); self.slider.setSingleStep(1); self.slider.setTracking(True)

        self.lbl_val = qtw.QLabel()

        lay = qtw.QVBoxLayout(self)

        # 1) Slider und Live-Wert
        lay.addWidget(self.slider)
        lay.addWidget(self.lbl_val)

        # 2) Nur Min/Max in einer Zeile (Step wird nicht angezeigt)
        row = qtw.QHBoxLayout()
        row.setSpacing(12)
        row.addWidget(qtw.QLabel("Min"))
        row.addWidget(self.spin_min)
        row.addSpacing(8)
        row.addWidget(qtw.QLabel("Max"))
        row.addWidget(self.spin_max)
        row.addStretch(1)
        lay.addLayout(row)

        # Step-SpinBox nicht anzeigen (weiterhin intern verwendbar)
        self.spin_step.hide()

        self.spin_min.valueChanged.connect(self._on_limits_changed)
        self.spin_max.valueChanged.connect(self._on_limits_changed)
        self.spin_step.valueChanged.connect(self._on_step_changed)
        self.slider.valueChanged.connect(self._on_slider_changed)

        self._on_limits_changed()
        self.set_value(initial_value)

    def _value_from_slider(self, s: int) -> float:
        a = self.spin_min.value(); b = self.spin_max.value()
        if b <= a: b = a + 1e-6
        return a + (b - a) * (s / 1000.0)

    def _slider_from_value(self, x: float) -> int:
        a = self.spin_min.value(); b = self.spin_max.value()
        if b <= a: b = a + 1e-6
        t = (x - a) / (b - a)
        return int(np.clip(round(t * 1000.0), 0, 1000))

    def _on_limits_changed(self):
        cur_val = self.value()
        self.set_value(cur_val)

    def _on_step_changed(self):
        total = max(1e-6, (self.spin_max.value() - self.spin_min.value()))
        page = max(1, int(round(self.spin_step.value() * 1000.0 / total)))
        self.slider.setPageStep(page)

    def _on_slider_changed(self, s: int):
        x = self._value_from_slider(s)
        unit = "m" if "AXIS_LIN" in self._axis_type else "deg"
        self.lbl_val.setText(f"Wert: {x:.6f} {unit}")
        if self._on_value_changed:
            self._on_value_changed(x)

    def value(self) -> float:
        return self._value_from_slider(self.slider.value())

    def set_value(self, x: float):
        self.slider.blockSignals(True)
        self.slider.setValue(self._slider_from_value(x))
        self.slider.blockSignals(False)
        self._on_slider_changed(self.slider.value())