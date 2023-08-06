Textures
********

.. currentmodule:: ModernGL

.. automethod:: Context.texture(size, components, data=None, samples=0, floats=False) -> Texture
	:noindex:

.. automethod:: Context.depth_texture(size, data=None, samples=0) -> Texture
	:noindex:

.. autoclass:: Texture
	:members: width, height, size, samples, components, depth

	.. automethod:: write(self, data, viewport=None)
	.. automethod:: use(location=0)

.. toctree::
	:maxdepth: 4
