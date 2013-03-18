# -*- coding: utf-8 -*-
"""
    _utf7
    ~~~~~

    Faster :mod:`utf7` written in C.

    :copyright: (c) 2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
import io

from utf7 import __version__


ctypedef unsigned long num_t
cdef extern from "utf7.h":
    __pack(num_t num, write)
    __unpack(read)


# raw


cpdef _pack(num_t num, write):
    return __pack(num, write)


cpdef _unpack(read):
    return __unpack(read)


# stream


cpdef pack(num_t num, buf):
    return _pack(num, buf.write)


cpdef unpack(buf):
    return _unpack(buf.read)


cpdef pack_socket(num_t num, sock):
    return _pack(num, sock.send)


cpdef unpack_socket(sock):
    return _unpack(sock.recv)


cpdef pack_bytes(num_t num):
    buf = io.BytesIO()
    pack(num, buf)
    return buf.getvalue()


cpdef unpack_bytes(bytes packed):
    return unpack(io.BytesIO(packed))


# aliases


packb = pack_bytes
unpackb = unpack_bytes
dump = pack
dumps = packb
load = unpack
loads = unpackb
encode = packb
decode = unpackb
