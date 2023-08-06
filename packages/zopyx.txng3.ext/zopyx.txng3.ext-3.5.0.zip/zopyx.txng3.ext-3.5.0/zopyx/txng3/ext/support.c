/*
 TextIndexNG V 3
 The next generation TextIndex for Zope

 This software is governed by a license. See
 LICENSE.txt for the terms of this license.
*/

#include "Python.h"
#include <stdlib.h>
#if PY_MAJOR_VERSION >= 3
#define PY3K
#endif

static PyObject *
stopwordfilter(PyObject *modinfo, PyObject *args)
{
    PyObject *stopwords, *words, *list;
    int i, len;

    list = PyList_New(0);

    if (! (PyArg_ParseTuple(args,"OO",&words,&stopwords)))
        return NULL;

    words = PySequence_Fast(words, "1st argument must be a sequence");
    len = PyObject_Length(words);

    for (i=0; i<len; i++) {
        PyObject *item  = PySequence_Fast_GET_ITEM(words, i);

        if (PyDict_GetItem(stopwords, item) == NULL)
            PyList_Append(list,item);
    }

    Py_XDECREF(words);

    return list;
}


static struct PyMethodDef support_module_methods[] =
    {
        { "stopwordfilter", (PyCFunction) stopwordfilter, METH_VARARGS,
            "stopwordfilter(wordslist,stopword dict') " "-- filters words from wordslist that are stopwords"
        },
        { NULL, NULL }
    };

#ifdef PY3K
static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "support",                      /* m_name */
        "TexnIndexNG support module",   /* m_doc */
        -1,                             /* m_size */
        support_module_methods,         /* m_methods */
        NULL,                           /* m_reload */
        NULL,                           /* m_traverse */
        NULL,                           /* m_clear */
        NULL,                           /* m_free */
    };
#endif

static PyObject*
module_init(void)
{
    PyObject *m;

    /* Create the module and add the functions */
#ifdef PY3K
    m = PyModule_Create(&moduledef);
#else
    m = Py_InitModule3("support", support_module_methods,
                        "TextIndexNG support module");
#endif
    return m;
}


#ifdef PY3K
PyMODINIT_FUNC PyInit_support(void)
{
    return module_init();
}
#else
PyMODINIT_FUNC initsupport(void)
{
    module_init();
}
#endif
