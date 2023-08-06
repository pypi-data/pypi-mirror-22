#pragma once

#include "Python.hpp"

#include "ProgramStageMember.hpp"

struct MGLSubroutine : public MGLProgramStageMember {
	PyObject * name;
	unsigned index;
};

extern PyTypeObject MGLSubroutine_Type;

MGLSubroutine * MGLSubroutine_New();
void MGLSubroutine_Invalidate(MGLSubroutine * subroutine);
void MGLSubroutine_Complete(MGLSubroutine * subroutine);
