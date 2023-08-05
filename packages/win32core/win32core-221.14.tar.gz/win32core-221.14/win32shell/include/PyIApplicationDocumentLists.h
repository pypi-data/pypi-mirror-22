// Requires Windows 7 SDK to build
#if WINVER >= 0x0601

// This file declares the IApplicationDocumentLists Interface for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyIApplicationDocumentLists : public PyIUnknown
{
public:
	MAKE_PYCOM_CTOR(PyIApplicationDocumentLists);
	static IApplicationDocumentLists *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
	static PyObject *SetAppID(PyObject *self, PyObject *args);
	static PyObject *GetList(PyObject *self, PyObject *args);

protected:
	PyIApplicationDocumentLists(IUnknown *pdisp);
	~PyIApplicationDocumentLists();
};

#endif // WINVER