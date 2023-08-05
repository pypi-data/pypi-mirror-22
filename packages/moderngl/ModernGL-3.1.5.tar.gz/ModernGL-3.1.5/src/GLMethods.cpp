#include "GLMethods.hpp"

#include <cstdio>
#include <cstdlib>

#define INVALID_METHOD(method) (!(method))

void GLAPI FakeGetProgramStageiv(GLuint program, GLenum shadertype, GLenum pname, GLint * values) {
	values[0] = 0;
}

#if defined(_WIN32) || defined(_WIN64)

#include <Windows.h>

#ifdef MemoryBarrier
#undef MemoryBarrier
#endif

void * LoadMethod(const char * method) {
	method += 1; // ingore leading underscore

	static HMODULE opengl32 = LoadLibrary("opengl32.dll");

	void * proc = (void *)GetProcAddress(opengl32, method);

	if (proc) {
		return proc;
	}

	proc = (void *)wglGetProcAddress(method);

	if (proc) {
		return proc;
	}

	// printf("%s NOT found!\n", method);
	return 0;
}

#elif defined(__APPLE__)

#import <mach-o/dyld.h>
#import <stdlib.h>
#import <string.h>

void * LoadMethod(const char * method) {
	NSSymbol symbol = 0;

	if (NSIsSymbolNameDefined(method)) {
		symbol = NSLookupAndBindSymbol(method);
	}

	return symbol ? NSAddressOfSymbol(symbol) : 0;
}

#else

#include <dlfcn.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

typedef const void * (* PROC_glXGetProcAddress)(const char *);

void * LoadMethod(const char * method) {
	method += 1; // ingore leading underscore

	static void * libgl = dlopen("libGL.so.1", RTLD_LAZY);
	static PROC_glXGetProcAddress glXGetProcAddress = (PROC_glXGetProcAddress)dlsym(libgl, "glXGetProcAddress");

	void * proc = (void *)dlsym(libgl, method);

	if (proc) {
		// printf("%s found!\n", method);
		return proc;
	}

	proc = (void *)glXGetProcAddress(method);

	if (proc) {
		// printf("%s found!\n", method);
		return proc;
	}

	// printf("%s NOT found!\n", method);
	return 0;
}

#endif

bool GLMethods::load() {
	this->ActiveShaderProgram = (PROC_glActiveShaderProgram)LoadMethod("_glActiveShaderProgram");
	this->ActiveTexture = (PROC_glActiveTexture)LoadMethod("_glActiveTexture");
	this->AttachShader = (PROC_glAttachShader)LoadMethod("_glAttachShader");
	this->BeginConditionalRender = (PROC_glBeginConditionalRender)LoadMethod("_glBeginConditionalRender");
	this->BeginQuery = (PROC_glBeginQuery)LoadMethod("_glBeginQuery");
	this->BeginQueryIndexed = (PROC_glBeginQueryIndexed)LoadMethod("_glBeginQueryIndexed");
	this->BeginTransformFeedback = (PROC_glBeginTransformFeedback)LoadMethod("_glBeginTransformFeedback");
	this->BindAttribLocation = (PROC_glBindAttribLocation)LoadMethod("_glBindAttribLocation");
	this->BindBuffer = (PROC_glBindBuffer)LoadMethod("_glBindBuffer");
	this->BindBufferBase = (PROC_glBindBufferBase)LoadMethod("_glBindBufferBase");
	this->BindBufferRange = (PROC_glBindBufferRange)LoadMethod("_glBindBufferRange");
	this->BindBuffersBase = (PROC_glBindBuffersBase)LoadMethod("_glBindBuffersBase");
	this->BindBuffersRange = (PROC_glBindBuffersRange)LoadMethod("_glBindBuffersRange");
	this->BindFragDataLocation = (PROC_glBindFragDataLocation)LoadMethod("_glBindFragDataLocation");
	this->BindFragDataLocationIndexed = (PROC_glBindFragDataLocationIndexed)LoadMethod("_glBindFragDataLocationIndexed");
	this->BindFramebuffer = (PROC_glBindFramebuffer)LoadMethod("_glBindFramebuffer");
	this->BindImageTexture = (PROC_glBindImageTexture)LoadMethod("_glBindImageTexture");
	this->BindImageTextures = (PROC_glBindImageTextures)LoadMethod("_glBindImageTextures");
	this->BindProgramPipeline = (PROC_glBindProgramPipeline)LoadMethod("_glBindProgramPipeline");
	this->BindRenderbuffer = (PROC_glBindRenderbuffer)LoadMethod("_glBindRenderbuffer");
	this->BindSampler = (PROC_glBindSampler)LoadMethod("_glBindSampler");
	this->BindSamplers = (PROC_glBindSamplers)LoadMethod("_glBindSamplers");
	this->BindTexture = (PROC_glBindTexture)LoadMethod("_glBindTexture");
	this->BindTextureUnit = (PROC_glBindTextureUnit)LoadMethod("_glBindTextureUnit");
	this->BindTextures = (PROC_glBindTextures)LoadMethod("_glBindTextures");
	this->BindTransformFeedback = (PROC_glBindTransformFeedback)LoadMethod("_glBindTransformFeedback");
	this->BindVertexArray = (PROC_glBindVertexArray)LoadMethod("_glBindVertexArray");
	this->BindVertexBuffer = (PROC_glBindVertexBuffer)LoadMethod("_glBindVertexBuffer");
	this->BindVertexBuffers = (PROC_glBindVertexBuffers)LoadMethod("_glBindVertexBuffers");
	this->BlendColor = (PROC_glBlendColor)LoadMethod("_glBlendColor");
	this->BlendEquation = (PROC_glBlendEquation)LoadMethod("_glBlendEquation");
	this->BlendEquationSeparate = (PROC_glBlendEquationSeparate)LoadMethod("_glBlendEquationSeparate");
	this->BlendEquationSeparatei = (PROC_glBlendEquationSeparatei)LoadMethod("_glBlendEquationSeparatei");
	this->BlendEquationi = (PROC_glBlendEquationi)LoadMethod("_glBlendEquationi");
	this->BlendFunc = (PROC_glBlendFunc)LoadMethod("_glBlendFunc");
	this->BlendFuncSeparate = (PROC_glBlendFuncSeparate)LoadMethod("_glBlendFuncSeparate");
	this->BlendFuncSeparatei = (PROC_glBlendFuncSeparatei)LoadMethod("_glBlendFuncSeparatei");
	this->BlendFunci = (PROC_glBlendFunci)LoadMethod("_glBlendFunci");
	this->BlitFramebuffer = (PROC_glBlitFramebuffer)LoadMethod("_glBlitFramebuffer");
	this->BlitNamedFramebuffer = (PROC_glBlitNamedFramebuffer)LoadMethod("_glBlitNamedFramebuffer");
	this->BufferData = (PROC_glBufferData)LoadMethod("_glBufferData");
	this->BufferStorage = (PROC_glBufferStorage)LoadMethod("_glBufferStorage");
	this->BufferSubData = (PROC_glBufferSubData)LoadMethod("_glBufferSubData");
	this->CheckFramebufferStatus = (PROC_glCheckFramebufferStatus)LoadMethod("_glCheckFramebufferStatus");
	this->CheckNamedFramebufferStatus = (PROC_glCheckNamedFramebufferStatus)LoadMethod("_glCheckNamedFramebufferStatus");
	this->ClampColor = (PROC_glClampColor)LoadMethod("_glClampColor");
	this->Clear = (PROC_glClear)LoadMethod("_glClear");
	this->ClearBufferData = (PROC_glClearBufferData)LoadMethod("_glClearBufferData");
	this->ClearBufferSubData = (PROC_glClearBufferSubData)LoadMethod("_glClearBufferSubData");
	this->ClearBufferfi = (PROC_glClearBufferfi)LoadMethod("_glClearBufferfi");
	this->ClearBufferfv = (PROC_glClearBufferfv)LoadMethod("_glClearBufferfv");
	this->ClearBufferiv = (PROC_glClearBufferiv)LoadMethod("_glClearBufferiv");
	this->ClearBufferuiv = (PROC_glClearBufferuiv)LoadMethod("_glClearBufferuiv");
	this->ClearColor = (PROC_glClearColor)LoadMethod("_glClearColor");
	this->ClearDepth = (PROC_glClearDepth)LoadMethod("_glClearDepth");
	this->ClearDepthf = (PROC_glClearDepthf)LoadMethod("_glClearDepthf");
	this->ClearNamedBufferData = (PROC_glClearNamedBufferData)LoadMethod("_glClearNamedBufferData");
	this->ClearNamedBufferSubData = (PROC_glClearNamedBufferSubData)LoadMethod("_glClearNamedBufferSubData");
	this->ClearNamedFramebufferfi = (PROC_glClearNamedFramebufferfi)LoadMethod("_glClearNamedFramebufferfi");
	this->ClearNamedFramebufferfv = (PROC_glClearNamedFramebufferfv)LoadMethod("_glClearNamedFramebufferfv");
	this->ClearNamedFramebufferiv = (PROC_glClearNamedFramebufferiv)LoadMethod("_glClearNamedFramebufferiv");
	this->ClearNamedFramebufferuiv = (PROC_glClearNamedFramebufferuiv)LoadMethod("_glClearNamedFramebufferuiv");
	this->ClearStencil = (PROC_glClearStencil)LoadMethod("_glClearStencil");
	this->ClearTexImage = (PROC_glClearTexImage)LoadMethod("_glClearTexImage");
	this->ClearTexSubImage = (PROC_glClearTexSubImage)LoadMethod("_glClearTexSubImage");
	this->ClientWaitSync = (PROC_glClientWaitSync)LoadMethod("_glClientWaitSync");
	this->ClipControl = (PROC_glClipControl)LoadMethod("_glClipControl");
	this->ColorMask = (PROC_glColorMask)LoadMethod("_glColorMask");
	this->ColorMaski = (PROC_glColorMaski)LoadMethod("_glColorMaski");
	this->CompileShader = (PROC_glCompileShader)LoadMethod("_glCompileShader");
	this->CompressedTexImage1D = (PROC_glCompressedTexImage1D)LoadMethod("_glCompressedTexImage1D");
	this->CompressedTexImage2D = (PROC_glCompressedTexImage2D)LoadMethod("_glCompressedTexImage2D");
	this->CompressedTexImage3D = (PROC_glCompressedTexImage3D)LoadMethod("_glCompressedTexImage3D");
	this->CompressedTexSubImage1D = (PROC_glCompressedTexSubImage1D)LoadMethod("_glCompressedTexSubImage1D");
	this->CompressedTexSubImage2D = (PROC_glCompressedTexSubImage2D)LoadMethod("_glCompressedTexSubImage2D");
	this->CompressedTexSubImage3D = (PROC_glCompressedTexSubImage3D)LoadMethod("_glCompressedTexSubImage3D");
	this->CompressedTextureSubImage1D = (PROC_glCompressedTextureSubImage1D)LoadMethod("_glCompressedTextureSubImage1D");
	this->CompressedTextureSubImage2D = (PROC_glCompressedTextureSubImage2D)LoadMethod("_glCompressedTextureSubImage2D");
	this->CompressedTextureSubImage3D = (PROC_glCompressedTextureSubImage3D)LoadMethod("_glCompressedTextureSubImage3D");
	this->CopyBufferSubData = (PROC_glCopyBufferSubData)LoadMethod("_glCopyBufferSubData");
	this->CopyImageSubData = (PROC_glCopyImageSubData)LoadMethod("_glCopyImageSubData");
	this->CopyNamedBufferSubData = (PROC_glCopyNamedBufferSubData)LoadMethod("_glCopyNamedBufferSubData");
	this->CopyTexImage1D = (PROC_glCopyTexImage1D)LoadMethod("_glCopyTexImage1D");
	this->CopyTexImage2D = (PROC_glCopyTexImage2D)LoadMethod("_glCopyTexImage2D");
	this->CopyTexSubImage1D = (PROC_glCopyTexSubImage1D)LoadMethod("_glCopyTexSubImage1D");
	this->CopyTexSubImage2D = (PROC_glCopyTexSubImage2D)LoadMethod("_glCopyTexSubImage2D");
	this->CopyTexSubImage3D = (PROC_glCopyTexSubImage3D)LoadMethod("_glCopyTexSubImage3D");
	this->CopyTextureSubImage1D = (PROC_glCopyTextureSubImage1D)LoadMethod("_glCopyTextureSubImage1D");
	this->CopyTextureSubImage2D = (PROC_glCopyTextureSubImage2D)LoadMethod("_glCopyTextureSubImage2D");
	this->CopyTextureSubImage3D = (PROC_glCopyTextureSubImage3D)LoadMethod("_glCopyTextureSubImage3D");
	this->CreateBuffers = (PROC_glCreateBuffers)LoadMethod("_glCreateBuffers");
	this->CreateFramebuffers = (PROC_glCreateFramebuffers)LoadMethod("_glCreateFramebuffers");
	this->CreateProgram = (PROC_glCreateProgram)LoadMethod("_glCreateProgram");
	this->CreateProgramPipelines = (PROC_glCreateProgramPipelines)LoadMethod("_glCreateProgramPipelines");
	this->CreateQueries = (PROC_glCreateQueries)LoadMethod("_glCreateQueries");
	this->CreateRenderbuffers = (PROC_glCreateRenderbuffers)LoadMethod("_glCreateRenderbuffers");
	this->CreateSamplers = (PROC_glCreateSamplers)LoadMethod("_glCreateSamplers");
	this->CreateShader = (PROC_glCreateShader)LoadMethod("_glCreateShader");
	this->CreateShaderProgramv = (PROC_glCreateShaderProgramv)LoadMethod("_glCreateShaderProgramv");
	this->CreateTextures = (PROC_glCreateTextures)LoadMethod("_glCreateTextures");
	this->CreateTransformFeedbacks = (PROC_glCreateTransformFeedbacks)LoadMethod("_glCreateTransformFeedbacks");
	this->CreateVertexArrays = (PROC_glCreateVertexArrays)LoadMethod("_glCreateVertexArrays");
	this->CullFace = (PROC_glCullFace)LoadMethod("_glCullFace");
	this->DebugMessageCallback = (PROC_glDebugMessageCallback)LoadMethod("_glDebugMessageCallback");
	this->DebugMessageControl = (PROC_glDebugMessageControl)LoadMethod("_glDebugMessageControl");
	this->DebugMessageInsert = (PROC_glDebugMessageInsert)LoadMethod("_glDebugMessageInsert");
	this->DeleteBuffers = (PROC_glDeleteBuffers)LoadMethod("_glDeleteBuffers");
	this->DeleteFramebuffers = (PROC_glDeleteFramebuffers)LoadMethod("_glDeleteFramebuffers");
	this->DeleteProgram = (PROC_glDeleteProgram)LoadMethod("_glDeleteProgram");
	this->DeleteProgramPipelines = (PROC_glDeleteProgramPipelines)LoadMethod("_glDeleteProgramPipelines");
	this->DeleteQueries = (PROC_glDeleteQueries)LoadMethod("_glDeleteQueries");
	this->DeleteRenderbuffers = (PROC_glDeleteRenderbuffers)LoadMethod("_glDeleteRenderbuffers");
	this->DeleteSamplers = (PROC_glDeleteSamplers)LoadMethod("_glDeleteSamplers");
	this->DeleteShader = (PROC_glDeleteShader)LoadMethod("_glDeleteShader");
	this->DeleteSync = (PROC_glDeleteSync)LoadMethod("_glDeleteSync");
	this->DeleteTextures = (PROC_glDeleteTextures)LoadMethod("_glDeleteTextures");
	this->DeleteTransformFeedbacks = (PROC_glDeleteTransformFeedbacks)LoadMethod("_glDeleteTransformFeedbacks");
	this->DeleteVertexArrays = (PROC_glDeleteVertexArrays)LoadMethod("_glDeleteVertexArrays");
	this->DepthFunc = (PROC_glDepthFunc)LoadMethod("_glDepthFunc");
	this->DepthMask = (PROC_glDepthMask)LoadMethod("_glDepthMask");
	this->DepthRange = (PROC_glDepthRange)LoadMethod("_glDepthRange");
	this->DepthRangeArrayv = (PROC_glDepthRangeArrayv)LoadMethod("_glDepthRangeArrayv");
	this->DepthRangeIndexed = (PROC_glDepthRangeIndexed)LoadMethod("_glDepthRangeIndexed");
	this->DepthRangef = (PROC_glDepthRangef)LoadMethod("_glDepthRangef");
	this->DetachShader = (PROC_glDetachShader)LoadMethod("_glDetachShader");
	this->Disable = (PROC_glDisable)LoadMethod("_glDisable");
	this->DisableVertexArrayAttrib = (PROC_glDisableVertexArrayAttrib)LoadMethod("_glDisableVertexArrayAttrib");
	this->DisableVertexAttribArray = (PROC_glDisableVertexAttribArray)LoadMethod("_glDisableVertexAttribArray");
	this->Disablei = (PROC_glDisablei)LoadMethod("_glDisablei");
	this->DispatchCompute = (PROC_glDispatchCompute)LoadMethod("_glDispatchCompute");
	this->DispatchComputeIndirect = (PROC_glDispatchComputeIndirect)LoadMethod("_glDispatchComputeIndirect");
	this->DrawArrays = (PROC_glDrawArrays)LoadMethod("_glDrawArrays");
	this->DrawArraysIndirect = (PROC_glDrawArraysIndirect)LoadMethod("_glDrawArraysIndirect");
	this->DrawArraysInstanced = (PROC_glDrawArraysInstanced)LoadMethod("_glDrawArraysInstanced");
	this->DrawArraysInstancedBaseInstance = (PROC_glDrawArraysInstancedBaseInstance)LoadMethod("_glDrawArraysInstancedBaseInstance");
	this->DrawBuffer = (PROC_glDrawBuffer)LoadMethod("_glDrawBuffer");
	this->DrawBuffers = (PROC_glDrawBuffers)LoadMethod("_glDrawBuffers");
	this->DrawElements = (PROC_glDrawElements)LoadMethod("_glDrawElements");
	this->DrawElementsBaseVertex = (PROC_glDrawElementsBaseVertex)LoadMethod("_glDrawElementsBaseVertex");
	this->DrawElementsIndirect = (PROC_glDrawElementsIndirect)LoadMethod("_glDrawElementsIndirect");
	this->DrawElementsInstanced = (PROC_glDrawElementsInstanced)LoadMethod("_glDrawElementsInstanced");
	this->DrawElementsInstancedBaseInstance = (PROC_glDrawElementsInstancedBaseInstance)LoadMethod("_glDrawElementsInstancedBaseInstance");
	this->DrawElementsInstancedBaseVertex = (PROC_glDrawElementsInstancedBaseVertex)LoadMethod("_glDrawElementsInstancedBaseVertex");
	this->DrawElementsInstancedBaseVertexBaseInstance = (PROC_glDrawElementsInstancedBaseVertexBaseInstance)LoadMethod("_glDrawElementsInstancedBaseVertexBaseInstance");
	this->DrawRangeElements = (PROC_glDrawRangeElements)LoadMethod("_glDrawRangeElements");
	this->DrawRangeElementsBaseVertex = (PROC_glDrawRangeElementsBaseVertex)LoadMethod("_glDrawRangeElementsBaseVertex");
	this->DrawTransformFeedback = (PROC_glDrawTransformFeedback)LoadMethod("_glDrawTransformFeedback");
	this->DrawTransformFeedbackInstanced = (PROC_glDrawTransformFeedbackInstanced)LoadMethod("_glDrawTransformFeedbackInstanced");
	this->DrawTransformFeedbackStream = (PROC_glDrawTransformFeedbackStream)LoadMethod("_glDrawTransformFeedbackStream");
	this->DrawTransformFeedbackStreamInstanced = (PROC_glDrawTransformFeedbackStreamInstanced)LoadMethod("_glDrawTransformFeedbackStreamInstanced");
	this->Enable = (PROC_glEnable)LoadMethod("_glEnable");
	this->EnableVertexArrayAttrib = (PROC_glEnableVertexArrayAttrib)LoadMethod("_glEnableVertexArrayAttrib");
	this->EnableVertexAttribArray = (PROC_glEnableVertexAttribArray)LoadMethod("_glEnableVertexAttribArray");
	this->Enablei = (PROC_glEnablei)LoadMethod("_glEnablei");
	this->EndConditionalRender = (PROC_glEndConditionalRender)LoadMethod("_glEndConditionalRender");
	this->EndQuery = (PROC_glEndQuery)LoadMethod("_glEndQuery");
	this->EndQueryIndexed = (PROC_glEndQueryIndexed)LoadMethod("_glEndQueryIndexed");
	this->EndTransformFeedback = (PROC_glEndTransformFeedback)LoadMethod("_glEndTransformFeedback");
	this->FenceSync = (PROC_glFenceSync)LoadMethod("_glFenceSync");
	this->Finish = (PROC_glFinish)LoadMethod("_glFinish");
	this->Flush = (PROC_glFlush)LoadMethod("_glFlush");
	this->FlushMappedBufferRange = (PROC_glFlushMappedBufferRange)LoadMethod("_glFlushMappedBufferRange");
	this->FlushMappedNamedBufferRange = (PROC_glFlushMappedNamedBufferRange)LoadMethod("_glFlushMappedNamedBufferRange");
	this->FramebufferParameteri = (PROC_glFramebufferParameteri)LoadMethod("_glFramebufferParameteri");
	this->FramebufferRenderbuffer = (PROC_glFramebufferRenderbuffer)LoadMethod("_glFramebufferRenderbuffer");
	this->FramebufferTexture = (PROC_glFramebufferTexture)LoadMethod("_glFramebufferTexture");
	this->FramebufferTexture1D = (PROC_glFramebufferTexture1D)LoadMethod("_glFramebufferTexture1D");
	this->FramebufferTexture2D = (PROC_glFramebufferTexture2D)LoadMethod("_glFramebufferTexture2D");
	this->FramebufferTexture3D = (PROC_glFramebufferTexture3D)LoadMethod("_glFramebufferTexture3D");
	this->FramebufferTextureLayer = (PROC_glFramebufferTextureLayer)LoadMethod("_glFramebufferTextureLayer");
	this->FrontFace = (PROC_glFrontFace)LoadMethod("_glFrontFace");
	this->GenBuffers = (PROC_glGenBuffers)LoadMethod("_glGenBuffers");
	this->GenFramebuffers = (PROC_glGenFramebuffers)LoadMethod("_glGenFramebuffers");
	this->GenProgramPipelines = (PROC_glGenProgramPipelines)LoadMethod("_glGenProgramPipelines");
	this->GenQueries = (PROC_glGenQueries)LoadMethod("_glGenQueries");
	this->GenRenderbuffers = (PROC_glGenRenderbuffers)LoadMethod("_glGenRenderbuffers");
	this->GenSamplers = (PROC_glGenSamplers)LoadMethod("_glGenSamplers");
	this->GenTextures = (PROC_glGenTextures)LoadMethod("_glGenTextures");
	this->GenTransformFeedbacks = (PROC_glGenTransformFeedbacks)LoadMethod("_glGenTransformFeedbacks");
	this->GenVertexArrays = (PROC_glGenVertexArrays)LoadMethod("_glGenVertexArrays");
	this->GenerateMipmap = (PROC_glGenerateMipmap)LoadMethod("_glGenerateMipmap");
	this->GenerateTextureMipmap = (PROC_glGenerateTextureMipmap)LoadMethod("_glGenerateTextureMipmap");
	this->GetActiveAtomicCounterBufferiv = (PROC_glGetActiveAtomicCounterBufferiv)LoadMethod("_glGetActiveAtomicCounterBufferiv");
	this->GetActiveAttrib = (PROC_glGetActiveAttrib)LoadMethod("_glGetActiveAttrib");
	this->GetActiveSubroutineName = (PROC_glGetActiveSubroutineName)LoadMethod("_glGetActiveSubroutineName");
	this->GetActiveSubroutineUniformName = (PROC_glGetActiveSubroutineUniformName)LoadMethod("_glGetActiveSubroutineUniformName");
	this->GetActiveSubroutineUniformiv = (PROC_glGetActiveSubroutineUniformiv)LoadMethod("_glGetActiveSubroutineUniformiv");
	this->GetActiveUniform = (PROC_glGetActiveUniform)LoadMethod("_glGetActiveUniform");
	this->GetActiveUniformBlockName = (PROC_glGetActiveUniformBlockName)LoadMethod("_glGetActiveUniformBlockName");
	this->GetActiveUniformBlockiv = (PROC_glGetActiveUniformBlockiv)LoadMethod("_glGetActiveUniformBlockiv");
	this->GetActiveUniformName = (PROC_glGetActiveUniformName)LoadMethod("_glGetActiveUniformName");
	this->GetActiveUniformsiv = (PROC_glGetActiveUniformsiv)LoadMethod("_glGetActiveUniformsiv");
	this->GetAttachedShaders = (PROC_glGetAttachedShaders)LoadMethod("_glGetAttachedShaders");
	this->GetAttribLocation = (PROC_glGetAttribLocation)LoadMethod("_glGetAttribLocation");
	this->GetBooleani_v = (PROC_glGetBooleani_v)LoadMethod("_glGetBooleani_v");
	this->GetBooleanv = (PROC_glGetBooleanv)LoadMethod("_glGetBooleanv");
	this->GetBufferParameteri64v = (PROC_glGetBufferParameteri64v)LoadMethod("_glGetBufferParameteri64v");
	this->GetBufferParameteriv = (PROC_glGetBufferParameteriv)LoadMethod("_glGetBufferParameteriv");
	this->GetBufferPointerv = (PROC_glGetBufferPointerv)LoadMethod("_glGetBufferPointerv");
	this->GetBufferSubData = (PROC_glGetBufferSubData)LoadMethod("_glGetBufferSubData");
	this->GetCompressedTexImage = (PROC_glGetCompressedTexImage)LoadMethod("_glGetCompressedTexImage");
	this->GetCompressedTextureImage = (PROC_glGetCompressedTextureImage)LoadMethod("_glGetCompressedTextureImage");
	this->GetCompressedTextureSubImage = (PROC_glGetCompressedTextureSubImage)LoadMethod("_glGetCompressedTextureSubImage");
	this->GetDebugMessageLog = (PROC_glGetDebugMessageLog)LoadMethod("_glGetDebugMessageLog");
	this->GetDoublei_v = (PROC_glGetDoublei_v)LoadMethod("_glGetDoublei_v");
	this->GetDoublev = (PROC_glGetDoublev)LoadMethod("_glGetDoublev");
	this->GetError = (PROC_glGetError)LoadMethod("_glGetError");
	this->GetFloati_v = (PROC_glGetFloati_v)LoadMethod("_glGetFloati_v");
	this->GetFloatv = (PROC_glGetFloatv)LoadMethod("_glGetFloatv");
	this->GetFragDataIndex = (PROC_glGetFragDataIndex)LoadMethod("_glGetFragDataIndex");
	this->GetFragDataLocation = (PROC_glGetFragDataLocation)LoadMethod("_glGetFragDataLocation");
	this->GetFramebufferAttachmentParameteriv = (PROC_glGetFramebufferAttachmentParameteriv)LoadMethod("_glGetFramebufferAttachmentParameteriv");
	this->GetFramebufferParameteriv = (PROC_glGetFramebufferParameteriv)LoadMethod("_glGetFramebufferParameteriv");
	this->GetGraphicsResetStatus = (PROC_glGetGraphicsResetStatus)LoadMethod("_glGetGraphicsResetStatus");
	this->GetInteger64i_v = (PROC_glGetInteger64i_v)LoadMethod("_glGetInteger64i_v");
	this->GetInteger64v = (PROC_glGetInteger64v)LoadMethod("_glGetInteger64v");
	this->GetIntegeri_v = (PROC_glGetIntegeri_v)LoadMethod("_glGetIntegeri_v");
	this->GetIntegerv = (PROC_glGetIntegerv)LoadMethod("_glGetIntegerv");
	this->GetInternalformati64v = (PROC_glGetInternalformati64v)LoadMethod("_glGetInternalformati64v");
	this->GetInternalformativ = (PROC_glGetInternalformativ)LoadMethod("_glGetInternalformativ");
	this->GetMultisamplefv = (PROC_glGetMultisamplefv)LoadMethod("_glGetMultisamplefv");
	this->GetNamedBufferParameteri64v = (PROC_glGetNamedBufferParameteri64v)LoadMethod("_glGetNamedBufferParameteri64v");
	this->GetNamedBufferParameteriv = (PROC_glGetNamedBufferParameteriv)LoadMethod("_glGetNamedBufferParameteriv");
	this->GetNamedBufferPointerv = (PROC_glGetNamedBufferPointerv)LoadMethod("_glGetNamedBufferPointerv");
	this->GetNamedBufferSubData = (PROC_glGetNamedBufferSubData)LoadMethod("_glGetNamedBufferSubData");
	this->GetNamedFramebufferAttachmentParameteriv = (PROC_glGetNamedFramebufferAttachmentParameteriv)LoadMethod("_glGetNamedFramebufferAttachmentParameteriv");
	this->GetNamedFramebufferParameteriv = (PROC_glGetNamedFramebufferParameteriv)LoadMethod("_glGetNamedFramebufferParameteriv");
	this->GetNamedRenderbufferParameteriv = (PROC_glGetNamedRenderbufferParameteriv)LoadMethod("_glGetNamedRenderbufferParameteriv");
	this->GetObjectLabel = (PROC_glGetObjectLabel)LoadMethod("_glGetObjectLabel");
	this->GetObjectPtrLabel = (PROC_glGetObjectPtrLabel)LoadMethod("_glGetObjectPtrLabel");
	this->GetPointerv = (PROC_glGetPointerv)LoadMethod("_glGetPointerv");
	this->GetProgramBinary = (PROC_glGetProgramBinary)LoadMethod("_glGetProgramBinary");
	this->GetProgramInfoLog = (PROC_glGetProgramInfoLog)LoadMethod("_glGetProgramInfoLog");
	this->GetProgramInterfaceiv = (PROC_glGetProgramInterfaceiv)LoadMethod("_glGetProgramInterfaceiv");
	this->GetProgramPipelineInfoLog = (PROC_glGetProgramPipelineInfoLog)LoadMethod("_glGetProgramPipelineInfoLog");
	this->GetProgramPipelineiv = (PROC_glGetProgramPipelineiv)LoadMethod("_glGetProgramPipelineiv");
	this->GetProgramResourceIndex = (PROC_glGetProgramResourceIndex)LoadMethod("_glGetProgramResourceIndex");
	this->GetProgramResourceLocation = (PROC_glGetProgramResourceLocation)LoadMethod("_glGetProgramResourceLocation");
	this->GetProgramResourceLocationIndex = (PROC_glGetProgramResourceLocationIndex)LoadMethod("_glGetProgramResourceLocationIndex");
	this->GetProgramResourceName = (PROC_glGetProgramResourceName)LoadMethod("_glGetProgramResourceName");
	this->GetProgramResourceiv = (PROC_glGetProgramResourceiv)LoadMethod("_glGetProgramResourceiv");
	this->GetProgramStageiv = (PROC_glGetProgramStageiv)LoadMethod("_glGetProgramStageiv");
	this->GetProgramiv = (PROC_glGetProgramiv)LoadMethod("_glGetProgramiv");
	this->GetQueryBufferObjecti64v = (PROC_glGetQueryBufferObjecti64v)LoadMethod("_glGetQueryBufferObjecti64v");
	this->GetQueryBufferObjectiv = (PROC_glGetQueryBufferObjectiv)LoadMethod("_glGetQueryBufferObjectiv");
	this->GetQueryBufferObjectui64v = (PROC_glGetQueryBufferObjectui64v)LoadMethod("_glGetQueryBufferObjectui64v");
	this->GetQueryBufferObjectuiv = (PROC_glGetQueryBufferObjectuiv)LoadMethod("_glGetQueryBufferObjectuiv");
	this->GetQueryIndexediv = (PROC_glGetQueryIndexediv)LoadMethod("_glGetQueryIndexediv");
	this->GetQueryObjecti64v = (PROC_glGetQueryObjecti64v)LoadMethod("_glGetQueryObjecti64v");
	this->GetQueryObjectiv = (PROC_glGetQueryObjectiv)LoadMethod("_glGetQueryObjectiv");
	this->GetQueryObjectui64v = (PROC_glGetQueryObjectui64v)LoadMethod("_glGetQueryObjectui64v");
	this->GetQueryObjectuiv = (PROC_glGetQueryObjectuiv)LoadMethod("_glGetQueryObjectuiv");
	this->GetQueryiv = (PROC_glGetQueryiv)LoadMethod("_glGetQueryiv");
	this->GetRenderbufferParameteriv = (PROC_glGetRenderbufferParameteriv)LoadMethod("_glGetRenderbufferParameteriv");
	this->GetSamplerParameterIiv = (PROC_glGetSamplerParameterIiv)LoadMethod("_glGetSamplerParameterIiv");
	this->GetSamplerParameterIuiv = (PROC_glGetSamplerParameterIuiv)LoadMethod("_glGetSamplerParameterIuiv");
	this->GetSamplerParameterfv = (PROC_glGetSamplerParameterfv)LoadMethod("_glGetSamplerParameterfv");
	this->GetSamplerParameteriv = (PROC_glGetSamplerParameteriv)LoadMethod("_glGetSamplerParameteriv");
	this->GetShaderInfoLog = (PROC_glGetShaderInfoLog)LoadMethod("_glGetShaderInfoLog");
	this->GetShaderPrecisionFormat = (PROC_glGetShaderPrecisionFormat)LoadMethod("_glGetShaderPrecisionFormat");
	this->GetShaderSource = (PROC_glGetShaderSource)LoadMethod("_glGetShaderSource");
	this->GetShaderiv = (PROC_glGetShaderiv)LoadMethod("_glGetShaderiv");
	this->GetString = (PROC_glGetString)LoadMethod("_glGetString");
	this->GetStringi = (PROC_glGetStringi)LoadMethod("_glGetStringi");
	this->GetSubroutineIndex = (PROC_glGetSubroutineIndex)LoadMethod("_glGetSubroutineIndex");
	this->GetSubroutineUniformLocation = (PROC_glGetSubroutineUniformLocation)LoadMethod("_glGetSubroutineUniformLocation");
	this->GetSynciv = (PROC_glGetSynciv)LoadMethod("_glGetSynciv");
	this->GetTexImage = (PROC_glGetTexImage)LoadMethod("_glGetTexImage");
	this->GetTexLevelParameterfv = (PROC_glGetTexLevelParameterfv)LoadMethod("_glGetTexLevelParameterfv");
	this->GetTexLevelParameteriv = (PROC_glGetTexLevelParameteriv)LoadMethod("_glGetTexLevelParameteriv");
	this->GetTexParameterIiv = (PROC_glGetTexParameterIiv)LoadMethod("_glGetTexParameterIiv");
	this->GetTexParameterIuiv = (PROC_glGetTexParameterIuiv)LoadMethod("_glGetTexParameterIuiv");
	this->GetTexParameterfv = (PROC_glGetTexParameterfv)LoadMethod("_glGetTexParameterfv");
	this->GetTexParameteriv = (PROC_glGetTexParameteriv)LoadMethod("_glGetTexParameteriv");
	this->GetTextureImage = (PROC_glGetTextureImage)LoadMethod("_glGetTextureImage");
	this->GetTextureLevelParameterfv = (PROC_glGetTextureLevelParameterfv)LoadMethod("_glGetTextureLevelParameterfv");
	this->GetTextureLevelParameteriv = (PROC_glGetTextureLevelParameteriv)LoadMethod("_glGetTextureLevelParameteriv");
	this->GetTextureParameterIiv = (PROC_glGetTextureParameterIiv)LoadMethod("_glGetTextureParameterIiv");
	this->GetTextureParameterIuiv = (PROC_glGetTextureParameterIuiv)LoadMethod("_glGetTextureParameterIuiv");
	this->GetTextureParameterfv = (PROC_glGetTextureParameterfv)LoadMethod("_glGetTextureParameterfv");
	this->GetTextureParameteriv = (PROC_glGetTextureParameteriv)LoadMethod("_glGetTextureParameteriv");
	this->GetTextureSubImage = (PROC_glGetTextureSubImage)LoadMethod("_glGetTextureSubImage");
	this->GetTransformFeedbackVarying = (PROC_glGetTransformFeedbackVarying)LoadMethod("_glGetTransformFeedbackVarying");
	this->GetTransformFeedbacki64_v = (PROC_glGetTransformFeedbacki64_v)LoadMethod("_glGetTransformFeedbacki64_v");
	this->GetTransformFeedbacki_v = (PROC_glGetTransformFeedbacki_v)LoadMethod("_glGetTransformFeedbacki_v");
	this->GetTransformFeedbackiv = (PROC_glGetTransformFeedbackiv)LoadMethod("_glGetTransformFeedbackiv");
	this->GetUniformBlockIndex = (PROC_glGetUniformBlockIndex)LoadMethod("_glGetUniformBlockIndex");
	this->GetUniformIndices = (PROC_glGetUniformIndices)LoadMethod("_glGetUniformIndices");
	this->GetUniformLocation = (PROC_glGetUniformLocation)LoadMethod("_glGetUniformLocation");
	this->GetUniformSubroutineuiv = (PROC_glGetUniformSubroutineuiv)LoadMethod("_glGetUniformSubroutineuiv");
	this->GetUniformdv = (PROC_glGetUniformdv)LoadMethod("_glGetUniformdv");
	this->GetUniformfv = (PROC_glGetUniformfv)LoadMethod("_glGetUniformfv");
	this->GetUniformiv = (PROC_glGetUniformiv)LoadMethod("_glGetUniformiv");
	this->GetUniformuiv = (PROC_glGetUniformuiv)LoadMethod("_glGetUniformuiv");
	this->GetVertexArrayIndexed64iv = (PROC_glGetVertexArrayIndexed64iv)LoadMethod("_glGetVertexArrayIndexed64iv");
	this->GetVertexArrayIndexediv = (PROC_glGetVertexArrayIndexediv)LoadMethod("_glGetVertexArrayIndexediv");
	this->GetVertexArrayiv = (PROC_glGetVertexArrayiv)LoadMethod("_glGetVertexArrayiv");
	this->GetVertexAttribIiv = (PROC_glGetVertexAttribIiv)LoadMethod("_glGetVertexAttribIiv");
	this->GetVertexAttribIuiv = (PROC_glGetVertexAttribIuiv)LoadMethod("_glGetVertexAttribIuiv");
	this->GetVertexAttribLdv = (PROC_glGetVertexAttribLdv)LoadMethod("_glGetVertexAttribLdv");
	this->GetVertexAttribPointerv = (PROC_glGetVertexAttribPointerv)LoadMethod("_glGetVertexAttribPointerv");
	this->GetVertexAttribdv = (PROC_glGetVertexAttribdv)LoadMethod("_glGetVertexAttribdv");
	this->GetVertexAttribfv = (PROC_glGetVertexAttribfv)LoadMethod("_glGetVertexAttribfv");
	this->GetVertexAttribiv = (PROC_glGetVertexAttribiv)LoadMethod("_glGetVertexAttribiv");
	this->GetnCompressedTexImage = (PROC_glGetnCompressedTexImage)LoadMethod("_glGetnCompressedTexImage");
	this->GetnTexImage = (PROC_glGetnTexImage)LoadMethod("_glGetnTexImage");
	this->GetnUniformdv = (PROC_glGetnUniformdv)LoadMethod("_glGetnUniformdv");
	this->GetnUniformfv = (PROC_glGetnUniformfv)LoadMethod("_glGetnUniformfv");
	this->GetnUniformiv = (PROC_glGetnUniformiv)LoadMethod("_glGetnUniformiv");
	this->GetnUniformuiv = (PROC_glGetnUniformuiv)LoadMethod("_glGetnUniformuiv");
	this->Hint = (PROC_glHint)LoadMethod("_glHint");
	this->InvalidateBufferData = (PROC_glInvalidateBufferData)LoadMethod("_glInvalidateBufferData");
	this->InvalidateBufferSubData = (PROC_glInvalidateBufferSubData)LoadMethod("_glInvalidateBufferSubData");
	this->InvalidateFramebuffer = (PROC_glInvalidateFramebuffer)LoadMethod("_glInvalidateFramebuffer");
	this->InvalidateNamedFramebufferData = (PROC_glInvalidateNamedFramebufferData)LoadMethod("_glInvalidateNamedFramebufferData");
	this->InvalidateNamedFramebufferSubData = (PROC_glInvalidateNamedFramebufferSubData)LoadMethod("_glInvalidateNamedFramebufferSubData");
	this->InvalidateSubFramebuffer = (PROC_glInvalidateSubFramebuffer)LoadMethod("_glInvalidateSubFramebuffer");
	this->InvalidateTexImage = (PROC_glInvalidateTexImage)LoadMethod("_glInvalidateTexImage");
	this->InvalidateTexSubImage = (PROC_glInvalidateTexSubImage)LoadMethod("_glInvalidateTexSubImage");
	this->IsBuffer = (PROC_glIsBuffer)LoadMethod("_glIsBuffer");
	this->IsEnabled = (PROC_glIsEnabled)LoadMethod("_glIsEnabled");
	this->IsEnabledi = (PROC_glIsEnabledi)LoadMethod("_glIsEnabledi");
	this->IsFramebuffer = (PROC_glIsFramebuffer)LoadMethod("_glIsFramebuffer");
	this->IsProgram = (PROC_glIsProgram)LoadMethod("_glIsProgram");
	this->IsProgramPipeline = (PROC_glIsProgramPipeline)LoadMethod("_glIsProgramPipeline");
	this->IsQuery = (PROC_glIsQuery)LoadMethod("_glIsQuery");
	this->IsRenderbuffer = (PROC_glIsRenderbuffer)LoadMethod("_glIsRenderbuffer");
	this->IsSampler = (PROC_glIsSampler)LoadMethod("_glIsSampler");
	this->IsShader = (PROC_glIsShader)LoadMethod("_glIsShader");
	this->IsSync = (PROC_glIsSync)LoadMethod("_glIsSync");
	this->IsTexture = (PROC_glIsTexture)LoadMethod("_glIsTexture");
	this->IsTransformFeedback = (PROC_glIsTransformFeedback)LoadMethod("_glIsTransformFeedback");
	this->IsVertexArray = (PROC_glIsVertexArray)LoadMethod("_glIsVertexArray");
	this->LineWidth = (PROC_glLineWidth)LoadMethod("_glLineWidth");
	this->LinkProgram = (PROC_glLinkProgram)LoadMethod("_glLinkProgram");
	this->LogicOp = (PROC_glLogicOp)LoadMethod("_glLogicOp");
	this->MapBuffer = (PROC_glMapBuffer)LoadMethod("_glMapBuffer");
	this->MapBufferRange = (PROC_glMapBufferRange)LoadMethod("_glMapBufferRange");
	this->MapNamedBuffer = (PROC_glMapNamedBuffer)LoadMethod("_glMapNamedBuffer");
	this->MapNamedBufferRange = (PROC_glMapNamedBufferRange)LoadMethod("_glMapNamedBufferRange");
	this->MemoryBarrier = (PROC_glMemoryBarrier)LoadMethod("_glMemoryBarrier");
	this->MemoryBarrierByRegion = (PROC_glMemoryBarrierByRegion)LoadMethod("_glMemoryBarrierByRegion");
	this->MinSampleShading = (PROC_glMinSampleShading)LoadMethod("_glMinSampleShading");
	this->MultiDrawArrays = (PROC_glMultiDrawArrays)LoadMethod("_glMultiDrawArrays");
	this->MultiDrawArraysIndirect = (PROC_glMultiDrawArraysIndirect)LoadMethod("_glMultiDrawArraysIndirect");
	this->MultiDrawElements = (PROC_glMultiDrawElements)LoadMethod("_glMultiDrawElements");
	this->MultiDrawElementsBaseVertex = (PROC_glMultiDrawElementsBaseVertex)LoadMethod("_glMultiDrawElementsBaseVertex");
	this->MultiDrawElementsIndirect = (PROC_glMultiDrawElementsIndirect)LoadMethod("_glMultiDrawElementsIndirect");
	this->NamedBufferData = (PROC_glNamedBufferData)LoadMethod("_glNamedBufferData");
	this->NamedBufferStorage = (PROC_glNamedBufferStorage)LoadMethod("_glNamedBufferStorage");
	this->NamedBufferSubData = (PROC_glNamedBufferSubData)LoadMethod("_glNamedBufferSubData");
	this->NamedFramebufferDrawBuffer = (PROC_glNamedFramebufferDrawBuffer)LoadMethod("_glNamedFramebufferDrawBuffer");
	this->NamedFramebufferDrawBuffers = (PROC_glNamedFramebufferDrawBuffers)LoadMethod("_glNamedFramebufferDrawBuffers");
	this->NamedFramebufferParameteri = (PROC_glNamedFramebufferParameteri)LoadMethod("_glNamedFramebufferParameteri");
	this->NamedFramebufferReadBuffer = (PROC_glNamedFramebufferReadBuffer)LoadMethod("_glNamedFramebufferReadBuffer");
	this->NamedFramebufferRenderbuffer = (PROC_glNamedFramebufferRenderbuffer)LoadMethod("_glNamedFramebufferRenderbuffer");
	this->NamedFramebufferTexture = (PROC_glNamedFramebufferTexture)LoadMethod("_glNamedFramebufferTexture");
	this->NamedFramebufferTextureLayer = (PROC_glNamedFramebufferTextureLayer)LoadMethod("_glNamedFramebufferTextureLayer");
	this->NamedRenderbufferStorage = (PROC_glNamedRenderbufferStorage)LoadMethod("_glNamedRenderbufferStorage");
	this->NamedRenderbufferStorageMultisample = (PROC_glNamedRenderbufferStorageMultisample)LoadMethod("_glNamedRenderbufferStorageMultisample");
	this->ObjectLabel = (PROC_glObjectLabel)LoadMethod("_glObjectLabel");
	this->ObjectPtrLabel = (PROC_glObjectPtrLabel)LoadMethod("_glObjectPtrLabel");
	this->PatchParameterfv = (PROC_glPatchParameterfv)LoadMethod("_glPatchParameterfv");
	this->PatchParameteri = (PROC_glPatchParameteri)LoadMethod("_glPatchParameteri");
	this->PauseTransformFeedback = (PROC_glPauseTransformFeedback)LoadMethod("_glPauseTransformFeedback");
	this->PixelStoref = (PROC_glPixelStoref)LoadMethod("_glPixelStoref");
	this->PixelStorei = (PROC_glPixelStorei)LoadMethod("_glPixelStorei");
	this->PointParameterf = (PROC_glPointParameterf)LoadMethod("_glPointParameterf");
	this->PointParameterfv = (PROC_glPointParameterfv)LoadMethod("_glPointParameterfv");
	this->PointParameteri = (PROC_glPointParameteri)LoadMethod("_glPointParameteri");
	this->PointParameteriv = (PROC_glPointParameteriv)LoadMethod("_glPointParameteriv");
	this->PointSize = (PROC_glPointSize)LoadMethod("_glPointSize");
	this->PolygonMode = (PROC_glPolygonMode)LoadMethod("_glPolygonMode");
	this->PolygonOffset = (PROC_glPolygonOffset)LoadMethod("_glPolygonOffset");
	this->PopDebugGroup = (PROC_glPopDebugGroup)LoadMethod("_glPopDebugGroup");
	this->PrimitiveRestartIndex = (PROC_glPrimitiveRestartIndex)LoadMethod("_glPrimitiveRestartIndex");
	this->ProgramBinary = (PROC_glProgramBinary)LoadMethod("_glProgramBinary");
	this->ProgramParameteri = (PROC_glProgramParameteri)LoadMethod("_glProgramParameteri");
	this->ProgramUniform1d = (PROC_glProgramUniform1d)LoadMethod("_glProgramUniform1d");
	this->ProgramUniform1dv = (PROC_glProgramUniform1dv)LoadMethod("_glProgramUniform1dv");
	this->ProgramUniform1f = (PROC_glProgramUniform1f)LoadMethod("_glProgramUniform1f");
	this->ProgramUniform1fv = (PROC_glProgramUniform1fv)LoadMethod("_glProgramUniform1fv");
	this->ProgramUniform1i = (PROC_glProgramUniform1i)LoadMethod("_glProgramUniform1i");
	this->ProgramUniform1iv = (PROC_glProgramUniform1iv)LoadMethod("_glProgramUniform1iv");
	this->ProgramUniform1ui = (PROC_glProgramUniform1ui)LoadMethod("_glProgramUniform1ui");
	this->ProgramUniform1uiv = (PROC_glProgramUniform1uiv)LoadMethod("_glProgramUniform1uiv");
	this->ProgramUniform2d = (PROC_glProgramUniform2d)LoadMethod("_glProgramUniform2d");
	this->ProgramUniform2dv = (PROC_glProgramUniform2dv)LoadMethod("_glProgramUniform2dv");
	this->ProgramUniform2f = (PROC_glProgramUniform2f)LoadMethod("_glProgramUniform2f");
	this->ProgramUniform2fv = (PROC_glProgramUniform2fv)LoadMethod("_glProgramUniform2fv");
	this->ProgramUniform2i = (PROC_glProgramUniform2i)LoadMethod("_glProgramUniform2i");
	this->ProgramUniform2iv = (PROC_glProgramUniform2iv)LoadMethod("_glProgramUniform2iv");
	this->ProgramUniform2ui = (PROC_glProgramUniform2ui)LoadMethod("_glProgramUniform2ui");
	this->ProgramUniform2uiv = (PROC_glProgramUniform2uiv)LoadMethod("_glProgramUniform2uiv");
	this->ProgramUniform3d = (PROC_glProgramUniform3d)LoadMethod("_glProgramUniform3d");
	this->ProgramUniform3dv = (PROC_glProgramUniform3dv)LoadMethod("_glProgramUniform3dv");
	this->ProgramUniform3f = (PROC_glProgramUniform3f)LoadMethod("_glProgramUniform3f");
	this->ProgramUniform3fv = (PROC_glProgramUniform3fv)LoadMethod("_glProgramUniform3fv");
	this->ProgramUniform3i = (PROC_glProgramUniform3i)LoadMethod("_glProgramUniform3i");
	this->ProgramUniform3iv = (PROC_glProgramUniform3iv)LoadMethod("_glProgramUniform3iv");
	this->ProgramUniform3ui = (PROC_glProgramUniform3ui)LoadMethod("_glProgramUniform3ui");
	this->ProgramUniform3uiv = (PROC_glProgramUniform3uiv)LoadMethod("_glProgramUniform3uiv");
	this->ProgramUniform4d = (PROC_glProgramUniform4d)LoadMethod("_glProgramUniform4d");
	this->ProgramUniform4dv = (PROC_glProgramUniform4dv)LoadMethod("_glProgramUniform4dv");
	this->ProgramUniform4f = (PROC_glProgramUniform4f)LoadMethod("_glProgramUniform4f");
	this->ProgramUniform4fv = (PROC_glProgramUniform4fv)LoadMethod("_glProgramUniform4fv");
	this->ProgramUniform4i = (PROC_glProgramUniform4i)LoadMethod("_glProgramUniform4i");
	this->ProgramUniform4iv = (PROC_glProgramUniform4iv)LoadMethod("_glProgramUniform4iv");
	this->ProgramUniform4ui = (PROC_glProgramUniform4ui)LoadMethod("_glProgramUniform4ui");
	this->ProgramUniform4uiv = (PROC_glProgramUniform4uiv)LoadMethod("_glProgramUniform4uiv");
	this->ProgramUniformMatrix2dv = (PROC_glProgramUniformMatrix2dv)LoadMethod("_glProgramUniformMatrix2dv");
	this->ProgramUniformMatrix2fv = (PROC_glProgramUniformMatrix2fv)LoadMethod("_glProgramUniformMatrix2fv");
	this->ProgramUniformMatrix2x3dv = (PROC_glProgramUniformMatrix2x3dv)LoadMethod("_glProgramUniformMatrix2x3dv");
	this->ProgramUniformMatrix2x3fv = (PROC_glProgramUniformMatrix2x3fv)LoadMethod("_glProgramUniformMatrix2x3fv");
	this->ProgramUniformMatrix2x4dv = (PROC_glProgramUniformMatrix2x4dv)LoadMethod("_glProgramUniformMatrix2x4dv");
	this->ProgramUniformMatrix2x4fv = (PROC_glProgramUniformMatrix2x4fv)LoadMethod("_glProgramUniformMatrix2x4fv");
	this->ProgramUniformMatrix3dv = (PROC_glProgramUniformMatrix3dv)LoadMethod("_glProgramUniformMatrix3dv");
	this->ProgramUniformMatrix3fv = (PROC_glProgramUniformMatrix3fv)LoadMethod("_glProgramUniformMatrix3fv");
	this->ProgramUniformMatrix3x2dv = (PROC_glProgramUniformMatrix3x2dv)LoadMethod("_glProgramUniformMatrix3x2dv");
	this->ProgramUniformMatrix3x2fv = (PROC_glProgramUniformMatrix3x2fv)LoadMethod("_glProgramUniformMatrix3x2fv");
	this->ProgramUniformMatrix3x4dv = (PROC_glProgramUniformMatrix3x4dv)LoadMethod("_glProgramUniformMatrix3x4dv");
	this->ProgramUniformMatrix3x4fv = (PROC_glProgramUniformMatrix3x4fv)LoadMethod("_glProgramUniformMatrix3x4fv");
	this->ProgramUniformMatrix4dv = (PROC_glProgramUniformMatrix4dv)LoadMethod("_glProgramUniformMatrix4dv");
	this->ProgramUniformMatrix4fv = (PROC_glProgramUniformMatrix4fv)LoadMethod("_glProgramUniformMatrix4fv");
	this->ProgramUniformMatrix4x2dv = (PROC_glProgramUniformMatrix4x2dv)LoadMethod("_glProgramUniformMatrix4x2dv");
	this->ProgramUniformMatrix4x2fv = (PROC_glProgramUniformMatrix4x2fv)LoadMethod("_glProgramUniformMatrix4x2fv");
	this->ProgramUniformMatrix4x3dv = (PROC_glProgramUniformMatrix4x3dv)LoadMethod("_glProgramUniformMatrix4x3dv");
	this->ProgramUniformMatrix4x3fv = (PROC_glProgramUniformMatrix4x3fv)LoadMethod("_glProgramUniformMatrix4x3fv");
	this->ProvokingVertex = (PROC_glProvokingVertex)LoadMethod("_glProvokingVertex");
	this->PushDebugGroup = (PROC_glPushDebugGroup)LoadMethod("_glPushDebugGroup");
	this->QueryCounter = (PROC_glQueryCounter)LoadMethod("_glQueryCounter");
	this->ReadBuffer = (PROC_glReadBuffer)LoadMethod("_glReadBuffer");
	this->ReadPixels = (PROC_glReadPixels)LoadMethod("_glReadPixels");
	this->ReadnPixels = (PROC_glReadnPixels)LoadMethod("_glReadnPixels");
	this->ReleaseShaderCompiler = (PROC_glReleaseShaderCompiler)LoadMethod("_glReleaseShaderCompiler");
	this->RenderbufferStorage = (PROC_glRenderbufferStorage)LoadMethod("_glRenderbufferStorage");
	this->RenderbufferStorageMultisample = (PROC_glRenderbufferStorageMultisample)LoadMethod("_glRenderbufferStorageMultisample");
	this->ResumeTransformFeedback = (PROC_glResumeTransformFeedback)LoadMethod("_glResumeTransformFeedback");
	this->SampleCoverage = (PROC_glSampleCoverage)LoadMethod("_glSampleCoverage");
	this->SampleMaski = (PROC_glSampleMaski)LoadMethod("_glSampleMaski");
	this->SamplerParameterIiv = (PROC_glSamplerParameterIiv)LoadMethod("_glSamplerParameterIiv");
	this->SamplerParameterIuiv = (PROC_glSamplerParameterIuiv)LoadMethod("_glSamplerParameterIuiv");
	this->SamplerParameterf = (PROC_glSamplerParameterf)LoadMethod("_glSamplerParameterf");
	this->SamplerParameterfv = (PROC_glSamplerParameterfv)LoadMethod("_glSamplerParameterfv");
	this->SamplerParameteri = (PROC_glSamplerParameteri)LoadMethod("_glSamplerParameteri");
	this->SamplerParameteriv = (PROC_glSamplerParameteriv)LoadMethod("_glSamplerParameteriv");
	this->Scissor = (PROC_glScissor)LoadMethod("_glScissor");
	this->ScissorArrayv = (PROC_glScissorArrayv)LoadMethod("_glScissorArrayv");
	this->ScissorIndexed = (PROC_glScissorIndexed)LoadMethod("_glScissorIndexed");
	this->ScissorIndexedv = (PROC_glScissorIndexedv)LoadMethod("_glScissorIndexedv");
	this->ShaderBinary = (PROC_glShaderBinary)LoadMethod("_glShaderBinary");
	this->ShaderSource = (PROC_glShaderSource)LoadMethod("_glShaderSource");
	this->ShaderStorageBlockBinding = (PROC_glShaderStorageBlockBinding)LoadMethod("_glShaderStorageBlockBinding");
	this->StencilFunc = (PROC_glStencilFunc)LoadMethod("_glStencilFunc");
	this->StencilFuncSeparate = (PROC_glStencilFuncSeparate)LoadMethod("_glStencilFuncSeparate");
	this->StencilMask = (PROC_glStencilMask)LoadMethod("_glStencilMask");
	this->StencilMaskSeparate = (PROC_glStencilMaskSeparate)LoadMethod("_glStencilMaskSeparate");
	this->StencilOp = (PROC_glStencilOp)LoadMethod("_glStencilOp");
	this->StencilOpSeparate = (PROC_glStencilOpSeparate)LoadMethod("_glStencilOpSeparate");
	this->TexBuffer = (PROC_glTexBuffer)LoadMethod("_glTexBuffer");
	this->TexBufferRange = (PROC_glTexBufferRange)LoadMethod("_glTexBufferRange");
	this->TexImage1D = (PROC_glTexImage1D)LoadMethod("_glTexImage1D");
	this->TexImage2D = (PROC_glTexImage2D)LoadMethod("_glTexImage2D");
	this->TexImage2DMultisample = (PROC_glTexImage2DMultisample)LoadMethod("_glTexImage2DMultisample");
	this->TexImage3D = (PROC_glTexImage3D)LoadMethod("_glTexImage3D");
	this->TexImage3DMultisample = (PROC_glTexImage3DMultisample)LoadMethod("_glTexImage3DMultisample");
	this->TexParameterIiv = (PROC_glTexParameterIiv)LoadMethod("_glTexParameterIiv");
	this->TexParameterIuiv = (PROC_glTexParameterIuiv)LoadMethod("_glTexParameterIuiv");
	this->TexParameterf = (PROC_glTexParameterf)LoadMethod("_glTexParameterf");
	this->TexParameterfv = (PROC_glTexParameterfv)LoadMethod("_glTexParameterfv");
	this->TexParameteri = (PROC_glTexParameteri)LoadMethod("_glTexParameteri");
	this->TexParameteriv = (PROC_glTexParameteriv)LoadMethod("_glTexParameteriv");
	this->TexStorage1D = (PROC_glTexStorage1D)LoadMethod("_glTexStorage1D");
	this->TexStorage2D = (PROC_glTexStorage2D)LoadMethod("_glTexStorage2D");
	this->TexStorage2DMultisample = (PROC_glTexStorage2DMultisample)LoadMethod("_glTexStorage2DMultisample");
	this->TexStorage3D = (PROC_glTexStorage3D)LoadMethod("_glTexStorage3D");
	this->TexStorage3DMultisample = (PROC_glTexStorage3DMultisample)LoadMethod("_glTexStorage3DMultisample");
	this->TexSubImage1D = (PROC_glTexSubImage1D)LoadMethod("_glTexSubImage1D");
	this->TexSubImage2D = (PROC_glTexSubImage2D)LoadMethod("_glTexSubImage2D");
	this->TexSubImage3D = (PROC_glTexSubImage3D)LoadMethod("_glTexSubImage3D");
	this->TextureBarrier = (PROC_glTextureBarrier)LoadMethod("_glTextureBarrier");
	this->TextureBuffer = (PROC_glTextureBuffer)LoadMethod("_glTextureBuffer");
	this->TextureBufferRange = (PROC_glTextureBufferRange)LoadMethod("_glTextureBufferRange");
	this->TextureParameterIiv = (PROC_glTextureParameterIiv)LoadMethod("_glTextureParameterIiv");
	this->TextureParameterIuiv = (PROC_glTextureParameterIuiv)LoadMethod("_glTextureParameterIuiv");
	this->TextureParameterf = (PROC_glTextureParameterf)LoadMethod("_glTextureParameterf");
	this->TextureParameterfv = (PROC_glTextureParameterfv)LoadMethod("_glTextureParameterfv");
	this->TextureParameteri = (PROC_glTextureParameteri)LoadMethod("_glTextureParameteri");
	this->TextureParameteriv = (PROC_glTextureParameteriv)LoadMethod("_glTextureParameteriv");
	this->TextureStorage1D = (PROC_glTextureStorage1D)LoadMethod("_glTextureStorage1D");
	this->TextureStorage2D = (PROC_glTextureStorage2D)LoadMethod("_glTextureStorage2D");
	this->TextureStorage2DMultisample = (PROC_glTextureStorage2DMultisample)LoadMethod("_glTextureStorage2DMultisample");
	this->TextureStorage3D = (PROC_glTextureStorage3D)LoadMethod("_glTextureStorage3D");
	this->TextureStorage3DMultisample = (PROC_glTextureStorage3DMultisample)LoadMethod("_glTextureStorage3DMultisample");
	this->TextureSubImage1D = (PROC_glTextureSubImage1D)LoadMethod("_glTextureSubImage1D");
	this->TextureSubImage2D = (PROC_glTextureSubImage2D)LoadMethod("_glTextureSubImage2D");
	this->TextureSubImage3D = (PROC_glTextureSubImage3D)LoadMethod("_glTextureSubImage3D");
	this->TextureView = (PROC_glTextureView)LoadMethod("_glTextureView");
	this->TransformFeedbackBufferBase = (PROC_glTransformFeedbackBufferBase)LoadMethod("_glTransformFeedbackBufferBase");
	this->TransformFeedbackBufferRange = (PROC_glTransformFeedbackBufferRange)LoadMethod("_glTransformFeedbackBufferRange");
	this->TransformFeedbackVaryings = (PROC_glTransformFeedbackVaryings)LoadMethod("_glTransformFeedbackVaryings");
	this->Uniform1d = (PROC_glUniform1d)LoadMethod("_glUniform1d");
	this->Uniform1dv = (PROC_glUniform1dv)LoadMethod("_glUniform1dv");
	this->Uniform1f = (PROC_glUniform1f)LoadMethod("_glUniform1f");
	this->Uniform1fv = (PROC_glUniform1fv)LoadMethod("_glUniform1fv");
	this->Uniform1i = (PROC_glUniform1i)LoadMethod("_glUniform1i");
	this->Uniform1iv = (PROC_glUniform1iv)LoadMethod("_glUniform1iv");
	this->Uniform1ui = (PROC_glUniform1ui)LoadMethod("_glUniform1ui");
	this->Uniform1uiv = (PROC_glUniform1uiv)LoadMethod("_glUniform1uiv");
	this->Uniform2d = (PROC_glUniform2d)LoadMethod("_glUniform2d");
	this->Uniform2dv = (PROC_glUniform2dv)LoadMethod("_glUniform2dv");
	this->Uniform2f = (PROC_glUniform2f)LoadMethod("_glUniform2f");
	this->Uniform2fv = (PROC_glUniform2fv)LoadMethod("_glUniform2fv");
	this->Uniform2i = (PROC_glUniform2i)LoadMethod("_glUniform2i");
	this->Uniform2iv = (PROC_glUniform2iv)LoadMethod("_glUniform2iv");
	this->Uniform2ui = (PROC_glUniform2ui)LoadMethod("_glUniform2ui");
	this->Uniform2uiv = (PROC_glUniform2uiv)LoadMethod("_glUniform2uiv");
	this->Uniform3d = (PROC_glUniform3d)LoadMethod("_glUniform3d");
	this->Uniform3dv = (PROC_glUniform3dv)LoadMethod("_glUniform3dv");
	this->Uniform3f = (PROC_glUniform3f)LoadMethod("_glUniform3f");
	this->Uniform3fv = (PROC_glUniform3fv)LoadMethod("_glUniform3fv");
	this->Uniform3i = (PROC_glUniform3i)LoadMethod("_glUniform3i");
	this->Uniform3iv = (PROC_glUniform3iv)LoadMethod("_glUniform3iv");
	this->Uniform3ui = (PROC_glUniform3ui)LoadMethod("_glUniform3ui");
	this->Uniform3uiv = (PROC_glUniform3uiv)LoadMethod("_glUniform3uiv");
	this->Uniform4d = (PROC_glUniform4d)LoadMethod("_glUniform4d");
	this->Uniform4dv = (PROC_glUniform4dv)LoadMethod("_glUniform4dv");
	this->Uniform4f = (PROC_glUniform4f)LoadMethod("_glUniform4f");
	this->Uniform4fv = (PROC_glUniform4fv)LoadMethod("_glUniform4fv");
	this->Uniform4i = (PROC_glUniform4i)LoadMethod("_glUniform4i");
	this->Uniform4iv = (PROC_glUniform4iv)LoadMethod("_glUniform4iv");
	this->Uniform4ui = (PROC_glUniform4ui)LoadMethod("_glUniform4ui");
	this->Uniform4uiv = (PROC_glUniform4uiv)LoadMethod("_glUniform4uiv");
	this->UniformBlockBinding = (PROC_glUniformBlockBinding)LoadMethod("_glUniformBlockBinding");
	this->UniformMatrix2dv = (PROC_glUniformMatrix2dv)LoadMethod("_glUniformMatrix2dv");
	this->UniformMatrix2fv = (PROC_glUniformMatrix2fv)LoadMethod("_glUniformMatrix2fv");
	this->UniformMatrix2x3dv = (PROC_glUniformMatrix2x3dv)LoadMethod("_glUniformMatrix2x3dv");
	this->UniformMatrix2x3fv = (PROC_glUniformMatrix2x3fv)LoadMethod("_glUniformMatrix2x3fv");
	this->UniformMatrix2x4dv = (PROC_glUniformMatrix2x4dv)LoadMethod("_glUniformMatrix2x4dv");
	this->UniformMatrix2x4fv = (PROC_glUniformMatrix2x4fv)LoadMethod("_glUniformMatrix2x4fv");
	this->UniformMatrix3dv = (PROC_glUniformMatrix3dv)LoadMethod("_glUniformMatrix3dv");
	this->UniformMatrix3fv = (PROC_glUniformMatrix3fv)LoadMethod("_glUniformMatrix3fv");
	this->UniformMatrix3x2dv = (PROC_glUniformMatrix3x2dv)LoadMethod("_glUniformMatrix3x2dv");
	this->UniformMatrix3x2fv = (PROC_glUniformMatrix3x2fv)LoadMethod("_glUniformMatrix3x2fv");
	this->UniformMatrix3x4dv = (PROC_glUniformMatrix3x4dv)LoadMethod("_glUniformMatrix3x4dv");
	this->UniformMatrix3x4fv = (PROC_glUniformMatrix3x4fv)LoadMethod("_glUniformMatrix3x4fv");
	this->UniformMatrix4dv = (PROC_glUniformMatrix4dv)LoadMethod("_glUniformMatrix4dv");
	this->UniformMatrix4fv = (PROC_glUniformMatrix4fv)LoadMethod("_glUniformMatrix4fv");
	this->UniformMatrix4x2dv = (PROC_glUniformMatrix4x2dv)LoadMethod("_glUniformMatrix4x2dv");
	this->UniformMatrix4x2fv = (PROC_glUniformMatrix4x2fv)LoadMethod("_glUniformMatrix4x2fv");
	this->UniformMatrix4x3dv = (PROC_glUniformMatrix4x3dv)LoadMethod("_glUniformMatrix4x3dv");
	this->UniformMatrix4x3fv = (PROC_glUniformMatrix4x3fv)LoadMethod("_glUniformMatrix4x3fv");
	this->UniformSubroutinesuiv = (PROC_glUniformSubroutinesuiv)LoadMethod("_glUniformSubroutinesuiv");
	this->UnmapBuffer = (PROC_glUnmapBuffer)LoadMethod("_glUnmapBuffer");
	this->UnmapNamedBuffer = (PROC_glUnmapNamedBuffer)LoadMethod("_glUnmapNamedBuffer");
	this->UseProgram = (PROC_glUseProgram)LoadMethod("_glUseProgram");
	this->UseProgramStages = (PROC_glUseProgramStages)LoadMethod("_glUseProgramStages");
	this->ValidateProgram = (PROC_glValidateProgram)LoadMethod("_glValidateProgram");
	this->ValidateProgramPipeline = (PROC_glValidateProgramPipeline)LoadMethod("_glValidateProgramPipeline");
	this->VertexArrayAttribBinding = (PROC_glVertexArrayAttribBinding)LoadMethod("_glVertexArrayAttribBinding");
	this->VertexArrayAttribFormat = (PROC_glVertexArrayAttribFormat)LoadMethod("_glVertexArrayAttribFormat");
	this->VertexArrayAttribIFormat = (PROC_glVertexArrayAttribIFormat)LoadMethod("_glVertexArrayAttribIFormat");
	this->VertexArrayAttribLFormat = (PROC_glVertexArrayAttribLFormat)LoadMethod("_glVertexArrayAttribLFormat");
	this->VertexArrayBindingDivisor = (PROC_glVertexArrayBindingDivisor)LoadMethod("_glVertexArrayBindingDivisor");
	this->VertexArrayElementBuffer = (PROC_glVertexArrayElementBuffer)LoadMethod("_glVertexArrayElementBuffer");
	this->VertexArrayVertexBuffer = (PROC_glVertexArrayVertexBuffer)LoadMethod("_glVertexArrayVertexBuffer");
	this->VertexArrayVertexBuffers = (PROC_glVertexArrayVertexBuffers)LoadMethod("_glVertexArrayVertexBuffers");
	this->VertexAttrib1d = (PROC_glVertexAttrib1d)LoadMethod("_glVertexAttrib1d");
	this->VertexAttrib1dv = (PROC_glVertexAttrib1dv)LoadMethod("_glVertexAttrib1dv");
	this->VertexAttrib1f = (PROC_glVertexAttrib1f)LoadMethod("_glVertexAttrib1f");
	this->VertexAttrib1fv = (PROC_glVertexAttrib1fv)LoadMethod("_glVertexAttrib1fv");
	this->VertexAttrib1s = (PROC_glVertexAttrib1s)LoadMethod("_glVertexAttrib1s");
	this->VertexAttrib1sv = (PROC_glVertexAttrib1sv)LoadMethod("_glVertexAttrib1sv");
	this->VertexAttrib2d = (PROC_glVertexAttrib2d)LoadMethod("_glVertexAttrib2d");
	this->VertexAttrib2dv = (PROC_glVertexAttrib2dv)LoadMethod("_glVertexAttrib2dv");
	this->VertexAttrib2f = (PROC_glVertexAttrib2f)LoadMethod("_glVertexAttrib2f");
	this->VertexAttrib2fv = (PROC_glVertexAttrib2fv)LoadMethod("_glVertexAttrib2fv");
	this->VertexAttrib2s = (PROC_glVertexAttrib2s)LoadMethod("_glVertexAttrib2s");
	this->VertexAttrib2sv = (PROC_glVertexAttrib2sv)LoadMethod("_glVertexAttrib2sv");
	this->VertexAttrib3d = (PROC_glVertexAttrib3d)LoadMethod("_glVertexAttrib3d");
	this->VertexAttrib3dv = (PROC_glVertexAttrib3dv)LoadMethod("_glVertexAttrib3dv");
	this->VertexAttrib3f = (PROC_glVertexAttrib3f)LoadMethod("_glVertexAttrib3f");
	this->VertexAttrib3fv = (PROC_glVertexAttrib3fv)LoadMethod("_glVertexAttrib3fv");
	this->VertexAttrib3s = (PROC_glVertexAttrib3s)LoadMethod("_glVertexAttrib3s");
	this->VertexAttrib3sv = (PROC_glVertexAttrib3sv)LoadMethod("_glVertexAttrib3sv");
	this->VertexAttrib4Nbv = (PROC_glVertexAttrib4Nbv)LoadMethod("_glVertexAttrib4Nbv");
	this->VertexAttrib4Niv = (PROC_glVertexAttrib4Niv)LoadMethod("_glVertexAttrib4Niv");
	this->VertexAttrib4Nsv = (PROC_glVertexAttrib4Nsv)LoadMethod("_glVertexAttrib4Nsv");
	this->VertexAttrib4Nub = (PROC_glVertexAttrib4Nub)LoadMethod("_glVertexAttrib4Nub");
	this->VertexAttrib4Nubv = (PROC_glVertexAttrib4Nubv)LoadMethod("_glVertexAttrib4Nubv");
	this->VertexAttrib4Nuiv = (PROC_glVertexAttrib4Nuiv)LoadMethod("_glVertexAttrib4Nuiv");
	this->VertexAttrib4Nusv = (PROC_glVertexAttrib4Nusv)LoadMethod("_glVertexAttrib4Nusv");
	this->VertexAttrib4bv = (PROC_glVertexAttrib4bv)LoadMethod("_glVertexAttrib4bv");
	this->VertexAttrib4d = (PROC_glVertexAttrib4d)LoadMethod("_glVertexAttrib4d");
	this->VertexAttrib4dv = (PROC_glVertexAttrib4dv)LoadMethod("_glVertexAttrib4dv");
	this->VertexAttrib4f = (PROC_glVertexAttrib4f)LoadMethod("_glVertexAttrib4f");
	this->VertexAttrib4fv = (PROC_glVertexAttrib4fv)LoadMethod("_glVertexAttrib4fv");
	this->VertexAttrib4iv = (PROC_glVertexAttrib4iv)LoadMethod("_glVertexAttrib4iv");
	this->VertexAttrib4s = (PROC_glVertexAttrib4s)LoadMethod("_glVertexAttrib4s");
	this->VertexAttrib4sv = (PROC_glVertexAttrib4sv)LoadMethod("_glVertexAttrib4sv");
	this->VertexAttrib4ubv = (PROC_glVertexAttrib4ubv)LoadMethod("_glVertexAttrib4ubv");
	this->VertexAttrib4uiv = (PROC_glVertexAttrib4uiv)LoadMethod("_glVertexAttrib4uiv");
	this->VertexAttrib4usv = (PROC_glVertexAttrib4usv)LoadMethod("_glVertexAttrib4usv");
	this->VertexAttribBinding = (PROC_glVertexAttribBinding)LoadMethod("_glVertexAttribBinding");
	this->VertexAttribDivisor = (PROC_glVertexAttribDivisor)LoadMethod("_glVertexAttribDivisor");
	this->VertexAttribFormat = (PROC_glVertexAttribFormat)LoadMethod("_glVertexAttribFormat");
	this->VertexAttribI1i = (PROC_glVertexAttribI1i)LoadMethod("_glVertexAttribI1i");
	this->VertexAttribI1iv = (PROC_glVertexAttribI1iv)LoadMethod("_glVertexAttribI1iv");
	this->VertexAttribI1ui = (PROC_glVertexAttribI1ui)LoadMethod("_glVertexAttribI1ui");
	this->VertexAttribI1uiv = (PROC_glVertexAttribI1uiv)LoadMethod("_glVertexAttribI1uiv");
	this->VertexAttribI2i = (PROC_glVertexAttribI2i)LoadMethod("_glVertexAttribI2i");
	this->VertexAttribI2iv = (PROC_glVertexAttribI2iv)LoadMethod("_glVertexAttribI2iv");
	this->VertexAttribI2ui = (PROC_glVertexAttribI2ui)LoadMethod("_glVertexAttribI2ui");
	this->VertexAttribI2uiv = (PROC_glVertexAttribI2uiv)LoadMethod("_glVertexAttribI2uiv");
	this->VertexAttribI3i = (PROC_glVertexAttribI3i)LoadMethod("_glVertexAttribI3i");
	this->VertexAttribI3iv = (PROC_glVertexAttribI3iv)LoadMethod("_glVertexAttribI3iv");
	this->VertexAttribI3ui = (PROC_glVertexAttribI3ui)LoadMethod("_glVertexAttribI3ui");
	this->VertexAttribI3uiv = (PROC_glVertexAttribI3uiv)LoadMethod("_glVertexAttribI3uiv");
	this->VertexAttribI4bv = (PROC_glVertexAttribI4bv)LoadMethod("_glVertexAttribI4bv");
	this->VertexAttribI4i = (PROC_glVertexAttribI4i)LoadMethod("_glVertexAttribI4i");
	this->VertexAttribI4iv = (PROC_glVertexAttribI4iv)LoadMethod("_glVertexAttribI4iv");
	this->VertexAttribI4sv = (PROC_glVertexAttribI4sv)LoadMethod("_glVertexAttribI4sv");
	this->VertexAttribI4ubv = (PROC_glVertexAttribI4ubv)LoadMethod("_glVertexAttribI4ubv");
	this->VertexAttribI4ui = (PROC_glVertexAttribI4ui)LoadMethod("_glVertexAttribI4ui");
	this->VertexAttribI4uiv = (PROC_glVertexAttribI4uiv)LoadMethod("_glVertexAttribI4uiv");
	this->VertexAttribI4usv = (PROC_glVertexAttribI4usv)LoadMethod("_glVertexAttribI4usv");
	this->VertexAttribIFormat = (PROC_glVertexAttribIFormat)LoadMethod("_glVertexAttribIFormat");
	this->VertexAttribIPointer = (PROC_glVertexAttribIPointer)LoadMethod("_glVertexAttribIPointer");
	this->VertexAttribL1d = (PROC_glVertexAttribL1d)LoadMethod("_glVertexAttribL1d");
	this->VertexAttribL1dv = (PROC_glVertexAttribL1dv)LoadMethod("_glVertexAttribL1dv");
	this->VertexAttribL2d = (PROC_glVertexAttribL2d)LoadMethod("_glVertexAttribL2d");
	this->VertexAttribL2dv = (PROC_glVertexAttribL2dv)LoadMethod("_glVertexAttribL2dv");
	this->VertexAttribL3d = (PROC_glVertexAttribL3d)LoadMethod("_glVertexAttribL3d");
	this->VertexAttribL3dv = (PROC_glVertexAttribL3dv)LoadMethod("_glVertexAttribL3dv");
	this->VertexAttribL4d = (PROC_glVertexAttribL4d)LoadMethod("_glVertexAttribL4d");
	this->VertexAttribL4dv = (PROC_glVertexAttribL4dv)LoadMethod("_glVertexAttribL4dv");
	this->VertexAttribLFormat = (PROC_glVertexAttribLFormat)LoadMethod("_glVertexAttribLFormat");
	this->VertexAttribLPointer = (PROC_glVertexAttribLPointer)LoadMethod("_glVertexAttribLPointer");
	this->VertexAttribP1ui = (PROC_glVertexAttribP1ui)LoadMethod("_glVertexAttribP1ui");
	this->VertexAttribP1uiv = (PROC_glVertexAttribP1uiv)LoadMethod("_glVertexAttribP1uiv");
	this->VertexAttribP2ui = (PROC_glVertexAttribP2ui)LoadMethod("_glVertexAttribP2ui");
	this->VertexAttribP2uiv = (PROC_glVertexAttribP2uiv)LoadMethod("_glVertexAttribP2uiv");
	this->VertexAttribP3ui = (PROC_glVertexAttribP3ui)LoadMethod("_glVertexAttribP3ui");
	this->VertexAttribP3uiv = (PROC_glVertexAttribP3uiv)LoadMethod("_glVertexAttribP3uiv");
	this->VertexAttribP4ui = (PROC_glVertexAttribP4ui)LoadMethod("_glVertexAttribP4ui");
	this->VertexAttribP4uiv = (PROC_glVertexAttribP4uiv)LoadMethod("_glVertexAttribP4uiv");
	this->VertexAttribPointer = (PROC_glVertexAttribPointer)LoadMethod("_glVertexAttribPointer");
	this->VertexBindingDivisor = (PROC_glVertexBindingDivisor)LoadMethod("_glVertexBindingDivisor");
	this->Viewport = (PROC_glViewport)LoadMethod("_glViewport");
	this->ViewportArrayv = (PROC_glViewportArrayv)LoadMethod("_glViewportArrayv");
	this->ViewportIndexedf = (PROC_glViewportIndexedf)LoadMethod("_glViewportIndexedf");
	this->ViewportIndexedfv = (PROC_glViewportIndexedfv)LoadMethod("_glViewportIndexedfv");

	// Fake implementation

	if (INVALID_METHOD(this->GetProgramStageiv)) {
		this->GetProgramStageiv = FakeGetProgramStageiv;
	}

	// Must have

	// TODO: remove some checks (double, subroutines, compute shader)

	if (INVALID_METHOD(this->ActiveTexture)) {
		return false;
	}

	if (INVALID_METHOD(this->AttachShader)) {
		return false;
	}

	if (INVALID_METHOD(this->BeginTransformFeedback)) {
		return false;
	}

	if (INVALID_METHOD(this->BindBuffer)) {
		return false;
	}

	if (INVALID_METHOD(this->BindBufferBase)) {
		return false;
	}

	if (INVALID_METHOD(this->BindFramebuffer)) {
		return false;
	}

	if (INVALID_METHOD(this->BindRenderbuffer)) {
		return false;
	}

	if (INVALID_METHOD(this->BindTexture)) {
		return false;
	}

	if (INVALID_METHOD(this->BindVertexArray)) {
		return false;
	}

	if (INVALID_METHOD(this->BlendFunc)) {
		return false;
	}

	if (INVALID_METHOD(this->BufferData)) {
		return false;
	}

	if (INVALID_METHOD(this->BufferSubData)) {
		return false;
	}

	if (INVALID_METHOD(this->CheckFramebufferStatus)) {
		return false;
	}

	if (INVALID_METHOD(this->Clear)) {
		return false;
	}

	if (INVALID_METHOD(this->ClearColor)) {
		return false;
	}

	if (INVALID_METHOD(this->CompileShader)) {
		return false;
	}

	if (INVALID_METHOD(this->CopyBufferSubData)) {
		return false;
	}

	if (INVALID_METHOD(this->CreateProgram)) {
		return false;
	}

	if (INVALID_METHOD(this->CreateShader)) {
		return false;
	}

	if (INVALID_METHOD(this->DeleteBuffers)) {
		return false;
	}

	if (INVALID_METHOD(this->DeleteFramebuffers)) {
		return false;
	}

	if (INVALID_METHOD(this->DeleteProgram)) {
		return false;
	}

	if (INVALID_METHOD(this->DeleteRenderbuffers)) {
		return false;
	}

	if (INVALID_METHOD(this->DeleteShader)) {
		return false;
	}

	if (INVALID_METHOD(this->DeleteTextures)) {
		return false;
	}

	if (INVALID_METHOD(this->DeleteVertexArrays)) {
		return false;
	}

	if (INVALID_METHOD(this->Disable)) {
		return false;
	}

	if (INVALID_METHOD(this->DisableVertexAttribArray)) {
		return false;
	}

	if (INVALID_METHOD(this->DrawArraysInstanced)) {
		return false;
	}

	if (INVALID_METHOD(this->DrawElementsInstanced)) {
		return false;
	}

	if (INVALID_METHOD(this->Enable)) {
		return false;
	}

	if (INVALID_METHOD(this->EnableVertexAttribArray)) {
		return false;
	}

	if (INVALID_METHOD(this->EndTransformFeedback)) {
		return false;
	}

	if (INVALID_METHOD(this->Finish)) {
		return false;
	}

	if (INVALID_METHOD(this->Flush)) {
		return false;
	}

	if (INVALID_METHOD(this->FramebufferRenderbuffer)) {
		return false;
	}

	if (INVALID_METHOD(this->FramebufferTexture2D)) {
		return false;
	}

	if (INVALID_METHOD(this->GenBuffers)) {
		return false;
	}

	if (INVALID_METHOD(this->GenFramebuffers)) {
		return false;
	}

	if (INVALID_METHOD(this->GenRenderbuffers)) {
		return false;
	}

	if (INVALID_METHOD(this->GenTextures)) {
		return false;
	}

	if (INVALID_METHOD(this->GenVertexArrays)) {
		return false;
	}

	if (INVALID_METHOD(this->GetActiveAttrib)) {
		return false;
	}

	if (INVALID_METHOD(this->GetActiveSubroutineName)) {
		return false;
	}

	if (INVALID_METHOD(this->GetActiveSubroutineUniformName)) {
		return false;
	}

	if (INVALID_METHOD(this->GetActiveUniform)) {
		return false;
	}

	if (INVALID_METHOD(this->GetActiveUniformBlockiv)) {
		return false;
	}

	if (INVALID_METHOD(this->GetActiveUniformBlockName)) {
		return false;
	}

	if (INVALID_METHOD(this->GetAttribLocation)) {
		return false;
	}

	if (INVALID_METHOD(this->GetFloatv)) {
		return false;
	}

	if (INVALID_METHOD(this->GetIntegerv)) {
		return false;
	}

	if (INVALID_METHOD(this->GetProgramInfoLog)) {
		return false;
	}

	if (INVALID_METHOD(this->GetProgramiv)) {
		return false;
	}

	if (INVALID_METHOD(this->GetShaderInfoLog)) {
		return false;
	}

	if (INVALID_METHOD(this->GetShaderiv)) {
		return false;
	}

	if (INVALID_METHOD(this->GetString)) {
		return false;
	}

	if (INVALID_METHOD(this->GetSubroutineIndex)) {
		return false;
	}

	if (INVALID_METHOD(this->GetSubroutineUniformLocation)) {
		return false;
	}

	if (INVALID_METHOD(this->GetTransformFeedbackVarying)) {
		return false;
	}

	if (INVALID_METHOD(this->GetUniformdv)) {
		return false;
	}

	if (INVALID_METHOD(this->GetUniformfv)) {
		return false;
	}

	if (INVALID_METHOD(this->GetUniformiv)) {
		return false;
	}

	if (INVALID_METHOD(this->GetUniformLocation)) {
		return false;
	}

	if (INVALID_METHOD(this->GetUniformuiv)) {
		return false;
	}

	if (INVALID_METHOD(this->GetVertexAttribiv)) {
		return false;
	}

	if (INVALID_METHOD(this->LineWidth)) {
		return false;
	}

	if (INVALID_METHOD(this->LinkProgram)) {
		return false;
	}

	if (INVALID_METHOD(this->MapBufferRange)) {
		return false;
	}

	if (INVALID_METHOD(this->PointSize)) {
		return false;
	}

	if (INVALID_METHOD(this->PrimitiveRestartIndex)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform1dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform1fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform1iv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform1uiv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform2dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform2fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform2iv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform2uiv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform3dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform3fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform3iv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform3uiv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform4dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform4fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform4iv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniform4uiv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix2dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix2fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix2x3dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix2x3fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix2x4dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix2x4fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix3dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix3fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix3x2dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix3x2fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix3x4dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix3x4fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix4dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix4fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix4x2dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix4x2fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix4x3dv)) {
		return false;
	}

	if (INVALID_METHOD(this->ProgramUniformMatrix4x3fv)) {
		return false;
	}

	if (INVALID_METHOD(this->ReadPixels)) {
		return false;
	}

	if (INVALID_METHOD(this->RenderbufferStorage)) {
		return false;
	}

	if (INVALID_METHOD(this->ShaderSource)) {
		return false;
	}

	if (INVALID_METHOD(this->TexImage2D)) {
		return false;
	}

	if (INVALID_METHOD(this->TexParameteri)) {
		return false;
	}

	if (INVALID_METHOD(this->TexSubImage2D)) {
		return false;
	}

	if (INVALID_METHOD(this->TransformFeedbackVaryings)) {
		return false;
	}

	if (INVALID_METHOD(this->UnmapBuffer)) {
		return false;
	}

	if (INVALID_METHOD(this->UseProgram)) {
		return false;
	}

	if (INVALID_METHOD(this->VertexAttribDivisor)) {
		return false;
	}

	if (INVALID_METHOD(this->VertexAttribIPointer)) {
		return false;
	}

	if (INVALID_METHOD(this->VertexAttribLPointer)) {
		return false;
	}

	if (INVALID_METHOD(this->VertexAttribPointer)) {
		return false;
	}

	if (INVALID_METHOD(this->Viewport)) {
		return false;
	}

	return true;
}
