#pragma once

#include "Python.hpp"

#include "ProgramStageMember.hpp"

struct MGLSubroutineUniform : public MGLProgramStageMember {
	PyObject * name;
	int location;
};

extern PyTypeObject MGLSubroutineUniform_Type;

MGLSubroutineUniform * MGLSubroutineUniform_New();
void MGLSubroutineUniform_Complete(MGLSubroutineUniform * subroutine_uniform);
