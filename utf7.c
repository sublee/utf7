/*
    utf7.c
    ~~~~~~

    C implementation of :func:`utf7._pack` and :func:`utf7._unpack`.

    :copyright: (c) 2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
*/
#include <Python.h>
#include "utf7.h"


PyObject* __pack(num_t num, PyObject* write) {
    size_t size = 0;
    unsigned char byte;
    unsigned char bytes[10];
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
    PyObject* rv = PyObject_CallFunction(write, "s#", bytes, size);
    Py_DECREF(rv);
    return Py_BuildValue("n", size);
}


PyObject* __unpack(PyObject* read) {
    PyObject* str;
    unsigned char byte = 0x80;
    num_t num = 0;
    size_t shift;
    for (shift = 0; byte & 0x80; shift += 7) {
        str = PyObject_CallFunction(read, "i", 1);
        if (!PyString_Size(str)) {
            PyErr_SetString(PyExc_IOError, "Buffer empty");
            return NULL;
        }
        byte = *(unsigned char*)PyString_AsString(str);
        if (shift == 63 && byte > 0x01) {
            PyErr_SetString(PyExc_OverflowError, "8 bytes exceeded");
            return NULL;
        }
        num |= (byte & 0x7f) << shift;
    }
    return Py_BuildValue("k", num);
}
