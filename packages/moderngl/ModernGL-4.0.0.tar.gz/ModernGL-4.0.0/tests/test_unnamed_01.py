import unittest

import ModernGL, struct

class TestBuffer(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.ctx = ModernGL.create_standalone_context()

		self.vert = self.ctx.vertex_shader('''
			#version 330

			in mat2 in_m;
			in vec2 in_v;

			out vec2 out_v;

			uniform float mult;

			void main() {
				out_v = in_m * in_v * mult;
			}
		''')

		self.prog = self.ctx.program(self.vert, ['out_v'])

	@classmethod
	def tearDownClass(self):
		self.ctx.release()

	def test_1(self):
		buf_m = self.ctx.buffer(struct.pack('4f', 1, 1, 1, 2))
		buf_v = self.ctx.buffer(struct.pack('2f', 4, 7))
		res = self.ctx.buffer(reserve = buf_v.size)

		vao = self.ctx.vertex_array(self.prog, [
			(buf_m, '4f', ['in_m']),
			(buf_v, '2f', ['in_v']),
		])

		self.prog.uniforms['mult'].value = 0.0
		vao.transform(res, ModernGL.POINTS);
		x, y = struct.unpack('2f', res.read())
		self.assertAlmostEqual(x, 0.0)
		self.assertAlmostEqual(y, 0.0)

		self.prog.uniforms['mult'].value = 1.0
		vao.transform(res, ModernGL.POINTS);
		x, y = struct.unpack('2f', res.read())
		self.assertAlmostEqual(x, 11.0)
		self.assertAlmostEqual(y, 18.0)

		self.prog.uniforms['mult'].value = 2.0
		vao.transform(res, ModernGL.POINTS);
		x, y = struct.unpack('2f', res.read())
		self.assertAlmostEqual(x, 22.0)
		self.assertAlmostEqual(y, 36.0)


if __name__ == '__main__':
	unittest.main()
