from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent

class DropLabel(QLabel):
    fileDropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(('.dsf', '.arc')):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(('.dsf', '.arc')):
                print(f"✅ Dropped file: {path}")
                self.fileDropped.emit(path)
                return

        print("❌ Dropped unsupported file.")
        self.setText("Unsupported file")