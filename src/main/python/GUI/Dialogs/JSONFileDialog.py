from PyQt5.QtWidgets import QFileDialog, QWidget
import logging

class JSONFileDialog:
    def json_dialog(self):
        logging.info('json_dialog(): Instantiated')
        widget = QFileDialog()
        filename, _ = QFileDialog.getOpenFileNames(widget, "Choose a JSON file", "", "JSON Files (*.JSON)")
        return filename[0]
        logging.info('json_dialog(): Completed')
        