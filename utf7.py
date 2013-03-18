# -*- coding: utf-8 -*-
"""
    utf7
    ~~~~

    Encoder/decoder for an UTF-7 encoded unsigned integer used by
    ```BinaryWriter.Write(String)`` <http://msdn.microsoft.com/en-us/library/
    yzxa6408.aspx>`_ in Microsoft .NET Framework.

    :copyright: (c) 2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


__version__ = '0.9.3'
__all__ = ['pack', 'unpack', 'pack_socket', 'unpack_socket',
           'pack_bytes', 'unpack_bytes', 'packb', 'unpackb',
           'dump', 'dumps', 'load', 'loads', 'encode', 'decode']


def _pack(num, write):
    """Encodes the unsigned integer by UTF-7 to the buffer."""
    if num < 0:
        raise OverflowError('Cannot pack negative number')
    array = bytearray()
    while True:
        byte = num & 0x7f
        num >>= 7
        if num:
            # 1st bit is a flag to indecate to read more
            array.append(byte | 0x80)
        else:
            array.append(byte)
            break
    write(array)
    return len(array)


def _unpack(read):
    """Decodes the unsigned integer by UTF-7 from the buffer."""
    num = 0
    shift = 0
    byte = 0x80
    while byte & 0x80:
        try:
            byte = ord(read(1))
        except TypeError:
            raise IOError('Buffer empty')
        num |= (byte & 0x7f) << shift
        shift += 7
    return num


def pack(num, buf):
    return _pack(num, buf.write)


def unpack(buf):
    return _unpack(buf.read)


def pack_socket(num, sock):
    return _pack(num, sock.send)


def unpack_socket(sock):
    return _unpack(sock.recv)


def pack_bytes(num):
    buf = BytesIO()
    pack(num, buf)
    return buf.getvalue()


def unpack_bytes(packed):
    return unpack(BytesIO(packed))


# aliases
packb = pack_bytes
unpackb = unpack_bytes
dump = pack
dumps = packb
load = unpack
loads = unpackb
encode = packb
decode = unpackb
