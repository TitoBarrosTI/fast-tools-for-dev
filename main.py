import sys
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QMenu
from PySide6.QtUiTools import loadUiType
from rules import b64ToImage, imageFileToBase64, obtainPixMap, generatePass, isBase64Image, isImageFile, selectFile, selectFileToHash, seekText, genHash256, genFileHash256, b64_wrapped

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

        # buttons & edits
        self.btnObtainB64.clicked.connect(self.on_click_obtainB64)
        self.btnGenImageFromB64.clicked.connect(self.on_click_gen_image_fromB64)

        self.btnObtainImg.clicked.connect(self.on_click_obtain_image)
        self.btnGenB64.clicked.connect(self.on_click_gen_image_from_b64)
        
        self.btnGenPass.clicked.connect(self.on_click_genpass)
        self.btnCopyPass.clicked.connect(self.on_click_genpass_copy)
        self.btnOpenFileText.clicked.connect(self.on_click_open_file_text)
        self.btnGetFileForCrypto.clicked.connect(self.on_click_open_file_text_crypto)
        self.btnSearchInFile.clicked.connect(self.on_click_seek_text)
        self.lnEdSearchInFile.returnPressed.connect(self.btnSearchInFile.click)
        self.chbxIsFile.setEnabled(True)
        self.chbxIsFile.stateChanged.connect(self.on_click_toogle_button_get_file_for_crypto)
        self.btnGenCrypto.clicked.connect(self.on_click_encrypt)
        self.btnGenCrypto.setEnabled(True)

        self.lblImgB64.customContextMenuRequested.connect(self.menuCtxImgB64)

    def menuCtxImgB64(self, pos):
        menu = QMenu(self)
        clearImgAction = QAction("Clear image", self) # type: ignore
        clearImgAction.triggered.connect(self.clear_label)
        menu.addAction(clearImgAction)
        menu.exec(self.lblImgB64.mapToGlobal(pos))

    def clear_label(self):
        self.lblImgB64.clear()
        self.lblImgB64.setToolTip('')

    def on_click_obtain_image(self):
        from PySide6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(self,"Choose a image file","","Images (*.jpg *.png *.bmp)")
               
        if path and isImageFile(path):
            self.lblImgB64.setPixmap(obtainPixMap(self, path))
            self.lblImgB64.setToolTip(path)
            self.btnGenB64.setEnabled(True)
        else:
            self.btnGenB64.setEnabled(False)

    def on_click_gen_image_from_b64(self):
        b64 = str(self.lblImgB64.toolTip()).strip()
        if b64:
            b64_wrapped(self.txtB64,imageFileToBase64(self,b64))
            self.btnGenB64.setEnabled(False)
        else: QMessageBox.warning(self,"No content","No images available to generate Base64 content.")

    def on_click_encrypt(self):
        # if not self.edtOriginEncrypt.text():
        #     QMessageBox.information(self,'Warning','Any text for encrypt')
        #     return None
        
        if self.lstCryptoMode.currentRow() == -1:
            QMessageBox.information(self,'Warning','Select a encrypt mode')
            return None
        else:
            if self.lstCryptoMode.currentItem().text() == 'SHA256':
                self.edtHashGenerated.setText(genHash256(self.edtOriginEncrypt.text()))
        
    def on_click_toogle_button_get_file_for_crypto(self, state) -> None:
        self.btnGetFileForCrypto.setEnabled(state == Qt.CheckState.Checked)
    
    def on_click_open_file_text(self) -> None:
        content = selectFile(self)
        if content:
            self.textFile.setPlainText(content)

    def on_click_open_file_text_crypto(self):
        content = selectFileToHash(self)
        if content:
            self.edtOriginEncrypt.setText(genFileHash256(content))

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

                if isBase64Image(content):
                    self.btnGenImageFromB64.setEnabled(True)
                    if content.startswith("data:image"):
                        self.txtB64.setPlainText(content.split(',',1)[1])
                    else:
                        self.txtB64.setPlainText(content)
    
    def on_click_gen_image_fromB64(self):
        if not self.textFile.toPlainText().strip():
            b64text = self.txtB64.toPlainText()
            b64ToImage(self,b64text,self.lblImgB64)
    
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