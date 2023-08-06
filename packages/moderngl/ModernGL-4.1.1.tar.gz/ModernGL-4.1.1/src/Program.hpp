#pragma once

#include "Python.hpp"

#include "ContextMember.hpp"
#include "Primitive.hpp"

struct MGLProgramStage;

struct MGLProgram : public MGLContextMember {
	PyObject * shaders;

	MGLProgramStage * vertex_shader;
	MGLProgramStage * fragment_shader;
	MGLProgramStage * geometry_shader;
	MGLProgramStage * tess_evaluation_shader;
	MGLProgramStage * tess_control_shader;

	PyObject * uniforms;
	PyObject * uniform_blocks;
	PyObject * attributes;
	PyObject * varyings;

	MGLPrimitive * geometry_input;
	MGLPrimitive * geometry_output;

	int program_obj;

	int geometry_vertices;
	int num_varyings;
};

extern PyTypeObject MGLProgram_Type;

MGLProgram * MGLProgram_New();
void MGLProgram_Invalidate(MGLProgram * program);
void MGLProgram_Compile(MGLProgram * program, PyObject * outputs);
