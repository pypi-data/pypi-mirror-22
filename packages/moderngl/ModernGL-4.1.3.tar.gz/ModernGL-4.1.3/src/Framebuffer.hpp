#pragma once

#include "Python.hpp"

#include "ContextMember.hpp"

struct MGLFramebuffer : public MGLContextMember {
	PyObject * color_attachments;
	PyObject * depth_attachment;

	unsigned * draw_buffers;
	int draw_buffers_len;

	int framebuffer_obj;

	int width;
	int height;
	int samples;
};

extern PyTypeObject MGLFramebuffer_Type;

MGLFramebuffer * MGLFramebuffer_New();
void MGLFramebuffer_Invalidate(MGLFramebuffer * framebuffer);
