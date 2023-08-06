#pragma once

#include "Python.hpp"

#define TRACE __FILE__, __LINE__

struct MGLError {
	PyException_HEAD

	PyObject * github;
};

extern PyTypeObject MGLError_Type;

MGLError * MGLError_FromFormat(const char * filename, int line, const char * format, ...);
MGLError * MGLError_FromMessage(const char * filename, int line, PyObject * message);
