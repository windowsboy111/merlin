import lzma


def compress(path: str, content):
    f = lzma.open(path, 'w')
    f.write(bytes(content, encoding='utf-8'))
    f.close()


def decompress(path):
    f = lzma.open(path, 'r')
    result = f.read()
    f.close()
    return result
