import uuid

@staticmethod
def gen_uuid() -> str:
    return str (uuid.uuid4())