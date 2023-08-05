// This file implements the IActiveScriptSiteDebug Interface and Gateway for Python.
// Generated by makegw.py

#include "stdafx.h"
#include "PyIActiveScriptSiteDebug.h"

// @doc - This file contains autoduck documentation
// ---------------------------------------------------
//
// Interface Implementation

PyIActiveScriptSiteDebug::PyIActiveScriptSiteDebug(IUnknown *pdisp):
	PyIUnknown(pdisp)
{
	ob_type = &type;
}

PyIActiveScriptSiteDebug::~PyIActiveScriptSiteDebug()
{
}

/* static */ IActiveScriptSiteDebug *PyIActiveScriptSiteDebug::GetI(PyObject *self)
{
	return (IActiveScriptSiteDebug *)PyIUnknown::GetI(self);
}

// @pymethod |PyIActiveScriptSiteDebug|GetDocumentContextFromPosition|Description of GetDocumentContextFromPosition.
PyObject *PyIActiveScriptSiteDebug::GetDocumentContextFromPosition(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	IActiveScriptSiteDebug *pIASSD = GetI(self);
	if ( pIASSD == NULL )
		return NULL;
	// @pyparm int|dwSourceContext||Description for dwSourceContext
	// @pyparm int|uCharacterOffset||Description for uCharacterOffset
	// @pyparm int|uNumChars||Description for uNumChars
	DWORD dwSourceContext;
	ULONG uCharacterOffset;
	ULONG uNumChars;
	IDebugDocumentContext *ppsc;
	if ( !PyArg_ParseTuple(args, "iii:GetDocumentContextFromPosition", &dwSourceContext, &uCharacterOffset, &uNumChars) )
		return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIASSD->GetDocumentContextFromPosition( dwSourceContext, uCharacterOffset, uNumChars, &ppsc );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	return PyCom_PyObjectFromIUnknown(ppsc, IID_IDebugDocumentContext, FALSE);
}

// @pymethod |PyIActiveScriptSiteDebug|GetApplication|Description of GetApplication.
PyObject *PyIActiveScriptSiteDebug::GetApplication(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	IActiveScriptSiteDebug *pIASSD = GetI(self);
	if ( pIASSD == NULL )
		return NULL;
	IDebugApplication *ppda;
	if ( !PyArg_ParseTuple(args, ":GetApplication") )
		return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIASSD->GetApplication( &ppda );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	return PyCom_PyObjectFromIUnknown(ppda, IID_IDebugApplication, FALSE);
}

// @pymethod |PyIActiveScriptSiteDebug|GetRootApplicationNode|Description of GetRootApplicationNode.
PyObject *PyIActiveScriptSiteDebug::GetRootApplicationNode(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	IActiveScriptSiteDebug *pIASSD = GetI(self);
	if ( pIASSD == NULL )
		return NULL;
	IDebugApplicationNode *ppdan;
	if ( !PyArg_ParseTuple(args, ":GetRootApplicationNode") )
		return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIASSD->GetRootApplicationNode( &ppdan );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	return PyCom_PyObjectFromIUnknown(ppdan, IID_IDebugApplicationNode, FALSE);
}

// @pymethod int, int|PyIActiveScriptSiteDebug|OnScriptErrorDebug|Allows a smart host to control the handling of runtime errors
// @rdesc The result is a tuple of (bCallDebugger, bCallOnScriptErrorWhenContinuing)
PyObject *PyIActiveScriptSiteDebug::OnScriptErrorDebug(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	IActiveScriptSiteDebug *pIASSD = GetI(self);
	if ( pIASSD == NULL )
		return NULL;
	PyObject *obad;
	if ( !PyArg_ParseTuple(args, "O:OnScriptErrorDebug", &obad) )
		return NULL;
	IActiveScriptErrorDebug *pad;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obad, IID_IActiveScriptErrorDebug, (void **)&pad, FALSE /* bNoneOK */))
		return NULL;
	BOOL bEnterDebugger, bCallOnError;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIASSD->OnScriptErrorDebug( pad, &bEnterDebugger, &bCallOnError );
	if (pad) pad->Release();
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	return Py_BuildValue("ii", bEnterDebugger, bCallOnError);
}

// @object PyIActiveScriptSiteDebug|Description of the interface
static struct PyMethodDef PyIActiveScriptSiteDebug_methods[] =
{
	{ "GetDocumentContextFromPosition", PyIActiveScriptSiteDebug::GetDocumentContextFromPosition, 1 }, // @pymeth GetDocumentContextFromPosition|Description of GetDocumentContextFromPosition
	{ "GetApplication", PyIActiveScriptSiteDebug::GetApplication, 1 }, // @pymeth GetApplication|Description of GetApplication
	{ "GetRootApplicationNode", PyIActiveScriptSiteDebug::GetRootApplicationNode, 1 }, // @pymeth GetRootApplicationNode|Description of GetRootApplicationNode
	{ "OnScriptErrorDebug", PyIActiveScriptSiteDebug::OnScriptErrorDebug, 1 }, // @pymeth OnScriptErrorDebug|Allows a smart host to control the handling of runtime errors
	{ NULL }
};

PyComTypeObject PyIActiveScriptSiteDebug::type("PyIActiveScriptSiteDebug",
		&PyIUnknown::type,
		sizeof(PyIActiveScriptSiteDebug),
		PyIActiveScriptSiteDebug_methods,
		GET_PYCOM_CTOR(PyIActiveScriptSiteDebug));
// ---------------------------------------------------
//
// Gateway Implementation

STDMETHODIMP PyGActiveScriptSiteDebug::GetDocumentContextFromPosition(
#ifdef _WIN64
		/* [in] */ DWORDLONG dwSourceContext,
#else
		/* [in] */ DWORD dwSourceContext,
#endif
		/* [in] */ ULONG uCharacterOffset,
		/* [in] */ ULONG uNumChars,
		/* [out] */ IDebugDocumentContext __RPC_FAR *__RPC_FAR * ppsc)
{
	PY_GATEWAY_METHOD;
	if (ppsc==NULL) return E_POINTER;
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("GetDocumentContextFromPosition", &result, "iii", dwSourceContext, uCharacterOffset, uNumChars);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	PyObject *obppsc;
	if (!PyArg_Parse(result, "O" , &obppsc)) return PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obppsc, IID_IDebugDocumentContext, (void **)ppsc, FALSE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) hr = PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGActiveScriptSiteDebug::GetApplication(
		/* [out] */ IDebugApplication __RPC_FAR *__RPC_FAR * ppda)
{
	PY_GATEWAY_METHOD;
	if (ppda==NULL) return E_POINTER;
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("GetApplication", &result);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	PyObject *obppda;
	if (!PyArg_Parse(result, "O" , &obppda)) return PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obppda, IID_IDebugApplication, (void **)ppda, FALSE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) hr = PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGActiveScriptSiteDebug::GetRootApplicationNode(
		/* [out] */ IDebugApplicationNode __RPC_FAR *__RPC_FAR * ppda)
{
	PY_GATEWAY_METHOD;
	if (ppda==NULL) return E_POINTER;
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("GetRootApplicationNode", &result);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	PyObject *obppda;
	if (!PyArg_Parse(result, "O" , &obppda)) return PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obppda, IID_IDebugApplicationNode, (void **)ppda, TRUE ))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) hr = PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	Py_DECREF(result);
	return hr;
}


STDMETHODIMP PyGActiveScriptSiteDebug::OnScriptErrorDebug(
		/* [in] */ IActiveScriptErrorDebug __RPC_FAR * pErrorDebug,
		/* [out] */ BOOL __RPC_FAR * pfEnterDebugger,
		/* [out] */ BOOL __RPC_FAR * pfCallOnScriptErrorWhenContinuing)
{
	PY_GATEWAY_METHOD;
	PyObject *obpErrorDebug;
	obpErrorDebug = PyCom_PyObjectFromIUnknown(pErrorDebug, IID_IActiveScriptErrorDebug, TRUE);
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("OnScriptErrorDebug", &result, "O", obpErrorDebug);
	Py_XDECREF(obpErrorDebug);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	if (!PyArg_ParseTuple(result, "ii" , pfEnterDebugger, pfCallOnScriptErrorWhenContinuing)) return PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	Py_DECREF(result);
	return hr;
}
