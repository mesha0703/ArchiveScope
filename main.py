"""Main window and application bootstrap for the CNC archive visualizer."""

import sys
import logging
from pathlib import Path
import shutil

from PySide6 import QtWidgets as qtw
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from ui.main_window import Ui_MainWindow
from ui.archive_info_widgets import (
    ArchiveDragAndDropSurface,
    CwArchiveDriveInfo,
    CwControllerInfo,
    CwKinematicTree,
)
from core.export_archive import export_archive
from core.manipulate_dsf import parse_filters_from_dsf
from core.manipulate_arc import parse_filters_from_arc
from core.logging_setup import setup_logging
import config

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    """Main application window handling archive loading, tab switching,
    compare mode, exporting, and optional log save on close."""

    def __init__(self, log_path: str | Path | None = None):
        super().__init__()
        self.setupUi(self)
        # Store log path for later use (e.g., offer to save on exit)
        self.log_path = Path(log_path) if log_path is not None else None

        # Archive added flag
        self.num_archives = 0
        self.current_tab = 0

        # Compare mode flag. Toggles when compare button "=" is pressed
        self.compare_mode = False

        # Keep references to loaded archives (order must match the menus)
        self.archives = []

        # Create a Layout in which the archives will display
        self.layout_archives_surface = qtw.QHBoxLayout(self.fr_archivesSurface)

        # Create a list to hold drag-and-drop surfaces for multiple archives. Create only one for now.
        self.archive_drag_and_drop_surfaces = [ArchiveDragAndDropSurface()]
        self.layout_archives_surface.addWidget(self.archive_drag_and_drop_surfaces[0])

        # Connect the drag-and-drop surface to the update_archive method
        self.archive_drag_and_drop_surfaces[0].archive_added_signal.connect(self.update_archive)

        # ===== Initialize Tabs =====

        # Each archive will have a CwArchiveDriveInfo Widget for each tab
        self.cw_current_setpoint_drive_info = []
        self.cw_speed_setpoint_drive_info = []
        self.cw_actual_speed_drive_info = []
        self.cw_controller_info = []
        self.cw_kinematic_tree_view = []

        for _ in range(config.MAX_PARALLEL_ARCHIVES):
            current_setpoint = CwArchiveDriveInfo("current_setpoint")
            speed_setpoint = CwArchiveDriveInfo("speed_setpoint")
            actual_speed = CwArchiveDriveInfo("actual_speed")
            controller_info = CwControllerInfo()
            kinematic_tree_view = CwKinematicTree()

            self.cw_current_setpoint_drive_info.append(current_setpoint)
            self.cw_speed_setpoint_drive_info.append(speed_setpoint)
            self.cw_actual_speed_drive_info.append(actual_speed)
            self.cw_controller_info.append(controller_info)
            self.cw_kinematic_tree_view.append(kinematic_tree_view)

            self.layout_archives_surface.addWidget(current_setpoint)
            current_setpoint.hide()
            self.layout_archives_surface.addWidget(speed_setpoint)
            speed_setpoint.hide()
            self.layout_archives_surface.addWidget(actual_speed)
            actual_speed.hide()
            self.layout_archives_surface.addWidget(controller_info)
            controller_info.hide()
            self.layout_archives_surface.addWidget(kinematic_tree_view)
            kinematic_tree_view.hide()
   
        # ==========

        # Initialize submenu for removing archives
        self.actionRemoveArchiveSubmenu = qtw.QMenu("Archiv entfernen")
        self.actionRemove.setMenu(self.actionRemoveArchiveSubmenu)
        self.actionRemoveArchiveSubmenu.triggered.connect(self.on_remove_archive_action_triggered)

        # Initialize submenu for exporting archives (one entry per archive)
        self.actionExportArchiveSubmenu = qtw.QMenu("Archiv exportieren")
        self.actionExport.setMenu(self.actionExportArchiveSubmenu)
        self.actionExportArchiveSubmenu.triggered.connect(self.on_export_archive_action_triggered)

        # Connect the tab changed signal to the on_tab_changed method
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

        # Connect the "Add Archive > Browse Files" Action to add_archive_browse_files_clicked method
        self.actionAddArchive_Browse.triggered.connect(self.add_archive_browse_files_clicked)

        # Connect the "Add Archive > Add Archive Window" Action to add_archive_add_window_clicked method
        self.actionAddWindow.triggered.connect(self.add_archive_add_window_clicked)

        # Connect "+" button to add_archive_browse_files_clicked method
        self.pb_addArchive.clicked.connect(self.add_archive_add_window_clicked)

        # Connect "=" Compare button to compare_clicked method
        self.pb_compare.clicked.connect(self.compare_clicked)

        # Start with the first tab selected
        self.tabWidget.setCurrentIndex(0)

    def on_tab_changed(self, index):
        """Show/hide widgets for the selected tab index."""
        self.current_tab = index

        # Check if archive has been added
        if self.num_archives == 0:
            # If no archive is added, hide all drive info widgets
            for n in range(config.MAX_PARALLEL_ARCHIVES):
                self.cw_current_setpoint_drive_info[n].hide()
                self.cw_speed_setpoint_drive_info[n].hide()
                self.cw_actual_speed_drive_info[n].hide()
                self.cw_controller_info[n].hide()
                self.cw_kinematic_tree_view[n].hide()
            return

        if index == 0:
            # Show the Current Setpoint Filter tab
            for n in range(self.num_archives):
                self.cw_current_setpoint_drive_info[n].show()
                self.cw_speed_setpoint_drive_info[n].hide()
                self.cw_actual_speed_drive_info[n].hide()
                self.cw_controller_info[n].hide()
                self.cw_kinematic_tree_view[n].hide()

            self.current_tab = 0  # Update current tab index
        elif index == 1:
            # Show the Speed Setpoint Filter tab
            for n in range(self.num_archives):
                self.cw_current_setpoint_drive_info[n].hide()
                self.cw_speed_setpoint_drive_info[n].show()
                self.cw_actual_speed_drive_info[n].hide()
                self.cw_controller_info[n].hide()
                self.cw_kinematic_tree_view[n].hide()

            self.current_tab = 1  # Update current tab index
        elif index == 2:
            # Show the Actual Speed Filter tab
            for n in range(self.num_archives):
                self.cw_current_setpoint_drive_info[n].hide()
                self.cw_speed_setpoint_drive_info[n].hide()
                self.cw_actual_speed_drive_info[n].show()
                self.cw_controller_info[n].hide()
                self.cw_kinematic_tree_view[n].hide()

            self.current_tab = 2  # Update current tab index
        elif index == 3:
            # Show the Controller Info tab
            for n in range(self.num_archives):
                self.cw_current_setpoint_drive_info[n].hide()
                self.cw_speed_setpoint_drive_info[n].hide()
                self.cw_actual_speed_drive_info[n].hide()
                self.cw_controller_info[n].show()
                self.cw_kinematic_tree_view[n].hide()

            self.current_tab = 3  # Update current tab index
        elif index == 4:
            # Show the Kinematic Tree tab
            for n in range(self.num_archives):
                self.cw_current_setpoint_drive_info[n].hide()
                self.cw_speed_setpoint_drive_info[n].hide()
                self.cw_actual_speed_drive_info[n].hide()
                self.cw_controller_info[n].hide()
                self.cw_kinematic_tree_view[n].show()

            self.current_tab = 4  # Update current tab index
        else:
            print(f"❌ Unknown tab index: {index}. Hiding all drive info widgets.")
            # Hide all drive info widgets if an unknown tab is selected
            for n in range(config.MAX_PARALLEL_ARCHIVES):
                self.cw_current_setpoint_drive_info[n].hide()
                self.cw_speed_setpoint_drive_info[n].hide()
                self.cw_actual_speed_drive_info[n].hide()
                self.cw_controller_info[n].hide()
                self.cw_kinematic_tree_view[n].hide()

            self.current_tab = 0  # Reset current tab to 0

    def update_archive(self, archive):
        """Parse and register a newly added archive, wiring it into UI widgets."""

        parse_result = None
        if archive.type == "DSF":
            parse_result = parse_filters_from_dsf(archive)

        elif archive.type == "ARC":
            parse_result = parse_filters_from_arc(archive)
            if archive.is_binary:
                qtw.QMessageBox.warning(self, "Binäres Archiv",
                                        "Der gegebene Archiv ist im binären Format und kann nicht gelesen werden.")
        else:
            print(f"❌ Unknown archive type: {archive.type}")
            return
        
        if parse_result is None:
            qtw.QMessageBox.warning(self, "Fehlerhaftes Archiv", "Das Archiv beinhaltet keine Antriebsdaten.")
            self.archive_drag_and_drop_surfaces.pop()
            return  # Stop updating if the archive is invalid

        # Update the archive drag-and-drop surface with the new archive
        if self.num_archives < config.MAX_PARALLEL_ARCHIVES:
            self.cw_current_setpoint_drive_info[self.num_archives].update_archive(archive)
            self.cw_speed_setpoint_drive_info[self.num_archives].update_archive(archive)
            self.cw_actual_speed_drive_info[self.num_archives].update_archive(archive)
            self.cw_controller_info[self.num_archives].update_archive(archive)
            self.cw_kinematic_tree_view[self.num_archives].update_archive(archive)
        else:
            print(f"❌ Cannot add more than {config.MAX_PARALLEL_ARCHIVES} archives.")
            return

        # Track this archive and add to the Export submenu
        self.archives.append(archive)
        self.actionExportArchiveSubmenu.addAction(f"{archive.name}")

        self.num_archives += 1
        print(f"✅ Archive added. Total archives: {self.num_archives}")

        # Add this archive to the Remove Archive submenu (connection is set up once in __init__)
        self.actionRemoveArchiveSubmenu.addAction(f"{archive.name}")

        # After updating the archive number, update the tab widget to show the first tab
        self.on_tab_changed(self.current_tab)

    def export_archive_clicked(self, archive, original_archive):
        if self.num_archives == 0:
            qtw.QMessageBox.warning(self, "Kein Archiv verfügbar", "Bitte ein Archiv vor dem Export hinzufügen.")
            return
        
        if self.num_archives > 1:
            print("Multiple archives detected. Exporting the first archive only.")
            qtw.QMessageBox.warning(self, "Mehrere Archive", "Mehrere Archive beim Export entdeckt")
            return

        # Get the export path from the user
        export_path, _ = qtw.QFileDialog.getSaveFileName(
            self,
            "Export Archive",
            "",
            "Archive Files (*.dsf);;All Files (*)"
        )
        if not export_path:
            return  # User cancelled

        export_archive(archive, original_archive, export_path)

    def add_archive_browse_files_clicked(self):
        print(f"Adding archive Nr. {self.num_archives}")

        # Respect the hard limit on parallel archives
        if self.num_archives >= config.MAX_PARALLEL_ARCHIVES:
            qtw.QMessageBox.warning(self, "Maximale Anzahl an Archiven",
                                    f"Es können nicht mehr als {config.MAX_PARALLEL_ARCHIVES} Archiven hinzugefügt werden.")
            return

        # Ensure there is an empty drag-and-drop surface available for the next archive slot.
        # If all existing surfaces are already used (i.e., there's no empty window), create one on the fly.
        if len(self.archive_drag_and_drop_surfaces) <= self.num_archives:
            new_surface = ArchiveDragAndDropSurface()
            self.archive_drag_and_drop_surfaces.append(new_surface)
            self.layout_archives_surface.addWidget(new_surface)
            new_surface.archive_added_signal.connect(self.update_archive)
            new_surface.show()

        # Open the file dialog on the surface that corresponds to the next archive slot.
        self.archive_drag_and_drop_surfaces[self.num_archives].open_file_dialog()

    def add_archive_add_window_clicked(self):
        print("Adding archive window...")  # Placeholder for actual implementation

        if len(self.archive_drag_and_drop_surfaces) >= config.MAX_PARALLEL_ARCHIVES:
            qtw.QMessageBox.warning(self, "Maximale Anzahl an Archiven",
                                    f"Es können nicht mehr als {config.MAX_PARALLEL_ARCHIVES} Archiven hinzugefügt werden.")
            return

        # Only allow adding a new window if the last surface has an archive added
        if self.num_archives < len(self.archive_drag_and_drop_surfaces):
            qtw.QMessageBox.warning(self, "Leeres Fenster", f"Bitte erstmal das leere Fenster verwenden.")
            return

        # Create a new ArchiveDragAndDropSurface and add it to the layout
        new_surface = ArchiveDragAndDropSurface()
        self.archive_drag_and_drop_surfaces.append(new_surface)
        self.layout_archives_surface.addWidget(new_surface)

        # Connect the new surface's archive_added_signal to the update_archive method
        new_surface.archive_added_signal.connect(self.update_archive)

        # Show the new surface
        new_surface.show()

    def compare_clicked(self):
        # Determine desired state without mutating yet
        desired_state = not self.compare_mode

        # Only allow activating compare mode when exactly two archives are present
        if desired_state and self.num_archives != 2:
            qtw.QMessageBox.warning(self, "Fehler beim Vergleichen",
                                    "Vergleichsmodus ist nur bei zwei Archiven gleichzeitig möglich.")
            return

        # Apply new state
        self.compare_mode = desired_state
        print("Compare Mode activated" if self.compare_mode else "Compare Mode deactivated")

        if self.compare_mode:
            # Set button in different color to show that compare mode is active
            self.pb_compare.setIcon(QIcon(":/resources/equal_smns_24dp.svg"))

            # Activate compare mode for the two archives.
            self.cw_current_setpoint_drive_info[0].activate_compare_mode(self.cw_current_setpoint_drive_info[1])
            self.cw_current_setpoint_drive_info[1].activate_compare_mode(self.cw_current_setpoint_drive_info[0])
            self.cw_speed_setpoint_drive_info[0].activate_compare_mode(self.cw_speed_setpoint_drive_info[1])
            self.cw_speed_setpoint_drive_info[1].activate_compare_mode(self.cw_speed_setpoint_drive_info[0])
            self.cw_actual_speed_drive_info[0].activate_compare_mode(self.cw_actual_speed_drive_info[1])
            self.cw_actual_speed_drive_info[1].activate_compare_mode(self.cw_actual_speed_drive_info[0])
            self.cw_controller_info[0].activate_compare_mode(self.cw_controller_info[1])
            self.cw_controller_info[1].activate_compare_mode(self.cw_controller_info[0])
            self.cw_kinematic_tree_view[0].activate_compare_mode(self.cw_kinematic_tree_view[1])
            self.cw_kinematic_tree_view[1].activate_compare_mode(self.cw_kinematic_tree_view[0])
        else:
            # Reset icon
            self.pb_compare.setIcon(QIcon(":/resources/equal_blck_24dp.svg"))

            # Deactivate compare mode for the two archives
            self.cw_current_setpoint_drive_info[0].deactivate_compare_mode(self.cw_current_setpoint_drive_info[1])
            self.cw_current_setpoint_drive_info[1].deactivate_compare_mode(self.cw_current_setpoint_drive_info[0])
            self.cw_speed_setpoint_drive_info[0].deactivate_compare_mode(self.cw_speed_setpoint_drive_info[1])
            self.cw_speed_setpoint_drive_info[1].deactivate_compare_mode(self.cw_speed_setpoint_drive_info[0])
            self.cw_actual_speed_drive_info[0].deactivate_compare_mode(self.cw_actual_speed_drive_info[1])
            self.cw_actual_speed_drive_info[1].deactivate_compare_mode(self.cw_actual_speed_drive_info[0])
            self.cw_controller_info[0].deactivate_compare_mode(self.cw_controller_info[1])
            self.cw_controller_info[1].deactivate_compare_mode(self.cw_controller_info[0])
            self.cw_kinematic_tree_view[0].deactivate_compare_mode(self.cw_kinematic_tree_view[1])
            self.cw_kinematic_tree_view[1].deactivate_compare_mode(self.cw_kinematic_tree_view[0])

    def remove_archive_clicked(self, archive_index):
        # Deactivate compare mode if it was active
        if self.compare_mode: self.compare_clicked()

        # Remove archive reference (keeps order aligned with menus)
        if 0 <= archive_index < len(self.archives):
            self.archives.pop(archive_index)

        # Get all ArchiveDriveInfo widgets with the given archive index from their lists
        current_setpoint_drive_info_widget = self.cw_current_setpoint_drive_info[archive_index]
        speed_setpoint_drive_info_widget = self.cw_speed_setpoint_drive_info[archive_index]
        actual_speed_drive_info_widget = self.cw_actual_speed_drive_info[archive_index]
        drag_and_drop_surface = self.archive_drag_and_drop_surfaces[archive_index]
        controller_info_widget = self.cw_controller_info[archive_index]
        kinematic_tree_view_widget = self.cw_kinematic_tree_view[archive_index]

        # Delete the widgets from their lists
        self.cw_current_setpoint_drive_info.remove(current_setpoint_drive_info_widget)
        self.cw_speed_setpoint_drive_info.remove(speed_setpoint_drive_info_widget)
        self.cw_actual_speed_drive_info.remove(actual_speed_drive_info_widget)
        self.archive_drag_and_drop_surfaces.remove(drag_and_drop_surface)
        self.cw_controller_info.remove(controller_info_widget)
        self.cw_kinematic_tree_view.remove(kinematic_tree_view_widget)

        # Create new empty DriveInfo widgets
        new_current_setpoint_drive_info = CwArchiveDriveInfo("current_setpoint")
        new_speed_setpoint_drive_info = CwArchiveDriveInfo("speed_setpoint")
        new_actual_speed_drive_info = CwArchiveDriveInfo("actual_speed")
        new_controller_info = CwControllerInfo()
        new_kinematic_tree_view = CwKinematicTree()

        # Add the new widgets to the layout
        self.layout_archives_surface.addWidget(new_current_setpoint_drive_info)
        self.layout_archives_surface.addWidget(new_speed_setpoint_drive_info)
        self.layout_archives_surface.addWidget(new_actual_speed_drive_info)
        self.layout_archives_surface.addWidget(new_controller_info)
        self.layout_archives_surface.addWidget(new_kinematic_tree_view)

        # Append the new widgets to their respective lists
        self.cw_current_setpoint_drive_info.append(new_current_setpoint_drive_info)
        self.cw_speed_setpoint_drive_info.append(new_speed_setpoint_drive_info)
        self.cw_actual_speed_drive_info.append(new_actual_speed_drive_info)
        self.cw_controller_info.append(new_controller_info)
        self.cw_kinematic_tree_view.append(new_kinematic_tree_view)

        # Hide the new widgets initially
        new_current_setpoint_drive_info.hide()
        new_speed_setpoint_drive_info.hide()
        new_actual_speed_drive_info.hide()
        new_controller_info.hide()
        new_kinematic_tree_view.hide()

        # Delete old widgets
        current_setpoint_drive_info_widget.setParent(None)
        current_setpoint_drive_info_widget.deleteLater()
        speed_setpoint_drive_info_widget.setParent(None)
        speed_setpoint_drive_info_widget.deleteLater()
        actual_speed_drive_info_widget.setParent(None)
        actual_speed_drive_info_widget.deleteLater()
        controller_info_widget.setParent(None)
        controller_info_widget.deleteLater()
        kinematic_tree_view_widget.setParent(None)
        kinematic_tree_view_widget.deleteLater()

        # Decrease the number of archives
        self.num_archives -= 1
        self.on_tab_changed(self.current_tab)


    def on_remove_archive_action_triggered(self, action):
        """Handle clicks on the Remove Archive submenu by mapping the QAction to the current index."""
        actions = self.actionRemoveArchiveSubmenu.actions()
        try:
            index = actions.index(action)
        except ValueError:
            # Action not found; nothing to do
            return

        # Remove the clicked action first to keep menu in sync
        self.actionRemoveArchiveSubmenu.removeAction(action)

        # Remove the corresponding Export menu action to keep menus aligned
        export_actions = self.actionExportArchiveSubmenu.actions()
        if 0 <= index < len(export_actions):
            self.actionExportArchiveSubmenu.removeAction(export_actions[index])

        # Now remove the corresponding archive widgets
        self.remove_archive_clicked(index)


    def on_export_archive_action_triggered(self, action):
        """Handle clicks on the Export Archive submenu by mapping the QAction to the archive index."""
        actions = self.actionExportArchiveSubmenu.actions()
        try:
            index = actions.index(action)
        except ValueError:
            return
        self.export_archive_for_index(index)


    def export_archive_for_index(self, index: int):
        """Export the modified archive at a given list index to a user-selected path."""

        if index < 0 or index >= len(self.archives):
            print("❌ Error: Wrong index for the exporting archive.")
            qtw.QMessageBox.warning(self, "Archiv Export", "Fehler beim Auswahl des Archivs.")
            return

        archive = self.archives[index]
        original_archive = getattr(archive, "original_copy", None)
        if original_archive is None:
            print("❌ Error: No original copy of the archive found. Stopping export.")
            qtw.QMessageBox.warning(self, "Export Archive", "Export nicht möglich, da originales Archiv nicht gefunden wurde.")
            return

        # Get the export path from the user
        export_path, _ = qtw.QFileDialog.getSaveFileName(
            self,
            "Export Archive",
            "",
            "Archive Files (*.dsf);;All Files (*)"
        )
        if not export_path:
            return  # User cancelled

        export_archive(archive, original_archive, export_path)
        
    def closeEvent(self, event):
        """Handle application close: offer to save the log file and show its path."""
        print("⚠️ Closing application...")

        # Build a message asking to save the log
        msg = qtw.QMessageBox(self)
        msg.setWindowTitle("Anwendung beenden")
        msg.setIcon(qtw.QMessageBox.Icon.Question)
        msg.setText("Möchten Sie die Log‑Datei speichern?")

        cancel_btn = msg.addButton(qtw.QMessageBox.StandardButton.Cancel)
        cancel_btn.setText("Abbrechen")
        save_btn = msg.addButton("Speichern unter…", qtw.QMessageBox.ButtonRole.AcceptRole)
        close_btn = msg.addButton("Ohne Speichern schließen", qtw.QMessageBox.ButtonRole.DestructiveRole)
        msg.setDefaultButton(save_btn)
        msg.exec()

        clicked = msg.clickedButton()
        if clicked is cancel_btn:
            event.ignore()
            return

        if clicked is save_btn:
            # If we have a known log path, propose its name; otherwise fall back
            suggested_name = f"{config.APP_NAME}.log"

            target_path, _ = qtw.QFileDialog.getSaveFileName(
                self,
                "Log‑Datei speichern",
                suggested_name,
                "Log Dateien (*.log);;Alle Dateien (*)",
            )
            if not target_path:
                # User aborted save dialog -> do not close
                event.ignore()
                return

            try:
                if self.log_path is not None and Path(self.log_path).exists():
                    shutil.copyfile(str(self.log_path), target_path)
                else:
                    # Create an empty file if log is unknown/nonexistent
                    with open(target_path, "w", encoding="utf-8") as f:
                        f.write("")
            except Exception as ex:
                qtw.QMessageBox.critical(
                    self,
                    "Fehler beim Speichern",
                    f"Die Log‑Datei konnte nicht gespeichert werden.\n\nFehler: {ex}",
                )
                event.ignore()
                return

        # Close the window (either saved or explicitly chose to close without saving)
        event.accept()


if __name__ == "__main__":
    if config.ACTIVATE_LOGGING_IN_FILE:
        print(f"ACTIVATE_LOGGING_IN_FILE from config.py is set to True. All logs will be saved in a file.")
        log_path = setup_logging(config.APP_NAME, level=20)  # INFO
        logging.getLogger(__name__).info("Logging initialised: %s", log_path)
    else:
        print(f"ACTIVATE_LOGGING_IN_FILE from config.py is set to False. All logs will be printed in terminal.")
        log_path = None

    # Stop inheriting the OS colors
    qtw.QApplication.setDesktopSettingsAware(False)  # <- key line

    app = qtw.QApplication(sys.argv)

    # If Qt ≥ 6.8, explicitly hint "Light" to the platform
    try:
        from PySide6.QtGui import QGuiApplication
        QGuiApplication.styleHints().setColorScheme(Qt.ColorScheme.Light)
    except Exception:
        pass  # safe on older Qt

    window = MainWindow(log_path)
    window.setWindowIcon(QIcon(":/resources/ArchiveScope_icon.ico"))
    window.show()

    sys.exit(app.exec())