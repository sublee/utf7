/*
    utf7.c
    ~~~~~~

    C implementation of :func:`utf7._pack` and :func:`utf7._unpack`.

    :copyright: (c) 2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
*/
#include <Python.h>
#include "utf7.h"


size_t __pack(num_t num, PyObject* write) {
    size_t size = 0;
    char byte;
    char bytes[10];
    while (1) {
        byte = num & 0x7f;
        num >>= 7;
        if (num) {
            bytes[size++] = byte | 0x80;
        } else {
            bytes[size++] = byte;
            break;
        }
    }
    PyObject* bytearray = PyByteArray_FromStringAndSize(bytes, size);
    PyObject_CallFunction(write, "O", bytearray);
    return size;
}


num_t __unpack(PyObject* read, int* err) {
    size_t shift;
    char byte = 0x80;
    num_t num = 0;
    for (shift = 0; byte & 0x80; shift += 7) {
        byte = *(char*)PyString_AsString(PyObject_CallFunction(read, "i", 1));
        if (shift == 63 && byte > 0x01) {
            PyErr_SetString(PyExc_OverflowError, "Hello");
            *err = 1;
            return 0;
        }
        num |= (byte & 0x7f) << shift;
    }
    return num;
}
