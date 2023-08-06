#include <Python.h>

#include "quickhull/quickhull.hpp"

PyObject * meth_quick_hull(PyObject * self, PyObject * args) {
	PyObject * points;
	int ccw;

	int args_ok = PyArg_ParseTuple(
		args,
		"Op",
		&points,
		&ccw
	);

	quickhull::QuickHull<double> qh;
	std::vector<quickhull::Vector3<double>> pointCloud;

	int pointsSize = PyTuple_GET_SIZE(points);
	pointCloud.reserve(pointsSize);

	for (int i = 0; i < pointsSize; ++i) {
		PyObject * xyz = PyTuple_GET_ITEM(points, i);
		if (Py_TYPE(xyz) != &PyTuple_Type || PyTuple_GET_SIZE(xyz) != 3) {
			PyErr_Format(PyExc_Exception, "points[%d] must be a 3-tuple not %s", i, Py_TYPE(xyz)->tp_name);
			return 0;
		}

		double x = PyFloat_AsDouble(PyTuple_GET_ITEM(xyz, 0));
		double y = PyFloat_AsDouble(PyTuple_GET_ITEM(xyz, 1));
		double z = PyFloat_AsDouble(PyTuple_GET_ITEM(xyz, 2));

		if (PyErr_Occurred()) {
			PyErr_Format(PyExc_Exception, "points[%d] is not a valid vertex", i);
			return 0;
		}

		pointCloud.push_back(quickhull::Vector3<double>(x, y, z));
	}

	auto hull = qh.getConvexHull(pointCloud, ccw ? true : false, false);

	auto indexBuffer = hull.getIndexBuffer();
	auto vertexBuffer = hull.getVertexBuffer();

	int indexBufferSize = indexBuffer.size();
	int vertexBufferSize = vertexBuffer.size();

	PyObject * vertexList = PyList_New(vertexBufferSize);

	for (int i = 0; i < vertexBufferSize; ++i) {
		PyObject * x = PyFloat_FromDouble(vertexBuffer[i].x);
		PyObject * y = PyFloat_FromDouble(vertexBuffer[i].y);
		PyObject * z = PyFloat_FromDouble(vertexBuffer[i].z);
		PyObject * vertex = PyTuple_Pack(3, x, y, z);
		PyList_SET_ITEM(vertexList, i, vertex);
	}

	int trianglesSize = indexBufferSize / 3;
	PyObject * trianglesList = PyList_New(trianglesSize);

	for (int i = 0; i < trianglesSize; ++i) {
		PyObject * a = PyLong_FromLong(indexBuffer[i * 3 + 0]);
		PyObject * b = PyLong_FromLong(indexBuffer[i * 3 + 1]);
		PyObject * c = PyLong_FromLong(indexBuffer[i * 3 + 2]);
		PyObject * triangle = PyTuple_Pack(3, a, b, c);
		PyList_SET_ITEM(trianglesList, i, triangle);
	}

	return PyTuple_Pack(2, vertexList, trianglesList);
}

PyMethodDef methods[] = {
	{"quick_hull", (PyCFunction)meth_quick_hull, METH_VARARGS, 0},
	{0},
};

#if PY_MAJOR_VERSION >= 3

PyModuleDef moduledef = {
	PyModuleDef_HEAD_INIT,
	"hull",
	0,
	-1,
	methods,
	0,
	0,
	0,
	0,
};

PyObject * InitializeGLWindow(PyObject * module) {
	return module;
}

extern "C" PyObject * PyInit_hull() {
	PyObject * module = PyModule_Create(&moduledef);
	return InitializeGLWindow(module);
}

#else

extern "C" PyObject * inithull() {
	PyObject * module = Py_InitModule("hull", methods);
	return InitializeGLWindow(module);
}

#endif
