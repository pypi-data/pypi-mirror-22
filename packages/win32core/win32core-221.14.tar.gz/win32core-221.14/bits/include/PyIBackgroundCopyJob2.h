// This file declares the IBackgroundCopyJob2 Interface for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

#include "PyIBackgroundCopyJob.h"

class PyIBackgroundCopyJob2 : public PyIBackgroundCopyJob
{
public:
	MAKE_PYCOM_CTOR(PyIBackgroundCopyJob2);
	static IBackgroundCopyJob2 *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
	static PyObject *SetNotifyCmdLine(PyObject *self, PyObject *args);
	static PyObject *GetNotifyCmdLine(PyObject *self, PyObject *args);
	static PyObject *GetReplyProgress(PyObject *self, PyObject *args);
	static PyObject *GetReplyData(PyObject *self, PyObject *args);
	static PyObject *SetReplyFileName(PyObject *self, PyObject *args);
	static PyObject *GetReplyFileName(PyObject *self, PyObject *args);
	static PyObject *SetCredentials(PyObject *self, PyObject *args);

protected:
	PyIBackgroundCopyJob2(IUnknown *pdisp);
	~PyIBackgroundCopyJob2();
};
