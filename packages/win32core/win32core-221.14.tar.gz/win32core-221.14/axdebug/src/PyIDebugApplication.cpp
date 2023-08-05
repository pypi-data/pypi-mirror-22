// This file implements the IDebugApplication Interface and Gateway for Python.
// Generated by makegw.py

#include "stdafx.h"
#include "PyIRemoteDebugApplication.h"
#include "PyIDebugApplication.h"

// @doc - This file contains autoduck documentation
// ---------------------------------------------------
//
// Interface Implementation

PyIDebugApplication::PyIDebugApplication(IUnknown *pdisp):
	PyIRemoteDebugApplication(pdisp)
{
	ob_type = &type;
}

PyIDebugApplication::~PyIDebugApplication()
{
}

/* static */ IDebugApplication *PyIDebugApplication::GetI(PyObject *self)
{
	return (IDebugApplication *)PyIRemoteDebugApplication::GetI(self);
}

// @pymethod |PyIDebugApplication|SetName|Sets the name of the application.
PyObject *PyIDebugApplication::SetName(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	// @comm The provided name will be returned in subsequent calls  
	// to >om PyIRemoteDebugApplication.GetName>.
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	// @pyparm <o unicode>|pstrName||The name of the application.
	PyObject *obpstrName;
	BSTR pstrName;
	if ( !PyArg_ParseTuple(args, "O:SetName", &obpstrName) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_BstrFromPyObject(obpstrName, &pstrName)) bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->SetName( pstrName );
	PY_INTERFACE_POSTCALL;
	if (pstrName) SysFreeString(pstrName);
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod |PyIDebugApplication|StepOutComplete|Called by language engines, in single step mode, just before they return to their caller.
PyObject *PyIDebugApplication::StepOutComplete(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	// @comm The process debug manager uses this opportunity to notify all  
	// other script engines that they should break at the first opportunity. This is how  
	// cross language step modes are implemented. 
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	if ( !PyArg_ParseTuple(args, ":StepOutComplete") )
		return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->StepOutComplete( );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod |PyIDebugApplication|DebugOutput|Causes the given string to be displayed by the debugger IDE, normally in an output window.
PyObject *PyIDebugApplication::DebugOutput(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	// @comm  This mechanism provides the means for a language engine to implement language  
	// specific debugging output support. Example: Debug.writeln("Help") in JavaScript.  
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	// @pyparm <o unicode>|pstr||Description for pstr
	PyObject *obpstr;
	BSTR pstr;
	if ( !PyArg_ParseTuple(args, "O:DebugOutput", &obpstr) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_BstrFromPyObject(obpstr, &pstr)) bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->DebugOutput( pstr );
	PY_INTERFACE_POSTCALL;
	if (pstr) SysFreeString(pstr);
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod |PyIDebugApplication|StartDebugSession|Causes a default debugger IDE to be started and a debug session to be attached to  
// this application if one does not already exist.
PyObject *PyIDebugApplication::StartDebugSession(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	// @comm  This is used to implement just-in-time debugging. 
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	if ( !PyArg_ParseTuple(args, ":StartDebugSession") )
		return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->StartDebugSession( );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod int|PyIDebugApplication|HandleBreakPoint|Called by the language engine in the context of a thread that has hit a breakpoint.
PyObject *PyIDebugApplication::HandleBreakPoint(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	// @comm This method causes the current thread to block and a notification of the breakpoint  
	// to be sent to the debugger IDE. When the debugger IDE resumes the application this  
	// method returns with the action to be taken.  
	//  
	// Note: While in the breakpoint the language engine may be called in this thread to do  
	// various things such as enumerating stack frames or evaluating expressions.  

	// @rdesc The result is the break resume action - one of the BREAKRESUMEACTION contsants.

	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	// @pyparm int|br||Break reason - one of the BREAKREASON_* constants.
	BREAKREASON br;
	BREAKRESUMEACTION pbra;
	if ( !PyArg_ParseTuple(args, "i:HandleBreakPoint", &br) )
		return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->HandleBreakPoint( br, &pbra );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);

	PyObject *pyretval = Py_BuildValue("i", pbra);
	return pyretval;
}

// @pymethod |PyIDebugApplication|Close|Causes this application to release all references and enter a zombie state.
PyObject *PyIDebugApplication::Close(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	// @comm  Called by the owner of the application generally on shut down.  
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	if ( !PyArg_ParseTuple(args, ":Close") )
		return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->Close( );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod int|PyIDebugApplication|GetBreakFlags|Returns the current break flags for the application.
PyObject *PyIDebugApplication::GetBreakFlags(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	APPBREAKFLAGS pabf;
	IRemoteDebugApplicationThread *prdat;
	if ( !PyArg_ParseTuple(args, ":GetBreakFlags") )
		return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->GetBreakFlags( &pabf, &prdat );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	PyObject *obppcc = PyCom_PyObjectFromIUnknown(prdat, IID_IRemoteDebugApplicationThread, FALSE);
	if (obppcc==NULL)
		return NULL;
	PyObject *pyretval = Py_BuildValue("iO", pabf, obppcc);
	Py_DECREF(obppcc);
	return pyretval;
}

// @pymethod <o PyIDebugApplicationThread>|PyIDebugApplication|GetCurrentThread|Returns the application thread object associated with the currently running thread.
PyObject *PyIDebugApplication::GetCurrentThread(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	IDebugApplicationThread *pat;
	if ( !PyArg_ParseTuple(args, ":GetCurrentThread") )
		return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->GetCurrentThread( &pat );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	return PyCom_PyObjectFromIUnknown(pat, IID_IDebugApplicationThread, FALSE);
}

// @pymethod |PyIDebugApplication|CreateAsyncDebugOperation|Creates an IDebugAsyncOperation object to wrap a provided <o PyIDebugSyncOperation> object.
PyObject *PyIDebugApplication::CreateAsyncDebugOperation(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	// @comm This provides a mechanism for language engines to implement asynchronous expression and 
	// evaluation, etc. without having to know the details of synchronization with the 
	// debugger thread. See the descriptions for <o PyIDebugSyncOperation> and <o PyIDebugAsyncOperation> 
	// for more details.  
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	// @pyparm <o PyIDebugSyncOperation>|psdo||Description for psdo
	PyObject *obpsdo;
	IDebugSyncOperation *psdo;
	IDebugAsyncOperation *ppado;
	if ( !PyArg_ParseTuple(args, "O:CreateAsyncDebugOperation", &obpsdo) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obpsdo, IID_IDebugSyncOperation, (void **)&psdo, FALSE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->CreateAsyncDebugOperation( psdo, &ppado );
	psdo->Release();
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	return PyCom_PyObjectFromIUnknown(ppado, IID_IDebugAsyncOperation, FALSE);
}

// @pymethod int|PyIDebugApplication|AddStackFrameSniffer|Adds a stack frame sniffer to this application.
PyObject *PyIDebugApplication::AddStackFrameSniffer(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	// @comm Generally called by a language engine  
	// to expose its stack frames to the debugger. It is possible for other entities to  
	// expose stack frames.  
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	// @pyparm <o PyIDebugStackFrameSniffer>|pdsfs||Description for pdsfs
	PyObject *obpdsfs;
	IDebugStackFrameSniffer *pdsfs;
	DWORD pdwCookie;
	if ( !PyArg_ParseTuple(args, "O:AddStackFrameSniffer", &obpdsfs) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obpdsfs, IID_IDebugStackFrameSniffer, (void **)&pdsfs, FALSE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->AddStackFrameSniffer( pdsfs, &pdwCookie );
	pdsfs->Release();
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);

	PyObject *pyretval = Py_BuildValue("i", pdwCookie);
	return pyretval;
	// @rdesc The result is an integer cookie, to be passed to <om PyIDebugApplication.RemoveStackFrameSniffer>
}

// @pymethod |PyIDebugApplication|RemoveStackFrameSniffer|Removes a stack frame sniffer from this application.
PyObject *PyIDebugApplication::RemoveStackFrameSniffer(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	// @pyparm int|dwCookie||A cookie obtained from <om PyIDebugApplication.AddStackFrameSniffer>
	DWORD dwCookie;
	if ( !PyArg_ParseTuple(args, "i:RemoveStackFrameSniffer", &dwCookie) )
		return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->RemoveStackFrameSniffer( dwCookie );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod |PyIDebugApplication|QueryCurrentThreadIsDebuggerThread|Determines if the current running thread is the debugger thread. 
PyObject *PyIDebugApplication::QueryCurrentThreadIsDebuggerThread(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	if ( !PyArg_ParseTuple(args, ":QueryCurrentThreadIsDebuggerThread") )
		return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->QueryCurrentThreadIsDebuggerThread( );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	return PyInt_FromLong(hr);
	// @rdesc Returns S_OK if the current running thread is the debugger thread.  
	// Otherwise, returns S_FALSE.
}

// @pymethod |PyIDebugApplication|SynchronousCallInDebuggerThread|Provides a mechanism for the caller to run code in the debugger thread.
PyObject *PyIDebugApplication::SynchronousCallInDebuggerThread(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	// @comm This is generally  
	// used so that language engines and hosts can implement free threaded objects on top  
	// of their single threaded implementations.
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	// @pyparm <o PyIDebugThreadCall>|pptc||Description for pptc
	// @pyparm int|dwParam1||Description for dwParam1
	// @pyparm int|dwParam2||Description for dwParam2
	// @pyparm int|dwParam3||Description for dwParam3
	PyObject *obpptc;
	IDebugThreadCall *pptc;
	DWORD dwParam1;
	DWORD dwParam2;
	DWORD dwParam3;
	if ( !PyArg_ParseTuple(args, "Oiii:SynchronousCallInDebuggerThread", &obpptc, &dwParam1, &dwParam2, &dwParam3) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obpptc, IID_IDebugThreadCall, (void **)&pptc, FALSE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->SynchronousCallInDebuggerThread( pptc, dwParam1, dwParam2, dwParam3 );
	pptc->Release();
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod <o PyIDebugApplicationNode>|PyIDebugApplication|CreateApplicationNode|Creates a new application node which is associated with a specific document provider.
PyObject *PyIDebugApplication::CreateApplicationNode(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	// @comm Before it is visible, the new node must be  
	// attached to a parent node.
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	IDebugApplicationNode *pnode;
	if ( !PyArg_ParseTuple(args, ":CreateApplicationNode") )
		return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->CreateApplicationNode( &pnode );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	return PyCom_PyObjectFromIUnknown(pnode, IID_IDebugApplicationNode, FALSE);
}

// @pymethod |PyIDebugApplication|FireDebuggerEvent|Fire a generic event to the IApplicationDebugger (if any)
PyObject *PyIDebugApplication::FireDebuggerEvent(PyObject *self, PyObject *args)
{
	PY_INTERFACE_METHOD;
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	// @pyparm <o PyIIID>|guid||A GUID.
	// @pyparm <o PyIUnknown>|unknown||An unknown object.
	PyObject *obguid, *obunk;
	if ( !PyArg_ParseTuple(args, "OO:FireDebuggerEvent", &obguid, &obunk) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	IUnknown *punk;
	IID iid;
	if (!PyWinObject_AsIID(obguid, &iid))
		 bPythonIsHappy = FALSE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obunk, IID_IUnknown, (void **)&punk, FALSE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	PY_INTERFACE_PRECALL;
	HRESULT hr = pIDA->FireDebuggerEvent( iid, punk );
	punk->Release();
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return SetPythonCOMError(self,hr);
	Py_INCREF(Py_None);
	return Py_None;
}


// @pymethod |PyIDebugApplication|HandleRuntimeError|Description of HandleRuntimeError.
PyObject *PyIDebugApplication::HandleRuntimeError(PyObject *self, PyObject *args)
{
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	// @pyparm <o PyIActiveScriptErrorDebug>|pErrorDebug||Description for pErrorDebug
	// @pyparm <o PyIActiveScriptSite>|pScriptSite||Description for pScriptSite
	PyObject *obpErrorDebug;
	PyObject *obpScriptSite;
	IActiveScriptErrorDebug * pErrorDebug;
	IActiveScriptSite * pScriptSite;
	BREAKRESUMEACTION pbra;
	ERRORRESUMEACTION perra;
	BOOL pfCallOnScriptError;
	if ( !PyArg_ParseTuple(args, "OO:HandleRuntimeError", &obpErrorDebug, &obpScriptSite) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obpErrorDebug, IID_IActiveScriptErrorDebug, (void **)&pErrorDebug, TRUE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obpScriptSite, IID_IActiveScriptSite, (void **)&pScriptSite, TRUE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIDA->HandleRuntimeError( pErrorDebug, pScriptSite, &pbra, &perra, &pfCallOnScriptError );
	if (pErrorDebug) pErrorDebug->Release();
	if (pScriptSite) pScriptSite->Release();
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return OleSetOleError(hr);

	PyObject *pyretval = Py_BuildValue("iii", pbra, perra, pfCallOnScriptError);
	return pyretval;
}

// @pymethod |PyIDebugApplication|FCanJitDebug|Description of FCanJitDebug.
PyObject *PyIDebugApplication::FCanJitDebug(PyObject *self, PyObject *args)
{
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	if ( !PyArg_ParseTuple(args, ":FCanJitDebug") )
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIDA->FCanJitDebug( );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return OleSetOleError(hr);
	Py_INCREF(Py_None);
	return Py_None;

}

// @pymethod |PyIDebugApplication|FIsAutoJitDebugEnabled|Description of FIsAutoJitDebugEnabled.
PyObject *PyIDebugApplication::FIsAutoJitDebugEnabled(PyObject *self, PyObject *args)
{
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	if ( !PyArg_ParseTuple(args, ":FIsAutoJitDebugEnabled") )
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIDA->FIsAutoJitDebugEnabled( );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return OleSetOleError(hr);
	Py_INCREF(Py_None);
	return Py_None;

}

// @pymethod |PyIDebugApplication|AddGlobalExpressionContextProvider|Description of AddGlobalExpressionContextProvider.
PyObject *PyIDebugApplication::AddGlobalExpressionContextProvider(PyObject *self, PyObject *args)
{
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	// @pyparm <o PyIProvideExpressionContexts>|pdsfs||Description for pdsfs
	PyObject *obpdsfs;
	IProvideExpressionContexts * pdsfs;
#ifdef _WIN64
	DWORDLONG pdwCookie;
#else
	DWORD pdwCookie;
#endif
	if ( !PyArg_ParseTuple(args, "O:AddGlobalExpressionContextProvider", &obpdsfs) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obpdsfs, IID_IProvideExpressionContexts, (void **)&pdsfs, TRUE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIDA->AddGlobalExpressionContextProvider( pdsfs, &pdwCookie );
	if (pdsfs) pdsfs->Release();
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return OleSetOleError(hr);

	PyObject *pyretval = Py_BuildValue("i", pdwCookie);
	return pyretval;
}

// @pymethod |PyIDebugApplication|RemoveGlobalExpressionContextProvider|Description of RemoveGlobalExpressionContextProvider.
PyObject *PyIDebugApplication::RemoveGlobalExpressionContextProvider(PyObject *self, PyObject *args)
{
	IDebugApplication *pIDA = GetI(self);
	if ( pIDA == NULL )
		return NULL;
	// @pyparm int|dwCookie||Description for dwCookie
	DWORD dwCookie;
	if ( !PyArg_ParseTuple(args, "i:RemoveGlobalExpressionContextProvider", &dwCookie) )
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIDA->RemoveGlobalExpressionContextProvider( dwCookie );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return OleSetOleError(hr);
	Py_INCREF(Py_None);
	return Py_None;

}

// @object PyIDebugApplication|This interface is an extension of <o PyIRemoteDebugApplication>, exposing 
// non-remotable methods for use by language engines and hosts.
static struct PyMethodDef PyIDebugApplication_methods[] =
{
	{ "SetName", PyIDebugApplication::SetName, 1 }, // @pymeth SetName|Sets the name of the application.
	{ "StepOutComplete", PyIDebugApplication::StepOutComplete, 1 }, // @pymeth StepOutComplete|Called by language engines, in single step mode, just before they return to their caller.
	{ "DebugOutput", PyIDebugApplication::DebugOutput, 1 }, // @pymeth DebugOutput|Causes the given string to be displayed by the debugger IDE.  
	{ "StartDebugSession", PyIDebugApplication::StartDebugSession, 1 }, // @pymeth StartDebugSession|Causes a default debugger IDE to be started.
	{ "HandleBreakPoint", PyIDebugApplication::HandleBreakPoint, 1 }, // @pymeth HandleBreakPoint|Called by the language engine in the context of a thread that has hit a breakpoint.
	{ "Close", PyIDebugApplication::Close, 1 }, // @pymeth Close|Causes this application to release all references and enter a zombie state.
	{ "GetBreakFlags", PyIDebugApplication::GetBreakFlags, 1 }, // @pymeth GetBreakFlags|Returns the current break flags for the application.
	{ "GetCurrentThread", PyIDebugApplication::GetCurrentThread, 1 }, // @pymeth GetCurrentThread|Returns the application thread object associated with the currently running thread.
	{ "CreateAsyncDebugOperation", PyIDebugApplication::CreateAsyncDebugOperation, 1 }, // @pymeth CreateAsyncDebugOperation|Creates an IDebugAsyncOperation object to wrap a provided <o PyIDebugSyncOperation> object.
	{ "AddStackFrameSniffer", PyIDebugApplication::AddStackFrameSniffer, 1 }, // @pymeth AddStackFrameSniffer|Adds a stack frame sniffer to this application.
	{ "RemoveStackFrameSniffer", PyIDebugApplication::RemoveStackFrameSniffer, 1 }, // @pymeth RemoveStackFrameSniffer|Removes a stack frame sniffer from this application.
	{ "QueryCurrentThreadIsDebuggerThread", PyIDebugApplication::QueryCurrentThreadIsDebuggerThread, 1 }, // @pymeth QueryCurrentThreadIsDebuggerThread|Determines if the current running thread is the debugger thread. 
	{ "SynchronousCallInDebuggerThread", PyIDebugApplication::SynchronousCallInDebuggerThread, 1 }, // @pymeth SynchronousCallInDebuggerThread|Provides a mechanism for the caller to run code in the debugger thread.
	{ "CreateApplicationNode", PyIDebugApplication::CreateApplicationNode, 1 }, // @pymeth CreateApplicationNode|Creates a new application node which is associated with a specific document provider.
	{ "FireDebuggerEvent", PyIDebugApplication::FireDebuggerEvent, 1 }, // @pymeth FireDebuggerEvent|Fire a generic event to the IApplicationDebugger (if any)
	{ "HandleRuntimeError", PyIDebugApplication::HandleRuntimeError, 1 }, // @pymeth HandleRuntimeError|Description of HandleRuntimeError
	{ "FCanJitDebug", PyIDebugApplication::FCanJitDebug, 1 }, // @pymeth FCanJitDebug|Description of FCanJitDebug
	{ "FIsAutoJitDebugEnabled", PyIDebugApplication::FIsAutoJitDebugEnabled, 1 }, // @pymeth FIsAutoJitDebugEnabled|Description of FIsAutoJitDebugEnabled
	{ "AddGlobalExpressionContextProvider", PyIDebugApplication::AddGlobalExpressionContextProvider, 1 }, // @pymeth AddGlobalExpressionContextProvider|Description of AddGlobalExpressionContextProvider
	{ "RemoveGlobalExpressionContextProvider", PyIDebugApplication::RemoveGlobalExpressionContextProvider, 1 }, // @pymeth RemoveGlobalExpressionContextProvider|Description of RemoveGlobalExpressionContextProvider
	{ NULL }
};

PyComTypeObject PyIDebugApplication::type("PyIDebugApplication",
		&PyIRemoteDebugApplication::type,
		sizeof(PyIDebugApplication),
		PyIDebugApplication_methods,
		GET_PYCOM_CTOR(PyIDebugApplication));
// ---------------------------------------------------
//
// Gateway Implementation

// Std delegation

STDMETHODIMP PyGDebugApplication::ResumeFromBreakPoint(IRemoteDebugApplicationThread * prptFocus, BREAKRESUMEACTION bra, ERRORRESUMEACTION era) {return PyGRemoteDebugApplication::ResumeFromBreakPoint(prptFocus, bra, era);}
STDMETHODIMP PyGDebugApplication::CauseBreak(void) {return PyGRemoteDebugApplication::CauseBreak();}
STDMETHODIMP PyGDebugApplication::ConnectDebugger(IApplicationDebugger * pad) {return PyGRemoteDebugApplication::ConnectDebugger(pad);}
STDMETHODIMP PyGDebugApplication::DisconnectDebugger() {return PyGRemoteDebugApplication::DisconnectDebugger();}
STDMETHODIMP PyGDebugApplication::GetDebugger(IApplicationDebugger ** pad) {return PyGRemoteDebugApplication::GetDebugger(pad);}
STDMETHODIMP PyGDebugApplication::CreateInstanceAtApplication(REFCLSID rclsid,IUnknown * pUnkOuter,DWORD dwClsContext,REFIID riid,IUnknown ** ppvObject) {return PyGRemoteDebugApplication::CreateInstanceAtApplication(rclsid, pUnkOuter,dwClsContext,riid,ppvObject);}
STDMETHODIMP PyGDebugApplication::QueryAlive() {return PyGRemoteDebugApplication::QueryAlive();}
STDMETHODIMP PyGDebugApplication::EnumThreads(IEnumRemoteDebugApplicationThreads** pperdat) {return PyGRemoteDebugApplication::EnumThreads(pperdat);}
STDMETHODIMP PyGDebugApplication::GetName(BSTR * pbstrName) {return PyGRemoteDebugApplication::GetName(pbstrName);}
STDMETHODIMP PyGDebugApplication::GetRootNode(IDebugApplicationNode ** ppNode) {return PyGRemoteDebugApplication::GetRootNode(ppNode);}
STDMETHODIMP PyGDebugApplication::EnumGlobalExpressionContexts(IEnumDebugExpressionContexts **ppedec){return PyGRemoteDebugApplication::EnumGlobalExpressionContexts(ppedec);}

STDMETHODIMP PyGDebugApplication::SetName(
		/* [in] */ LPCOLESTR pstrName)
{
	PY_GATEWAY_METHOD;
	PyObject *obpstrName;
	obpstrName = PyWinObject_FromOLECHAR(pstrName);
	HRESULT hr=InvokeViaPolicy("SetName", NULL, "O", obpstrName);
	Py_XDECREF(obpstrName);
	return hr;
}

STDMETHODIMP PyGDebugApplication::StepOutComplete(
		void)
{
	PY_GATEWAY_METHOD;
	HRESULT hr=InvokeViaPolicy("StepOutComplete", NULL);
	return hr;
}

STDMETHODIMP PyGDebugApplication::DebugOutput(
		/* [in] */ LPCOLESTR pstr)
{
	PY_GATEWAY_METHOD;
	PyObject *obpstr;
	obpstr = PyWinObject_FromOLECHAR(pstr);
	HRESULT hr=InvokeViaPolicy("DebugOutput", NULL, "O", obpstr);
	Py_XDECREF(obpstr);
	return hr;
}

STDMETHODIMP PyGDebugApplication::StartDebugSession(
		void)
{
	PY_GATEWAY_METHOD;
	HRESULT hr=InvokeViaPolicy("StartDebugSession", NULL);
	return hr;
}

STDMETHODIMP PyGDebugApplication::HandleBreakPoint(
		/* [in] */ BREAKREASON br,
		/* [out] */ BREAKRESUMEACTION __RPC_FAR * pbra)
{
	PY_GATEWAY_METHOD;
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("HandleBreakPoint", &result, "i", br);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	if (!PyArg_Parse(result, "i" , pbra)) return PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGDebugApplication::Close(
		void)
{
	PY_GATEWAY_METHOD;
	HRESULT hr=InvokeViaPolicy("Close", NULL);
	return hr;
}

STDMETHODIMP PyGDebugApplication::GetBreakFlags(
		/* [out] */ APPBREAKFLAGS __RPC_FAR * pabf,
		/* [out] */ IRemoteDebugApplicationThread __RPC_FAR * __RPC_FAR *pprdatSteppingThread)
{
	PY_GATEWAY_METHOD;
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("GetBreakFlags", &result);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	PyObject *obrdat;
	if (!PyArg_Parse(result, "iO" , pabf, &obrdat)) return PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obrdat, IID_IRemoteDebugApplicationThread, (void **)pprdatSteppingThread, FALSE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) hr = PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGDebugApplication::GetCurrentThread(
		/* [out] */ IDebugApplicationThread __RPC_FAR *__RPC_FAR * pat)
{
	PY_GATEWAY_METHOD;
	if (pat==NULL) return E_POINTER;
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("GetCurrentThread", &result);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	PyObject *obpat;
	if (!PyArg_Parse(result, "O" , &obpat)) return PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obpat, IID_IDebugApplicationThread, (void **)pat, FALSE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) hr = PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGDebugApplication::CreateAsyncDebugOperation(
		/* [in] */ IDebugSyncOperation __RPC_FAR * psdo,
		/* [out] */ IDebugAsyncOperation __RPC_FAR *__RPC_FAR * ppado)
{
	PY_GATEWAY_METHOD;
	if (ppado==NULL) return E_POINTER;
	PyObject *obpsdo;
	obpsdo = PyCom_PyObjectFromIUnknown(psdo, IID_IDebugSyncOperation, TRUE);
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("CreateAsyncDebugOperation", &result, "O", obpsdo);
	Py_XDECREF(obpsdo);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	PyObject *obppado;
	if (!PyArg_Parse(result, "O" , &obppado)) return PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obppado, IID_IDebugAsyncOperation, (void **)ppado, FALSE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) hr = PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGDebugApplication::AddStackFrameSniffer(
		/* [in] */ IDebugStackFrameSniffer __RPC_FAR * pdsfs,
		/* [out] */ DWORD __RPC_FAR * pdwCookie)
{
	PY_GATEWAY_METHOD;
	PyObject *obpdsfs;
	obpdsfs = PyCom_PyObjectFromIUnknown(pdsfs, IID_IDebugStackFrameSniffer, TRUE);
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("AddStackFrameSniffer", &result, "O", obpdsfs);
	Py_XDECREF(obpdsfs);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	if (!PyArg_Parse(result, "i" , pdwCookie)) return PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGDebugApplication::RemoveStackFrameSniffer(
		/* [in] */ DWORD dwCookie)
{
	PY_GATEWAY_METHOD;
	HRESULT hr=InvokeViaPolicy("RemoveStackFrameSniffer", NULL, "i", dwCookie);
	return hr;
}

STDMETHODIMP PyGDebugApplication::QueryCurrentThreadIsDebuggerThread(
		void)
{
	PY_GATEWAY_METHOD;
	HRESULT hr=InvokeViaPolicy("QueryCurrentThreadIsDebuggerThread", NULL);
	return hr;
}

STDMETHODIMP PyGDebugApplication::SynchronousCallInDebuggerThread(
		/* [in] */ IDebugThreadCall __RPC_FAR * pptc,
#ifdef _WIN64
		/* [in] */ DWORDLONG dwParam1,
		/* [in] */ DWORDLONG dwParam2,
		/* [in] */ DWORDLONG dwParam3)
#else
		/* [in] */ DWORD dwParam1,
		/* [in] */ DWORD dwParam2,
		/* [in] */ DWORD dwParam3)
#endif
{
	PY_GATEWAY_METHOD;
	PyObject *obpptc;
	obpptc = PyCom_PyObjectFromIUnknown(pptc, IID_IDebugThreadCall, TRUE);
	HRESULT hr=InvokeViaPolicy("SynchronousCallInDebuggerThread", NULL, "Oiii", obpptc, dwParam1, dwParam2, dwParam3);
	Py_XDECREF(obpptc);
	return hr;
}

STDMETHODIMP PyGDebugApplication::CreateApplicationNode(  
		/* [out] */	IDebugApplicationNode **ppdanNew)
{
	PY_GATEWAY_METHOD;
	if (ppdanNew==NULL) return E_POINTER;
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("CreateApplicationNode", &result);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	PyObject *obnode;
	if (!PyArg_Parse(result, "O" , &obnode)) return PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	BOOL bPythonIsHappy = TRUE;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obnode, IID_IDebugApplicationNode, (void **)ppdanNew, FALSE /* bNoneOK */))
		 bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) hr = PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGDebugApplication::FireDebuggerEvent(
	/* [in]	*/ REFGUID riid,
	/* [in]	*/ IUnknown *punk)
{
	PY_GATEWAY_METHOD;
	if (punk==NULL) return E_POINTER;
	PyObject *obiid = PyWinObject_FromIID(riid);
	PyObject *obunk = PyCom_PyObjectFromIUnknown(punk, IID_IUnknown, TRUE);
	HRESULT hr=InvokeViaPolicy("CreateApplicationNode", NULL, "OO",obiid,obunk);
	Py_XDECREF(obiid);
	Py_XDECREF(obunk);
	return hr;
}

STDMETHODIMP PyGDebugApplication::HandleRuntimeError(
		/* [in] */ IActiveScriptErrorDebug __RPC_FAR * pErrorDebug,
		/* [in] */ IActiveScriptSite __RPC_FAR * pScriptSite,
		/* [out] */ BREAKRESUMEACTION __RPC_FAR * pbra,
		/* [out] */ ERRORRESUMEACTION __RPC_FAR * perra,
		/* [out] */ BOOL __RPC_FAR * pfCallOnScriptError)
{
	PY_GATEWAY_METHOD;
	PyObject *obpErrorDebug;
	PyObject *obpScriptSite;
	obpErrorDebug = PyCom_PyObjectFromIUnknown(pErrorDebug, IID_IActiveScriptErrorDebug, TRUE);
	obpScriptSite = PyCom_PyObjectFromIUnknown(pScriptSite, IID_IActiveScriptSite, TRUE);
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("HandleRuntimeError", &result, "OO", obpErrorDebug, obpScriptSite);
	Py_XDECREF(obpErrorDebug);
	Py_XDECREF(obpScriptSite);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	if (!PyArg_ParseTuple(result, "iii" , pbra, perra, pfCallOnScriptError)) return PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	Py_DECREF(result);
	return hr;
}

BOOL STDMETHODCALLTYPE PyGDebugApplication::FCanJitDebug(
		void)
{
	PY_GATEWAY_METHOD;
	HRESULT hr=InvokeViaPolicy("FCanJitDebug", NULL);
	if (FAILED(hr)) hr = FALSE;
	return hr;
}

BOOL STDMETHODCALLTYPE PyGDebugApplication::FIsAutoJitDebugEnabled(
		void)
{
	PY_GATEWAY_METHOD;
	HRESULT hr=InvokeViaPolicy("FIsAutoJitDebugEnabled", NULL);
	if (FAILED(hr)) hr = FALSE;
	return hr;
}

STDMETHODIMP PyGDebugApplication::AddGlobalExpressionContextProvider(
		/* [in] */ IProvideExpressionContexts __RPC_FAR * pdsfs,
#ifdef _WIN64
		/* [out] */ DWORDLONG __RPC_FAR * pdwCookie)
#else
		/* [out] */ DWORD __RPC_FAR * pdwCookie)
#endif
{
	PY_GATEWAY_METHOD;
	PyObject *obpdsfs;
	obpdsfs = PyCom_PyObjectFromIUnknown(pdsfs, IID_IProvideExpressionContexts, TRUE);
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("AddGlobalExpressionContextProvider", &result, "O", obpdsfs);
	Py_XDECREF(obpdsfs);
	if (FAILED(hr)) return hr;
	// Process the Python results, and convert back to the real params
	if (!PyArg_Parse(result, "i" , pdwCookie)) return PyCom_HandlePythonFailureToCOM(/*pexcepinfo*/);
	Py_DECREF(result);
	return hr;
}

STDMETHODIMP PyGDebugApplication::RemoveGlobalExpressionContextProvider(
#ifdef _WIN64
		/* [in] */ DWORDLONG dwCookie)
#else
		/* [in] */ DWORD dwCookie)
#endif
{
	PY_GATEWAY_METHOD;
	HRESULT hr=InvokeViaPolicy("RemoveGlobalExpressionContextProvider", NULL, "i", dwCookie);
	return hr;
}
