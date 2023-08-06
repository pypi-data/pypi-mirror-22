VertexArray
***********

.. currentmodule:: ModernGL

.. automethod:: Context.simple_vertex_array
	:noindex:

.. automethod:: Context.vertex_array
	:noindex:

.. autoclass:: VertexArray
	:members: program, attributes, index_buffer, vertices

	.. automethod:: render(mode=TRIANGLES, vertices=-1, first=0, instances=1)
	.. automethod:: transform(buf, mode=POINTS, vertices=-1, *, first=0, instances=1)

.. toctree::
	:maxdepth: 4
	:caption: Classes:

	Attributes <VertexArrayAttributes.rst>
