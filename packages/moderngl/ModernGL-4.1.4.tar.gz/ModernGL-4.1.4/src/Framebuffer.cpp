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
	gl.DrawBuffers(self->draw_buffers_len, self->draw_buffers);
	gl.ClearColor(r, g, b, a);

	for (int i = 0; i < self->draw_buffers_len; ++i) {
		gl.ColorMaski(
			i,
			self->color_mask[i * 4 + 0],
			self->color_mask[i * 4 + 1],
			self->color_mask[i * 4 + 2],
			self->color_mask[i * 4 + 3]
		);
	}

	gl.DepthMask(self->depth_mask);

	if (viewport != Py_None) {
		gl.Enable(GL_SCISSOR_TEST);
		gl.Scissor(x, y, width, height);
		gl.Clear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
		gl.Disable(GL_SCISSOR_TEST);
	} else {
		gl.Clear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
	}

	gl.BindFramebuffer(GL_FRAMEBUFFER, self->context->bound_framebuffer->framebuffer_obj);

	Py_RETURN_NONE;
}

PyObject * MGLFramebuffer_use(MGLFramebuffer * self) {
	const GLMethods & gl = self->context->gl;

	gl.BindFramebuffer(GL_FRAMEBUFFER, self->framebuffer_obj);
	gl.DrawBuffers(self->draw_buffers_len, self->draw_buffers);

	if (self->framebuffer_obj) {
		gl.Viewport(
			self->viewport_x,
			self->viewport_y,
			self->viewport_width,
			self->viewport_height
		);
	}

	for (int i = 0; i < self->draw_buffers_len; ++i) {
		gl.ColorMaski(
			i,
			self->color_mask[i * 4 + 0],
			self->color_mask[i * 4 + 1],
			self->color_mask[i * 4 + 2],
			self->color_mask[i * 4 + 3]
		);
	}

	gl.DepthMask(self->depth_mask);

	Py_INCREF(self);
	Py_INCREF(self->context->bound_framebuffer);
	self->context->bound_framebuffer = self;

	Py_RETURN_NONE;
}

PyObject * MGLFramebuffer_read(MGLFramebuffer * self, PyObject * args) {
	PyObject * viewport;
	int components;
	int alignment;
	int attachment;
	int floats;

	int args_ok = PyArg_ParseTuple(
		args,
		"OIIIp",
		&viewport,
		&components,
		&attachment,
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
	gl.ReadBuffer(GL_COLOR_ATTACHMENT0 + attachment);
	gl.PixelStorei(GL_UNPACK_ALIGNMENT, alignment);
	gl.ReadPixels(x, y, width, height, format, type, data);
	gl.BindFramebuffer(GL_FRAMEBUFFER, self->context->bound_framebuffer->framebuffer_obj);

	return result;
}

PyObject * MGLFramebuffer_read_into(MGLFramebuffer * self, PyObject * args) {
	PyObject * data;
	PyObject * viewport;
	int components;
	int attachment;
	int alignment;
	int floats;

	int args_ok = PyArg_ParseTuple(
		args,
		"OOIIIp",
		&data,
		&viewport,
		&components,
		&attachment,
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

	const GLMethods & gl = self->context->gl;

	gl.BindFramebuffer(GL_FRAMEBUFFER, self->framebuffer_obj);
	gl.ReadBuffer(GL_COLOR_ATTACHMENT0 + attachment);
	gl.PixelStorei(GL_UNPACK_ALIGNMENT, alignment);
	gl.ReadPixels(x, y, width, height, format, type, buffer_view.buf);
	gl.BindFramebuffer(GL_FRAMEBUFFER, self->context->bound_framebuffer->framebuffer_obj);

	PyBuffer_Release(&buffer_view);

	return PyLong_FromLong(expected_size);
}

PyMethodDef MGLFramebuffer_tp_methods[] = {
	{"clear", (PyCFunction)MGLFramebuffer_clear, METH_VARARGS, 0},
	{"use", (PyCFunction)MGLFramebuffer_use, METH_NOARGS, 0},
	{"read", (PyCFunction)MGLFramebuffer_read, METH_VARARGS, 0},
	{"read_into", (PyCFunction)MGLFramebuffer_read_into, METH_VARARGS, 0},
	{"release", (PyCFunction)MGLFramebuffer_release, METH_NOARGS, 0},
	{0},
};

PyObject * MGLFramebuffer_get_viewport(MGLFramebuffer * self, void * closure) {
	PyObject * x = PyLong_FromLong(self->viewport_x);
	PyObject * y = PyLong_FromLong(self->viewport_y);
	PyObject * width = PyLong_FromLong(self->viewport_width);
	PyObject * height = PyLong_FromLong(self->viewport_height);
	return PyTuple_Pack(4, x, y, width, height);
}

int MGLFramebuffer_set_viewport(MGLFramebuffer * self, PyObject * value, void * closure) {
	if (PyTuple_GET_SIZE(value) != 4) {
		MGLError_Set("the viewport must be a 4-tuple not %d-tuple", PyTuple_GET_SIZE(value));
		return -1;
	}

	int viewport_x = PyLong_AsLong(PyTuple_GET_ITEM(value, 0));
	int viewport_y = PyLong_AsLong(PyTuple_GET_ITEM(value, 1));
	int viewport_width = PyLong_AsLong(PyTuple_GET_ITEM(value, 2));
	int viewport_height = PyLong_AsLong(PyTuple_GET_ITEM(value, 3));

	if (PyErr_Occurred()) {
		MGLError_Set("the viewport is invalid");
		return -1;
	}

	self->viewport_x = viewport_x;
	self->viewport_y = viewport_y;
	self->viewport_width = viewport_width;
	self->viewport_height = viewport_height;

	return 0;
}

PyObject * MGLFramebuffer_get_color_mask(MGLFramebuffer * self, void * closure) {
	if (self->draw_buffers_len == 1) {
		PyObject * color_mask = PyTuple_New(4);
		PyTuple_SET_ITEM(color_mask, 0, PyBool_FromLong(self->color_mask[0]));
		PyTuple_SET_ITEM(color_mask, 1, PyBool_FromLong(self->color_mask[1]));
		PyTuple_SET_ITEM(color_mask, 2, PyBool_FromLong(self->color_mask[2]));
		PyTuple_SET_ITEM(color_mask, 3, PyBool_FromLong(self->color_mask[3]));
		return color_mask;
	}

	PyObject * res = PyTuple_New(self->draw_buffers_len);

	for (int i = 0; i < self->draw_buffers_len; ++i) {
		PyObject * color_mask = PyTuple_New(4);
		PyTuple_SET_ITEM(color_mask, 0, PyBool_FromLong(self->color_mask[i * 4 + 0]));
		PyTuple_SET_ITEM(color_mask, 1, PyBool_FromLong(self->color_mask[i * 4 + 1]));
		PyTuple_SET_ITEM(color_mask, 2, PyBool_FromLong(self->color_mask[i * 4 + 2]));
		PyTuple_SET_ITEM(color_mask, 3, PyBool_FromLong(self->color_mask[i * 4 + 3]));
		PyTuple_SET_ITEM(res, i, color_mask);
	}

	return res;
}

int MGLFramebuffer_set_color_mask(MGLFramebuffer * self, PyObject * value, void * closure) {
	if (self->draw_buffers_len == 1) {
		if (Py_TYPE(value) != &PyTuple_Type || PyTuple_GET_SIZE(value) != 4) {
			MGLError_Set("the color_mask must be a 4-tuple not %s", Py_TYPE(value)->tp_name);
			return -1;
		}

		PyObject * r = PyTuple_GET_ITEM(value, 0);
		PyObject * g = PyTuple_GET_ITEM(value, 1);
		PyObject * b = PyTuple_GET_ITEM(value, 2);
		PyObject * a = PyTuple_GET_ITEM(value, 3);

		if (r == Py_True) {
			self->color_mask[0] = true;
		} else if (r == Py_False) {
			self->color_mask[0] = false;
		} else {
			MGLError_Set("the color_mask[0] must be a bool not %s", Py_TYPE(r)->tp_name);
			return -1;
		}

		if (g == Py_True) {
			self->color_mask[1] = true;
		} else if (g == Py_False) {
			self->color_mask[1] = false;
		} else {
			MGLError_Set("the color_mask[1] must be a bool not %s", Py_TYPE(g)->tp_name);
			return -1;
		}

		if (b == Py_True) {
			self->color_mask[2] = true;
		} else if (b == Py_False) {
			self->color_mask[2] = false;
		} else {
			MGLError_Set("the color_mask[2] must be a bool not %s", Py_TYPE(b)->tp_name);
			return -1;
		}

		if (a == Py_True) {
			self->color_mask[3] = true;
		} else if (a == Py_False) {
			self->color_mask[3] = false;
		} else {
			MGLError_Set("the color_mask[3] must be a bool not %s", Py_TYPE(a)->tp_name);
			return -1;
		}
	} else {
		for (int i = 0; i < self->draw_buffers_len; ++i) {
			PyObject * color_mask = PyTuple_GET_ITEM(value, i);

			if (Py_TYPE(color_mask) != &PyTuple_Type || PyTuple_GET_SIZE(color_mask) != 4) {
				MGLError_Set("the color_mask must be a 4-tuple not %s", Py_TYPE(color_mask)->tp_name);
				return -1;
			}

			PyObject * r = PyTuple_GET_ITEM(color_mask, 0);
			PyObject * g = PyTuple_GET_ITEM(color_mask, 1);
			PyObject * b = PyTuple_GET_ITEM(color_mask, 2);
			PyObject * a = PyTuple_GET_ITEM(color_mask, 3);

			if (r == Py_True) {
				self->color_mask[i * 4 + 0] = true;
			} else if (r == Py_False) {
				self->color_mask[i * 4 + 0] = false;
			} else {
				MGLError_Set("the color_mask[%d][0] must be a bool not %s", i, Py_TYPE(r)->tp_name);
				return -1;
			}

			if (g == Py_True) {
				self->color_mask[i * 4 + 1] = true;
			} else if (g == Py_False) {
				self->color_mask[i * 4 + 1] = false;
			} else {
				MGLError_Set("the color_mask[%d][1] must be a bool not %s", i, Py_TYPE(g)->tp_name);
				return -1;
			}

			if (b == Py_True) {
				self->color_mask[i * 4 + 2] = true;
			} else if (b == Py_False) {
				self->color_mask[i * 4 + 2] = false;
			} else {
				MGLError_Set("the color_mask[%d][2] must be a bool not %s", i, Py_TYPE(b)->tp_name);
				return -1;
			}

			if (a == Py_True) {
				self->color_mask[i * 4 + 3] = true;
			} else if (a == Py_False) {
				self->color_mask[i * 4 + 3] = false;
			} else {
				MGLError_Set("the color_mask[%d][3] must be a bool not %s", i, Py_TYPE(a)->tp_name);
				return -1;
			}
		}
	}

	return 0;
}

PyObject * MGLFramebuffer_get_depth_mask(MGLFramebuffer * self, void * closure) {
	return PyBool_FromLong(self->depth_mask);
}

int MGLFramebuffer_set_depth_mask(MGLFramebuffer * self, PyObject * value, void * closure) {
	if (value == Py_True) {
		self->depth_mask = true;
	} else if (value == Py_False) {
		self->depth_mask = false;
	} else {
		MGLError_Set("the depth_mask must be a bool not %s", Py_TYPE(value)->tp_name);
		return -1;
	}

	return 0;
}

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
	if (!self->color_attachments) {
		MGLError_Set("missing color_attachments");
		return 0;
	}
	Py_INCREF(self->color_attachments);
	return self->color_attachments;
}

PyObject * MGLFramebuffer_get_depth_attachment(MGLFramebuffer * self, void * closure) {
	if (!self->depth_attachment) {
		MGLError_Set("missing depth_attachment");
		return 0;
	}
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
	{(char *)"viewport", (getter)MGLFramebuffer_get_viewport, (setter)MGLFramebuffer_set_viewport, 0, 0},
	{(char *)"color_mask", (getter)MGLFramebuffer_get_color_mask, (setter)MGLFramebuffer_set_color_mask, 0, 0},
	{(char *)"depth_mask", (getter)MGLFramebuffer_get_depth_mask, (setter)MGLFramebuffer_set_depth_mask, 0, 0},

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
