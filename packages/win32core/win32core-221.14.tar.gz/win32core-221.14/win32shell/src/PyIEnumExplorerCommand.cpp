// This file implements the IEnumExplorerCommand Interface and Gateway for Python.
// Generated by makegw.py

#include "shell_pch.h"
#include "PyIEnumExplorerCommand.h"

// @doc - This file contains autoduck documentation

// ---------------------------------------------------
//
// Interface Implementation

PyIEnumExplorerCommand::PyIEnumExplorerCommand(IUnknown *pdisp):
	PyIUnknown(pdisp)
{
	ob_type = &type;
}

PyIEnumExplorerCommand::~PyIEnumExplorerCommand()
{
}

/* static */ IEnumExplorerCommand *PyIEnumExplorerCommand::GetI(PyObject *self)
{
	return (IEnumExplorerCommand *)PyIUnknown::GetI(self);
}

// @pymethod object|PyIEnumExplorerCommand|Next|Retrieves a specified number of items in the enumeration sequence.
PyObject *PyIEnumExplorerCommand::Next(PyObject *self, PyObject *args)
{
	long celt = 1;
	// @pyparm int|num|1|Number of items to retrieve.
	if ( !PyArg_ParseTuple(args, "|l:Next", &celt) )
		return NULL;

	IEnumExplorerCommand *pIEExplorerCommand = GetI(self);
	if ( pIEExplorerCommand == NULL )
		return NULL;

	IExplorerCommand **rgVar = new IExplorerCommand *[celt];
	if ( rgVar == NULL ) {
		PyErr_SetString(PyExc_MemoryError, "allocating result ExplorerCommands");
		return NULL;
	}

	int i;
/*	for ( i = celt; i--; )
		// *** possibly init each structure element???
*/

	ULONG celtFetched = 0;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIEExplorerCommand->Next(celt, rgVar, &celtFetched);
	PY_INTERFACE_POSTCALL;
	if (  HRESULT_CODE(hr) != ERROR_NO_MORE_ITEMS && FAILED(hr) )
	{
		delete [] rgVar;
		return PyCom_BuildPyException(hr, pIEExplorerCommand, IID_IEnumExplorerCommand);
	}

	PyObject *result = PyTuple_New(celtFetched);
	if ( result != NULL )
	{
		for ( i = celtFetched; i--; )
		{
			PyObject *ob = PyCom_PyObjectFromIUnknown(rgVar[i], IID_IExplorerCommand, FALSE);
			rgVar[i] = NULL;
			if ( ob == NULL )
			{
				Py_DECREF(result);
				result = NULL;
				break;
			}
			PyTuple_SET_ITEM(result, i, ob);
		}
	}
	for ( i = celtFetched; i--; ) PYCOM_RELEASE(rgVar[i]);
	delete [] rgVar;
	return result;
}

// @pymethod |PyIEnumExplorerCommand|Skip|Skips over the next specified elementes.
PyObject *PyIEnumExplorerCommand::Skip(PyObject *self, PyObject *args)
{
	long celt;
	if ( !PyArg_ParseTuple(args, "l:Skip", &celt) )
		return NULL;

	IEnumExplorerCommand *pIEExplorerCommand = GetI(self);
	if ( pIEExplorerCommand == NULL )
		return NULL;

	PY_INTERFACE_PRECALL;
	HRESULT hr = pIEExplorerCommand->Skip(celt);
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIEExplorerCommand, IID_IEnumExplorerCommand);

	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod |PyIEnumExplorerCommand|Reset|Resets the enumeration sequence to the beginning.
PyObject *PyIEnumExplorerCommand::Reset(PyObject *self, PyObject *args)
{
	if ( !PyArg_ParseTuple(args, ":Reset") )
		return NULL;

	IEnumExplorerCommand *pIEExplorerCommand = GetI(self);
	if ( pIEExplorerCommand == NULL )
		return NULL;

	PY_INTERFACE_PRECALL;
	HRESULT hr = pIEExplorerCommand->Reset();
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIEExplorerCommand, IID_IEnumExplorerCommand);

	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod <o PyIEnumExplorerCommand>|PyIEnumExplorerCommand|Clone|Creates another enumerator that contains the same enumeration state as the current one
PyObject *PyIEnumExplorerCommand::Clone(PyObject *self, PyObject *args)
{
	if ( !PyArg_ParseTuple(args, ":Clone") )
		return NULL;

	IEnumExplorerCommand *pIEExplorerCommand = GetI(self);
	if ( pIEExplorerCommand == NULL )
		return NULL;

	IEnumExplorerCommand *pClone;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIEExplorerCommand->Clone(&pClone);
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIEExplorerCommand, IID_IEnumExplorerCommand);

	return PyCom_PyObjectFromIUnknown(pClone, IID_IEnumExplorerCommand, FALSE);
}

// @object PyIEnumExplorerCommand|A Python interface to IEnumExplorerCommand
static struct PyMethodDef PyIEnumExplorerCommand_methods[] =
{
	{ "Next", PyIEnumExplorerCommand::Next, 1 },    // @pymeth Next|Retrieves a specified number of items in the enumeration sequence.
	{ "Skip", PyIEnumExplorerCommand::Skip, 1 },	// @pymeth Skip|Skips over the next specified elementes.
	{ "Reset", PyIEnumExplorerCommand::Reset, 1 },	// @pymeth Reset|Resets the enumeration sequence to the beginning.
	{ "Clone", PyIEnumExplorerCommand::Clone, 1 },	// @pymeth Clone|Creates another enumerator that contains the same enumeration state as the current one.
	{ NULL }
};

PyComEnumTypeObject PyIEnumExplorerCommand::type("PyIEnumExplorerCommand",
		&PyIUnknown::type,
		sizeof(PyIEnumExplorerCommand),
		PyIEnumExplorerCommand_methods,
		GET_PYCOM_CTOR(PyIEnumExplorerCommand));

// ---------------------------------------------------
//
// Gateway Implementation

// Std delegation
/*
STDMETHODIMP_(ULONG) PyGEnumExplorerCommand::AddRef(void) {return PyGatewayBase::AddRef();}
STDMETHODIMP_(ULONG) PyGEnumExplorerCommand::Release(void) {return PyGatewayBase::Release();}
STDMETHODIMP PyGEnumExplorerCommand::QueryInterface(REFIID iid, void ** obj) {return PyGatewayBase::QueryInterface(iid, obj);}
STDMETHODIMP PyGEnumExplorerCommand::GetTypeInfoCount(UINT FAR* pctInfo) {return PyGatewayBase::GetTypeInfoCount(pctInfo);}
STDMETHODIMP PyGEnumExplorerCommand::GetTypeInfo(UINT itinfo, LCID lcid, ITypeInfo FAR* FAR* pptInfo) {return PyGatewayBase::GetTypeInfo(itinfo, lcid, pptInfo);}
STDMETHODIMP PyGEnumExplorerCommand::GetIDsOfNames(REFIID refiid, OLECHAR FAR* FAR* rgszNames, UINT cNames, LCID lcid, DISPID FAR* rgdispid) {return PyGatewayBase::GetIDsOfNames( refiid, rgszNames, cNames, lcid, rgdispid);}
STDMETHODIMP PyGEnumExplorerCommand::Invoke(DISPID dispid, REFIID riid, LCID lcid, WORD wFlags, DISPPARAMS FAR* params, VARIANT FAR* pVarResult, EXCEPINFO FAR* pexcepinfo, UINT FAR* puArgErr) {return PyGatewayBase::Invoke( dispid, riid, lcid, wFlags, params, pVarResult, pexcepinfo, puArgErr);}
 */
STDMETHODIMP PyGEnumExplorerCommand::Next( 
            /* [in] */ ULONG celt,
            /* [length_is][size_is][out] */ IExplorerCommand __RPC_FAR * __RPC_FAR *rgVar,
            /* [out] */ ULONG __RPC_FAR *pCeltFetched)
{
	PY_GATEWAY_METHOD;
	PyObject *result;
	Py_ssize_t len;
	HRESULT hr = InvokeViaPolicy("Next", &result, "i", celt);
	if ( FAILED(hr) )
		return hr;

	if ( !PySequence_Check(result) )
		goto error;
	len = PyObject_Length(result);
	if ( len == -1 )
		goto error;
	if ( len > (int)celt)
		len = celt;
	if ( pCeltFetched )
		*pCeltFetched = (ULONG)len;
	int i;
	for ( i = 0; i < len; ++i )
	{
		PyObject *ob = PySequence_GetItem(result, i);
		if ( ob == NULL )
			goto error;

		if ( !PyCom_InterfaceFromPyObject(ob, IID_IExplorerCommand, (void **)&rgVar[i], FALSE) )
		{
			Py_DECREF(result);
			return MAKE_PYCOM_GATEWAY_FAILURE_CODE("Next");
		}
	}
	Py_DECREF(result);
	return len < (int)celt ? S_FALSE : S_OK;
  error:
	PyErr_Clear();	// just in case
	Py_DECREF(result);
	return PyCom_SetCOMErrorFromSimple(E_FAIL, IID_IEnumExplorerCommand, "Next() did not return a sequence of objects");
}

STDMETHODIMP PyGEnumExplorerCommand::Skip( 
            /* [in] */ ULONG celt)
{
	PY_GATEWAY_METHOD;
	return InvokeViaPolicy("Skip", NULL, "i", celt);
}

STDMETHODIMP PyGEnumExplorerCommand::Reset(void)
{
	PY_GATEWAY_METHOD;
	return InvokeViaPolicy("Reset");
}

STDMETHODIMP PyGEnumExplorerCommand::Clone( 
            /* [out] */ IEnumExplorerCommand __RPC_FAR *__RPC_FAR *ppEnum)
{
	PY_GATEWAY_METHOD;
	PyObject * result;
	HRESULT hr = InvokeViaPolicy("Clone", &result);
	if ( FAILED(hr) )
		return hr;

	/*
	** Make sure we have the right kind of object: we should have some kind
	** of IUnknown subclass wrapped into a PyIUnknown instance.
	*/
	if ( !PyIBase::is_object(result, &PyIUnknown::type) )
	{
		/* the wrong kind of object was returned to us */
		Py_DECREF(result);
		return PyCom_SetCOMErrorFromSimple(E_FAIL, IID_IEnumExplorerCommand);
	}

	/*
	** Get the IUnknown out of the thing. note that the Python ob maintains
	** a reference, so we don't have to explicitly AddRef() here.
	*/
	IUnknown *punk = ((PyIUnknown *)result)->m_obj;
	if ( !punk )
	{
		/* damn. the object was released. */
		Py_DECREF(result);
		return PyCom_SetCOMErrorFromSimple(E_FAIL, IID_IEnumExplorerCommand);
	}

	/*
	** Get the interface we want. note it is returned with a refcount.
	** This QI is actually going to instantiate a PyGEnumExplorerCommand.
	*/
	hr = punk->QueryInterface(IID_IEnumExplorerCommand, (LPVOID *)ppEnum);

	/* done with the result; this DECREF is also for <punk> */
	Py_DECREF(result);

	return PyCom_SetCOMErrorFromSimple(hr, IID_IEnumExplorerCommand, "Python could not convert the result from Next() into the required COM interface");
}
