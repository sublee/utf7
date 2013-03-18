#include <Python.h>

typedef unsigned long num_t;

size_t __pack(num_t num, PyObject* write);
num_t __unpack(PyObject* read, int* err);
