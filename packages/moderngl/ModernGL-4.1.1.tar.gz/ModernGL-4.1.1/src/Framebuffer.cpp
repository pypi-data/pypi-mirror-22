#include "Framebuffer.hpp"

#include "Error.hpp"
#include "InvalidObject.hpp"
#include "Renderbuffer.hpp"
#include "Texture.hpp"

PyObject * MGLFramebuffer_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLFramebuffer * self = (MGLFramebuffer *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLFramebuffer_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLFramebuffer_tp_dealloc(MGLFramebuffer * self) {

	#ifdef MGL_VERBOSE
	printf("MGLFramebuffer_tp_dealloc %p\n", self);
	#endif

	MGLFramebuffer_Type.tp_free((PyObject *)self);
}

int MGLFramebuffer_tp_init(MGLFramebuffer * self, PyObject * args, PyObject * kwargs) {
	MGLError_Set("cannot create mgl.Framebuffer manually");
	return -1;
}

PyObject * MGLFramebuffer_release(MGLFramebuffer * self) {
	MGLFramebuffer_Invalidate(self);
	Py_RETURN_NONE;
}

PyObject * MGLFramebuffer_clear(MGLFramebuffer * self, PyObject * args) {
	float r, g, b, a;
	PyObject * viewport;

	int args_ok = PyArg_ParseTuple(
		args,
		"ffffO",
		&r,
		&g,
		&b,
		&a,
		&viewport
	);

	if (!args_ok) {
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

	const GLMethods & gl = self->context->gl;

	gl.BindFramebuffer(GL_FRAMEBUFFER, self->framebuffer_obj);

	gl.ClearColor(r, g, b, a);

	if (viewport != Py_None) {
		gl.Enable(GL_SCISSOR_TEST);
		gl.Scissor(x, y, width, height);
		gl.Clear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
		gl.Disable(GL_SCISSOR_TEST);
	} else {
		gl.Clear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
	}

	Py_RETURN_NONE;
}

PyObject * MGLFramebuffer_use(MGLFramebuffer * self) {
	self->context->gl.BindFramebuffer(GL_FRAMEBUFFER, self->framebuffer_obj);
	Py_RETURN_NONE;
}

PyObject * MGLFramebuffer_read(MGLFramebuffer * self, PyObject * args) {
	PyObject * viewport;
	int components;
	int alignment;
	int floats;

	int args_ok = PyArg_ParseTuple(
		args,
		"OIIp",
		&viewport,
		&components,
		&alignment,
		&floats
	);

	if (!args_ok) {
		return 0;
	}

	if (alignment != 1 && alignment != 2 && alignment != 4 && alignment != 8) {
		MGLError_Set("the alignment must be 1, 2, 4 or 8");
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

	int expected_size = width * components * (floats ?  4 : 1);
	expected_size = (expected_size + alignment - 1) / alignment * alignment;
	expected_size = expected_size * height;

	int type = floats ? GL_FLOAT : GL_UNSIGNED_BYTE;

	const int formats[] = {0, GL_RED, GL_RG, GL_RGB, GL_RGBA};
	int format = formats[components];

	PyObject * result = PyBytes_FromStringAndSize(0, expected_size);
	char * data = PyBytes_AS_STRING(result);

	const GLMethods & gl = self->context->gl;

	gl.BindFramebuffer(GL_FRAMEBUFFER, self->framebuffer_obj);

	gl.PixelStorei(GL_UNPACK_ALIGNMENT, alignment);
	gl.ReadPixels(x, y, width, height, format, type, data);

	return result;
}

PyMethodDef MGLFramebuffer_tp_methods[] = {
	{"clear", (PyCFunction)MGLFramebuffer_clear, METH_NOARGS, 0},
	{"use", (PyCFunction)MGLFramebuffer_use, METH_NOARGS, 0},
	{"read", (PyCFunction)MGLFramebuffer_read, METH_VARARGS, 0},
	{"release", (PyCFunction)MGLFramebuffer_release, METH_NOARGS, 0},
	{0},
};

PyObject * MGLFramebuffer_get_width(MGLFramebuffer * self, void * closure) {
	return PyLong_FromLong(self->width);
}

PyObject * MGLFramebuffer_get_height(MGLFramebuffer * self, void * closure) {
	return PyLong_FromLong(self->height);
}

PyObject * MGLFramebuffer_get_samples(MGLFramebuffer * self, void * closure) {
	return PyLong_FromLong(self->samples);
}

PyObject * MGLFramebuffer_get_color_attachments(MGLFramebuffer * self, void * closure) {
	Py_INCREF(self->color_attachments);
	return self->color_attachments;
}

PyObject * MGLFramebuffer_get_depth_attachment(MGLFramebuffer * self, void * closure) {
	Py_INCREF(self->depth_attachment);
	return self->depth_attachment;
}

MGLContext * MGLFramebuffer_get_context(MGLFramebuffer * self, void * closure) {
	Py_INCREF(self->context);
	return self->context;
}

PyObject * MGLFramebuffer_get_glo(MGLFramebuffer * self, void * closure) {
	return PyLong_FromLong(self->framebuffer_obj);
}

PyGetSetDef MGLFramebuffer_tp_getseters[] = {
	{(char *)"width", (getter)MGLFramebuffer_get_width, 0, 0, 0},
	{(char *)"height", (getter)MGLFramebuffer_get_height, 0, 0, 0},
	{(char *)"samples", (getter)MGLFramebuffer_get_samples, 0, 0, 0},
	{(char *)"color_attachments", (getter)MGLFramebuffer_get_color_attachments, 0, 0, 0},
	{(char *)"depth_attachment", (getter)MGLFramebuffer_get_depth_attachment, 0, 0, 0},
	{(char *)"context", (getter)MGLFramebuffer_get_context, 0, 0, 0},
	{(char *)"glo", (getter)MGLFramebuffer_get_glo, 0, 0, 0},
	{0},
};

PyTypeObject MGLFramebuffer_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"mgl.Framebuffer",                                      // tp_name
	sizeof(MGLFramebuffer),                                 // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLFramebuffer_tp_dealloc,                  // tp_dealloc
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
	MGLFramebuffer_tp_methods,                              // tp_methods
	0,                                                      // tp_members
	MGLFramebuffer_tp_getseters,                            // tp_getset
	0,                                                      // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLFramebuffer_tp_init,                       // tp_init
	0,                                                      // tp_alloc
	MGLFramebuffer_tp_new,                                  // tp_new
};

MGLFramebuffer * MGLFramebuffer_New() {
	MGLFramebuffer * self = (MGLFramebuffer *)MGLFramebuffer_tp_new(&MGLFramebuffer_Type, 0, 0);
	return self;
}

void MGLFramebuffer_Invalidate(MGLFramebuffer * framebuffer) {
	if (Py_TYPE(framebuffer) == &MGLInvalidObject_Type) {

		#ifdef MGL_VERBOSE
		printf("MGLFramebuffer_Invalidate %p already released\n", framebuffer);
		#endif

		return;
	}

	#ifdef MGL_VERBOSE
	printf("MGLFramebuffer_Invalidate %p\n", framebuffer);
	#endif

	if (framebuffer->framebuffer_obj) {
		framebuffer->context->gl.DeleteFramebuffers(1, (GLuint *)&framebuffer->framebuffer_obj);

		if (framebuffer->color_attachments) {
			int color_attachments_len = (int)PyTuple_GET_SIZE(framebuffer->color_attachments);

			for (int i = 0; i < color_attachments_len; ++i) {
				PyObject * attachment = PyTuple_GET_ITEM(framebuffer->color_attachments, i);

				if (Py_TYPE(attachment) == &MGLTexture_Type) {
					MGLTexture * texture = (MGLTexture *)attachment;
					if (Py_REFCNT(texture) == 2) {
						MGLTexture_Invalidate(texture);
					}
				} else if (Py_TYPE(attachment) == &MGLRenderbuffer_Type) {
					MGLRenderbuffer * renderbuffer = (MGLRenderbuffer *)attachment;
					if (Py_REFCNT(renderbuffer) == 2) {
						MGLRenderbuffer_Invalidate(renderbuffer);
					}
				}
			}

			Py_DECREF(framebuffer->color_attachments);
		}

		if (framebuffer->depth_attachment) {
			if (Py_TYPE(framebuffer->depth_attachment) == &MGLTexture_Type) {
				MGLTexture * texture = (MGLTexture *)framebuffer->depth_attachment;
				if (Py_REFCNT(texture) == 2) {
					MGLTexture_Invalidate(texture);
				}
			} else if (Py_TYPE(framebuffer->depth_attachment) == &MGLRenderbuffer_Type) {
				MGLRenderbuffer * renderbuffer = (MGLRenderbuffer *)framebuffer->depth_attachment;
				if (Py_REFCNT(renderbuffer) == 2) {
					MGLRenderbuffer_Invalidate(renderbuffer);
				}
			}

			Py_DECREF(framebuffer->depth_attachment);
		}

		Py_DECREF(framebuffer->context);
	}

	Py_TYPE(framebuffer) = &MGLInvalidObject_Type;

	Py_DECREF(framebuffer);
}
