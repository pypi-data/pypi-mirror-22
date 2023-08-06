#include "EnableFlag.hpp"

#include "Error.hpp"

PyObject * MGLEnableFlag_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLEnableFlag * self = (MGLEnableFlag *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLEnableFlag_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLEnableFlag_tp_dealloc(MGLEnableFlag * self) {

	#ifdef MGL_VERBOSE
	printf("MGLEnableFlag_tp_dealloc %p\n", self);
	#endif

	Py_TYPE(self)->tp_free((PyObject *)self);
}

int MGLEnableFlag_tp_init(MGLEnableFlag * self, PyObject * args, PyObject * kwargs) {
	MGLError_Set("cannot create mgl.EnableFlag manually");
	return -1;
}

PyMethodDef MGLEnableFlag_tp_methods[] = {
	{0},
};

PyGetSetDef MGLEnableFlag_tp_getseters[] = {
	{0},
};

PyTypeObject MGLEnableFlag_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"mgl.EnableFlag",                                       // tp_name
	sizeof(MGLEnableFlag),                                  // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLEnableFlag_tp_dealloc,                   // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	0,                                                      // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	0,                                                      // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT,                                     // tp_flags
	0,                                                      // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLEnableFlag_tp_methods,                               // tp_methods
	0,                                                      // tp_members
	MGLEnableFlag_tp_getseters,                             // tp_getset
	0,                                                      // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLEnableFlag_tp_init,                        // tp_init
	0,                                                      // tp_alloc
	MGLEnableFlag_tp_new,                                   // tp_new
};

MGLEnableFlag * MGLEnableFlag_New() {
	MGLEnableFlag * self = (MGLEnableFlag *)MGLEnableFlag_tp_new(&MGLEnableFlag_Type, 0, 0);
	return self;
}

MGLEnableFlag * MGL_BLEND;
MGLEnableFlag * MGL_DEPTH_TEST;
MGLEnableFlag * MGL_CULL_FACE;
MGLEnableFlag * MGL_MULTISAMPLE;
