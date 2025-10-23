# logging_setup.py
from __future__ import annotations
import os
import sys
import platform
import traceback
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from PySide6 import QtCore, QtWidgets
from config import APP_NAME, APP_VERSION


def _default_log_dir(app_name: str) -> Path:
    # Windows: %LOCALAPPDATA%\AppName\logs
    # Linux: ~/.local/state/AppName/logs (Fallback ~/.local/share)
    # macOS: ~/Library/Logs/AppName
    home = Path.home()
    if os.name == "nt":
        base = Path(os.getenv("LOCALAPPDATA", home / "AppData" / "Local"))
        return base / app_name / "logs"
    elif sys.platform == "darwin":
        return home / "Library" / "Logs" / app_name
    else:
        base = Path(os.getenv("XDG_STATE_HOME", home / ".local" / "state"))
        return base / app_name / "logs"


def setup_logging(
    app_name: str = APP_NAME,
    level: int = logging.INFO,
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 5,
) -> Path:
    log_dir = _default_log_dir(app_name)
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"{app_name}.log"

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(fmt)
    file_handler.setLevel(level)
    root.addHandler(file_handler)

    # Optional: Alle print()/stderr-Ausgaben ebenfalls ins Log umleiten
    class _StreamToLogger:
        def __init__(self, logger: logging.Logger, level: int):
            self.logger = logger
            self.level = level
            self._buffer = ""

        def write(self, message: str):
            if message and message != "\n":
                for line in message.rstrip().splitlines():
                    self.logger.log(self.level, line)

        def flush(self):  # für Kompatibilität
            pass

    sys.stdout = _StreamToLogger(logging.getLogger("stdout"), logging.INFO)
    sys.stderr = _StreamToLogger(logging.getLogger("stderr"), logging.ERROR)

    _install_global_exception_hook(app_name)
    _install_qt_message_handler()

    _log_session_header(app_name, log_file)
    return log_file


def _log_session_header(app_name: str, log_file: Path):
    logging.getLogger(__name__).info(
        "===== %s started =====\nPython: %s\nApp version:%s\nOS: %s\nExecutable: %s\nLog: %s",
        app_name,
        sys.version.replace("\n", " "),
        APP_VERSION,
        f"{platform.system()} {platform.release()} ({platform.version()})",
        sys.executable,
        str(log_file),
    )


def _install_global_exception_hook(app_name: str):
    def _excepthook(exc_type, exc_value, exc_tb):
        logger = logging.getLogger("UncaughtException")
        tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        logger.critical("Uncaught exception:\n%s", tb_str)

        if QtWidgets is not None:
            try:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                msg.setWindowTitle(f"{app_name} – Fehler")
                msg.setText("Ein unerwarteter Fehler ist aufgetreten.")
                msg.setInformativeText("Details wurden in der Log-Datei gespeichert.")
                msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                msg.exec()
            except Exception:
                pass

        # Danach regulär beenden
        sys.__excepthook__(exc_type, exc_value, exc_tb)

    sys.excepthook = _excepthook


def _install_qt_message_handler():
    if QtCore is None:
        return

    def qt_handler(mode, ctx, msg):
        logger = logging.getLogger("Qt")
        # QtMsgType → Level
        level_map = {
            QtCore.QtMsgType.QtDebugMsg: logging.DEBUG,
            QtCore.QtMsgType.QtInfoMsg: logging.INFO,
            QtCore.QtMsgType.QtWarningMsg: logging.WARNING,
            QtCore.QtMsgType.QtCriticalMsg: logging.ERROR,
            QtCore.QtMsgType.QtFatalMsg: logging.CRITICAL,
        }
        level = level_map.get(mode, logging.INFO)
        where = f"{ctx.file}:{ctx.line} ({ctx.function})" if ctx.file else ""
        logger.log(level, "Qt: %s %s", msg, where)

    QtCore.qInstallMessageHandler(qt_handler)