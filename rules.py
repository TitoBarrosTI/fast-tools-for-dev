def showBase64(self,b64_str,B64ImgDestiny):
    try:
        import base64
        data = base64.b64decode(b64_str)
    except:
        print("Invalid base64")
        return

    from PySide6.QtGui import QPixmap
    from PySide6.QtCore import QByteArray

    pix = QPixmap()
    pix.loadFromData(data)

    if pix.isNull():
        print("Not is a valid image")
        return
    
    B64ImgDestiny.setPixmap(pix)
    B64ImgDestiny.setScaledContents(True)

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

def is_base64_image(data: str) -> bool:
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
    from PySide6.QtWidgets import QFileDialog
    path, _ = QFileDialog.getOpenFileName(parent,'Choose a file','','All files (*.*)')

    if not path:
        return None
    
    if path:
        with open(path,'r',encoding='utf-8', errors='ignore') as f:
            return f.read()
        
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