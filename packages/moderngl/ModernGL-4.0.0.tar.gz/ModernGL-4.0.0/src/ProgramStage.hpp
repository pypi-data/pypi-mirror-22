#pragma once

#include "Python.hpp"

#include "ProgramMember.hpp"
#include "Shader.hpp"

struct MGLProgramStage : public MGLObject {
	PyObject * subroutines;
	PyObject * subroutine_uniforms;
};

extern PyTypeObject MGLProgramStage_Type;

MGLProgramStage * MGLProgramStage_New();
void MGLProgramStage_Complete(MGLProgramStage * program_stage, int shader_type, int program_obj, int & location_base, const GLMethods & gl);
