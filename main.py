import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtUiTools import loadUiType
from rules import showBase64, generatePass, is_base64_image, selectFile, seekText

# === TO EMBED DESIGNER IN EXECUTABLE ===
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path) # type: ignore
    return os.path.join(os.path.abspath("."), relative_path)

ui_path = resource_path("main_window.ui")
Ui_MainWindow, BaseClass = loadUiType(ui_path) # type: ignore
# ======================================

class MainWindow(BaseClass, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.tabWidget.setCurrentIndex(0)

        # buttons
        self.btnObtainB64.clicked.connect(self.on_click_obtainB64)
        self.btnGenB64.clicked.connect(self.on_click_gen64)
        self.btnGenPass.clicked.connect(self.on_click_genpass)
        self.btnCopyPass.clicked.connect(self.on_click_genpass_copy)
        self.btnOpenFileText.clicked.connect(self.on_click_open_file_text)
        self.btnSearchInFile.clicked.connect(self.on_click_seek_text)
        self.lnEdSearchInFile.returnPressed.connect(self.btnSearchInFile.click)        

    def on_click_open_file_text(self):
        content = selectFile(self)
        if content:
            self.textFile.setPlainText(content)

    def on_click_seek_text(self):
        results = seekText(self.lnEdSearchInFile.text(), self.textFile.toPlainText())

        if results:
            QMessageBox.information(
                     self,
                    'Results',
                    '\n'.join(results)
                )
        else:
                QMessageBox.information(
                    self,
                    'Results',
                    'No matches found.'
            )
    
    def on_click_obtainB64(self):
        from PySide6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(
            self,"Choose a file with B64 content","","All files (*.*)"
        )
        if path:
            with open(path,'r',encoding='utf-8', errors='ignore') as f:
                content = f.read()

                if is_base64_image(content):
                    if content.startswith("data:image"):
                        self.txtB64.setPlainText(content.split(',',1)[1])
                        self.btnGenB64.setEnabled(True)
                    else: self.btnGenB64.setEnabled(False)
    
    def on_click_gen64(self):
        if not self.textFile.toPlainText().strip():
            b64text = self.txtB64.toPlainText()
            showBase64(self,b64text,self.lblImgB64)
    
    def on_click_genpass(self):
        self.edtGeneratedPass.setText(generatePass(int(self.spinPass.text()),bool(self.chbxNumbers.isChecked()),bool(self.chbxSymbols.isChecked()),bool(self.chbxCapitalLetter.isChecked())))

    def on_click_genpass_copy(self):
        from PySide6.QtGui import QClipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(self.edtGeneratedPass.text())

app = QApplication([])
window = MainWindow()
window.show()
app.exec()