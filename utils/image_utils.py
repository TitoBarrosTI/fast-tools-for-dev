import base64
from PySide6.QtGui import QPixmap

def b64ToImage(self,b64_str,B64ImgDestiny):
    try:
        data = base64.b64decode(b64_str)
    except:
        print("Invalid base64")
        return

    pix = QPixmap()
    if not pix.loadFromData(data):
        print("Not is a valid image")
        return
    
    B64ImgDestiny.setPixmap(pix)
    B64ImgDestiny.setScaledContents(True)

def imageFileToBase64(self, file_path):
    import base64

    with open(file_path, "rb") as img_file:
        img_bytes = img_file.read()

    return base64.b64encode(img_bytes).decode("utf-8")

def obtainPixMap(self, filePath):
    from PySide6.QtWidgets import QMessageBox

    if not filePath:
        return

    pix = QPixmap(filePath)

    if pix.isNull():
        QMessageBox.warning(self, "Error", "Invalid image")
        return
    
    return pix

def isBase64Image(data: str) -> bool:
    if not isinstance(data, str):
        return False

    # remove the prefix if comes like this: data:image/png;base64,...
    if data.startswith("data:image"):
        try:
            data = data.split(",", 1)[1]
        except IndexError:
            return False

    try:
        import base64
        decoded = base64.b64decode(data, validate=True)
    except Exception:
        return False

    # Real signatures of image file (magic numbers)
    signatures = {
        b"\xFF\xD8\xFF": "jpg",
        b"\x89PNG\r\n\x1A\n": "png",
        b"GIF87a": "gif",
        b"GIF89a": "gif",
        b"BM": "bmp",
        b"RIFF": "webp"
    }

    for sig in signatures:
        if decoded.startswith(sig):
            return True

    return False

def b64_wrapped(widget, b64_str, line_width: int=120):
    import textwrap
    wrapped = "\n".join(textwrap.wrap(b64_str,line_width))
    widget.setPlainText(wrapped)