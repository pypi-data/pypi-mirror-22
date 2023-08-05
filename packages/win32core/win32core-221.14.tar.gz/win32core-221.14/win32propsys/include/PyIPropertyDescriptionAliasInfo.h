// This file declares the IPropertyDescriptionAliasInfo Interface and Gateway for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

#include "_win32com.h"
#include "PythonCOMServer.h"
#include "propsys.h"

class PyIPropertyDescriptionAliasInfo : public PyIPropertyDescription
{
public:
	MAKE_PYCOM_CTOR(PyIPropertyDescriptionAliasInfo);
	static IPropertyDescriptionAliasInfo *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
	static PyObject *GetSortByAlias(PyObject *self, PyObject *args);
	static PyObject *GetAdditionalSortByAliases(PyObject *self, PyObject *args);

protected:
	PyIPropertyDescriptionAliasInfo(IUnknown *pdisp);
	~PyIPropertyDescriptionAliasInfo();
};
