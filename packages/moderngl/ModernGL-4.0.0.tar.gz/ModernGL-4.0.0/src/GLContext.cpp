#include "GLContext.hpp"

#include "Error.hpp"

#if defined(_WIN32) || defined(_WIN64)

#include <Windows.h>

const unsigned WGL_ACCELERATION             = 0x2003;
const unsigned WGL_COLOR_BITS               = 0x2014;
const unsigned WGL_CONTEXT_FLAGS            = 0x2094;
const unsigned WGL_CONTEXT_MAJOR_VERSION    = 0x2091;
const unsigned WGL_CONTEXT_MINOR_VERSION    = 0x2092;
const unsigned WGL_DEPTH_BITS               = 0x2022;
const unsigned WGL_DOUBLE_BUFFER            = 0x2011;
const unsigned WGL_DRAW_TO_WINDOW           = 0x2001;
const unsigned WGL_FULL_ACCELERATION        = 0x2027;
const unsigned WGL_PIXEL_TYPE               = 0x2013;
const unsigned WGL_SAMPLES                  = 0x2042;
const unsigned WGL_STENCIL_BITS             = 0x2023;
const unsigned WGL_SUPPORT_OPENGL           = 0x2010;
const unsigned WGL_TYPE_RGBA                = 0x202B;
const unsigned WGL_CONTEXT_PROFILE_MASK     = 0x9126;
const unsigned WGL_CONTEXT_CORE_PROFILE_BIT = 0x0001;

typedef int (WINAPI * mglChoosePixelFormatProc)(HDC hdc, const int * piAttribIList, const float * pfAttribFList, unsigned nMaxFormats, int * piFormats, unsigned * nNumFormats);
typedef HGLRC (WINAPI * mglCreateContextAttribsProc)(HDC hdc, HGLRC hglrc, const int * attribList);

mglChoosePixelFormatProc mglChoosePixelFormat;
mglCreateContextAttribsProc mglCreateContextAttribs;

PIXELFORMATDESCRIPTOR pfd = {
	sizeof(PIXELFORMATDESCRIPTOR),	// nSize
	1,								// nVersion
	PFD_DRAW_TO_WINDOW |
	PFD_SUPPORT_OPENGL |
	PFD_GENERIC_ACCELERATED |
	PFD_DOUBLEBUFFER,				// dwFlags
	0,								// iPixelType
	32,								// cColorBits
	0,								// cRedBits
	0,								// cRedShift
	0,								// cGreenBits
	0,								// cGreenShift
	0,								// cBlueBits
	0,								// cBlueShift
	0,								// cAlphaBits
	0,								// cAlphaShift
	0,								// cAccumBits
	0,								// cAccumRedBits
	0,								// cAccumGreenBits
	0,								// cAccumBlueBits
	0,								// cAccumAlphaBits
	24,								// cDepthBits
	0,								// cStencilBits
	0,								// cAuxBuffers
	0,								// iLayerType
	0,								// bReserved
	0,								// dwLayerMask
	0,								// dwVisibleMask
	0,								// dwDamageMask
};

GLContext LoadCurrentGLContext() {
	GLContext context = {};

	HGLRC hrc = wglGetCurrentContext();
	HDC hdc = wglGetCurrentDC();

	if (!hrc || !hdc) {
		MGLError * error = MGLError_FromFormat(TRACE, "Cannot detect current context.");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return context;
	}

	HWND hwnd = WindowFromDC(hdc);

	context.hwnd = (void *)hwnd;
	context.hdc = (void *)hdc;
	context.hrc = (void *)hrc;
	context.standalone = false;

	return context;
}

void InitModernContext() {
	static bool initialized = false;

	if (initialized) {
		return;
	}

	initialized = true;

	HMODULE hinst = GetModuleHandle(0);

	if (!hinst) {
		return;
	}

	WNDCLASS extClass = {
		CS_OWNDC,						// style
		DefWindowProc,					// lpfnWndProc
		0,								// cbClsExtra
		0,								// cbWndExtra
		hinst,							// hInstance
		0,								// hIcon
		0,								// hCursor
		0,								// hbrBackground
		0,								// lpszMenuName
		"ContextLoader",				// lpszClassName
	};

	if (!RegisterClass(&extClass)) {
		return;
	}

	HWND loader_hwnd = CreateWindow(
		"ContextLoader",				// lpClassName
		0,								// lpWindowName
		0,								// dwStyle
		0,								// x
		0,								// y
		0,								// nWidth
		0,								// nHeight
		0,								// hWndParent
		0,								// hMenu
		hinst,							// hInstance
		0								// lpParam
	);

	if (!loader_hwnd) {
		return;
	}

	HDC loader_hdc = GetDC(loader_hwnd);

	if (!loader_hdc) {
		return;
	}

	int loader_pixelformat = ChoosePixelFormat(loader_hdc, &pfd);

	if (!loader_pixelformat) {
		return;
	}

	if (!SetPixelFormat(loader_hdc, loader_pixelformat, &pfd)) {
		return;
	}

	HGLRC loader_hglrc = wglCreateContext(loader_hdc);

	if (!loader_hglrc) {
		return;
	}

	if (!wglMakeCurrent(loader_hdc, loader_hglrc)) {
		return;
	}

	mglCreateContextAttribs = (mglCreateContextAttribsProc)wglGetProcAddress("wglCreateContextAttribsARB");
	if (!mglCreateContextAttribs) {
		return;
	}

	mglChoosePixelFormat = (mglChoosePixelFormatProc)wglGetProcAddress("wglChoosePixelFormatARB");
	if (!mglChoosePixelFormat) {
		return;
	}

	if (!wglMakeCurrent(0, 0)) {
		return;
	}

	if (!wglDeleteContext(loader_hglrc)) {
		return;
	}

	if (!ReleaseDC(loader_hwnd, loader_hdc)) {
		return;
	}

	if (!DestroyWindow(loader_hwnd)) {
		return;
	}

	if (!UnregisterClass("ContextLoader", hinst)) {
		return;
	}
}

GLContext CreateGLContext(int width, int height) {
	GLContext context = {};

	InitModernContext();

	HINSTANCE inst = GetModuleHandle(0);

	if (!inst) {
		MGLError * error = MGLError_FromFormat(TRACE, "Module handle is null");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return context;
	}

	static bool registered = false;

	if (!registered) {
		WNDCLASS wndClass = {
			CS_OWNDC,                            // style
			DefWindowProc,                       // lpfnWndProc
			0,                                   // cbClsExtra
			0,                                   // cbWndExtra
			inst,                                // hInstance
			0,                                   // hIcon
			0,                                   // hCursor
			0,                                   // hbrBackground
			0,                                   // lpszMenuName
			"StandaloneContext",                 // lpszClassName
		};

		if (!RegisterClass(&wndClass)) {
			MGLError * error = MGLError_FromFormat(TRACE, "Cannot register window class");
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return context;
		}

		registered = true;
	}

	HWND hwnd = CreateWindowEx(
		0,                                   // exStyle
		"StandaloneContext",                 // lpClassName
		0,                                   // lpWindowName
		0,                                   // dwStyle
		0,                                   // x
		0,                                   // y
		0,                                   // nWidth
		0,                                   // nHeight
		0,                                   // hWndParent
		0,                                   // hMenu
		inst,                                // hInstance
		0                                    // lpParam
	);

	if (!hwnd) {
		MGLError * error = MGLError_FromFormat(TRACE, "Cannot create window");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return context;
	}

	HDC hdc = GetDC(hwnd);

	if (!hdc) {
		MGLError * error = MGLError_FromFormat(TRACE, "Cannot create device content");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return context;
	}

	HGLRC hrc = 0;

	if (mglCreateContextAttribs && mglChoosePixelFormat) {

		int pixelformat = 0;
		unsigned num_formats = 0;

		if (!mglChoosePixelFormat(hdc, 0, 0, 1, &pixelformat, &num_formats)) {
			MGLError * error = MGLError_FromFormat(TRACE, "Cannot choose pixel format");
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return context;
		}

		if (!num_formats) {
			MGLError * error = MGLError_FromFormat(TRACE, "No pixel formats available");
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return context;
		}

		if (!SetPixelFormat(hdc, pixelformat, &pfd)) {
			MGLError * error = MGLError_FromFormat(TRACE, "Cannot set pixel format");
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return context;
		}

		int major[] = {4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 0};
		int minor[] = {5, 4, 3, 2, 1, 0, 3, 2, 1, 0, 0};

		for (int i = 0; i < 10; ++i) {
			int attribs[] = {
				WGL_CONTEXT_PROFILE_MASK, WGL_CONTEXT_CORE_PROFILE_BIT,
				WGL_CONTEXT_MAJOR_VERSION, major[i],
				WGL_CONTEXT_MINOR_VERSION, minor[i],
				0, 0,
			};

			hrc = mglCreateContextAttribs(hdc, 0, attribs);

			if (hrc) {
				break;
			}
		}

	} else {

		int pf = ChoosePixelFormat(hdc, &pfd);

		if (!pf) {
			MGLError * error = MGLError_FromFormat(TRACE, "Cannot choose pixel format");
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return context;
		}

		int set_pixel_format = SetPixelFormat(hdc, pf, &pfd);

		if (!set_pixel_format) {
			MGLError * error = MGLError_FromFormat(TRACE, "Cannot set pixel format");
			PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
			return context;
		}

		hrc = wglCreateContext(hdc);

	}

	if (!hrc) {
		MGLError * error = MGLError_FromFormat(TRACE, "Cannot create OpenGL context");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return context;
	}

	int make_current = wglMakeCurrent(hdc, hrc);

	if (!make_current) {
		MGLError * error = MGLError_FromFormat(TRACE, "Cannot select OpenGL context");
		PyErr_SetObject((PyObject *)&MGLError_Type, (PyObject *)error);
		return context;
	}

	context.hwnd = (void *)hwnd;
	context.hrc = (void *)hrc;
	context.hdc = (void *)hdc;
	context.standalone = true;

	return context;
}

void DestroyGLContext(const GLContext & context) {
	if (!context.standalone) {
		return;
	}

	if (wglGetCurrentContext() == context.hrc) {
		wglMakeCurrent(0, 0);
	}

	wglDeleteContext((HGLRC)context.hrc);
	ReleaseDC((HWND)context.hwnd, (HDC)context.hdc);
	DestroyWindow((HWND)context.hwnd);
}

#elif defined(__APPLE__)

#include <OpenGL/gl.h>

GLContext LoadCurrentGLContext() {
	GLContext context = {};
	return context;
}

GLContext CreateGLContext(int width, int height) {
	GLContext context = {};
	return context;
}

void DestroyGLContext(const GLContext & context) {
	// TODO:
}

#else

#include <GL/glx.h>
#include <GL/gl.h>

#define GLX_CONTEXT_MAJOR_VERSION_ARB 0x2091
#define GLX_CONTEXT_MINOR_VERSION_ARB 0x2092

typedef GLXContext (* GLXCREATECONTEXTATTRIBSARBPROC)(Display * display, GLXFBConfig config, GLXContext context, Bool direct, const int * attribs);

GLContext LoadCurrentGLContext() {
	GLContext context = {};
	return context;
}

GLContext CreateGLContext(int width, int height) {
	GLContext context = {};

	Display * dpy = XOpenDisplay(0);

	int nelements = 0;
	GLXFBConfig * fbc = glXChooseFBConfig(dpy, DefaultScreen(dpy), 0, &nelements);

	static int attributeList[] = {GLX_RGBA, GLX_DOUBLEBUFFER, GLX_RED_SIZE, 1, GLX_GREEN_SIZE, 1, GLX_BLUE_SIZE, 1, None};
	XVisualInfo * vi = glXChooseVisual(dpy, DefaultScreen(dpy), attributeList);

	XSetWindowAttributes swa;
	swa.colormap = XCreateColormap(dpy, RootWindow(dpy, vi->screen), vi->visual, AllocNone);
	swa.border_pixel = 0;
	swa.event_mask = StructureNotifyMask;
	Window win = XCreateWindow(dpy, RootWindow(dpy, vi->screen), 0, 0, 100, 100, 0, vi->depth, InputOutput, vi->visual, CWBorderPixel | CWColormap | CWEventMask, &swa);

	// XMapWindow(dpy, win);

	GLXCREATECONTEXTATTRIBSARBPROC glXCreateContextAttribsARB = (GLXCREATECONTEXTATTRIBSARBPROC)glXGetProcAddress((const GLubyte *)"glXCreateContextAttribsARB");

	int major[] = {4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 0};
	int minor[] = {5, 4, 3, 2, 1, 0, 3, 2, 1, 0, 0};

	GLXContext ctx = 0;

	for (int i = 0; i < 10; ++i) {
		int attribs[] = {
			GLX_CONTEXT_MAJOR_VERSION_ARB, major[i],
			GLX_CONTEXT_MINOR_VERSION_ARB, minor[i],
			0, 0,
		};

		ctx = glXCreateContextAttribsARB(dpy, *fbc, 0, true, attribs);

		if (ctx) {
			break;
		}
	}

	if (!ctx) {
		ctx = glXCreateContext(dpy, vi, 0, GL_TRUE);
	}

	glXMakeCurrent(dpy, win, ctx);

	context.display = (void *)dpy;
	context.window = (void *)win;
	context.context = (void *)ctx;

	return context;
}

void DestroyGLContext(const GLContext & context) {
	// TODO:
}

#endif
