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


__version__ = '0.9.2'
__all__ = ['pack', 'unpack', 'packb', 'unpackb',
           'dump', 'dumps', 'load', 'loads', 'encode', 'decode']


def pack(num, buf):
    """Encodes the unsigned integer by UTF-7 to the buffer."""
    if num < 0:
        raise OverflowError('Cannot pack negative number')
    array = bytearray()
    while num:
        byte = num & 0x7f
        num >>= 7
        if num:
            # 1st bit is a flag to indecate to read more
            array.append(byte | 0x80)
        else:
            array.append(byte)
            break
    buf.write(array)
    return len(array)


def unpack(buf):
    """Decodes the unsigned integer by UTF-7 from the buffer."""
    num = 0
    shift = 0
    byte = 0x80
    while byte & 0x80:
        try:
            byte = ord(buf.read(1))
        except TypeError:
            raise IOError('Buffer empty')
        num |= (byte & 0x7f) << shift
        shift += 7
    return num


def packb(num):
    buf = BytesIO()
    pack(num, buf)
    return buf.getvalue()


def unpackb(packed):
    return unpack(BytesIO(packed))


# aliases
dump = pack
dumps = packb
load = unpack
loads = unpackb
encode = packb
decode = unpackb
