#include "Texture.hpp"

#include "Error.hpp"
#include "InvalidObject.hpp"

#include "InlineMethods.hpp"

PyObject * MGLTexture_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLTexture * self = (MGLTexture *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLTexture_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLTexture_tp_dealloc(MGLTexture * self) {

	#ifdef MGL_VERBOSE
	printf("MGLTexture_tp_dealloc %p\n", self);
	#endif

	MGLTexture_Type.tp_free((PyObject *)self);
}

int MGLTexture_tp_init(MGLTexture * self, PyObject * args, PyObject * kwargs) {
	MGLError_Set("cannot create mgl.Texture manually");
	return -1;
}

PyObject * MGLTexture_read(MGLTexture * self, PyObject * args) {
	PyObject * viewport;
	int alignment;

	int args_ok = PyArg_ParseTuple(
		args,
		"OI",
		&viewport,
		&alignment
	);

	if (!args_ok) {
		return 0;
	}

	if (alignment != 1 && alignment != 2 && alignment != 4 && alignment != 8) {
		MGLError_Set("the alignment must be 1, 2, 4 or 8");
		return 0;
	}

	if (self->samples) {
		MGLError_Set("multisample textures cannot be read directly");
		return 0;
	}

	int x = 0;
	int y = 0;
	int width = self->width;
	int height = self->height;

	if (viewport != Py_None) {
		if (Py_TYPE(viewport) != &PyTuple_Type) {
			MGLError_Set("the viewport must be a tuple not %s", Py_TYPE(viewport)->tp_name);
			return 0;
		}

		if (PyTuple_GET_SIZE(viewport) == 4) {

			x = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 0));
			y = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 1));
			width = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 2));
			height = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 3));

		} else if (PyTuple_GET_SIZE(viewport) == 2) {

			width = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 0));
			height = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 1));

		} else {

			MGLError_Set("the viewport size %d is invalid", PyTuple_GET_SIZE(viewport));
			return 0;

		}

		if (PyErr_Occurred()) {
			MGLError_Set("wrong values in the viewport");
			return 0;
		}

	}

	int expected_size = width * self->components * (self->floats ?  4 : 1);
	expected_size = (expected_size + alignment - 1) / alignment * alignment;
	expected_size = expected_size * height;

	PyObject * result = PyBytes_FromStringAndSize(0, expected_size);
	char * data = PyBytes_AS_STRING(result);

	const int formats[] = {0, GL_RED, GL_RG, GL_RGB, GL_RGBA};

	int texture_target = self->samples ? GL_TEXTURE_2D_MULTISAMPLE : GL_TEXTURE_2D;
	int pixel_type = self->floats ? GL_FLOAT : GL_UNSIGNED_BYTE;
	int format = formats[self->components];

	const GLMethods & gl = self->context->gl;

	gl.ActiveTexture(GL_TEXTURE0 + self->context->default_texture_unit);
	gl.BindTexture(texture_target, self->texture_obj);

	gl.PixelStorei(GL_UNPACK_ALIGNMENT, alignment);
	gl.GetTexImage(texture_target, 0, format, pixel_type, data);

	return result;
}

PyObject * MGLTexture_read_into(MGLTexture * self, PyObject * args) {
	PyObject * data;
	PyObject * viewport;
	int alignment;

	int args_ok = PyArg_ParseTuple(
		args,
		"OOI",
		&data,
		&viewport,
		&alignment
	);

	if (!args_ok) {
		return 0;
	}

	if (alignment != 1 && alignment != 2 && alignment != 4 && alignment != 8) {
		MGLError_Set("the alignment must be 1, 2, 4 or 8");
		return 0;
	}

	if (self->samples) {
		MGLError_Set("multisample textures cannot be read directly");
		return 0;
	}

	int x = 0;
	int y = 0;
	int width = self->width;
	int height = self->height;

	if (viewport != Py_None) {
		if (Py_TYPE(viewport) != &PyTuple_Type) {
			MGLError_Set("the viewport must be a tuple not %s", Py_TYPE(viewport)->tp_name);
			return 0;
		}

		if (PyTuple_GET_SIZE(viewport) == 4) {

			x = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 0));
			y = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 1));
			width = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 2));
			height = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 3));

		} else if (PyTuple_GET_SIZE(viewport) == 2) {

			width = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 0));
			height = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 1));

		} else {

			MGLError_Set("the viewport size %d is invalid", PyTuple_GET_SIZE(viewport));
			return 0;

		}

		if (PyErr_Occurred()) {
			MGLError_Set("wrong values in the viewport");
			return 0;
		}

	}

	int expected_size = width * self->components * (self->floats ?  4 : 1);
	expected_size = (expected_size + alignment - 1) / alignment * alignment;
	expected_size = expected_size * height;

	Py_buffer buffer_view;

	int get_buffer = PyObject_GetBuffer(data, &buffer_view, PyBUF_WRITABLE);
	if (get_buffer < 0) {
		MGLError_Set("the buffer (%s) does not support buffer interface", Py_TYPE(data)->tp_name);
		return 0;
	}

	if (buffer_view.len < expected_size) {
		MGLError_Set("the buffer is too small %d < %d", buffer_view.len, expected_size);
		PyBuffer_Release(&buffer_view);
		return 0;
	}

	const int formats[] = {0, GL_RED, GL_RG, GL_RGB, GL_RGBA};

	int texture_target = self->samples ? GL_TEXTURE_2D_MULTISAMPLE : GL_TEXTURE_2D;
	int pixel_type = self->floats ? GL_FLOAT : GL_UNSIGNED_BYTE;
	int format = formats[self->components];

	const GLMethods & gl = self->context->gl;

	gl.ActiveTexture(GL_TEXTURE0 + self->context->default_texture_unit);
	gl.BindTexture(texture_target, self->texture_obj);

	gl.PixelStorei(GL_UNPACK_ALIGNMENT, alignment);
	gl.GetTexImage(texture_target, 0, format, pixel_type, buffer_view.buf);

	PyBuffer_Release(&buffer_view);
	Py_RETURN_NONE;
}

PyObject * MGLTexture_write(MGLTexture * self, PyObject * args) {
	PyObject * data;
	PyObject * viewport;
	int alignment;

	int args_ok = PyArg_ParseTuple(
		args,
		"OOI",
		&data,
		&viewport,
		&alignment
	);

	if (!args_ok) {
		return 0;
	}

	if (alignment != 1 && alignment != 2 && alignment != 4 && alignment != 8) {
		MGLError_Set("the alignment must be 1, 2, 4 or 8");
		return 0;
	}

	if (self->samples) {
		MGLError_Set("multisample textures cannot be written directly");
		return 0;
	}

	int x = 0;
	int y = 0;
	int width = self->width;
	int height = self->height;

	Py_buffer buffer_view;

	if (viewport != Py_None) {
		if (Py_TYPE(viewport) != &PyTuple_Type) {
			MGLError_Set("the viewport must be a tuple not %s", Py_TYPE(viewport)->tp_name);
			return 0;
		}

		if (PyTuple_GET_SIZE(viewport) == 4) {

			x = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 0));
			y = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 1));
			width = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 2));
			height = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 3));

		} else if (PyTuple_GET_SIZE(viewport) == 2) {

			width = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 0));
			height = PyLong_AsLong(PyTuple_GET_ITEM(viewport, 1));

		} else {

			MGLError_Set("the viewport size %d is invalid", PyTuple_GET_SIZE(viewport));
			return 0;

		}

		if (PyErr_Occurred()) {
			MGLError_Set("wrong values in the viewport");
			return 0;
		}

	}

	int expected_size = width * self->components * (self->floats ?  4 : 1);
	expected_size = (expected_size + alignment - 1) / alignment * alignment;
	expected_size = expected_size * height;

	PyObject_GetBuffer(data, &buffer_view, PyBUF_SIMPLE);

	if (buffer_view.len != expected_size) {
		MGLError_Set("data size mismatch %d != %d", buffer_view.len, expected_size);
		if (data != Py_None) {
			PyBuffer_Release(&buffer_view);
		}
		return 0;
	}

	const int formats[] = {0, GL_RED, GL_RG, GL_RGB, GL_RGBA};

	int texture_target = self->samples ? GL_TEXTURE_2D_MULTISAMPLE : GL_TEXTURE_2D;
	int pixel_type = self->floats ? GL_FLOAT : GL_UNSIGNED_BYTE;
	int format = formats[self->components];

	const GLMethods & gl = self->context->gl;

	gl.ActiveTexture(GL_TEXTURE0 + self->context->default_texture_unit);
	gl.BindTexture(texture_target, self->texture_obj);

	gl.PixelStorei(GL_PACK_ALIGNMENT, alignment);
	gl.TexSubImage2D(texture_target, 0, x, y, width, height, format, pixel_type, buffer_view.buf);

	PyBuffer_Release(&buffer_view);

	Py_RETURN_NONE;
}

PyObject * MGLTexture_clear(MGLTexture * self, PyObject * args) {

	// TODO:

	PyErr_Format(PyExc_NotImplementedError, "NYI");
	return 0;
}

PyObject * MGLTexture_use(MGLTexture * self, PyObject * args) {
	int index;

	int args_ok = PyArg_ParseTuple(
		args,
		"I",
		&index
	);

	if (!args_ok) {
		return 0;
	}

	int texture_target = self->samples ? GL_TEXTURE_2D_MULTISAMPLE : GL_TEXTURE_2D;

	const GLMethods & gl = self->context->gl;
	gl.ActiveTexture(GL_TEXTURE0 + index);
	gl.BindTexture(texture_target, self->texture_obj);

	Py_RETURN_NONE;
}

PyObject * MGLTexture_generate_mipmaps(MGLTexture * self, PyObject * args) {

	// TODO:

	PyErr_Format(PyExc_NotImplementedError, "NYI");
	return 0;
}

PyObject * MGLTexture_release(MGLTexture * self) {
	MGLTexture_Invalidate(self);
	Py_RETURN_NONE;
}

PyMethodDef MGLTexture_tp_methods[] = {
	{"read", (PyCFunction)MGLTexture_read, METH_VARARGS, 0},
	{"read_into", (PyCFunction)MGLTexture_read_into, METH_VARARGS, 0},
	{"write", (PyCFunction)MGLTexture_write, METH_VARARGS, 0},
	{"clear", (PyCFunction)MGLTexture_clear, METH_VARARGS, 0},
	{"use", (PyCFunction)MGLTexture_use, METH_VARARGS, 0},
	{"generate_mipmaps", (PyCFunction)MGLTexture_generate_mipmaps, METH_VARARGS, 0},
	{"release", (PyCFunction)MGLTexture_release, METH_NOARGS, 0},
	{0},
};

PyObject * MGLTexture_get_filter(MGLTexture * self) {
	PyErr_Format(PyExc_NotImplementedError, "NYI");
	return 0;
}

int MGLTexture_set_filter(MGLTexture * self, PyObject * value) {
	PyErr_Format(PyExc_NotImplementedError, "NYI");
	return -1;
}

PyObject * MGLTexture_get_swizzle(MGLTexture * self, void * closure) {
	PyErr_Format(PyExc_NotImplementedError, "NYI");
	return 0;
}

int MGLTexture_set_swizzle(MGLTexture * self, PyObject * value, void * closure) {
	const char * swizzle = PyUnicode_AsUTF8(value);

	if (!swizzle[0]) {
		MGLError_Set("the swizzle is empty");
		return -1;
	}

	int tex_swizzle[4] = {-1, -1, -1, -1};

	for (int i = 0; swizzle[i]; ++i) {
		if (i > 3) {
			MGLError_Set("the swizzle is too long");
			return -1;
		}

		tex_swizzle[i] = swizzle_from_char(swizzle[i]);

		if (tex_swizzle[i] == -1) {
			MGLError_Set("'%c' is not a valid swizzle parameter", swizzle[i]);
			return -1;
		}
	}

	int texture_target = self->samples ? GL_TEXTURE_2D_MULTISAMPLE : GL_TEXTURE_2D;

	const GLMethods & gl = self->context->gl;

	gl.ActiveTexture(GL_TEXTURE0 + self->context->default_texture_unit);
	gl.BindTexture(texture_target, self->texture_obj);

	gl.TexParameteri(texture_target, GL_TEXTURE_SWIZZLE_R, tex_swizzle[0]);
	if (tex_swizzle[1] != -1) {
		gl.TexParameteri(texture_target, GL_TEXTURE_SWIZZLE_G, tex_swizzle[1]);
		if (tex_swizzle[2] != -1) {
			gl.TexParameteri(texture_target, GL_TEXTURE_SWIZZLE_B, tex_swizzle[2]);
			if (tex_swizzle[3] != -1) {
				gl.TexParameteri(texture_target, GL_TEXTURE_SWIZZLE_A, tex_swizzle[3]);
			}
		}
	}

	return 0;
}

PyObject * MGLTexture_get_width(MGLTexture * self, void * closure) {
	return PyLong_FromLong(self->width);
}

PyObject * MGLTexture_get_height(MGLTexture * self, void * closure) {
	return PyLong_FromLong(self->height);
}

PyObject * MGLTexture_get_components(MGLTexture * self, void * closure) {
	return PyLong_FromLong(self->components);
}

PyObject * MGLTexture_get_samples(MGLTexture * self, void * closure) {
	return PyLong_FromLong(self->samples);
}

PyObject * MGLTexture_get_depth(MGLTexture * self, void * closure) {
	return PyBool_FromLong(self->depth);
}

MGLContext * MGLTexture_get_context(MGLTexture * self, void * closure) {
	Py_INCREF(self->context);
	return self->context;
}

PyObject * MGLTexture_get_glo(MGLTexture * self, void * closure) {
	return PyLong_FromLong(self->texture_obj);
}

PyGetSetDef MGLTexture_tp_getseters[] = {
	{(char *)"filter", (getter)MGLTexture_get_filter, (setter)MGLTexture_set_filter, 0, 0},
	{(char *)"swizzle", (getter)MGLTexture_get_swizzle, (setter)MGLTexture_set_swizzle, 0, 0},

	{(char *)"width", (getter)MGLTexture_get_width, 0, 0, 0},
	{(char *)"height", (getter)MGLTexture_get_height, 0, 0, 0},
	{(char *)"components", (getter)MGLTexture_get_components, 0, 0, 0},
	{(char *)"samples", (getter)MGLTexture_get_samples, 0, 0, 0},
	{(char *)"depth", (getter)MGLTexture_get_depth, 0, 0, 0},
	{(char *)"context", (getter)MGLTexture_get_context, 0, 0, 0},
	{(char *)"glo", (getter)MGLTexture_get_glo, 0, 0, 0},
	{0},
};

PyTypeObject MGLTexture_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"mgl.Texture",                                          // tp_name
	sizeof(MGLTexture),                                     // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLTexture_tp_dealloc,                      // tp_dealloc
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
	MGLTexture_tp_methods,                                  // tp_methods
	0,                                                      // tp_members
	MGLTexture_tp_getseters,                                // tp_getset
	0,                                                      // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLTexture_tp_init,                           // tp_init
	0,                                                      // tp_alloc
	MGLTexture_tp_new,                                      // tp_new
};

MGLTexture * MGLTexture_New() {
	MGLTexture * self = (MGLTexture *)MGLTexture_tp_new(&MGLTexture_Type, 0, 0);
	return self;
}

void MGLTexture_Invalidate(MGLTexture * texture) {
	if (Py_TYPE(texture) == &MGLInvalidObject_Type) {

		#ifdef MGL_VERBOSE
		printf("MGLTexture_Invalidate %p already released\n", texture);
		#endif

		return;
	}

	#ifdef MGL_VERBOSE
	printf("MGLTexture_Invalidate %p\n", texture);
	#endif

	texture->context->gl.DeleteTextures(1, (GLuint *)&texture->texture_obj);

	Py_DECREF(texture->context);

	Py_TYPE(texture) = &MGLInvalidObject_Type;

	Py_DECREF(texture);
}
