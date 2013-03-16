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


__version__ = '0.9.0'
__all__ = ['packb', 'pack', 'unpackb', 'unpack', 'loads', 'load', 'dumps',
           'dump']


def packb(num):
    buf = []
    while True:
        byte = num & 0xff
        num >>= 7
        if num:
            buf.append(byte | 0x80)
        else:
            buf.append(byte)
            break
    size = len(buf)
    return struct.pack('<%dB' % size, *buf)


def pack(num, buf):
    buf.write(packb(num))


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


loads = packb
load = pack
dumps = unpackb
dump = unpack
