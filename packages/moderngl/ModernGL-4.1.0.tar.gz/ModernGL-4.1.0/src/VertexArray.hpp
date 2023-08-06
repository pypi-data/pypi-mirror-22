#pragma once

#include "Python.hpp"

#include "ContextMember.hpp"
#include "Program.hpp"
#include "Buffer.hpp"

struct MGLVertexArray : public MGLContextMember {
	MGLProgram * program;

	MGLBuffer * index_buffer;

	PyObject * attributes;

	unsigned * subroutine_uniform_locations;
	int num_subroutine_uniform_locations;

	int num_vertex_shader_subroutine_uniform_locations;
	int num_fragment_shader_subroutine_uniform_locations;
	int num_geometry_shader_subroutine_uniform_locations;
	int num_tess_evaluation_shader_subroutine_uniform_locations;
	int num_tess_control_shader_subroutine_uniform_locations;

	int vertex_array_obj;
	int num_vertices;
};

extern PyTypeObject MGLVertexArray_Type;

MGLVertexArray * MGLVertexArray_New();
void MGLVertexArray_Invalidate(MGLVertexArray * vertex_array);
void MGLVertexArray_Complete(MGLVertexArray * vertex_array);
