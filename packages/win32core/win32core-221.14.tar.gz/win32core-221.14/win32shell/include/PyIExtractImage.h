// This file declares the IExtractImage Interface for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyIExtractImage : public PyIUnknown
{
public:
	MAKE_PYCOM_CTOR(PyIExtractImage);
	static IExtractImage *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
	static PyObject *GetLocation(PyObject *self, PyObject *args);
	static PyObject *Extract(PyObject *self, PyObject *args);

protected:
	PyIExtractImage(IUnknown *pdisp);
	~PyIExtractImage();
};
