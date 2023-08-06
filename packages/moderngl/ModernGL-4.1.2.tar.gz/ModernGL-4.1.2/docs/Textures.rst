Textures
********

.. currentmodule:: ModernGL

.. automethod:: Context.texture(size, components, data=None, samples=0, floats=False) -> Texture
	:noindex:

.. automethod:: Context.depth_texture(size, data=None, samples=0) -> Texture
	:noindex:

.. autoclass:: Texture
	:members: width, height, size, samples, components, depth

	.. automethod:: read(viewport=None, alignment=1) -> bytes
	.. automethod:: read_into(buffer, viewport=None, alignment=1)
	.. automethod:: write(data, viewport=None)
	.. automethod:: use(location=0)

.. toctree::
	:maxdepth: 4
