"""
The base-encoding library.  
Copyright (C) windowsboy111 2020  
You can know more about base_encoding [here](https://github.com/windowsboy111/base-encoding)  
LICENSE: MIT
"""


char64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
char128 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789あいうえおかきくけこさしすせそざじずぜぞたちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわをん"
char256 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわをんァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヲンヴヵヶ亜唖娃阿哀愛挨姶逢葵茜穐悪握渥旭葦芦鯵梓圧斡扱宛姐虻飴絢綾"


class IntEncoder:
    @classmethod
    def encode_base64(cls, value: int) -> str:
        return (char64[value] if (value < 64) else cls.encode_base64(value // 64) + char64[value % 64]) if value >= 64 else char64[value]

    @classmethod
    def decode_base64(cls, value: str) -> int:
        return (char64.index(value[-1]) + cls.decode_base64(value[:-1]) * 64) if (len(value) > 1) else char64.index(value)

    @classmethod
    def encode_base128(cls, value: int) -> str:
        return (char128[value] if (value < 128) else cls.encode_base128(value // 128) + char128[value % 128]) if value >= 128 else char128[value]

    @classmethod
    def decode_base128(cls, value: str) -> int:
        return (char128.index(value[-1]) + cls.decode_base128(value[:-1]) * 128) if (len(value) > 1) else char128.index(value)

    @classmethod
    def encode_base256(cls, value: int) -> str:
        return (char256[value] if (value < 256) else cls.encode_base256(value // 256) + char256[value % 256]) if value >= 256 else char256[value]

    @classmethod
    def decode_base256(cls, value: str) -> int:
        return (char256.index(value[-1]) + cls.decode_base256(value[:-1]) * 256) if (len(value) > 1) else char256.index(value)


class StrEncoder:
    @classmethod
    def encode_base64(cls, value: str) -> str:
        return IntEncoder.encode_base64(ord(value))

    @classmethod
    def decode_base64(cls, value: str) -> str:
        return chr(IntEncoder.decode_base64(value))

    @classmethod
    def encode_base128(cls, value: str) -> str:
        return IntEncoder.encode_base128(ord(value))

    @classmethod
    def decode_base128(cls, value: str) -> str:
        return chr(IntEncoder.decode_base64(value))

    @classmethod
    def encode_base256(cls, value: str) -> str:
        return IntEncoder.encode_base256(ord(value))

    @classmethod
    def decode_base256(cls, value: str) -> str:
        return chr(IntEncoder.decode_base256(value))
