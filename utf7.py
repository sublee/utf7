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
import struct
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


__version__ = '0.9.1'
__all__ = [
    'packb', 'pack', 'unpackb', 'unpack', 'dumps', 'dump', 'loads', 'load']


def packb(num):
    buf = BytesIO()
    pack(num, buf)
    return buf.getvalue()


def pack(num, buf):
    array = []
    while True:
        byte = num & 0xff
        num >>= 7
        if num:
            array.append(byte | 0x80)
        else:
            array.append(byte)
            break
    size = len(array)
    buf.write(struct.pack('<%dB' % size, *array))
    return size


def unpackb(packed):
    return unpack(BytesIO(packed))


def unpack(buf):
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


dumps = packb
dump = pack
loads = unpackb
load = unpack
