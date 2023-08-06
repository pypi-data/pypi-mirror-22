#include "Context.hpp"

#include "Error.hpp"
#include "Buffer.hpp"
#include "ComputeShader.hpp"
#include "Texture.hpp"
#include "VertexArray.hpp"
#include "Program.hpp"
#include "Shader.hpp"
#include "Framebuffer.hpp"
#include "FramebufferAttachment.hpp"
#include "Renderbuffer.hpp"
#include "EnableFlag.hpp"
#include "InvalidObject.hpp"
#include "Attribute.hpp"
#include "Uniform.hpp"

#include "BufferFormat.hpp"

PyObject * MGLContext_tp_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
	MGLContext * self = (MGLContext *)type->tp_alloc(type, 0);

	#ifdef MGL_VERBOSE
	printf("MGLContext_tp_new %p\n", self);
	#endif

	if (self) {
	}

	return (PyObject *)self;
}

void MGLContext_tp_dealloc(MGLContext * self) {

	#ifdef MGL_VERBOSE
	printf("MGLContext_tp_dealloc %p\n", self);
	#endif

	MGLContext_Type.tp_free((PyObject *)self);
}

int MGLContext_tp_init(MGLContext * self, PyObject * args, PyObject * kwargs) {
	MGLError * error = MGLError_FromFormat(TRACE, "Cannot create Context manually");
	PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
	return -1;
}

PyObject * MGLContext_tp_str(MGLContext * self) {
	return PyUnicode_FromFormat("<mgl.Context");
}

PyObject * MGLContext_clear(MGLContext * self, PyObject * args) {
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
	int width = 0;
	int height = 0;

	if (viewport != Py_None) {
		if (Py_TYPE(viewport) != &PyTuple_Type) {
			MGLError * error = MGLError_FromFormat(TRACE, "the viewport must be a tuple not %s", Py_TYPE(viewport)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
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

			MGLError * error = MGLError_FromFormat(TRACE, "the viewport size %d is invalid", PyTuple_GET_SIZE(viewport));
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;

		}

		if (PyErr_Occurred()) {
			MGLError * error = MGLError_FromFormat(TRACE, "wrong values in the viewport");
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

	}

	const GLMethods & gl = self->gl;

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

PyObject * MGLContext_enable(MGLContext * self, PyObject * args) {
	MGLEnableFlag * flags;

	int args_ok = PyArg_ParseTuple(
		args,
		"O!",
		&MGLEnableFlag_Type,
		&flags
	);

	if (!args_ok) {
		return 0;
	}

	self->gl.Enable(flags->flag);

	Py_RETURN_NONE;
}

PyObject * MGLContext_disable(MGLContext * self, PyObject * args) {
	MGLEnableFlag * flags;

	int args_ok = PyArg_ParseTuple(
		args,
		"O!",
		&MGLEnableFlag_Type,
		&flags
	);

	if (!args_ok) {
		return 0;
	}

	self->gl.Disable(flags->flag);

	Py_RETURN_NONE;
}

PyObject * MGLContext_finish(MGLContext * self) {
	self->gl.Finish();
	Py_RETURN_NONE;
}

PyObject * MGLContext_copy_buffer(MGLContext * self, PyObject * args) {
	MGLBuffer * dst;
	MGLBuffer * src;

	int size;
	int read_offset;
	int write_offset;

	int args_ok = PyArg_ParseTuple(
		args,
		"O!O!III",
		&MGLBuffer_Type,
		&dst,
		&MGLBuffer_Type,
		&src,
		&size,
		&read_offset,
		&write_offset
	);

	if (!args_ok) {
		return 0;
	}

	if (size < 0) {
		size = src->size - read_offset;
	}

	if (read_offset < 0 || write_offset < 0) {
		MGLError * error = MGLError_FromFormat(TRACE, "buffer underflow");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	if (read_offset + size > src->size || write_offset + size > dst->size) {
		MGLError * error = MGLError_FromFormat(TRACE, "buffer overflow");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	const GLMethods & gl = self->gl;

	gl.BindBuffer(GL_COPY_READ_BUFFER, src->buffer_obj);
	gl.BindBuffer(GL_COPY_WRITE_BUFFER, dst->buffer_obj);
	gl.CopyBufferSubData(GL_COPY_READ_BUFFER, GL_COPY_WRITE_BUFFER, read_offset, write_offset, size);

	Py_RETURN_NONE;
}

PyObject * MGLContext_copy_framebuffer(MGLContext * self, PyObject * args) {
	PyObject * dst;
	MGLFramebuffer * src;

	int args_ok = PyArg_ParseTuple(
		args,
		"OO!",
		&dst,
		&MGLFramebuffer_Type,
		&src
	);

	if (!args_ok) {
		return 0;
	}

	const GLMethods & gl = self->gl;

	// If the sizes of the source and destination rectangles are not equal,
	// filter specifies the interpolation method that will be applied to resize the source image,
	// and must be GL_NEAREST or GL_LINEAR. GL_LINEAR is only a valid interpolation
	// method for the color buffer. If filter is not GL_NEAREST and mask includes
	// GL_DEPTH_BUFFER_BIT or GL_STENCIL_BUFFER_BIT, no data is transferred and a
	// GL_INVALID_OPERATION error is generated.

	if (Py_TYPE(dst) == &MGLFramebuffer_Type) {

		MGLFramebuffer * dst_framebuffer = (MGLFramebuffer *)dst;

		int width = src->width < dst_framebuffer->width ? src->width : dst_framebuffer->width;
		int height = src->height < dst_framebuffer->height ? src->height : dst_framebuffer->height;

		gl.BindFramebuffer(GL_READ_FRAMEBUFFER, src->framebuffer_obj);
		gl.BindFramebuffer(GL_DRAW_FRAMEBUFFER, dst_framebuffer->framebuffer_obj);
		gl.BlitFramebuffer(
			0, 0, width, height,
			0, 0, width, height,
			GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT,
			GL_NEAREST
		);

	} else if (Py_TYPE(dst) == &MGLFramebuffer_Type) {

		MGLTexture * dst_texture = (MGLTexture *)dst;

		int width = src->width < dst_texture->width ? src->width : dst_texture->width;
		int height = src->height < dst_texture->height ? src->height : dst_texture->height;

		gl.BindFramebuffer(GL_READ_FRAMEBUFFER, src->framebuffer_obj);

		const int formats[] = {0, GL_RED, GL_RG, GL_RGB, GL_RGBA};
		int texture_target = dst_texture->samples ? GL_TEXTURE_2D_MULTISAMPLE : GL_TEXTURE_2D;
		int format = formats[dst_texture->components];

		gl.CopyTexImage2D(texture_target, 0, format, 0, 0, width, height, 0);

	} else {

		MGLError * error = MGLError_FromFormat(TRACE, "dst must be a framebuffer or a texture");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;

	}

	Py_RETURN_NONE;
}

MGLBuffer * MGLContext_buffer(MGLContext * self, PyObject * args) {
	PyObject * data;
	int reserve;
	int dynamic;

	int args_ok = PyArg_ParseTuple(
		args,
		"OIp",
		&data,
		&reserve,
		&dynamic
	);

	if (!args_ok) {
		return 0;
	}

	if ((data != Py_None && reserve) || (data == Py_None && !reserve)) {
		MGLError * error = MGLError_FromFormat(TRACE, "data and reserve are mutually exclusive");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	Py_buffer buffer_view;

	if (data != Py_None) {
		int get_buffer = PyObject_GetBuffer(data, &buffer_view, PyBUF_SIMPLE);
		if (get_buffer < 0) {
			MGLError * error = MGLError_FromFormat(TRACE, "data (%s) does not support buffer interface", Py_TYPE(data)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}
	} else {
		buffer_view.len = reserve;
		buffer_view.buf = 0;
	}

	if (!buffer_view.len) {
		MGLError * error = MGLError_FromFormat(TRACE, "buffer cannot be empty");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		if (data != Py_None) {
			PyBuffer_Release(&buffer_view);
		}
		return 0;
	}

	MGLBuffer * buffer = MGLBuffer_New();

	buffer->size = (int)buffer_view.len;
	buffer->dynamic = dynamic ? true : false;

	const GLMethods & gl = self->gl;

	buffer->buffer_obj = 0;
	gl.GenBuffers(1, (GLuint *)&buffer->buffer_obj);

	if (!buffer->buffer_obj) {
		MGLError * error = MGLError_FromFormat(TRACE, "Cannot create buffer object.");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	gl.BindBuffer(GL_ARRAY_BUFFER, buffer->buffer_obj);
	gl.BufferData(GL_ARRAY_BUFFER, buffer->size, buffer_view.buf, dynamic ? GL_DYNAMIC_DRAW : GL_STATIC_DRAW);

	Py_INCREF(self);
	buffer->context = self;

	if (data != Py_None) {
		PyBuffer_Release(&buffer_view);
	}

	Py_INCREF(buffer);
	return buffer;
}

MGLTexture * MGLContext_texture(MGLContext * self, PyObject * args) {
	int width;
	int height;

	int components;

	PyObject * data;

	int samples;
	int floats;

	int args_ok = PyArg_ParseTuple(
		args,
		"(II)IOIp",
		&width,
		&height,
		&components,
		&data,
		&samples,
		&floats
	);

	if (!args_ok) {
		return 0;
	}

	if (components < 1 || components > 4) {
		MGLError * error = MGLError_FromFormat(TRACE, "components must be 1, 2, 3 or 4");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	if (data != Py_None && samples) {
		MGLError * error = MGLError_FromFormat(TRACE, "cannot write data for a multisample texture");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	int expected_size = floats ? (width * height * components * 4) : (height * ((width * components + 3) & ~3));

	Py_buffer buffer_view;

	if (data != Py_None) {
		PyObject_GetBuffer(data, &buffer_view, PyBUF_SIMPLE);
	} else {
		buffer_view.len = expected_size;
		buffer_view.buf = 0;
	}

	if (buffer_view.len != expected_size) {
		MGLError * error = MGLError_FromFormat(TRACE, "data size mismatch %d != %d", buffer_view.len, expected_size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		if (data != Py_None) {
			PyBuffer_Release(&buffer_view);
		}
		return 0;
	}

	const int formats[] = {0, GL_RED, GL_RG, GL_RGB, GL_RGBA};

	int texture_target = samples ? GL_TEXTURE_2D_MULTISAMPLE : GL_TEXTURE_2D;
	int pixel_type = floats ? GL_FLOAT : GL_UNSIGNED_BYTE;
	int format = formats[components];

	const GLMethods & gl = self->gl;

	gl.ActiveTexture(GL_TEXTURE0 + self->default_texture_unit);

	MGLTexture * texture = MGLTexture_New();

	texture->texture_obj = 0;
	gl.GenTextures(1, (GLuint *)&texture->texture_obj);
	gl.BindTexture(texture_target, texture->texture_obj);
	gl.TexParameteri(texture_target, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	gl.TexParameteri(texture_target, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	if (samples) {
		gl.TexImage2DMultisample(texture_target, samples, format, width, height, true);
	} else {
		gl.TexImage2D(texture_target, 0, format, width, height, 0, format, pixel_type, buffer_view.buf);
	}

	if (data != Py_None) {
		PyBuffer_Release(&buffer_view);
	}

	texture->width = width;
	texture->height = height;
	texture->components = components;
	texture->samples = samples;
	texture->floats = floats ? true : false;
	texture->depth = false;

	Py_INCREF(self);
	texture->context = self;

	Py_INCREF(texture);
	return texture;
}

MGLTexture * MGLContext_depth_texture(MGLContext * self, PyObject * args) {
	int width;
	int height;

	PyObject * data;

	int samples;

	int args_ok = PyArg_ParseTuple(
		args,
		"(II)OI",
		&width,
		&height,
		&data,
		&samples
	);

	if (!args_ok) {
		return 0;
	}

	if (data != Py_None && samples) {
		MGLError * error = MGLError_FromFormat(TRACE, "cannot write data for a multisample texture");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	int expected_size = width * height * 4;

	Py_buffer buffer_view;

	if (data != Py_None) {
		PyObject_GetBuffer(data, &buffer_view, PyBUF_SIMPLE);
	} else {
		buffer_view.len = expected_size;
		buffer_view.buf = 0;
	}

	if (buffer_view.len != expected_size) {
		MGLError * error = MGLError_FromFormat(TRACE, "data size mismatch %d != %d", buffer_view.len, expected_size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		if (data != Py_None) {
			PyBuffer_Release(&buffer_view);
		}
		return 0;
	}

	int texture_target = samples ? GL_TEXTURE_2D_MULTISAMPLE : GL_TEXTURE_2D;
	int pixel_type = GL_FLOAT;

	const GLMethods & gl = self->gl;

	gl.ActiveTexture(GL_TEXTURE0 + self->default_texture_unit);

	MGLTexture * texture = MGLTexture_New();

	texture->texture_obj = 0;
	gl.GenTextures(1, (GLuint *)&texture->texture_obj);
	gl.BindTexture(texture_target, texture->texture_obj);
	gl.TexParameteri(texture_target, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	gl.TexParameteri(texture_target, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	gl.TexImage2D(texture_target, 0, GL_DEPTH_COMPONENT24, width, height, 0, GL_DEPTH_COMPONENT, pixel_type, buffer_view.buf);

	if (data != Py_None) {
		PyBuffer_Release(&buffer_view);
	}

	texture->width = width;
	texture->height = height;
	texture->components = 1;
	texture->samples = samples;
	texture->floats = true;
	texture->depth = true;

	Py_INCREF(self);
	texture->context = self;

	Py_INCREF(texture);
	return texture;
}

MGLVertexArray * MGLContext_vertex_array(MGLContext * self, PyObject * args) {
	MGLProgram * program;
	PyObject * content;
	MGLBuffer * index_buffer;

	int args_ok = PyArg_ParseTuple(
		args,
		"O!OO",
		&MGLProgram_Type,
		&program,
		&content,
		&index_buffer
	);

	if (!args_ok) {
		return 0;
	}

	if (program->context != self) {
		MGLError * error = MGLError_FromFormat(TRACE, "program belongs to a different context");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	if (index_buffer != (MGLBuffer *)Py_None && index_buffer->context != self) {
		MGLError * error = MGLError_FromFormat(TRACE, "index_buffer belongs to a different context");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	int content_len = (int)PyTuple_GET_SIZE(content);

	if (!content_len) {
		MGLError * error = MGLError_FromFormat(TRACE, "content must not be emtpy");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	for (int i = 0; i < content_len; ++i) {
		PyObject * tuple = PyTuple_GET_ITEM(content, i);

		if (Py_TYPE(tuple) != &PyTuple_Type) {
			MGLError * error = MGLError_FromFormat(TRACE, "content[%d] must be a tuple not %s", i, Py_TYPE(tuple)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		int size = (int)PyTuple_GET_SIZE(tuple);

		if (size != 3) {
			MGLError * error = MGLError_FromFormat(TRACE, "content[%d] must be a tuple of size 3 not %d", i, size);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		PyObject * buffer = PyTuple_GET_ITEM(tuple, 0);
		PyObject * format = PyTuple_GET_ITEM(tuple, 1);
		PyObject * attributes = PyTuple_GET_ITEM(tuple, 2);

		if (Py_TYPE(buffer) != &MGLBuffer_Type) {
			MGLError * error = MGLError_FromFormat(TRACE, "content[%d][0] must be a mgl.Buffer not %s", i, Py_TYPE(buffer)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		if (Py_TYPE(format) != &PyUnicode_Type) {
			MGLError * error = MGLError_FromFormat(TRACE, "content[%d][1] must be a str not %s", i, Py_TYPE(format)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		if (Py_TYPE(attributes) != &PyTuple_Type) {
			MGLError * error = MGLError_FromFormat(TRACE, "content[%d][2] must be a list not %s", i, Py_TYPE(attributes)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		if (((MGLBuffer *)buffer)->context != self) {
			MGLError * error = MGLError_FromFormat(TRACE, "content[%d][0] belongs to a different context", i);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		FormatIterator it = FormatIterator(PyUnicode_AsUTF8(format));
		FormatInfo format_info = it.info();

		if (!format_info.valid) {
			MGLError * error = MGLError_FromFormat(TRACE, "content[%d][1] is an invalid format", i);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		if (i == 0 && format_info.per_instance) {
			MGLError * error = MGLError_FromFormat(TRACE, "the first vertex attribute must not be a per instance attribute");
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		int attributes_len = (int)PyTuple_GET_SIZE(attributes);

		if (!attributes_len) {
			MGLError * error = MGLError_FromFormat(TRACE, "content[%d][2] must not be empty", i);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		if (attributes_len != format_info.nodes) {
			MGLError * error = MGLError_FromFormat(TRACE, "content[%d][1] and content[%d][2] size mismatch %d != %d", i, i, format_info.nodes, attributes_len);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		for (int j = 0; j < attributes_len; ++j) {
			PyObject * attribute = PyTuple_GET_ITEM(attributes, j);

			if (Py_TYPE(attribute) != &PyUnicode_Type) {
				MGLError * error = MGLError_FromFormat(TRACE, "content[%d][2][%d] must be a str not %s", i, j, Py_TYPE(attribute)->tp_name);
				PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
				return 0;
			}

			{
				const char * name = PyUnicode_AsUTF8(attribute);

				FormatNode * node = it.next();

				while (node->shape == 'x') {
					node = it.next();
				}

				MGLAttribute * attribute = (MGLAttribute *)PyDict_GetItemString(program->attributes, name);

				if (!attribute) {
					MGLError * error = MGLError_FromFormat(TRACE, "%s is not a valid attribute", name);
					PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
					return 0;
				}

				int scalars = attribute->dimension * attribute->array_length;

				if (scalars != node->count) {
					MGLError * error = MGLError_FromFormat(TRACE, "%s size is %d not %d", name, scalars, node->count);
					PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
					return 0;
				}

				if (attribute->shape != node->shape) {
					MGLError * error = MGLError_FromFormat(TRACE, "%s shape is '%c' not '%c'", name, attribute->shape, node->shape);
					PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
					return 0;
				}
			}
		}
	}

	if (index_buffer != (MGLBuffer *)Py_None && Py_TYPE(index_buffer) != &MGLBuffer_Type) {
		MGLError * error = MGLError_FromFormat(TRACE, "index_buffer must be a mgl.Buffer not %s", Py_TYPE(index_buffer)->tp_name);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	const GLMethods & gl = self->gl;

	MGLVertexArray * array = MGLVertexArray_New();

	Py_INCREF(program);
	array->program = program;

	array->vertex_array_obj = 0;
	gl.GenVertexArrays(1, (GLuint *)&array->vertex_array_obj);
	gl.BindVertexArray(array->vertex_array_obj);

	gl.UseProgram(program->program_obj);

	Py_INCREF(index_buffer);
	array->index_buffer = index_buffer;

	if (index_buffer != (MGLBuffer *)Py_None) {
		array->num_vertices = index_buffer->size / 4;
		gl.BindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer->buffer_obj);
	} else {
		array->num_vertices = -1;
	}

	for (int i = 0; i < content_len; ++i) {
		PyObject * tuple = PyTuple_GET_ITEM(content, i);

		MGLBuffer * buffer = (MGLBuffer *)PyTuple_GET_ITEM(tuple, 0);
		const char * format = PyUnicode_AsUTF8(PyTuple_GET_ITEM(tuple, 1));
		PyObject * attributes = PyTuple_GET_ITEM(tuple, 2);

		FormatIterator it = FormatIterator(format);
		FormatInfo format_info = it.info();

		int buf_vertices = buffer->size / format_info.size;

		if (!format_info.per_instance && array->index_buffer == (MGLBuffer *)Py_None && (!i || array->num_vertices > buf_vertices)) {
			array->num_vertices = buf_vertices;
		}

		gl.BindBuffer(GL_ARRAY_BUFFER, buffer->buffer_obj);

		char * ptr = 0;

		int attributes_len = (int)PyTuple_GET_SIZE(attributes);

		for (int j = 0; j < attributes_len; ++j) {
			FormatNode * node = it.next();

			while (node->shape == 'x') {
				ptr += node->count * node->size;
				node = it.next();
			}

			MGLAttribute * attribute = (MGLAttribute *)PyDict_GetItem(program->attributes, PyTuple_GET_ITEM(attributes, j));

			for (int r = 0; r < attribute->rows_length; ++r) {
				int location = attribute->location + r;

				if (attribute->normalizable) {
					((gl_attribute_normal_ptr_proc)attribute->gl_attrib_ptr_proc)(location, attribute->row_length, attribute->scalar_type, false, format_info.size, ptr);
				} else {
					((gl_attribute_ptr_proc)attribute->gl_attrib_ptr_proc)(location, attribute->row_length, attribute->scalar_type, format_info.size, ptr);
				}

				if (format_info.per_instance) {
					gl.VertexAttribDivisor(location, 1);
				}

				gl.EnableVertexAttribArray(location);

				ptr += attribute->row_size;
			}
		}
	}

	Py_INCREF(self);
	array->context = self;

	MGLVertexArray_Complete(array);

	Py_INCREF(array);
	return array;
}

MGLProgram * MGLContext_program(MGLContext * self, PyObject * args) {
	PyObject * shaders;
	PyObject * varyings;

	int args_ok = PyArg_ParseTuple(
		args,
		"OO",
		&shaders,
		&varyings
	);

	if (!args_ok) {
		return 0;
	}

	int num_varyings = (int)PyTuple_GET_SIZE(varyings);

	for (int i = 0; i < num_varyings; ++i) {
		PyObject * item = PyTuple_GET_ITEM(varyings, i);
		if (Py_TYPE(item) != &PyUnicode_Type) {
			MGLError * error = MGLError_FromFormat(TRACE, "varyings[%d] must be a str not %s", i, Py_TYPE(item)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}
	}

	int counter[NUM_SHADER_SLOTS] = {};

	int num_shaders = (int)PyTuple_GET_SIZE(shaders);

	for (int i = 0; i < num_shaders; ++i) {
		PyObject * item = PyTuple_GET_ITEM(shaders, i);
		if (Py_TYPE(item) != &MGLShader_Type) {
			MGLError * error = MGLError_FromFormat(TRACE, "shaders[%d] must be a mgl.Shader not %s", i, Py_TYPE(item)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		MGLShader * shader = (MGLShader *)item;

		if (shader->context != self) {
			MGLError * error = MGLError_FromFormat(TRACE, "shaders[%d] belongs to a different context", i);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		counter[shader->shader_slot] += 1;

		if (counter[shader->shader_slot] > 1) {
			MGLError * error = MGLError_FromFormat(TRACE, "shaders has duplicate %s", SHADER_NAME[shader->shader_slot]);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}
	}

	MGLProgram * program = MGLProgram_New();

	Py_INCREF(shaders);
	program->shaders = shaders;

	Py_INCREF(self);
	program->context = self;

	MGLProgram_Compile(program, varyings);

	if (PyErr_Occurred()) {
		Py_DECREF(program);
		return 0;
	}

	Py_INCREF(program);
	return program;
}

template <int ShaderSlot>
MGLShader * MGLContext_shader(MGLContext * self, PyObject * args) {
	PyObject * source;

	int args_ok = PyArg_ParseTuple(
		args,
		"O",
		&source
	);

	if (!args_ok) {
		return 0;
	}

	if (!PyUnicode_Check(source)) {
		MGLError * error = MGLError_FromFormat(TRACE, "source must be a str not %s", Py_TYPE(source)->tp_name);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	MGLShader * shader = MGLShader_New();

	shader->shader_slot = ShaderSlot;
	shader->shader_type = SHADER_TYPE[ShaderSlot];

	Py_INCREF(source);
	shader->source = source;

	Py_INCREF(self);
	shader->context = self;

	MGLShader_Compile(shader);

	if (PyErr_Occurred()) {
		Py_DECREF(shader);
		return 0;
	}

	Py_INCREF(shader);
	return shader;
}

MGLFramebuffer * MGLContext_framebuffer(MGLContext * self, PyObject * args) {
	PyObject * color_attachments;
	PyObject * depth_attachment;

	int args_ok = PyArg_ParseTuple(
		args,
		"OO",
		&color_attachments,
		&depth_attachment
	);

	if (!args_ok) {
		return 0;
	}

	// If the attachment sizes are not all identical, rendering will be limited to the
	// largest area that can fit in all of the attachments (an intersection of rectangles
	// having a lower left of (0; 0) and an upper right of (width; height) for each
	// attachment).

	int width = 0;
	int height = 0;
	int samples = 0;

	int color_attachments_len = (int)PyTuple_GET_SIZE(color_attachments);

	if (!color_attachments_len) {
		MGLError * error = MGLError_FromFormat(TRACE, "color_attachments must not be empty");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	for (int i = 0; i < color_attachments_len; ++i) {
		PyObject * item = PyTuple_GET_ITEM(color_attachments, i);

		if (Py_TYPE(item) != &MGLTexture_Type && Py_TYPE(item) != &MGLRenderbuffer_Type) {
			MGLError * error = MGLError_FromFormat(TRACE, "color_attachments[%d] must be a Renderbuffer or Texture not %s", i, Py_TYPE(item)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		MGLFramebufferAttachment * attachment = (MGLFramebufferAttachment *)item;

		if (i == 0) {
			width = attachment->width;
			height = attachment->height;
			samples = attachment->samples;
		} else {
			if (attachment->width != width || attachment->height != height || attachment->samples != samples) {
				MGLError * error = MGLError_FromFormat(TRACE, "color_attachments have different size or samples");
				PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
				return 0;
			}
		}

		if (attachment->context != self) {
			MGLError * error = MGLError_FromFormat(TRACE, "color_attachments[%d] belongs to a different context", i);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}
	}

	const GLMethods & gl = self->gl;

	if (depth_attachment != Py_None) {

		if (Py_TYPE(depth_attachment) != &MGLTexture_Type && Py_TYPE(depth_attachment) != &MGLRenderbuffer_Type) {
			MGLError * error = MGLError_FromFormat(TRACE, "depth_attachment must be a Renderbuffer or Texture not %s", Py_TYPE(depth_attachment)->tp_name);
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

		MGLFramebufferAttachment * attachment = (MGLFramebufferAttachment *)depth_attachment;

		if (attachment->context != self) {
			MGLError * error = MGLError_FromFormat(TRACE, "depth_attachment belongs to a different context");
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return 0;
		}

	} else {

		MGLRenderbuffer * renderbuffer = MGLRenderbuffer_New();

		renderbuffer->renderbuffer_obj = 0;
		gl.GenRenderbuffers(1, (GLuint *)&renderbuffer->renderbuffer_obj);
		gl.BindRenderbuffer(GL_RENDERBUFFER, renderbuffer->renderbuffer_obj);

		if (samples == 0) {
			gl.RenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, width, height);
		} else {
			gl.RenderbufferStorageMultisample(GL_RENDERBUFFER, samples, GL_DEPTH_COMPONENT24, width, height);
		}

		renderbuffer->width = width;
		renderbuffer->height = height;
		renderbuffer->components = 1;
		renderbuffer->samples = samples;
		renderbuffer->floats = true;
		renderbuffer->depth = true;

		Py_INCREF(self);
		renderbuffer->context = self;

		Py_INCREF(renderbuffer);
		depth_attachment = (PyObject *)renderbuffer;

	}

	int draw_framebuffer = 0;
	gl.GetIntegerv(GL_FRAMEBUFFER_BINDING, (GLint *)&draw_framebuffer);

	MGLFramebuffer * framebuffer = MGLFramebuffer_New();

	framebuffer->framebuffer_obj = 0;
	gl.GenFramebuffers(1, (GLuint *)&framebuffer->framebuffer_obj);
	gl.BindFramebuffer(GL_FRAMEBUFFER, framebuffer->framebuffer_obj);

	for (int i = 0; i < color_attachments_len; ++i) {
		PyObject * item = PyTuple_GET_ITEM(color_attachments, i);

		if (Py_TYPE(item) == &MGLTexture_Type) {

			MGLTexture * texture = (MGLTexture *)item;

			gl.FramebufferTexture2D(
				GL_FRAMEBUFFER,
				GL_COLOR_ATTACHMENT0 + i,
				texture->samples ? GL_TEXTURE_2D_MULTISAMPLE : GL_TEXTURE_2D,
				texture->texture_obj,
				0
			);

		} else if (Py_TYPE(item) == &MGLRenderbuffer_Type) {

			MGLRenderbuffer * renderbuffer = (MGLRenderbuffer *)item;

			gl.FramebufferRenderbuffer(
				GL_FRAMEBUFFER,
				GL_COLOR_ATTACHMENT0 + i,
				GL_RENDERBUFFER,
				renderbuffer->renderbuffer_obj
			);
		}
	}

	if (Py_TYPE(depth_attachment) == &MGLTexture_Type) {
		MGLTexture * texture = (MGLTexture *)depth_attachment;

		gl.FramebufferTexture2D(
			GL_FRAMEBUFFER,
			GL_DEPTH_ATTACHMENT,
			texture->samples ? GL_TEXTURE_2D_MULTISAMPLE : GL_TEXTURE_2D,
			texture->texture_obj,
			0
		);

	} else if (Py_TYPE(depth_attachment) == &MGLRenderbuffer_Type) {
		MGLRenderbuffer * renderbuffer = (MGLRenderbuffer *)depth_attachment;

		gl.FramebufferRenderbuffer(
			GL_FRAMEBUFFER,
			GL_DEPTH_ATTACHMENT,
			GL_RENDERBUFFER,
			renderbuffer->renderbuffer_obj
		);
	}

	int status = gl.CheckFramebufferStatus(GL_FRAMEBUFFER);

	gl.BindFramebuffer(GL_FRAMEBUFFER, draw_framebuffer);

	if (status != GL_FRAMEBUFFER_COMPLETE) {
		const char * message = "framebuffer is not complete";

		switch (status) {
			case GL_FRAMEBUFFER_UNDEFINED:
				message = "framebuffer is not complete 0";
				break;

			case GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT:
				message = "framebuffer is not complete 1";
				break;

			case GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT:
				message = "framebuffer is not complete 2";
				break;

			case GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER:
				message = "framebuffer is not complete 3";
				break;

			case GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER:
				message = "framebuffer is not complete 4";
				break;

			case GL_FRAMEBUFFER_UNSUPPORTED:
				message = "framebuffer is not complete 5";
				break;

			case GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE:
				message = "framebuffer is not complete 6";
				break;

			case GL_FRAMEBUFFER_INCOMPLETE_LAYER_TARGETS:
				message = "framebuffer is not complete 7";
				break;
		}

		MGLError * error = MGLError_FromFormat(TRACE, message);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	framebuffer->color_attachments = color_attachments;
	framebuffer->depth_attachment = depth_attachment;

	framebuffer->width = width;
	framebuffer->height = height;

	Py_INCREF(self);
	framebuffer->context = self;

	Py_INCREF(framebuffer);
	return framebuffer;
}

MGLRenderbuffer * MGLContext_renderbuffer(MGLContext * self, PyObject * args) {
	int width;
	int height;

	int components;

	int samples;
	int floats;

	int args_ok = PyArg_ParseTuple(
		args,
		"(II)IIp",
		&width,
		&height,
		&components,
		&samples,
		&floats
	);

	if (!args_ok) {
		return 0;
	}

	if (components < 1 || components > 4) {
		MGLError * error = MGLError_FromFormat(TRACE, "components must be 1, 2, 3 or 4");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	const int int_formats[] = {0, GL_R8UI, GL_RG8UI, GL_RGB8UI, GL_RGBA8UI};
	const int float_formats[] = {0, GL_R32F, GL_RG32F, GL_RGB32F, GL_RGBA32F};

	int format = floats ? float_formats[components] : int_formats[components];

	const GLMethods & gl = self->gl;

	MGLRenderbuffer * renderbuffer = MGLRenderbuffer_New();

	renderbuffer->renderbuffer_obj = 0;
	gl.GenRenderbuffers(1, (GLuint *)&renderbuffer->renderbuffer_obj);
	gl.BindRenderbuffer(GL_RENDERBUFFER, renderbuffer->renderbuffer_obj);

	if (samples == 0) {
		gl.RenderbufferStorage(GL_RENDERBUFFER, format, width, height);
	} else {
		gl.RenderbufferStorageMultisample(GL_RENDERBUFFER, samples, format, width, height);
	}

	renderbuffer->width = width;
	renderbuffer->height = height;
	renderbuffer->components = components;
	renderbuffer->samples = samples;
	renderbuffer->floats = floats ? true : false;
	renderbuffer->depth = false;

	Py_INCREF(self);
	renderbuffer->context = self;

	Py_INCREF(renderbuffer);
	return renderbuffer;
}

MGLRenderbuffer * MGLContext_depth_renderbuffer(MGLContext * self, PyObject * args) {
	int width;
	int height;

	int samples;

	int args_ok = PyArg_ParseTuple(
		args,
		"(II)I",
		&width,
		&height,
		&samples
	);

	if (!args_ok) {
		return 0;
	}

	const GLMethods & gl = self->gl;

	MGLRenderbuffer * renderbuffer = MGLRenderbuffer_New();

	renderbuffer->renderbuffer_obj = 0;
	gl.GenRenderbuffers(1, (GLuint *)&renderbuffer->renderbuffer_obj);
	gl.BindRenderbuffer(GL_RENDERBUFFER, renderbuffer->renderbuffer_obj);

	if (samples == 0) {
		gl.RenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, width, height);
	} else {
		gl.RenderbufferStorageMultisample(GL_RENDERBUFFER, samples, GL_DEPTH_COMPONENT24, width, height);
	}

	renderbuffer->width = width;
	renderbuffer->height = height;
	renderbuffer->components = 1;
	renderbuffer->samples = samples;
	renderbuffer->floats = true;
	renderbuffer->depth = true;

	Py_INCREF(self);
	renderbuffer->context = self;

	Py_INCREF(renderbuffer);
	return renderbuffer;
}

MGLComputeShader * MGLContext_compute_shader(MGLContext * self, PyObject * args) {
	PyObject * source;

	int args_ok = PyArg_ParseTuple(
		args,
		"O",
		&source
	);

	if (!args_ok) {
		return 0;
	}

	if (!PyUnicode_Check(source)) {
		MGLError * error = MGLError_FromFormat(TRACE, "source must be a str not %s", Py_TYPE(source)->tp_name);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	MGLComputeShader * compute_shader = MGLComputeShader_New();

	Py_INCREF(source);
	compute_shader->source = source;

	Py_INCREF(self);
	compute_shader->context = self;

	const char * source_str = PyUnicode_AsUTF8(source);

	const GLMethods & gl = self->gl;

	int shader_obj = gl.CreateShader(GL_COMPUTE_SHADER);

	if (!shader_obj) {
		MGLError * error = MGLError_FromFormat(TRACE, "cannot create shader object");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	gl.ShaderSource(shader_obj, 1, &source_str, 0);
	gl.CompileShader(shader_obj);

	int compiled = GL_FALSE;
	gl.GetShaderiv(shader_obj, GL_COMPILE_STATUS, &compiled);

	if (!compiled) {
		const char * message = "GLSL Compiler failed";
		const char * title = "ComputeShader";
		const char * underline = "=============";

		int log_len = 0;
		gl.GetShaderiv(shader_obj, GL_INFO_LOG_LENGTH, &log_len);

		char * log = new char[log_len];
		gl.GetShaderInfoLog(shader_obj, log_len, &log_len, log);

		gl.DeleteShader(shader_obj);

		MGLError * error = MGLError_FromFormat(TRACE, "%s\n\n%s\n%s\n%s\n", message, title, underline, log);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);

		delete[] log;
		return 0;
	}

	compute_shader->shader_obj = shader_obj;

	int program_obj = gl.CreateProgram();

	if (!program_obj) {
		MGLError * error = MGLError_FromFormat(TRACE, "cannot create program object");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	gl.AttachShader(program_obj, shader_obj);
	gl.LinkProgram(program_obj);

	int linked = GL_FALSE;
	gl.GetProgramiv(program_obj, GL_LINK_STATUS, &linked);

	if (!linked) {
		const char * message = "GLSL Linker failed";
		const char * title = "ComputeShader";
		const char * underline = "=============";

		int log_len = 0;
		gl.GetProgramiv(program_obj, GL_INFO_LOG_LENGTH, &log_len);

		char * log = new char[log_len];
		gl.GetProgramInfoLog(program_obj, log_len, &log_len, log);

		gl.DeleteProgram(program_obj);

		MGLError * error = MGLError_FromFormat(TRACE, "%s\n\n%s\n%s\n%s\n", message, title, underline, log);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);

		delete[] log;
		return 0;
	}

	compute_shader->program_obj = program_obj;

	return compute_shader;
}

PyObject * MGLContext_release(MGLContext * self) {
	// MGLContext_Invalidate(self);
	Py_RETURN_NONE;
}

PyMethodDef MGLContext_tp_methods[] = {
	{"clear", (PyCFunction)MGLContext_clear, METH_VARARGS, 0},
	{"enable", (PyCFunction)MGLContext_enable, METH_VARARGS, 0},
	{"disable", (PyCFunction)MGLContext_disable, METH_VARARGS, 0},
	{"finish", (PyCFunction)MGLContext_finish, METH_NOARGS, 0},
	{"copy_buffer", (PyCFunction)MGLContext_copy_buffer, METH_VARARGS, 0},
	{"copy_framebuffer", (PyCFunction)MGLContext_copy_framebuffer, METH_VARARGS, 0},

	{"buffer", (PyCFunction)MGLContext_buffer, METH_VARARGS, 0},
	{"texture", (PyCFunction)MGLContext_texture, METH_VARARGS, 0},
	{"depth_texture", (PyCFunction)MGLContext_depth_texture, METH_VARARGS, 0},
	{"vertex_array", (PyCFunction)MGLContext_vertex_array, METH_VARARGS, 0},
	{"program", (PyCFunction)MGLContext_program, METH_VARARGS, 0},
	{"vertex_shader", (PyCFunction)MGLContext_shader<VERTEX_SHADER_SLOT>, METH_VARARGS, 0},
	{"fragment_shader", (PyCFunction)MGLContext_shader<FRAGMENT_SHADER_SLOT>, METH_VARARGS, 0},
	{"geometry_shader", (PyCFunction)MGLContext_shader<GEOMETRY_SHADER_SLOT>, METH_VARARGS, 0},
	{"tess_evaluation_shader", (PyCFunction)MGLContext_shader<TESS_EVALUATION_SHADER_SLOT>, METH_VARARGS, 0},
	{"tess_control_shader", (PyCFunction)MGLContext_shader<TESS_CONTROL_SHADER_SLOT>, METH_VARARGS, 0},
	{"framebuffer", (PyCFunction)MGLContext_framebuffer, METH_VARARGS, 0},
	{"renderbuffer", (PyCFunction)MGLContext_renderbuffer, METH_VARARGS, 0},
	{"depth_renderbuffer", (PyCFunction)MGLContext_depth_renderbuffer, METH_VARARGS, 0},
	{"compute_shader", (PyCFunction)MGLContext_compute_shader, METH_VARARGS, 0},

	{"release", (PyCFunction)MGLContext_release, METH_NOARGS, 0},

	{0},
};

PyObject * MGLContext_get_line_width(MGLContext * self) {
	float line_width = 0.0f;

	self->gl.GetFloatv(GL_LINE_WIDTH, &line_width);

	return PyFloat_FromDouble(line_width);
}

int MGLContext_set_line_width(MGLContext * self, PyObject * value) {
	float line_width = (float)PyFloat_AsDouble(value);

	if (PyErr_Occurred()) {
		return -1;
	}

	self->gl.LineWidth(line_width);

	return 0;
}

PyObject * MGLContext_get_point_size(MGLContext * self) {
	float point_size = 0.0f;

	self->gl.GetFloatv(GL_POINT_SIZE, &point_size);

	return PyFloat_FromDouble(point_size);
}

int MGLContext_set_point_size(MGLContext * self, PyObject * value) {
	float point_size = (float)PyFloat_AsDouble(value);

	if (PyErr_Occurred()) {
		return -1;
	}

	self->gl.PointSize(point_size);

	return 0;
}

PyObject * MGLContext_get_viewport(MGLContext * self) {
	int viewport[4] = {};

	self->gl.GetIntegerv(GL_VIEWPORT, viewport);

	PyObject * x = PyLong_FromLong(viewport[0]);
	PyObject * y = PyLong_FromLong(viewport[1]);
	PyObject * width = PyLong_FromLong(viewport[2]);
	PyObject * height = PyLong_FromLong(viewport[3]);

	return PyTuple_Pack(4, x, y, width, height);
}

int MGLContext_set_viewport(MGLContext * self, PyObject * value) {
	int size = (int)PyTuple_GET_SIZE(value);

	if (PyErr_Occurred()) {
		return -1;
	}

	if (size != 4) {
		MGLError * error = MGLError_FromFormat(TRACE, "viewport must be a tuple of size 4 not %d", size);
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return -1;
	}

	int x = PyLong_AsLong(PyTuple_GET_ITEM(value, 0));
	int y = PyLong_AsLong(PyTuple_GET_ITEM(value, 1));
	int width = PyLong_AsLong(PyTuple_GET_ITEM(value, 2));
	int height = PyLong_AsLong(PyTuple_GET_ITEM(value, 3));

	if (PyErr_Occurred()) {
		return -1;
	}

	self->gl.Viewport(x, y, width, height);

	return 0;
}

PyObject * MGLContext_get_default_texture_unit(MGLContext * self) {
	return PyLong_FromLong(self->default_texture_unit);
}

int MGLContext_set_default_texture_unit(MGLContext * self, PyObject * value) {
	int default_texture_unit = PyLong_AsLong(value);

	if (PyErr_Occurred()) {
		return -1;
	}

	self->default_texture_unit = default_texture_unit;

	return 0;
}

PyObject * MGLContext_get_max_texture_units(MGLContext * self) {
	return PyLong_FromLong(self->max_texture_units);
}

PyObject * MGLContext_get_default_framebuffer(MGLContext * self) {
	if (!self->default_framebuffer) {
		MGLFramebuffer * framebuffer = MGLFramebuffer_New();

		framebuffer->framebuffer_obj = 0;

		framebuffer->color_attachments = 0;
		framebuffer->depth_attachment = 0;

		// NO INCREF
		framebuffer->context = self;

		framebuffer->width = 0;
		framebuffer->height = 0;

		self->default_framebuffer = (PyObject *)framebuffer;
	}

	Py_INCREF(self->default_framebuffer);
	return self->default_framebuffer;
}

PyObject * MGLContext_get_vendor(MGLContext * self, void * closure) {
	const char * vendor = (const char *)self->gl.GetString(GL_VENDOR);

	if (!vendor) {
		MGLError * error = MGLError_FromFormat(TRACE, "Missing vendor information");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	return PyUnicode_FromFormat("%s", vendor);
}

PyObject * MGLContext_get_renderer(MGLContext * self, void * closure) {
	const char * renderer = (const char *)self->gl.GetString(GL_RENDERER);

	if (!renderer) {
		MGLError * error = MGLError_FromFormat(TRACE, "Missing renderer information");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	return PyUnicode_FromFormat("%s", renderer);
}

PyObject * MGLContext_get_version(MGLContext * self, void * closure) {
	const char * version = (const char *)self->gl.GetString(GL_VERSION);

	if (!version) {
		MGLError * error = MGLError_FromFormat(TRACE, "Missing version information");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return 0;
	}

	return PyUnicode_FromFormat("%s", version);
}

PyObject * MGLContext_get_version_code(MGLContext * self, void * closure) {
	int major = 0;
	int minor = 0;

	const GLMethods & gl = self->gl;
	gl.GetIntegerv(GL_MAJOR_VERSION, &major);
	gl.GetIntegerv(GL_MINOR_VERSION, &minor);

	return PyLong_FromLong(major * 100 + minor * 10);
}

PyGetSetDef MGLContext_tp_getseters[] = {
	{(char *)"line_width", (getter)MGLContext_get_line_width, (setter)MGLContext_set_line_width, 0, 0},
	{(char *)"point_size", (getter)MGLContext_get_point_size, (setter)MGLContext_set_point_size, 0, 0},
	{(char *)"viewport", (getter)MGLContext_get_viewport, (setter)MGLContext_set_viewport, 0, 0},
	{(char *)"default_texture_unit", (getter)MGLContext_get_default_texture_unit, (setter)MGLContext_set_default_texture_unit, 0, 0},
	{(char *)"max_texture_units", (getter)MGLContext_get_max_texture_units, 0, 0, 0},
	{(char *)"default_framebuffer", (getter)MGLContext_get_default_framebuffer, 0, 0, 0},

	{(char *)"vendor", (getter)MGLContext_get_vendor, 0, 0, 0},
	{(char *)"renderer", (getter)MGLContext_get_renderer, 0, 0, 0},
	{(char *)"version", (getter)MGLContext_get_version, 0, 0, 0},
	{(char *)"version_code", (getter)MGLContext_get_version_code, 0, 0, 0},
	{0},
};

PyTypeObject MGLContext_Type = {
	PyVarObject_HEAD_INIT(0, 0)
	"mgl.Context",                                          // tp_name
	sizeof(MGLContext),                                     // tp_basicsize
	0,                                                      // tp_itemsize
	(destructor)MGLContext_tp_dealloc,                      // tp_dealloc
	0,                                                      // tp_print
	0,                                                      // tp_getattr
	0,                                                      // tp_setattr
	0,                                                      // tp_reserved
	(reprfunc)MGLContext_tp_str,                            // tp_repr
	0,                                                      // tp_as_number
	0,                                                      // tp_as_sequence
	0,                                                      // tp_as_mapping
	0,                                                      // tp_hash
	0,                                                      // tp_call
	(reprfunc)MGLContext_tp_str,                            // tp_str
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
	MGLContext_tp_methods,                                  // tp_methods
	0,                                                      // tp_members
	MGLContext_tp_getseters,                                // tp_getset
	0,                                                      // tp_base
	0,                                                      // tp_dict
	0,                                                      // tp_descr_get
	0,                                                      // tp_descr_set
	0,                                                      // tp_dictoffset
	(initproc)MGLContext_tp_init,                           // tp_init
	0,                                                      // tp_alloc
	MGLContext_tp_new,                                      // tp_new
};

MGLContext * MGLContext_New() {
	MGLContext * self = (MGLContext *)MGLContext_tp_new(&MGLContext_Type, 0, 0);
	return self;
}

void MGLContext_Invalidate(MGLContext * context) {
	if (Py_TYPE(context) == &MGLInvalidObject_Type) {

		#ifdef MGL_VERBOSE
		printf("MGLContext_Invalidate %p already released\n", context);
		#endif

		return;
	}

	#ifdef MGL_VERBOSE
	printf("MGLContext_Invalidate %p\n", context);
	#endif

	DestroyGLContext(context->gl_context);

	Py_TYPE(context) = &MGLInvalidObject_Type;

	Py_DECREF(context);
}

void MGLContext_Initialize(MGLContext * self) {

	GLMethods & gl = self->gl;

	if (!gl.load()) {
		return;
	}

	gl.BlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

	// gl.Enable(GL_PRIMITIVE_RESTART_FIXED_INDEX);

	gl.Enable(GL_PRIMITIVE_RESTART);
	gl.PrimitiveRestartIndex(-1);

	gl.GetIntegerv(GL_MAX_TEXTURE_IMAGE_UNITS, (GLint *)&self->max_texture_units);
	self->default_texture_unit = self->max_texture_units - 1;
}
