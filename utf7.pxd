# -*- coding: utf-8 -*-
"""
    _utf7
    ~~~~~

    Faster utf7 compiled with Cython.

    :copyright: (c) 2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
cimport cython


@cython.locals(array=list, byte=int, size=size_t)
cpdef size_t pack(unsigned int num, buf)


@cython.locals(num=int, shift=int, byte=int)
cpdef unsigned int unpack(buf)


cpdef bytes packb(unsigned int num)
cpdef unsigned int unpackb(bytes packed)
