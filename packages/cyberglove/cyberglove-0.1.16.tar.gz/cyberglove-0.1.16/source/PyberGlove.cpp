#include <Python.h>
#include "numpy/arrayobject.h"
#include "CyberGlove.h"
#include "CyberGlove_utils.h"

static PyObject *cyberglove_init(PyObject *self, PyObject *args);
static PyObject *cyberglove_getdata(PyObject *self, PyObject *args);
static PyObject *cyberglove_clean(PyObject *self, PyObject *args);

static cgOption* opt;
static int initialized = 0;

static const char *cyberglove_doc = " \
Cyberglove module, provides access to data from the glove, transformed into \
a more convenient representation (which matches our shadowhand simulation). \
";

static PyMethodDef CybergloveMethods[] = {
    {"init",  cyberglove_init, METH_VARARGS, "Initialize the glove"},
    {"getdata",  cyberglove_getdata, METH_NOARGS, "Get data from the glove"},
    {"clean",  cyberglove_clean, METH_NOARGS, "Cleanup and close glove"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef cyberglovemodule = {
   PyModuleDef_HEAD_INIT,
   "cyberglove",   /* name of module */
   cyberglove_doc, /* module documentation, may be NULL */
   -1,             /* module keeps state in global variables. */
   CybergloveMethods
};

static PyObject *
cyberglove_init(PyObject *self, PyObject *args)
{
    int result = 1;
    const char *config_filename;

    if (!PyArg_ParseTuple(args, "s", &config_filename))
        return NULL;

    if (initialized) {
        PyErr_SetString(PyExc_RuntimeError, "Already initialized!");
        return NULL;
    }

    opt = readOptions(config_filename);
    if(opt->USEGLOVE) {
    	result = cGlove_init(opt);
        initialized = 1;
    }

    return PyBool_FromLong(result);
}

static PyObject *
cyberglove_getdata(PyObject *self, PyObject *args)
{
    PyObject *data;
    npy_intp ndim;

    if (!initialized) {
        PyErr_SetString(PyExc_RuntimeError, "Cannot getdata without init()!");
        return NULL;
    }

    ndim = opt->calibSenor_n;
    data = PyArray_SimpleNew(1, &ndim, NPY_DOUBLE);

    cGlove_getData((cgNum *)PyArray_DATA(data), opt->calibSenor_n);

    return data;
}

static PyObject *
cyberglove_clean(PyObject *self, PyObject *args)
{
    if (initialized) {
        cGlove_clean(NULL);
        initialized = 0;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

void cleanup_atexit(void) {
    if (initialized) {
        cGlove_clean(NULL);
        initialized = 0;
    }
}

PyMODINIT_FUNC
PyInit_cyberglove(void)
{
    PyObject *m;

    m = PyModule_Create(&cyberglovemodule);
    if (m == NULL)
        return NULL;

    import_array();  // Required for NumPy

    Py_AtExit(cleanup_atexit);  // Ensure cleanup even on crash

    return m;
}
