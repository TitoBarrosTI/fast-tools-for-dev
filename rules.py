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