#include "BufferAccess.hpp"

#include "Error.hpp"

PyObject * MGLBufferAccess_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLBufferAccess * self = (MGLBufferAccess *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLBufferAccess_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLBufferAccess_tp_dealloc(MGLBufferAccess * self) {

	#ifdef MGL_VERBOSE
	printf("MGLBufferAccess_tp_dealloc %p\n", self);
	#endif

	MGLBufferAccess_Type.tp_free((PyObject *)self);
}

int MGLBufferAccess_tp_init(MGLBufferAccess * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_FromFormat(TRACE, "Cannot create mgl.BufferAccess manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLBufferAccess_tp_str(MGLBufferAccess * self) {
	return PyUnicode_FromFormat("<mgl.BufferAccess>");
}

PyObject * MGLBufferAccess_open(MGLBufferAccess * self) {
	if (self->ptr) {
		MGLError * error = MGLError_FromFormat(TRACE, "BufferAccess.open: Already open");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	const GLMethods & gl = self->buffer->context->gl;
	gl.BindBuffer(GL_ARRAY_BUFFER, self->buffer_obj);
	self->ptr = gl.MapBufferRange(GL_ARRAY_BUFFER, self->offset, self->size, self->access);

	if (!self->ptr) {
		MGLError * error = MGLError_FromFormat(TRACE, "BufferAccess.open: Cannot map buffer");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	Py_RETURN_NONE;
}

PyObject * MGLBufferAccess_close(MGLBufferAccess * self) {
	if (self->ptr) {
		const GLMethods & gl = self->buffer->context->gl;
		gl.BindBuffer(GL_ARRAY_BUFFER, self->buffer_obj);
		gl.UnmapBuffer(GL_ARRAY_BUFFER);
	}
	Py_RETURN_NONE;
}

PyObject * MGLBufferAccess_read(MGLBufferAccess * self, PyObject * args) {
	int size;
	int offset;

	int args_ok = PyArg_ParseTuple(
		args,
		"II",
		&size,
		&offset
	);

	if (!args_ok) {
		return 0;
	}

	if (size == -1) {
		size = self->size - offset;
	}

	if (offset < 0 || size < 0 || size + offset > self->size) {
		MGLError * error = MGLError_FromFormat(TRACE, "BufferAccess.read: offset = %d or size = %d out of range", offset, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	if (!self->ptr) {
		MGLError * error = MGLError_FromFormat(TRACE, "BufferAccess.read: Call BufferAccess.open() first");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	return PyBytes_FromStringAndSize((const char *)self->ptr, size);
}

PyObject * MGLBufferAccess_write(MGLBufferAccess * self, PyObject * args) {
	const char * data;
	int size;
	int offset;

	int args_ok = PyArg_ParseTuple(
		args,
		"y#I",
		&data,
		&size,
		&offset
	);

	if (!args_ok) {
		return 0;
	}

	if (offset < 0 || size + offset > self->size) {
		MGLError * error = MGLError_FromFormat(TRACE, "BufferAccess.write: offset = %d or size = %d out of range", offset, size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	if (!self->ptr) {
		MGLError * error = MGLError_FromFormat(TRACE, "BufferAccess.write: Call BufferAccess.open() first");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	memcpy(self->ptr, data, size);

	Py_RETURN_NONE;
}

PyMethodDef MGLBufferAccess_tp_methods[] = {
	{"open", (PyCFunction)MGLBufferAccess_open, METH_NOARGS, 0},
	{"close", (PyCFunction)MGLBufferAccess_close, METH_VARARGS, 0},

	{"read", (PyCFunction)MGLBufferAccess_read, METH_VARARGS, 0},
	{"write", (PyCFunction)MGLBufferAccess_write, METH_VARARGS, 0},
	{0},
};

MGLBuffer * MGLBufferAccess_get_buffer(MGLBufferAccess * self) {
	Py_INCREF(self->buffer);
	return self->buffer;
}

PyObject * MGLBufferAccess_get_offset(MGLBufferAccess * self) {
	return PyLong_FromLong(self->offset);
}

PyObject * MGLBufferAccess_get_size(MGLBufferAccess * self) {
	return PyLong_FromLong(self->size);
}

PyObject * MGLBufferAccess_get_readonly(MGLBufferAccess * self) {
	return PyBool_FromLong(self->access & GL_MAP_WRITE_BIT);
}

PyGetSetDef MGLBufferAccess_tp_getseters[] = {
	{(char *)"buffer", (getter)MGLBufferAccess_get_buffer, 0, 0, 0},
	{(char *)"offset", (getter)MGLBufferAccess_get_offset, 0, 0, 0},
	{(char *)"size", (getter)MGLBufferAccess_get_size, 0, 0, 0},
	{(char *)"readonly", (getter)MGLBufferAccess_get_readonly, 0, 0, 0},
	{0},
};

PyTypeObject MGLBufferAccess_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"mgl.BufferAccess",                                     // tp_name
	sizeof(MGLBufferAccess),                                // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLBufferAccess_tp_dealloc,                 // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLBufferAccess_tp_str,                       // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	0,                                                      // tp_str
	0,                                                      // tp_getattro
	0,                                                      // tp_setattro
	0,                                                      // tp_as_buffer
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,               // tp_flags
	0,                                                      // tp_doc
	0,                                                      // tp_traverse
	0,                                                      // tp_clear
	0,                                                      // tp_richcompare
	0,                                                      // tp_weaklistoffset
	0,                                                      // tp_iter
	0,                                                      // tp_iternext
	MGLBufferAccess_tp_methods,                             // tp_methods
	0,                                                      // tp_members
	MGLBufferAccess_tp_getseters,                           // tp_getset
	0,                                                      // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLBufferAccess_tp_init,                      // tp_init
	0,                                                      // tp_alloc
	MGLBufferAccess_tp_new,                                 // tp_new
};

MGLBufferAccess * MGLBufferAccess_New() {
	MGLBufferAccess * self = (MGLBufferAccess *)MGLBufferAccess_tp_new(&MGLBufferAccess_Type, 0, 0);
	return self;
}
