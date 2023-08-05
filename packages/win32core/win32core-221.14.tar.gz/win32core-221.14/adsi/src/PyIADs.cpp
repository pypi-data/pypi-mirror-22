// This file implements the IADs Interface and Gateway for Python.
// Generated by makegw.py
// This interface does not use SWIG, mainly so we can implement a custom
// getattr for the type.
// All "get_" methods have been exposed as properties.

#include "_win32com.h"
#include "PyADSIutil.h"
#include "PyIADs.h"

// @doc - This file contains autoduck documentation
// ---------------------------------------------------
//
// Interface Implementation

PyIADs::PyIADs(IUnknown *pdisp):
	PyIDispatch(pdisp)
{
	ob_type = &type;
}

PyIADs::~PyIADs()
{
}

/* static */ IADs *PyIADs::GetI(PyObject *self)
{
	return (IADs *)PyIDispatch::GetI(self);
}

// @pymethod |PyIADs|GetInfo|Description of GetInfo.
PyObject *PyIADs::GetInfo(PyObject *self, PyObject *args)
{
	IADs *pIAD = GetI(self);
	if ( pIAD == NULL )
		return NULL;
	if ( !PyArg_ParseTuple(args, ":GetInfo") )
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIAD->GetInfo( );

	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIAD, IID_IADs );
	Py_INCREF(Py_None);
	return Py_None;

}

// @pymethod |PyIADs|SetInfo|Description of SetInfo.
PyObject *PyIADs::SetInfo(PyObject *self, PyObject *args)
{
	IADs *pIAD = GetI(self);
	if ( pIAD == NULL )
		return NULL;
	if ( !PyArg_ParseTuple(args, ":SetInfo") )
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIAD->SetInfo( );

	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIAD, IID_IADs );
	Py_INCREF(Py_None);
	return Py_None;

}

// @pymethod object|PyIADs|Get|Description of Get.
// @rdesc The result is a Python object converted from a COM variant.  It
// may be an array, or any types supported by COM variant.
PyObject *PyIADs::Get(PyObject *self, PyObject *args)
{
	IADs *pIAD = GetI(self);
	if ( pIAD == NULL )
		return NULL;
	VARIANT val;
	VariantInit(&val);
	// @pyparm <o PyUnicode>|prop||The name of the property to fetch
	PyObject *obbstrName;
	BSTR bstrName;
	if ( !PyArg_ParseTuple(args, "O:Get", &obbstrName) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (bPythonIsHappy && !PyWinObject_AsBstr(obbstrName, &bstrName)) bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIAD->Get( bstrName, &val );
	SysFreeString(bstrName);
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIAD, IID_IADs );
	PyObject *ret = PyCom_PyObjectFromVariant(&val);
	{
	PY_INTERFACE_PRECALL;
	VariantClear(&val);
	PY_INTERFACE_POSTCALL;
	}
	return ret;
}

// @pymethod |PyIADs|Put|Description of Put.
PyObject *PyIADs::Put(PyObject *self, PyObject *args)
{
	IADs *pIAD = GetI(self);
	if ( pIAD == NULL )
		return NULL;
	// @pyparm <o PyUnicode>|property||The property name to set
	// @pyparm object|val||The value to set.
	PyObject *obbstrName;
	PyObject *obvProp;
	BSTR bstrName;
	VARIANT vProp;
	VariantInit(&vProp);
	if ( !PyArg_ParseTuple(args, "OO:Put", &obbstrName, &obvProp) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (bPythonIsHappy && !PyWinObject_AsBstr(obbstrName, &bstrName)) bPythonIsHappy = FALSE;
	if ( !PyCom_VariantFromPyObject(obvProp, &vProp) )
		bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIAD->Put( bstrName, vProp );
	SysFreeString(bstrName);
	VariantClear(&vProp);
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIAD, IID_IADs );
	Py_INCREF(Py_None);
	return Py_None;

}

/****
// @pymethod |PyIADs|GetEx|Description of GetEx.
PyObject *PyIADs::GetEx(PyObject *self, PyObject *args)
{
	IADs *pIAD = GetI(self);
	if ( pIAD == NULL )
		return NULL;
	// @pyparm <o unicode>|bstrName||Description for bstrName
// *** The input argument pvProp of type "VARIANT *" was not processed ***
//     Please check the conversion function is appropriate and exists!
	VARIANT * pvProp;
	PyObject *obpvProp;
	// @pyparm <o PyVARIANT *>|pvProp||Description for pvProp
	PyObject *obbstrName;
	BSTR bstrName;
	if ( !PyArg_ParseTuple(args, "OO:GetEx", &obbstrName, &obpvProp) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (bPythonIsHappy && !PyWinObject_AsBstr(obbstrName, &bstrName)) bPythonIsHappy = FALSE;
	if (bPythonIsHappy && !PyObject_AsVARIANT *( obpvProp, &pvProp )) bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIAD->GetEx( bstrName, pvProp );
	PyObject_FreeVARIANT *(pvProp);

	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIAD, IID_IADs );
// *** The output argument pvProp of type "VARIANT *" was not processed ***
//     The type 'VARIANT *' (pvProp) is unknown.
	Py_INCREF(Py_None);
	return Py_None;

}

// @pymethod |PyIADs|PutEx|Description of PutEx.
PyObject *PyIADs::PutEx(PyObject *self, PyObject *args)
{
	IADs *pIAD = GetI(self);
	if ( pIAD == NULL )
		return NULL;
	// @pyparm int|lnControlCode||Description for lnControlCode
	// @pyparm <o unicode>|bstrName||Description for bstrName
	// @pyparm <o PyVARIANT>|vProp||Description for vProp
	PyObject *obbstrName;
	PyObject *obvProp;
	long lnControlCode;
	BSTR bstrName;
	VARIANT vProp;
	if ( !PyArg_ParseTuple(args, "lOO:PutEx", &lnControlCode, &obbstrName, &obvProp) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (bPythonIsHappy && !PyWinObject_AsBstr(obbstrName, &bstrName)) bPythonIsHappy = FALSE;
	if ( !PyCom_VariantFromPyObject(obvProp, &vProp) )
		bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIAD->PutEx( lnControlCode, bstrName, vProp );

	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIAD, IID_IADs );
	Py_INCREF(Py_None);
	return Py_None;

}

// @pymethod |PyIADs|GetInfoEx|Description of GetInfoEx.
PyObject *PyIADs::GetInfoEx(PyObject *self, PyObject *args)
{
	IADs *pIAD = GetI(self);
	if ( pIAD == NULL )
		return NULL;
	// @pyparm <o PyVARIANT>|vProperties||Description for vProperties
	// @pyparm int|lnReserved||Description for lnReserved
	PyObject *obvProperties;
	VARIANT vProperties;
	long lnReserved;
	if ( !PyArg_ParseTuple(args, "Ol:GetInfoEx", &obvProperties, &lnReserved) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if ( !PyCom_VariantFromPyObject(obvProperties, &vProperties) )
		bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIAD->GetInfoEx( vProperties, lnReserved );

	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIAD, IID_IADs );
	Py_INCREF(Py_None);
	return Py_None;

}
***/
// @object PyIADs|An object representing the IADs interface.
// In most cases you can achieve the same result via IDispatch - however, this
// interface allows you get get and set properties without the IDispatch
// overhead.
static struct PyMethodDef PyIADs_methods[] =
{
	{ "GetInfo", PyIADs::GetInfo, 1 }, // @pymeth GetInfo|Description of GetInfo
	{ "SetInfo", PyIADs::SetInfo, 1 }, // @pymeth SetInfo|Description of SetInfo
	{ "Get", PyIADs::Get, 1 }, // @pymeth Get|Description of Get
	{ "Put", PyIADs::Put, 1 }, // @pymeth Put|Description of Put
	{ "get", PyIADs::Get, 1 }, // @pymeth get|Synonym for Get
	{ "put", PyIADs::Put, 1 }, // @pymeth put|Synonym for Put
	{ NULL }
};

PyObject* PyIADs_getattro(PyObject *ob, PyObject *obname)
{
	char *name = PYWIN_ATTR_CONVERT(obname);
	if (!name) return NULL;

	IADs *p = PyIADs::GetI(ob);
	
	// These are all BSTR values
	BSTR ret = NULL;
	HRESULT hr;
	BOOL bad = FALSE;
	Py_BEGIN_ALLOW_THREADS
	// docs refer to 'property' as AdsPath, but function is ADsPath
	// allow both
	// @prop <o PyUnicode>|ADsPath|
	// @prop <o PyUnicode>|AdsPath|Synonym for ADsPath
	if (strcmp(name, "AdsPath")==0 || strcmp(name, "ADsPath")==0)
		hr = p->get_ADsPath(&ret);
	// @prop <o PyUnicode>|Class|
	else if (strcmp(name, "Class")==0)
		hr = p->get_Class(&ret);
	// @prop <o PyUnicode>|GUID|Like the IADs method, this returns a string rather than a GUID object.
	else if (strcmp(name, "GUID")==0)
		hr = p->get_GUID(&ret);
	// @prop <o PyUnicode>|Name|
	else if (strcmp(name, "Name")==0)
		hr = p->get_Name(&ret);
	// @prop <o PyUnicode>|Parent|
	else if (strcmp(name, "Parent")==0)
		hr = p->get_Parent(&ret);
	// @prop <o PyUnicode>|Schema|
	else if (strcmp(name, "Schema")==0)
		hr = p->get_Schema(&ret);
	else
		bad = TRUE;
	Py_END_ALLOW_THREADS
	if (bad)
		return PyIBase::getattro(ob, obname);
	if (FAILED(hr))
		return PyCom_BuildPyException(hr, p, IID_IADs );
	PyObject *rc = MakeBstrToObj(ret);
	SysFreeString(ret);
	return rc;
}

PyComTypeObject PyIADs::type("PyIADs",
		&PyIDispatch::type,
		sizeof(PyIADs),
		PyIADs_methods,
		GET_PYCOM_CTOR(PyIADs));
