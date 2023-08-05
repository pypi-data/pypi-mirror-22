// This file declares the IEnumObjects Interface for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyIEnumObjects : public PyIUnknown
{
public:
	MAKE_PYCOM_CTOR(PyIEnumObjects);
	static IEnumObjects *GetI(PyObject *self);
	static PyComEnumTypeObject type;

	// The Python methods
	static PyObject *Next(PyObject *self, PyObject *args);
	static PyObject *Skip(PyObject *self, PyObject *args);
	static PyObject *Reset(PyObject *self, PyObject *args);
	static PyObject *Clone(PyObject *self, PyObject *args);


protected:
	PyIEnumObjects(IUnknown *pdisp);
	~PyIEnumObjects();
};
