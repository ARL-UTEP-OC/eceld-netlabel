from PyQt5.QtWidgets import QFileDialog, QWidget
import logging

class WiresharkFileDialog:
    def wireshark_dialog(self):
        logging.info('wireshark_dialog(): Instantiated')
        widget = QFileDialog()
        filename, _ = QFileDialog.getOpenFileNames(widget, "Choose a Wireshark file", "", "Wireshark Files (*.pcapng)")
        return filename[0]
        logging.info('wireshark_dialog(): Completed')