from PySide6.QtGui import QPixmap
from PySide6.QtCore import QByteArray
import base64

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

def generatePass(width=15,numbers=True,symbols=True,capitalLetters=True):
    import secrets
    import string    

    base = string.ascii_lowercase
    
    map = {
        "numbers": string.digits,
        "symbols": string.punctuation,
        "capitalLetters": string.ascii_uppercase
    }

    flags = {
        "numbers": bool(numbers),
        "symbols": bool(symbols),
        "capitalLetters": bool(capitalLetters)
    }
    
    chars = base + "".join(map[k] for k in flags if flags[k] is True)

    return ''.join(secrets.choice(chars) for _ in range(width))

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

def selectFileToHash(parent):
    from PySide6.QtWidgets import QFileDialog, QMessageBox
    path, _ = QFileDialog.getOpenFileName(parent,'Choose a file','','All files (*.*)')

    if not path:
        return None
    
    if path:
        print("RETURN PATH: " + path)
        return path
        
def seekText(pattern, data:str ):
    if not isinstance(pattern, str) or not pattern or not isinstance(data, str) or not str:
        return []
    
    results = []
    ocurrence = 0
    MAX_SHOW = 10

    for num_line, line in enumerate(data.splitlines(), start=1):
        begin = 0
        while True:
            pos = line.find(pattern, begin)
            if pos == -1:
                break
            
            ocurrence +=1
            
            if ocurrence <= MAX_SHOW:
                if ocurrence == 1:
                    results.append(
                        f'Founded:\n\non the line {num_line}, collumn {pos}: {line}.strip()')
                else:
                    results.append(f'on the line {num_line}, collumn {pos}: {line}'.strip())
            
            begin = pos + len(pattern)

    if ocurrence > MAX_SHOW:
        results.append(f'\n\n there may be more {(ocurrence-10)} ocurrences')

    return results

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
    
import hashlib

def genHash256(phrase: str):
    return hashlib.sha256(phrase.encode('utf-8')).hexdigest()

from enum import Enum
class HashMode(Enum):
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"
    MD5 = "md5"

def genHash(phrase: str, mode:HashMode):
    match mode:
        case HashMode.SHA256:
            return hashlib.sha256(phrase.encode()).hexdigest()
        case HashMode.SHA384:
            return hashlib.sha384(phrase.encode()).hexdigest()        
        case HashMode.SHA512:
            return hashlib.sha512(phrase.encode()).hexdigest()
        case HashMode.MD5:
            return hashlib.md5(phrase.encode()).hexdigest()
        case _:
            raise ValueError("Invalid mode")

def genFileHash256(path: str) -> str:
    print(path)
    
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(4096):  # read blocks of 4 KB
            h.update(chunk)
    return h.hexdigest()

def b64_wrapped(widget, b64_str, line_width: int=120):
    import textwrap
    wrapped = "\n".join(textwrap.wrap(b64_str,line_width))
    widget.setPlainText(wrapped)
