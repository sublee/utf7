cimport cython


@cython.locals(array=list, byte=int, size=int)
cpdef int pack(int num, buf)

@cython.locals(num=int, shift=int, byte=int)
cpdef int unpack(buf)

cpdef bytes packb(int num)
cpdef int unpackb(bytes packed)
