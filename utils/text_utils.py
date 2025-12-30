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
                        f'Founded:\n\non the line {num_line}, collumn {pos}: {line}'.strip())
                else:
                    results.append(f'on the line {num_line}, collumn {pos}: {line}'.strip())
            
            begin = pos + len(pattern)

    if ocurrence > MAX_SHOW:
        results.append(f'\n\n there may be more {(ocurrence-10)} ocurrences')

    return results

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