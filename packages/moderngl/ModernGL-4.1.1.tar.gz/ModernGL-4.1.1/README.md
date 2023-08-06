# ModernGL

:fire: modern OpenGL binding for Python (alternative to PyOpenGL)

- [ModernGL on PyPI](https://pypi.python.org/pypi/ModernGL/)
- [Documentation](https://moderngl.readthedocs.io/en/latest/)
- [Examples](https://moderngl.github.io/Examples.html)

## ModernGL and OpenGL

OpenGL is a great environment for developing portable, platform independent,
interactive 2D and 3D graphics applications. The API implementation in Python
is cumbersome, resulting in applications with high latency. To solve this
problem we have developed ModernGL, a wrapper over OpenGL that simplifies the
creation of simple graphics applications like scientific simulations, small
games or user interfaces. Usually, acquiring in-depth knowledge of OpenGL
requires a steep learning curve. In contrast, ModernGL is easy to learn and
use, moreover it is capable of rendering with the same performance and
quality, with less code written.

# Installation

Using pip:

```
pip install ModernGL
```

## An example with [source](https://moderngl.github.io/Examples/julia_fractal.html)

![Julia Fractal](https://moderngl.github.io/_images/julia_fractal.png)

## A short sample

```py

# Create a window first

ctx = ModernGL.create_context()

prog = ctx.program([
	ctx.vertex_shader('''
		#version 330
		in vec2 vert;
		void main() {
			gl_Position = vec4(vert, 0.0, 1.0);
		}
	'''),
	ctx.fragment_shader('''
		#version 330
		out vec4 color;
		void main() {
			color = vec4(0.2, 0.6, 0.9, 1.0);
		}
	'''),
])

vbo = ctx.buffer(struct.pack('6f', 0, 0, 1, 0, 0, 1))
vao = ctx.simple_vertex_array(prog, vbo, ['vert'])

# Render

vao.render(ModernGL.TRIANGLES)

```

## How to install

Installing on **Ubuntu** from source:
```
apt-get install python3-dev libgl1-mesa-dev libx11-dev
python3 setup.py install
```

...
