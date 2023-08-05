// This file declares the IPersistSerializedPropStorage Interface for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyIPersistSerializedPropStorage : public PyIUnknown
{
public:
	MAKE_PYCOM_CTOR(PyIPersistSerializedPropStorage);
	static IPersistSerializedPropStorage *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
	static PyObject *SetFlags(PyObject *self, PyObject *args);
	static PyObject *SetPropertyStorage(PyObject *self, PyObject *args);
	static PyObject *GetPropertyStorage(PyObject *self, PyObject *args);

protected:
	PyIPersistSerializedPropStorage(IUnknown *pdisp);
	~PyIPersistSerializedPropStorage();
};
