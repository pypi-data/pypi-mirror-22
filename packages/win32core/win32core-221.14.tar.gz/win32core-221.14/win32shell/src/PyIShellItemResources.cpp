// This file implements the IShellItemResources Interface and Gateway for Python.
// Generated by makegw.py

#include "shell_pch.h"
#include "PyIShellItemResources.h"

// @doc - This file contains autoduck documentation
// ---------------------------------------------------
//
// Interface Implementation

PyIShellItemResources::PyIShellItemResources(IUnknown *pdisp):
	PyIUnknown(pdisp)
{
	ob_type = &type;
}

PyIShellItemResources::~PyIShellItemResources()
{
}

/* static */ IShellItemResources *PyIShellItemResources::GetI(PyObject *self)
{
	return (IShellItemResources *)PyIUnknown::GetI(self);
}

// @pymethod |PyIShellItemResources|GetAttributes|Description of GetAttributes.
PyObject *PyIShellItemResources::GetAttributes(PyObject *self, PyObject *args)
{
	IShellItemResources *pISIR = GetI(self);
	if ( pISIR == NULL )
		return NULL;
	DWORD dwAttributes;
	if ( !PyArg_ParseTuple(args, ":GetAttributes") )
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pISIR->GetAttributes( &dwAttributes );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pISIR, IID_IShellItemResources );
	return PyLong_FromUnsignedLong(dwAttributes);
}

// @pymethod int|PyIShellItemResources|GetSize|Description of GetSize.
PyObject *PyIShellItemResources::GetSize(PyObject *self, PyObject *args)
{
	IShellItemResources *pISIR = GetI(self);
	if ( pISIR == NULL )
		return NULL;
	ULONGLONG ullSize;
	if ( !PyArg_ParseTuple(args, ":GetSize"))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pISIR->GetSize(&ullSize );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pISIR, IID_IShellItemResources );
	return PyLong_FromUnsignedLongLong(ullSize);
}

// @pymethod |PyIShellItemResources|GetTimes|Description of GetTimes.
PyObject *PyIShellItemResources::GetTimes(PyObject *self, PyObject *args)
{
	IShellItemResources *pISIR = GetI(self);
	if ( pISIR == NULL )
		return NULL;
	FILETIME ftCreation;
	FILETIME ftWrite;
	FILETIME ftAccess;
	if ( !PyArg_ParseTuple(args, ":GetTimes") )
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pISIR->GetTimes( &ftCreation, &ftWrite, &ftAccess );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pISIR, IID_IShellItemResources );
	return Py_BuildValue("NNN",
		PyWinObject_FromFILETIME(ftCreation),
		PyWinObject_FromFILETIME(ftWrite),
		PyWinObject_FromFILETIME(ftAccess));
}

// @pymethod |PyIShellItemResources|SetTimes|Description of SetTimes.
PyObject *PyIShellItemResources::SetTimes(PyObject *self, PyObject *args)
{
	IShellItemResources *pISIR = GetI(self);
	if ( pISIR == NULL )
		return NULL;
	// @pyparm <o PyTime>|pftCreation||Description for pftCreation
	// @pyparm <o PyTime>|pftWrite||Description for pftWrite
	// @pyparm <o PyTime>|pftAccess||Description for pftAccess
	FILETIME ftCreation;
	FILETIME ftWrite;
	FILETIME ftAccess;
	if ( !PyArg_ParseTuple(args, "O&O&O&:SetTimes", 
		PyWinObject_AsFILETIME, &ftCreation,
		PyWinObject_AsFILETIME, &ftWrite,
		PyWinObject_AsFILETIME, &ftAccess))
		return NULL;

	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pISIR->SetTimes( &ftCreation, &ftWrite, &ftAccess );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pISIR, IID_IShellItemResources );
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod |PyIShellItemResources|GetResourceDescription|Description of GetResourceDescription.
PyObject *PyIShellItemResources::GetResourceDescription(PyObject *self, PyObject *args)
{
	IShellItemResources *pISIR = GetI(self);
	if ( pISIR == NULL )
		return NULL;
	SHELL_ITEM_RESOURCE sir;
	PyObject *obpcsir;
	// @pyparm <o PySHELL_ITEM_RESOURCE>|pcsir||Description for pcsir
	LPWSTR pszDescription;
	if ( !PyArg_ParseTuple(args, "O:GetResourceDescription", &obpcsir))
		return NULL;
	if (!PyWinObject_AsSHELL_ITEM_RESOURCE( obpcsir, &sir ))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pISIR->GetResourceDescription(&sir, &pszDescription );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pISIR, IID_IShellItemResources );
	PyObject *ret = PyWinObject_FromWCHAR(pszDescription);
	CoTaskMemFree(pszDescription);	// ??? Docs don't specify how it should be freed ???
	return ret;
}

// @pymethod <o PyIEnumResources>|PyIShellItemResources|EnumResources|Description of EnumResources.
PyObject *PyIShellItemResources::EnumResources(PyObject *self, PyObject *args)
{
	IShellItemResources *pISIR = GetI(self);
	if ( pISIR == NULL )
		return NULL;
	IEnumResources *penumr;
	if ( !PyArg_ParseTuple(args, ":EnumResources"))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pISIR->EnumResources(&penumr);
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pISIR, IID_IShellItemResources);
	return PyCom_PyObjectFromIUnknown(penumr, IID_IEnumResources, FALSE);
}

// @pymethod boolean|PyIShellItemResources|SupportsResource|Description of SupportsResource.
PyObject *PyIShellItemResources::SupportsResource(PyObject *self, PyObject *args)
{
	IShellItemResources *pISIR = GetI(self);
	if ( pISIR == NULL )
		return NULL;
	SHELL_ITEM_RESOURCE sir;
	PyObject *obpcsir;
	// @pyparm <o PySHELL_ITEM_RESOURCE>|pcsir||Description for pcsir
	if ( !PyArg_ParseTuple(args, "O:SupportsResource", &obpcsir) )
		return NULL;
	if (!PyWinObject_AsSHELL_ITEM_RESOURCE( obpcsir, &sir ))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pISIR->SupportsResource(&sir);
	PY_INTERFACE_POSTCALL;
	return PyBool_FromLong(hr == S_OK);
}

// @pymethod <o PyIUnknown>|PyIShellItemResources|OpenResource|Description of OpenResource.
PyObject *PyIShellItemResources::OpenResource(PyObject *self, PyObject *args)
{
	IShellItemResources *pISIR = GetI(self);
	if ( pISIR == NULL )
		return NULL;
	SHELL_ITEM_RESOURCE sir;
	PyObject *obpcsir;
	// @pyparm <o PySHELL_ITEM_RESOURCE>|pcsir||Description for pcsir
	// @pyparm <o PyIID>|riid||The interface to return
	void *pv;
	IID riid;
	if ( !PyArg_ParseTuple(args, "OO&:OpenResource", &obpcsir, PyWinObject_AsIID, &riid))
		return NULL;
	if (!PyWinObject_AsSHELL_ITEM_RESOURCE( obpcsir, &sir ))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pISIR->OpenResource(&sir, riid, &pv );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pISIR, IID_IShellItemResources );
	return PyCom_PyObjectFromIUnknown((IUnknown *)pv, riid, FALSE);
}

// @pymethod interface|PyIShellItemResources|CreateResource|Description of CreateResource.
PyObject *PyIShellItemResources::CreateResource(PyObject *self, PyObject *args)
{
	IShellItemResources *pISIR = GetI(self);
	if ( pISIR == NULL )
		return NULL;
	SHELL_ITEM_RESOURCE sir;
	PyObject *obpcsir;
	// @pyparm <o PySHELL_ITEM_RESOURCE>|sir||Resource identifier
	// @pyparm <o PyIID>|riid||The interface to return
	void *pv;
	IID riid;
	if ( !PyArg_ParseTuple(args, "OO&:CreateResource", &obpcsir, PyWinObject_AsIID, &riid))
		return NULL;
	if (!PyWinObject_AsSHELL_ITEM_RESOURCE( obpcsir, &sir ))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pISIR->CreateResource(&sir, riid, &pv );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pISIR, IID_IShellItemResources );
	return PyCom_PyObjectFromIUnknown((IUnknown *)pv, riid, FALSE);
}

// @pymethod |PyIShellItemResources|MarkForDelete|Description of MarkForDelete.
PyObject *PyIShellItemResources::MarkForDelete(PyObject *self, PyObject *args)
{
	IShellItemResources *pISIR = GetI(self);
	if ( pISIR == NULL )
		return NULL;
	if ( !PyArg_ParseTuple(args, ":MarkForDelete") )
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pISIR->MarkForDelete( );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pISIR, IID_IShellItemResources );
	Py_INCREF(Py_None);
	return Py_None;
}

// @object PyIShellItemResources|Description of the interface
static struct PyMethodDef PyIShellItemResources_methods[] =
{
	{ "GetAttributes", PyIShellItemResources::GetAttributes, 1 }, // @pymeth GetAttributes|Description of GetAttributes
	{ "GetSize", PyIShellItemResources::GetSize, 1 }, // @pymeth GetSize|Description of GetSize
	{ "GetTimes", PyIShellItemResources::GetTimes, 1 }, // @pymeth GetTimes|Description of GetTimes
	{ "SetTimes", PyIShellItemResources::SetTimes, 1 }, // @pymeth SetTimes|Description of SetTimes
	{ "GetResourceDescription", PyIShellItemResources::GetResourceDescription, 1 }, // @pymeth GetResourceDescription|Description of GetResourceDescription
	{ "EnumResources", PyIShellItemResources::EnumResources, 1 }, // @pymeth EnumResources|Description of EnumResources
	{ "SupportsResource", PyIShellItemResources::SupportsResource, 1 }, // @pymeth SupportsResource|Description of SupportsResource
	{ "OpenResource", PyIShellItemResources::OpenResource, 1 }, // @pymeth OpenResource|Description of OpenResource
	{ "CreateResource", PyIShellItemResources::CreateResource, 1 }, // @pymeth CreateResource|Description of CreateResource
	{ "MarkForDelete", PyIShellItemResources::MarkForDelete, 1 }, // @pymeth MarkForDelete|Description of MarkForDelete
	{ NULL }
};

PyComTypeObject PyIShellItemResources::type("PyIShellItemResources",
		&PyIUnknown::type,
		sizeof(PyIShellItemResources),
		PyIShellItemResources_methods,
		GET_PYCOM_CTOR(PyIShellItemResources));
// ---------------------------------------------------
//
// Gateway Implementation
STDMETHODIMP PyGShellItemResources::GetAttributes(
		/* [out] */ DWORD * pdwAttributes)
{
	PY_GATEWAY_METHOD;
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("GetAttributes", &result);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	*pdwAttributes = PyLong_AsUnsignedLong(result);
	if (*pdwAttributes == -1 && PyErr_Occurred())
		hr = MAKE_PYCOM_GATEWAY_FAILURE_CODE("GetAttributes");
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGShellItemResources::GetSize(
		/* [out] */ ULONGLONG * pullSize)
{
	PY_GATEWAY_METHOD;
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("GetSize", &result);
	if (FAILED(hr)) return hr;
	*pullSize = PyLong_AsUnsignedLongLong(result);
	if (*pullSize == -1 && PyErr_Occurred())
		hr = MAKE_PYCOM_GATEWAY_FAILURE_CODE("GetSize");
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGShellItemResources::GetTimes(
		/* [out] */ FILETIME * pftCreation,
		/* [out] */ FILETIME * pftWrite,
		/* [out] */ FILETIME * pftAccess)
{
	PY_GATEWAY_METHOD;
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("GetTimes", &result);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	if (!PyArg_ParseTuple(result, "O&O&O&" ,
		PyWinObject_AsFILETIME, pftCreation,
		PyWinObject_AsFILETIME, pftWrite,
		PyWinObject_AsFILETIME, pftAccess))
		hr = MAKE_PYCOM_GATEWAY_FAILURE_CODE("GetTimes");
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGShellItemResources::SetTimes(
		/* [in] */ const FILETIME * pftCreation,
		/* [in] */ const FILETIME * pftWrite,
		/* [in] */ const FILETIME * pftAccess)
{
	PY_GATEWAY_METHOD;
	HRESULT hr=InvokeViaPolicy("SetTimes", NULL, "NNN",
		PyWinObject_FromFILETIME(*pftCreation),
		PyWinObject_FromFILETIME(*pftWrite),
		PyWinObject_FromFILETIME(*pftAccess));
	return hr;
}

STDMETHODIMP PyGShellItemResources::GetResourceDescription(
		/* [in] */ const SHELL_ITEM_RESOURCE * pcsir,
		/* [out] */ LPWSTR * ppszDescription)
{
	PY_GATEWAY_METHOD;
	PyObject *obpcsir = PyWinObject_FromSHELL_ITEM_RESOURCE(pcsir);
	if (obpcsir==NULL) return MAKE_PYCOM_GATEWAY_FAILURE_CODE("GetResourceDescription");
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("GetResourceDescription", &result, "O", obpcsir);
	Py_DECREF(obpcsir);
	if (FAILED(hr)) return hr;
	// ??? Docs do not specify memory semantics, but this seems to work ... ???
	if (!PyWinObject_AsTaskAllocatedWCHAR(result, ppszDescription, FALSE))
		hr = MAKE_PYCOM_GATEWAY_FAILURE_CODE("GetResourceDescription");
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGShellItemResources::EnumResources(
		IEnumResources ** ppenumr)
{
	PY_GATEWAY_METHOD;
	if (ppenumr==NULL) return E_POINTER;
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("EnumResources", &result);
	if (FAILED(hr)) return hr;
	if (!PyCom_InterfaceFromPyObject(result, IID_IEnumResources, (void **)ppenumr, FALSE))
		hr = MAKE_PYCOM_GATEWAY_FAILURE_CODE("EnumResources");
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGShellItemResources::SupportsResource(
		/* [in] */ const SHELL_ITEM_RESOURCE * pcsir)
{
	PY_GATEWAY_METHOD;
	PyObject *obpcsir = PyWinObject_FromSHELL_ITEM_RESOURCE(pcsir);
	if (obpcsir==NULL) return MAKE_PYCOM_GATEWAY_FAILURE_CODE("SupportsResource");
	HRESULT hr=InvokeViaPolicy("SupportsResource", NULL, "O", obpcsir);
	Py_DECREF(obpcsir);
	return hr;
}

STDMETHODIMP PyGShellItemResources::OpenResource(
		/* [in] */ const SHELL_ITEM_RESOURCE * pcsir,
		/* [in] */ REFIID riid,
		/* [out] */ void ** ppv)
{
	PY_GATEWAY_METHOD;
	PyObject *obpcsir = PyWinObject_FromSHELL_ITEM_RESOURCE(pcsir);
	if (obpcsir==NULL) return MAKE_PYCOM_GATEWAY_FAILURE_CODE("OpenResource");
	if (ppv==NULL) return E_POINTER;
	PyObject *obriid;
	obriid = PyWinObject_FromIID(riid);
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("OpenResource", &result, "OO", obpcsir, obriid);
	Py_DECREF(obpcsir);
	Py_XDECREF(obriid);
	if (FAILED(hr)) return hr;
	if (!PyCom_InterfaceFromPyObject(result, riid, ppv, FALSE))
		hr = MAKE_PYCOM_GATEWAY_FAILURE_CODE("OpenResource");
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGShellItemResources::CreateResource(
		/* [in] */ const SHELL_ITEM_RESOURCE * pcsir,
		/* [in] */ REFIID riid,
		/* [out] */ void ** ppv)
{
	PY_GATEWAY_METHOD;
	PyObject *obpcsir = PyWinObject_FromSHELL_ITEM_RESOURCE(pcsir);
	if (obpcsir==NULL) return MAKE_PYCOM_GATEWAY_FAILURE_CODE("CreateResource");
	if (ppv==NULL) return E_POINTER;
	PyObject *obriid;
	obriid = PyWinObject_FromIID(riid);
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("CreateResource", &result, "OO", obpcsir, obriid);
	Py_DECREF(obpcsir);
	Py_XDECREF(obriid);
	if (FAILED(hr)) return hr;
	if (!PyCom_InterfaceFromPyObject(result, riid, ppv, FALSE))
		hr = MAKE_PYCOM_GATEWAY_FAILURE_CODE("OpenResource");
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGShellItemResources::MarkForDelete(
		void)
{
	PY_GATEWAY_METHOD;
	HRESULT hr=InvokeViaPolicy("MarkForDelete", NULL);
	return hr;
}

