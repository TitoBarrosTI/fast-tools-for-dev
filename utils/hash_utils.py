def selectFileToHash(parent):
    from PySide6.QtWidgets import QFileDialog, QMessageBox
    path, _ = QFileDialog.getOpenFileName(parent,'Choose a file','','All files (*.*)')

    if not path:
        return None
    
    if path:
        print("RETURN PATH: " + path)
        return path

import hashlib
from enum import Enum

class HashMode(Enum):
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"
    MD5 = "md5"
class HashUtils:
    @staticmethod
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

    @staticmethod
    def genFileHash256(path: str) -> str:
        print(path)
        
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(4096):  # read blocks of 4 KB
                h.update(chunk)
        return h.hexdigest()