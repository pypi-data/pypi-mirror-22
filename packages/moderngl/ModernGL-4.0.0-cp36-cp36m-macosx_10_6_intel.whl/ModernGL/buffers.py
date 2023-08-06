'''
    ModernGL buffers
'''

from .common import InvalidObject


class BufferAccess:
    '''
        :py:class:`BufferAccess` objects are designed to access
        a :py:class:`Buffer` object's content inside a ``with`` statement.
        The buffer is mapped and unmapped only once.

        Use :py:meth:`Buffer.access` to get a BufferAccess object.
    '''

    def __init__(self):
        self.mglo = None
        raise NotImplementedError('BufferAccess')

    def __enter__(self):
        self.mglo.open()
        return self

    def __exit__(self, *args):
        self.mglo.close()

    @staticmethod
    def new(obj):
        '''
            For internal use only.
        '''

        res = BufferAccess.__new__(BufferAccess)
        res.mglo = obj
        return res

    def open(self) -> None:
        '''
            Map the buffer.
            This method is called by ``__enter__``.
        '''

        self.mglo.open()

    def close(self) -> None:
        '''
            Unmap the buffer.
            This method is called by ``__exit__``.
        '''

        self.mglo.close()

    def read(self, size=-1, offset=0) -> bytes:
        '''
            Read the content.

            Args:
                size: The size. Value `-1` means all.

            Keyword Args:
                offset: The offset.

            Returns:
                bytes: binary data
        '''

        return self.mglo.read(size, offset)

    def write(self, data, offset=0) -> None:
        '''
            Write the content.

            Args:
                size: The data.

            Keyword Args:
                offset: The offset.
        '''

        self.mglo.write(data, offset)

    @property
    def offset(self) -> int:
        '''
            int: The offset.
        '''

        return self.mglo.offset

    @property
    def size(self) -> int:
        '''
            int: The size.
        '''

        return self.mglo.size

    @property
    def readonly(self) -> bool:
        '''
            bool: Is readonly.
        '''

        return self.mglo.readonly


class Buffer:
    '''
        Buffer Objects are OpenGL Objects that store an array of unformatted memory
        allocated by the OpenGL context, (data allocated on the GPU).
        These can be used to store vertex data, pixel data retrieved from images
        or the framebuffer, and a variety of other things.

        A Buffer object cannot be instantiated directly, it requires a context.
        Use :py:meth:`Context.buffer` to create one.

        Copy buffer content using :py:meth:`Context.copy_buffer`.
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

        res = Buffer.__new__(Buffer)
        res.mglo = obj
        return res

    @property
    def size(self) -> int:
        '''
            The size of the buffer.
        '''

        return self.mglo.size

    @property
    def dynamic(self) -> bool:
        '''
            Is the buffer created with the dynamic flag?
        '''

        return self.mglo.dynamic

    def access(self, *, size=-1, offset=0, readonly=False) -> BufferAccess:
        '''
            Create a :py:class:`BufferAccess` object.

            Keyword Args:
                size (int): The size. Value `-1` means all.
                offset (int): The offset.
                readonly (bool): The readonly.

            Examples:

                Simple with statement::

                    # The buffer will be mapped once and accessed multiple times.

                    >>> with buffer.access() as access:
                    ...     access.read(...)
                    ...     access.write(...)
        '''

        return BufferAccess.new(self.mglo.access(size, offset, readonly))

    def read(self, size=-1, *, offset=0) -> bytes:
        '''
            Read the content.

            Args:
                size (int): The size. Value ``-1`` means all.

            Keyword Args:
                offset (int): The offset.

            Returns:
                bytes: The content of the buffer.
        '''

        return self.mglo.read(size, offset)

    def write(self, data, offset=0) -> None:
        '''
            Write the content.

            Args:
                data: The data.

            Keyword Args:
                offset: The offset.
        '''

        self.mglo.write(data, offset)

    def orphan(self) -> None:
        '''
            Orphan the buffer.

            It is also called buffer re-specification.

            Reallocate the buffer object before you start modifying it.

            Since allocating storage is likely faster than the implicit synchronization,
            you gain significant performance advantages over synchronization.

            The old storage will still be used by the OpenGL commands that have been sent previously.
            It is likely that the GL driver will not be doing any allocation at all,
            but will just be pulling an old free block off the unused buffer queue and use it,
            so it is likely to be very efficient.

            Examples:

                Simple orphaning example::

                    # For simplicity the VertexArray creation is omitted

                    >>> vbo = ctx.buffer(reserve=1024)

                    # Fill the buffer

                    >>> vbo.write(some_temorary_data)

                    # Issue a render call that uses the vbo

                    >>> vao.render(...)

                    # Orphan the buffer

                    >>> vbo.orphan()

                    # Issue another render call without waiting for the previous one

                    >>> vbo.write(some_temorary_data)
                    >>> vao.render(...)
        '''

        self.mglo.orphan()

    def bind_to_uniform_block(self, location=0) -> None:
        '''
            ``NYI``

            Bind the buffer to a uniform block.

            Args:
                location: The uniform block location.
        '''

        self.mglo.bind_to_uniform_block(location)

    def bind_to_storage_buffer(self, location=0) -> None:
        '''
            ``NYI``

            Bind the buffer to a shader storage buffer.

            Args:
                location: The shader storage location.
        '''

        self.mglo.bind_to_storage_buffer(location)


def detect_format(program, attributes) -> str:
    '''
        Detect format for vertex attributes.
        The format returned does not contain padding.

        Args:
            program (Program): The program.
            attributes (list): A list of attribute names.

        Returns:
            str: The tightly packed format for the attributes.
    '''

    def fmt(attr):
        '''
            For internal use only.
        '''

        return attr.array_length * attr.dimension, attr.shape

    return ''.join('%d%s' % fmt(program.attributes[a]) for a in attributes)
