from PyQt5.QtWidgets import QFileDialog, QWidget
import logging

class JSONFolderDialog:
    def json_dialog(self):
        logging.info('json_dialog(): Instantiated')
        widget = QFileDialog()
        foldername = str(QFileDialog.getExistingDirectory(widget, "Select Directory"))
        return foldername
        logging.info('json_dialog(): Completed')
        