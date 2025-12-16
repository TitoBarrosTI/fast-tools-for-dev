def selectFile(parent):
    from PySide6.QtWidgets import QFileDialog, QMessageBox
    path, _ = QFileDialog.getOpenFileName(parent,'Choose a file','','All files (*.*)')

    if not path:
        return None
    
    if not isTextFile(path):
        QMessageBox.warning(parent, "Error", "File is not text")
        return None
    
    if path:
        with open(path,'r',encoding='utf-8', errors='ignore') as f:
            return f.read()
        
def isTextFile(path):
    with open(path, "rb") as f:
        chunk = f.read(2048)
    
    try:
        chunk.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False

def isImageFile(path):
    import imghdr
    return imghdr.what(path) is not None