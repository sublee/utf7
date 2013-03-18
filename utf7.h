#include <Python.h>

typedef unsigned long num_t;

PyObject* __pack(num_t num, PyObject* write);
PyObject* __unpack(PyObject* read);
