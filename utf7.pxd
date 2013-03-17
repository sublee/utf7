# -*- coding: utf-8 -*-
"""
    _utf7
    ~~~~~

    Faster utf7 compiled with Cython.

    :copyright: (c) 2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
cimport cython


ctypedef unsigned char byte_t


@cython.locals(array=bytearray, byte=byte_t, size=size_t)
cpdef size_t _pack(unsigned int num, write) nogil


@cython.locals(num=unsigned int, shift=size_t, byte=byte_t)
cpdef unsigned int _unpack(read) nogil
