"""
Referenced from: https://github.com/danakt/uuid-by-string
"""

import hashlib
import struct
from typing import List, Optional

HEX_DIGITS = '0123456789abcdef'


def int32_to_int8(i: int) -> int:
    int32 = struct.pack("I", i)
    int8 = struct.unpack("B" * 4, int32)
    return int8[0]


def uint8_to_hex(ubyte: int) -> str:
    first = ubyte >> 4
    second = ubyte - (first << 4)
    return HEX_DIGITS[first] + HEX_DIGITS[second]


def uint8array_to_hex(buf: List[int]) -> str:
    out = []
    for i in buf:
        out.append(uint8_to_hex(i))
    return "".join(out)


def string_to_char_buffer(s: str) -> List[int]:
    buf = []
    for i in s:
        int8 = int32_to_int8(ord(i))
        buf.append(int8)
    return buf


def concat_buffers(buf1: List[int], buf2: List[int]) -> List[int]:
    return buf1 + buf2


def hash_to_uuid(hash_buf, version) -> str:
    return "".join([
        uint8array_to_hex(hash_buf[:4]),
        "-",
        uint8array_to_hex(hash_buf[4:6]),
        "-",
        uint8_to_hex(hash_buf[6] & 0x0f | int(str(version * 10), 16)),
        uint8_to_hex(hash_buf[7]),
        "-",
        uint8_to_hex((hash_buf[8] & 0x3f) | 0x80),
        uint8_to_hex(hash_buf[9]),
        "-",
        uint8array_to_hex(hash_buf[10:16])
    ])


def md5_hash(buf: List[int]) -> List[int]:
    md5 = hashlib.md5()
    ba = bytearray(buf)
    md5.update(ba)
    digest = md5.digest()
    int8 = struct.unpack("B" * 16, digest[:16])
    return list(int8)


def sha1_hash(buf: List[int]) -> List[int]:
    sha1 = hashlib.sha1()
    ba = bytearray(buf)
    sha1.update(ba)
    digest = sha1.digest()
    int8 = struct.unpack("B" * 16, digest[:16])
    return list(int8)


def generate_uuid(
        target: str,
        namespace: Optional[str] = None,
        version: Optional[int] = 5) -> str:
    """
    Parameters
    ----------
    target: The string need to be generated for a uuid.
    namespace: A predefined namespace for generation.
    version: Version of UUID Available versions is 3 and 5
    * according to RFC-4122. The version is responsible for the hashing algorithm:
    * version 3 uses MD5, and version 5 uses SHA-1. Default is 5.

    Returns
    --------
    The UUID string for the given target.
    """

    if type(target) != str:
        raise ValueError("Value must be string")

    if type(namespace) == int:
        return generate_uuid(target, None, namespace)

    if not version:
        return generate_uuid(target, namespace, 5)

    if version != 3 and version != 5:
        raise TypeError("Version of UUID can be only 3 or 5")

    char_buf = string_to_char_buffer(target)
    if type(namespace) == str:
        namespace_char_buf = string_to_char_buffer(namespace)
    else:
        namespace_char_buf = []

    buf = concat_buffers(namespace_char_buf, char_buf)

    if version == 3:
        hash_arr = md5_hash(buf)
    else:
        hash_arr = sha1_hash(buf)

    return hash_to_uuid(hash_arr, version)
