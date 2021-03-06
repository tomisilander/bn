/* Generated by Pyrex 0.9.5.1a on Sat Feb 23 16:50:00 2008 */

#include "Python.h"
#include "structmember.h"
#ifndef PY_LONG_LONG
  #define PY_LONG_LONG LONG_LONG
#endif
#ifdef __cplusplus
#define __PYX_EXTERN_C extern "C"
#else
#define __PYX_EXTERN_C extern
#endif
__PYX_EXTERN_C double pow(double, double);
#include "bde_score.h"
#include "stdlib.h"
#include "cdata.h"


typedef struct {PyObject **p; char *s;} __Pyx_InternTabEntry; /*proto*/
typedef struct {PyObject **p; char *s; long n;} __Pyx_StringTabEntry; /*proto*/

static PyObject *__pyx_m;
static PyObject *__pyx_b;
static int __pyx_lineno;
static char *__pyx_filename;
static char **__pyx_f;

static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, int none_allowed, char *name); /*proto*/

static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list); /*proto*/

static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name); /*proto*/

static PyObject *__Pyx_UnpackItem(PyObject *); /*proto*/
static int __Pyx_EndUnpack(PyObject *); /*proto*/

static int __Pyx_InternStrings(__Pyx_InternTabEntry *t); /*proto*/

static PyTypeObject *__Pyx_ImportType(char *module_name, char *class_name, long size);  /*proto*/

static void __Pyx_AddTraceback(char *funcname); /*proto*/

/* Declarations from data */


struct __pyx_obj_4data_Data {
  PyObject_HEAD
  data (*dt);
};

static PyTypeObject *__pyx_ptype_4data_Data = 0;

/* Declarations from cscore */



/* Implementation of cscore */


static PyObject *__pyx_n_BN;
static PyObject *__pyx_n_score;
static PyObject *__pyx_n_cscore_ss_var;
static PyObject *__pyx_n_bn;

static PyObject *__pyx_n_parents;
static PyObject *__pyx_n_len;
static PyObject *__pyx_n_enumerate;

static PyObject *__pyx_f_6cscore_cscore_ss_var(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static PyObject *__pyx_f_6cscore_cscore_ss_var(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  struct __pyx_obj_4data_Data *__pyx_v_dat = 0;
  double __pyx_v_ess;
  PyObject *__pyx_v_bn = 0;
  int __pyx_v_v;
  PyObject *__pyx_v_parentset;
  int __pyx_v_nof_parents;
  int (*__pyx_v_parents);
  PyObject *__pyx_v_i;
  PyObject *__pyx_v_p;
  PyObject *__pyx_v_res;
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  PyObject *__pyx_2 = 0;
  PyObject *__pyx_3 = 0;
  int __pyx_4;
  int __pyx_5;
  static char *__pyx_argnames[] = {"dat","ess","bn","v",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "OdOi", __pyx_argnames, &__pyx_v_dat, &__pyx_v_ess, &__pyx_v_bn, &__pyx_v_v)) return 0;
  Py_INCREF(__pyx_v_dat);
  Py_INCREF(__pyx_v_bn);
  __pyx_v_parentset = Py_None; Py_INCREF(Py_None);
  __pyx_v_i = Py_None; Py_INCREF(Py_None);
  __pyx_v_p = Py_None; Py_INCREF(Py_None);
  __pyx_v_res = Py_None; Py_INCREF(Py_None);
  if (!__Pyx_ArgTypeTest(((PyObject *)__pyx_v_dat), __pyx_ptype_4data_Data, 0, "dat")) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 16; goto __pyx_L1;}

  /* "/home/tsilande/projects/bn/learn/pyx/cscore.pyx":18 */
  __pyx_1 = PyObject_GetAttr(__pyx_v_bn, __pyx_n_parents); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; goto __pyx_L1;}
  __pyx_2 = PyInt_FromLong(__pyx_v_v); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; goto __pyx_L1;}
  __pyx_3 = PyTuple_New(1); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; goto __pyx_L1;}
  PyTuple_SET_ITEM(__pyx_3, 0, __pyx_2);
  __pyx_2 = 0;
  __pyx_2 = PyObject_CallObject(__pyx_1, __pyx_3); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 18; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  Py_DECREF(__pyx_v_parentset);
  __pyx_v_parentset = __pyx_2;
  __pyx_2 = 0;

  /* "/home/tsilande/projects/bn/learn/pyx/cscore.pyx":21 */
  __pyx_1 = __Pyx_GetName(__pyx_b, __pyx_n_len); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; goto __pyx_L1;}
  __pyx_3 = PyTuple_New(1); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; goto __pyx_L1;}
  Py_INCREF(__pyx_v_parentset);
  PyTuple_SET_ITEM(__pyx_3, 0, __pyx_v_parentset);
  __pyx_2 = PyObject_CallObject(__pyx_1, __pyx_3); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  __pyx_4 = PyInt_AsLong(__pyx_2); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 21; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  __pyx_v_nof_parents = __pyx_4;

  /* "/home/tsilande/projects/bn/learn/pyx/cscore.pyx":24 */
  __pyx_v_parents = ((int (*))calloc(__pyx_v_nof_parents,(sizeof(int ))));

  /* "/home/tsilande/projects/bn/learn/pyx/cscore.pyx":26 */
  __pyx_1 = __Pyx_GetName(__pyx_b, __pyx_n_enumerate); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; goto __pyx_L1;}
  __pyx_3 = PyTuple_New(1); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; goto __pyx_L1;}
  Py_INCREF(__pyx_v_parentset);
  PyTuple_SET_ITEM(__pyx_3, 0, __pyx_v_parentset);
  __pyx_2 = PyObject_CallObject(__pyx_1, __pyx_3); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  __pyx_1 = PyObject_GetIter(__pyx_2); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  for (;;) {
    __pyx_3 = PyIter_Next(__pyx_1);
    if (!__pyx_3) {
      if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; goto __pyx_L1;}
      break;
    }
    __pyx_2 = PyObject_GetIter(__pyx_3); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; goto __pyx_L1;}
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    __pyx_3 = __Pyx_UnpackItem(__pyx_2); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; goto __pyx_L1;}
    Py_DECREF(__pyx_v_i);
    __pyx_v_i = __pyx_3;
    __pyx_3 = 0;
    __pyx_3 = __Pyx_UnpackItem(__pyx_2); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; goto __pyx_L1;}
    Py_DECREF(__pyx_v_p);
    __pyx_v_p = __pyx_3;
    __pyx_3 = 0;
    if (__Pyx_EndUnpack(__pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 26; goto __pyx_L1;}
    Py_DECREF(__pyx_2); __pyx_2 = 0;

    /* "/home/tsilande/projects/bn/learn/pyx/cscore.pyx":27 */
    __pyx_4 = PyInt_AsLong(__pyx_v_p); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 27; goto __pyx_L1;}
    __pyx_5 = PyInt_AsLong(__pyx_v_i); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 27; goto __pyx_L1;}
    (__pyx_v_parents[__pyx_5]) = __pyx_4;
  }
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/tsilande/projects/bn/learn/pyx/cscore.pyx":29 */
  __pyx_3 = PyFloat_FromDouble(bde_score(__pyx_v_dat->dt,__pyx_v_ess,__pyx_v_v,__pyx_v_nof_parents,__pyx_v_parents)); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 29; goto __pyx_L1;}
  Py_DECREF(__pyx_v_res);
  __pyx_v_res = __pyx_3;
  __pyx_3 = 0;

  /* "/home/tsilande/projects/bn/learn/pyx/cscore.pyx":31 */
  free(__pyx_v_parents);

  /* "/home/tsilande/projects/bn/learn/pyx/cscore.pyx":33 */
  Py_INCREF(__pyx_v_res);
  __pyx_r = __pyx_v_res;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  Py_XDECREF(__pyx_2);
  Py_XDECREF(__pyx_3);
  __Pyx_AddTraceback("cscore.cscore_ss_var");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_parentset);
  Py_DECREF(__pyx_v_i);
  Py_DECREF(__pyx_v_p);
  Py_DECREF(__pyx_v_res);
  Py_DECREF(__pyx_v_dat);
  Py_DECREF(__pyx_v_bn);
  return __pyx_r;
}

static __Pyx_InternTabEntry __pyx_intern_tab[] = {
  {&__pyx_n_BN, "BN"},
  {&__pyx_n_bn, "bn"},
  {&__pyx_n_cscore_ss_var, "cscore_ss_var"},
  {&__pyx_n_enumerate, "enumerate"},
  {&__pyx_n_len, "len"},
  {&__pyx_n_parents, "parents"},
  {&__pyx_n_score, "score"},
  {0, 0}
};

static struct PyMethodDef __pyx_methods[] = {
  {"cscore_ss_var", (PyCFunction)__pyx_f_6cscore_cscore_ss_var, METH_VARARGS|METH_KEYWORDS, 0},
  {0, 0, 0, 0}
};

static void __pyx_init_filenames(void); /*proto*/

PyMODINIT_FUNC initcscore(void); /*proto*/
PyMODINIT_FUNC initcscore(void) {
  PyObject *__pyx_1 = 0;
  PyObject *__pyx_2 = 0;
  __pyx_init_filenames();
  __pyx_m = Py_InitModule4("cscore", __pyx_methods, 0, 0, PYTHON_API_VERSION);
  if (!__pyx_m) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  __pyx_b = PyImport_AddModule("__builtin__");
  if (!__pyx_b) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  if (PyObject_SetAttrString(__pyx_m, "__builtins__", __pyx_b) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  if (__Pyx_InternStrings(__pyx_intern_tab) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;};
  __pyx_ptype_4data_Data = __Pyx_ImportType("data", "Data", sizeof(struct __pyx_obj_4data_Data)); if (!__pyx_ptype_4data_Data) {__pyx_filename = __pyx_f[1]; __pyx_lineno = 13; goto __pyx_L1;}

  /* "/home/tsilande/projects/bn/learn/pyx/cscore.pyx":1 */
  __pyx_1 = PyList_New(1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;}
  Py_INCREF(__pyx_n_BN);
  PyList_SET_ITEM(__pyx_1, 0, __pyx_n_BN);
  __pyx_2 = __Pyx_Import(__pyx_n_bn, __pyx_1); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_1 = PyObject_GetAttr(__pyx_2, __pyx_n_BN); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_BN, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 1; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  Py_DECREF(__pyx_2); __pyx_2 = 0;

  /* "/home/tsilande/projects/bn/learn/pyx/cscore.pyx":2 */
  __pyx_2 = __Pyx_Import(__pyx_n_score, 0); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 2; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_score, __pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 2; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;

  /* "/home/tsilande/projects/bn/learn/pyx/cscore.pyx":16 */
  return;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  Py_XDECREF(__pyx_2);
  __Pyx_AddTraceback("cscore");
}

static char *__pyx_filenames[] = {
  "cscore.pyx",
  "data.pxd",
};

/* Runtime support code */

static void __pyx_init_filenames(void) {
  __pyx_f = __pyx_filenames;
}

static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, int none_allowed, char *name) {
    if (!type) {
        PyErr_Format(PyExc_SystemError, "Missing type object");
        return 0;
    }
    if ((none_allowed && obj == Py_None) || PyObject_TypeCheck(obj, type))
        return 1;
    PyErr_Format(PyExc_TypeError,
        "Argument '%s' has incorrect type (expected %s, got %s)",
        name, type->tp_name, obj->ob_type->tp_name);
    return 0;
}

static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list) {
    PyObject *__import__ = 0;
    PyObject *empty_list = 0;
    PyObject *module = 0;
    PyObject *global_dict = 0;
    PyObject *empty_dict = 0;
    PyObject *list;
    __import__ = PyObject_GetAttrString(__pyx_b, "__import__");
    if (!__import__)
        goto bad;
    if (from_list)
        list = from_list;
    else {
        empty_list = PyList_New(0);
        if (!empty_list)
            goto bad;
        list = empty_list;
    }
    global_dict = PyModule_GetDict(__pyx_m);
    if (!global_dict)
        goto bad;
    empty_dict = PyDict_New();
    if (!empty_dict)
        goto bad;
    module = PyObject_CallFunction(__import__, "OOOO",
        name, global_dict, empty_dict, list);
bad:
    Py_XDECREF(empty_list);
    Py_XDECREF(__import__);
    Py_XDECREF(empty_dict);
    return module;
}

static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name) {
    PyObject *result;
    result = PyObject_GetAttr(dict, name);
    if (!result)
        PyErr_SetObject(PyExc_NameError, name);
    return result;
}

static void __Pyx_UnpackError(void) {
    PyErr_SetString(PyExc_ValueError, "unpack sequence of wrong size");
}

static PyObject *__Pyx_UnpackItem(PyObject *iter) {
    PyObject *item;
    if (!(item = PyIter_Next(iter))) {
        if (!PyErr_Occurred())
            __Pyx_UnpackError();
    }
    return item;
}

static int __Pyx_EndUnpack(PyObject *iter) {
    PyObject *item;
    if ((item = PyIter_Next(iter))) {
        Py_DECREF(item);
        __Pyx_UnpackError();
        return -1;
    }
    else if (!PyErr_Occurred())
        return 0;
    else
        return -1;
}

static int __Pyx_InternStrings(__Pyx_InternTabEntry *t) {
    while (t->p) {
        *t->p = PyString_InternFromString(t->s);
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}

static PyTypeObject *__Pyx_ImportType(char *module_name, char *class_name, 
    long size) 
{
    PyObject *py_module_name = 0;
    PyObject *py_class_name = 0;
    PyObject *py_name_list = 0;
    PyObject *py_module = 0;
    PyObject *result = 0;
    
    py_module_name = PyString_FromString(module_name);
    if (!py_module_name)
        goto bad;
    py_class_name = PyString_FromString(class_name);
    if (!py_class_name)
        goto bad;
    py_name_list = PyList_New(1);
    if (!py_name_list)
        goto bad;
    Py_INCREF(py_class_name);
    if (PyList_SetItem(py_name_list, 0, py_class_name) < 0)
        goto bad;
    py_module = __Pyx_Import(py_module_name, py_name_list);
    if (!py_module)
        goto bad;
    result = PyObject_GetAttr(py_module, py_class_name);
    if (!result)
        goto bad;
    if (!PyType_Check(result)) {
        PyErr_Format(PyExc_TypeError, 
            "%s.%s is not a type object",
            module_name, class_name);
        goto bad;
    }
    if (((PyTypeObject *)result)->tp_basicsize != size) {
        PyErr_Format(PyExc_ValueError, 
            "%s.%s does not appear to be the correct type object",
            module_name, class_name);
        goto bad;
    }
    goto done;
bad:
    Py_XDECREF(result);
    result = 0;
done:
    Py_XDECREF(py_module_name);
    Py_XDECREF(py_class_name);
    Py_XDECREF(py_name_list);
    return (PyTypeObject *)result;
}

#include "compile.h"
#include "frameobject.h"
#include "traceback.h"

static void __Pyx_AddTraceback(char *funcname) {
    PyObject *py_srcfile = 0;
    PyObject *py_funcname = 0;
    PyObject *py_globals = 0;
    PyObject *empty_tuple = 0;
    PyObject *empty_string = 0;
    PyCodeObject *py_code = 0;
    PyFrameObject *py_frame = 0;
    
    py_srcfile = PyString_FromString(__pyx_filename);
    if (!py_srcfile) goto bad;
    py_funcname = PyString_FromString(funcname);
    if (!py_funcname) goto bad;
    py_globals = PyModule_GetDict(__pyx_m);
    if (!py_globals) goto bad;
    empty_tuple = PyTuple_New(0);
    if (!empty_tuple) goto bad;
    empty_string = PyString_FromString("");
    if (!empty_string) goto bad;
    py_code = PyCode_New(
        0,            /*int argcount,*/
        0,            /*int nlocals,*/
        0,            /*int stacksize,*/
        0,            /*int flags,*/
        empty_string, /*PyObject *code,*/
        empty_tuple,  /*PyObject *consts,*/
        empty_tuple,  /*PyObject *names,*/
        empty_tuple,  /*PyObject *varnames,*/
        empty_tuple,  /*PyObject *freevars,*/
        empty_tuple,  /*PyObject *cellvars,*/
        py_srcfile,   /*PyObject *filename,*/
        py_funcname,  /*PyObject *name,*/
        __pyx_lineno,   /*int firstlineno,*/
        empty_string  /*PyObject *lnotab*/
    );
    if (!py_code) goto bad;
    py_frame = PyFrame_New(
        PyThreadState_Get(), /*PyThreadState *tstate,*/
        py_code,             /*PyCodeObject *code,*/
        py_globals,          /*PyObject *globals,*/
        0                    /*PyObject *locals*/
    );
    if (!py_frame) goto bad;
    py_frame->f_lineno = __pyx_lineno;
    PyTraceBack_Here(py_frame);
bad:
    Py_XDECREF(py_srcfile);
    Py_XDECREF(py_funcname);
    Py_XDECREF(empty_tuple);
    Py_XDECREF(empty_string);
    Py_XDECREF(py_code);
    Py_XDECREF(py_frame);
}
