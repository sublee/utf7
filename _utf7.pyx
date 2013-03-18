# -*- coding: utf-8 -*-
"""
    _utf7
    ~~~~~

    Faster :mod:`utf7` written in C.

    :copyright: (c) 2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
import io


ctypedef unsigned long num_t
cdef extern from "utf7.h":
    size_t __pack(num_t num, write)
    num_t __unpack(read, int* overflowed)


# raw


cpdef size_t _pack(num_t num, write):
    return __pack(num, write)


cpdef num_t _unpack(read) except? 0:
    #TODO: it should raise OverflowError
    cdef int err = 0
    return __unpack(read, &err)


# stream


cpdef size_t pack(num_t num, buf):
    return _pack(num, buf.write)


cpdef num_t unpack(buf):
    return _unpack(buf.read)


cpdef size_t pack_socket(num_t num, sock):
    return _pack(num, sock.send)


cpdef num_t unpack_socket(sock):
    return _unpack(sock.recv)


cpdef bytes pack_bytes(num_t num):
    buf = io.BytesIO()
    pack(num, buf)
    return buf.getvalue()


cpdef num_t unpack_bytes(bytes packed):
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
