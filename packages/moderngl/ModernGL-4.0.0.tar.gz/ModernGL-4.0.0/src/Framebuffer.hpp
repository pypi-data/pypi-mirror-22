#pragma once

#include "Python.hpp"

#include "ContextMember.hpp"

struct MGLFramebuffer : public MGLContextMember {
	PyObject * color_attachments;
	PyObject * depth_attachment;

	int width;
	int height;

	int framebuffer_obj;
};

extern PyTypeObject MGLFramebuffer_Type;

MGLFramebuffer * MGLFramebuffer_New();
void MGLFramebuffer_Invalidate(MGLFramebuffer * framebuffer);
