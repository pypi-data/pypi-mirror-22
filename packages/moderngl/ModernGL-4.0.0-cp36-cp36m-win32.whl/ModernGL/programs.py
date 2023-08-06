'''
    ModernGL programs
'''

# pylint: disable=too-few-public-methods

from .common import InvalidObject, Primitive, PRIMITIVES
from .program_members import UniformMap, UniformBlockMap, VaryingMap, AttributeMap, ProgramStage


class ComputeShader:
    '''
        ``NYI``

        ComputeShader
    '''

    def __init__(self):
        self.mglo = None
        raise NotImplementedError()

    def release(self):
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()
        self.__class__ = InvalidObject

    @staticmethod
    def new(obj):
        '''
            For internal use only.
        '''

        res = ComputeShader.__new__(ComputeShader)
        res.mglo = obj
        return res

    @property
    def source(self) -> str:
        '''
            The source code of the compute shader.
        '''

        return self.mglo.source

    def run(self, size_x=1, size_y=1, size_z=1) -> None:
        '''
            ``NYI``

            Run the compute shader.
        '''

        return self.mglo.run(size_x, size_y, size_z)


class Shader:
    '''
        Shader objects represent compiled GLSL code for a single shader stage.

        A Shader object cannot be instantiated directly, it requires a context.
        Use the following methods to create one:

            - :py:meth:`Context.vertex_shader`
            - :py:meth:`Context.fragment_shader`
            - :py:meth:`Context.geometry_shader`
            - :py:meth:`Context.tess_evaluation_shader`
            - :py:meth:`Context.tess_control_shader`
    '''

    def __init__(self):
        self.mglo = None
        raise NotImplementedError()

    def release(self):
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()
        self.__class__ = InvalidObject

    @staticmethod
    def new(obj):
        '''
            For internal use only.
        '''

        res = Shader.__new__(Shader)
        res.mglo = obj
        return res

    @property
    def source(self) -> str:
        '''
            The source code of the shader.
        '''

        return self.mglo.source

    @property
    def typename(self) -> str:
        '''
            The type of the shader.
            The return value is a string.

            - ``'VertexShader'``
            - ``'FragmentShader'``
            - ``'GeometryShader'``
            - ``'TessEvaluationShader'``
            - ``'TessControlShader'``
        '''

        return self.mglo.typename


class Program:
    '''
        A Program object represents fully processed executable code
        in the OpenGL Shading Language, for one or more Shader stages.

        In ModernGL, a Program object can be assigned to :py:class:`VertexArray` objects.
        The VertexArray object  is capable of binding the Program object once the
        :py:meth:`VertexArray.render` or :py:meth:`VertexArray.transform` is called.

        Program objects has no method called ``use()``, VertexArrays encapsulate this mechanism.

        A Program object cannot be instantiated directly, it requires a context.
        Use :py:meth:`Context.program` to create one.
    '''

    def __init__(self):
        self.mglo = None
        raise NotImplementedError()

    def release(self):
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()
        self.__class__ = InvalidObject

    @staticmethod
    def new(obj):
        '''
            For internal use only.
        '''

        res = Program.__new__(Program)
        res.mglo = obj
        return res

    @property
    def uniforms(self) -> UniformMap:
        '''
            :py:class:`UniformMap`: The uniforms of the program.
            The return value is a dictinary like object.
            It can be used to access :py:class:`Uniform` objects by name.

            Examples:

                Set the value of the uniforms::

                    # uniform vec3 eye_pos;
                    >>> program.uniforms['eye_pos'].value = (10.0, 20.0, 0.0)

                    # uniform sampler2D my_textures[3];
                    >>> program.uniforms['my_texture'].value = [0, 3, 2]

                    # The values of `my_textures` will be:
                    my_textures[0] = GL_TEXTURE0             # GL_TEXTURE0
                    my_textures[1] = GL_TEXTURE0 + 3         # GL_TEXTURE3
                    my_textures[2] = GL_TEXTURE0 + 2         # GL_TEXTURE2

                Get information about the uniforms::

                    >>> program.uniforms['eye_pos'].location
                    0

                    >>> program.uniforms['eye_pos'].dimension
                    3

                    >>> program.uniforms['eye_pos'].value
                    (10.0, 20.0, 0.0)

                    >>> program.uniforms['my_textures'].dimension
                    1

                    >>> program.uniforms['my_textures'].array_length
                    3
        '''

        return UniformMap.new(self.mglo.uniforms)

    @property
    def uniform_blocks(self) -> UniformBlockMap:
        '''
            :py:class:`UniformBlockMap`: The uniform blocks of the program.
            The return value is a dictinary like object.
            It can be used to access :py:class:`UniformBlock` objects by name.

            Examples:

                Get the location of the uniform block::

                    # uniform custom_material {
                    #     ...
                    # };

                    >>> program.uniform_blocks['custom_material'].location
                    16
        '''

        return UniformBlockMap.new(self.mglo.uniform_blocks)

    @property
    def attributes(self) -> AttributeMap:
        '''
            :py:class:`AttributeMap`: The attributes of the program.
            The return value is a dictinary like object.
            It can be used to access :py:class:`Attribute` objects by name.

            Examples:

                Set the default value for the attributes::

                    # in vec3 normal;
                    >>> program.attributes['normal'].default = (0.0, 0.0, 1.0)

                    # in vec2 texture_coordinates[3];
                    >>> program.attributes['texture_coordinates'].default = [
                    ...     (0.0, 0.0),
                    ...     (0.0, 0.0),
                    ...     (0.0, 0.0),
                    ... ]

                Get information about the attributes::

                    >>> program.attributes['normal'].default
                    (0.0, 0.0, 1.0)

                    >>> program.attributes['normal'].dimension
                    3

                    >>> program.attributes['texture_coordinates'].default
                    [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0)]

                    >>> program.attributes['texture_coordinates'].array_length
                    3

                    >>> program.attributes['texture_coordinates'].dimension
                    2
        '''

        return AttributeMap.new(self.mglo.attributes)

    @property
    def varyings(self) -> VaryingMap:
        '''
            :py:class:`VaryingMap`: The varyings of the program.
            The return value is a dictinary like object.
            It can be used to access :py:class:`Varying` objects by name.

            The only reason varyings were added to allow verifying
            varyings programatically, they do not hold any other information.

            Examples:

                Check varyings::

                    >>> 'vertex_out' in program.varyings
                    True
        '''

        return VaryingMap.new(self.mglo.varyings)

    @property
    def geometry_input(self) -> Primitive:
        '''
            :py:class:`Primitive`: The geometry input primitive.
            The GeometryShader's input primitive if the GeometryShader exists.
            The geometry input primitive will be used for validation.
        '''

        return PRIMITIVES[self.mglo.geometry_input]

    @property
    def geometry_output(self) -> Primitive:
        '''
            :py:class:`Primitive`: The geometry output primitive.
            The GeometryShader's output primitive if the GeometryShader exists.
        '''

        return PRIMITIVES[self.mglo.geometry_output]

    @property
    def geometry_vertices(self) -> int:
        '''
            :obj:`int`: The maximum number of vertices that
            the geometry shader will output.
        '''

        return self.mglo.geometry_vertices

    @property
    def vertex_shader(self) -> ProgramStage:
        '''
            :py:class:`ProgramStage`: The vertex shader program stage.

            The return value is NOT a Shader.
        '''

        stage = self.mglo.vertex_shader

        if stage is not None:
            stage = ProgramStage.new(stage)

        return stage

    @property
    def fragment_shader(self) -> ProgramStage:
        '''
            :py:class:`ProgramStage`: The fragment shader program stage.

            The return value is NOT a Shader.
        '''

        stage = self.mglo.fragment_shader

        if stage is not None:
            stage = ProgramStage.new(stage)

        return stage

    @property
    def geometry_shader(self) -> ProgramStage:
        '''
            :py:class:`ProgramStage`: The geometry shader program stage.

            The return value is NOT a Shader.
        '''

        stage = self.mglo.geometry_shader

        if stage is not None:
            stage = ProgramStage.new(stage)

        return stage

    @property
    def tess_evaluation_shader(self) -> ProgramStage:
        '''
            :py:class:`ProgramStage`: The tesselation evaluation shader program stage.

            The return value is NOT a Shader.
        '''

        stage = self.mglo.tess_evaluation_shader

        if stage is not None:
            stage = ProgramStage.new(stage)

        return stage

    @property
    def tess_control_shader(self) -> ProgramStage:
        '''
            :py:class:`ProgramStage`: The tesselation control shader program stage.

            The return value is NOT a Shader.
        '''

        stage = self.mglo.tess_control_shader

        if stage is not None:
            stage = ProgramStage.new(stage)

        return stage
