// This file implements the IOleInPlaceFrame Interface and Gateway for Python.
// Generated by makegw.py

#include "axcontrol_pch.h"
#include "PyIOleWindow.h"
#include "PyIOleInPlaceUIWindow.h"
#include "PyIOleInPlaceFrame.h"
#include "PyComTypeObjects.h"

// @doc - This file contains autoduck documentation
// ---------------------------------------------------
//
// Interface Implementation

PyIOleInPlaceFrame::PyIOleInPlaceFrame(IUnknown *pdisp):
	PyIOleInPlaceUIWindow(pdisp)
{
	ob_type = &type;
}

PyIOleInPlaceFrame::~PyIOleInPlaceFrame()
{
}

/* static */ IOleInPlaceFrame *PyIOleInPlaceFrame::GetI(PyObject *self)
{
	return (IOleInPlaceFrame *)PyIOleInPlaceUIWindow::GetI(self);
}

// @pymethod |PyIOleInPlaceFrame|InsertMenus|Description of InsertMenus.
PyObject *PyIOleInPlaceFrame::InsertMenus(PyObject *self, PyObject *args)
{
	IOleInPlaceFrame *pIOIPF = GetI(self);
	if ( pIOIPF == NULL )
		return NULL;
	// @pyparm int/long|hmenuShared||Description for hmenuShared
	// @pyparm <o PyOLEMENUGROUPWIDTHS>|menuWidths||
	OLEMENUGROUPWIDTHS menuWidths;
	PyObject *oblpMenuWidths;
	PyObject *obhmenuShared;
	HMENU hmenuShared;
	if ( !PyArg_ParseTuple(args, "OO:InsertMenus", &obhmenuShared, &oblpMenuWidths) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (bPythonIsHappy && !PyWinObject_AsHANDLE(obhmenuShared, (HANDLE *)&hmenuShared)) bPythonIsHappy = FALSE;
	if (bPythonIsHappy && !PyObject_AsOLEMENUGROUPWIDTHS( oblpMenuWidths, &menuWidths )) bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIOIPF->InsertMenus( hmenuShared, &menuWidths);
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIOIPF, IID_IOleInPlaceFrame);
	return PyObject_FromOLEMENUGROUPWIDTHS(&menuWidths);
}

// @pymethod |PyIOleInPlaceFrame|SetMenu|Description of SetMenu.
PyObject *PyIOleInPlaceFrame::SetMenu(PyObject *self, PyObject *args)
{
	IOleInPlaceFrame *pIOIPF = GetI(self);
	if ( pIOIPF == NULL )
		return NULL;
	// @pyparm int/long|hmenuShared||Description for hmenuShared
	// @pyparm int/long|holemenu||Description for holemenu
	// @pyparm int/long|hwndActiveObject||Description for hwndActiveObject
	PyObject *obhmenuShared;
	PyObject *obholemenu;
	PyObject *obhwndActiveObject;
	HMENU hmenuShared;
	HOLEMENU holemenu;
	HWND hwndActiveObject;
	if ( !PyArg_ParseTuple(args, "OOO:SetMenu", &obhmenuShared, &obholemenu, &obhwndActiveObject) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (bPythonIsHappy && !PyWinObject_AsHANDLE(obhmenuShared, (HANDLE *)&hmenuShared)) bPythonIsHappy = FALSE;
	if (bPythonIsHappy && !PyWinObject_AsHANDLE(obholemenu, (HANDLE *)&holemenu)) bPythonIsHappy = FALSE;
	if (bPythonIsHappy && !PyWinObject_AsHANDLE(obhwndActiveObject, (HANDLE *)&hwndActiveObject)) bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIOIPF->SetMenu( hmenuShared, holemenu, hwndActiveObject );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIOIPF, IID_IOleInPlaceFrame );
	Py_INCREF(Py_None);
	return Py_None;

}

// @pymethod |PyIOleInPlaceFrame|RemoveMenus|Description of RemoveMenus.
PyObject *PyIOleInPlaceFrame::RemoveMenus(PyObject *self, PyObject *args)
{
	IOleInPlaceFrame *pIOIPF = GetI(self);
	if ( pIOIPF == NULL )
		return NULL;
	// @pyparm int/long|hmenuShared||Description for hmenuShared
	PyObject *obhmenuShared;
	HMENU hmenuShared;
	if ( !PyArg_ParseTuple(args, "O:RemoveMenus", &obhmenuShared) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (bPythonIsHappy && !PyWinObject_AsHANDLE(obhmenuShared, (HANDLE *)&hmenuShared)) bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIOIPF->RemoveMenus( hmenuShared );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIOIPF, IID_IOleInPlaceFrame );
	Py_INCREF(Py_None);
	return Py_None;

}

// @pymethod |PyIOleInPlaceFrame|SetStatusText|Description of SetStatusText.
PyObject *PyIOleInPlaceFrame::SetStatusText(PyObject *self, PyObject *args)
{
	IOleInPlaceFrame *pIOIPF = GetI(self);
	if ( pIOIPF == NULL )
		return NULL;
	// @pyparm <o unicode>|pszStatusText||Description for pszStatusText
	PyObject *obpszStatusText;
	LPOLESTR pszStatusText;
	if ( !PyArg_ParseTuple(args, "O:SetStatusText", &obpszStatusText) )
		return NULL;
	BOOL bPythonIsHappy = TRUE;
	if (bPythonIsHappy && !PyWinObject_AsBstr(obpszStatusText, &pszStatusText)) bPythonIsHappy = FALSE;
	if (!bPythonIsHappy) return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIOIPF->SetStatusText( pszStatusText );
	SysFreeString(pszStatusText);
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIOIPF, IID_IOleInPlaceFrame );
	Py_INCREF(Py_None);
	return Py_None;

}

// @pymethod |PyIOleInPlaceFrame|EnableModeless|Description of EnableModeless.
PyObject *PyIOleInPlaceFrame::EnableModeless(PyObject *self, PyObject *args)
{
	IOleInPlaceFrame *pIOIPF = GetI(self);
	if ( pIOIPF == NULL )
		return NULL;
	// @pyparm int|fEnable||Description for fEnable
	BOOL fEnable;
	if ( !PyArg_ParseTuple(args, "i:EnableModeless", &fEnable) )
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIOIPF->EnableModeless( fEnable );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIOIPF, IID_IOleInPlaceFrame );
	Py_INCREF(Py_None);
	return Py_None;

}

// @pymethod |PyIOleInPlaceFrame|TranslateAccelerator|Description of TranslateAccelerator.
PyObject *PyIOleInPlaceFrame::TranslateAccelerator(PyObject *self, PyObject *args)
{
	IOleInPlaceFrame *pIOIPF = GetI(self);
	if ( pIOIPF == NULL )
		return NULL;
	PyObject *oblpmsg;
	// @pyparm <o PyMSG>|lpmsg||Description for lpmsg
	// @pyparm int|wID||Description for wID
	WORD wID;
	if ( !PyArg_ParseTuple(args, "Oh:TranslateAccelerator", &oblpmsg, &wID) )
		return NULL;
	MSG msg;
	if (!PyWinObject_AsMSG(oblpmsg, &msg))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIOIPF->TranslateAccelerator(&msg, wID);
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIOIPF, IID_IOleInPlaceFrame );
	Py_INCREF(Py_None);
	return Py_None;

}

// @object PyIOleInPlaceFrame|Description of the interface
static struct PyMethodDef PyIOleInPlaceFrame_methods[] =
{
	{ "InsertMenus", PyIOleInPlaceFrame::InsertMenus, 1 }, // @pymeth InsertMenus|Description of InsertMenus
	{ "SetMenu", PyIOleInPlaceFrame::SetMenu, 1 }, // @pymeth SetMenu|Description of SetMenu
	{ "RemoveMenus", PyIOleInPlaceFrame::RemoveMenus, 1 }, // @pymeth RemoveMenus|Description of RemoveMenus
	{ "SetStatusText", PyIOleInPlaceFrame::SetStatusText, 1 }, // @pymeth SetStatusText|Description of SetStatusText
	{ "EnableModeless", PyIOleInPlaceFrame::EnableModeless, 1 }, // @pymeth EnableModeless|Description of EnableModeless
	{ "TranslateAccelerator", PyIOleInPlaceFrame::TranslateAccelerator, 1 }, // @pymeth TranslateAccelerator|Description of TranslateAccelerator
	{ NULL }
};

PyComTypeObject PyIOleInPlaceFrame::type("PyIOleInPlaceFrame",
		&PyIOleInPlaceUIWindow::type,
		sizeof(PyIOleInPlaceFrame),
		PyIOleInPlaceFrame_methods,
		GET_PYCOM_CTOR(PyIOleInPlaceFrame));
// ---------------------------------------------------
//
// Gateway Implementation
// IOleWindow
STDMETHODIMP PyGOleInPlaceFrame::GetWindow(HWND __RPC_FAR * phwnd) {return PyGOleWindow::GetWindow(phwnd);}
STDMETHODIMP PyGOleInPlaceFrame::ContextSensitiveHelp(BOOL fEnterMode) {return PyGOleWindow::ContextSensitiveHelp(fEnterMode);}

// IOleInPlaceUIWindow
STDMETHODIMP PyGOleInPlaceFrame::GetBorder(LPRECT lpr)
	{return PyGOleInPlaceUIWindow::GetBorder(lpr);}

STDMETHODIMP PyGOleInPlaceFrame::RequestBorderSpace(LPCBORDERWIDTHS pbw)
	{return PyGOleInPlaceUIWindow::RequestBorderSpace(pbw);}

STDMETHODIMP PyGOleInPlaceFrame::SetBorderSpace(LPCBORDERWIDTHS pbw)
	{return PyGOleInPlaceUIWindow::SetBorderSpace(pbw);}

STDMETHODIMP PyGOleInPlaceFrame::SetActiveObject(IOleInPlaceActiveObject * pActiveObject, LPCOLESTR pszObjName)
	{return PyGOleInPlaceUIWindow::SetActiveObject(pActiveObject, pszObjName);}

// IOleInPlaceFrame
STDMETHODIMP PyGOleInPlaceFrame::InsertMenus(
		/* [in] */ HMENU hmenuShared,
		/* [out][in] */ LPOLEMENUGROUPWIDTHS lpMenuWidths)
{
	PY_GATEWAY_METHOD;
	PyObject *result;
	HRESULT hr=InvokeViaPolicy("InsertMenus", &result, "NN",
				   PyWinLong_FromHANDLE(hmenuShared),
				   PyObject_FromOLEMENUGROUPWIDTHS(lpMenuWidths));
	if (FAILED(hr)) return hr;
	PyObject_AsOLEMENUGROUPWIDTHS(result, lpMenuWidths);
	Py_DECREF(result);
	return MAKE_PYCOM_GATEWAY_FAILURE_CODE("InsertMenus");
}

STDMETHODIMP PyGOleInPlaceFrame::SetMenu(
		/* [in] */ HMENU hmenuShared,
		/* [in] */ HOLEMENU holemenu,
		/* [in] */ HWND hwndActiveObject)
{
	PY_GATEWAY_METHOD;
	return InvokeViaPolicy("SetMenu", NULL, "NNN",
				   PyWinLong_FromHANDLE(hmenuShared),
				   PyWinLong_FromHANDLE(holemenu),
				   PyWinLong_FromHANDLE(hwndActiveObject));
}

STDMETHODIMP PyGOleInPlaceFrame::RemoveMenus(
		/* [in] */ HMENU hmenuShared)
{
	PY_GATEWAY_METHOD;
	return InvokeViaPolicy("RemoveMenus", NULL, "N", PyWinLong_FromHANDLE(hmenuShared));
}

STDMETHODIMP PyGOleInPlaceFrame::SetStatusText(
		/* [unique][in] */ LPCOLESTR pszStatusText)
{
	PY_GATEWAY_METHOD;
	return InvokeViaPolicy("SetStatusText", NULL, "N", MakeOLECHARToObj(pszStatusText));
}

STDMETHODIMP PyGOleInPlaceFrame::EnableModeless(
		/* [in] */ BOOL fEnable)
{
	PY_GATEWAY_METHOD;
	return InvokeViaPolicy("EnableModeless", NULL, "i", fEnable);
}

STDMETHODIMP PyGOleInPlaceFrame::TranslateAccelerator(
		/* [in] */ LPMSG lpmsg,
		/* [in] */ WORD wID)
{
	PY_GATEWAY_METHOD;
	return InvokeViaPolicy("TranslateAccelerator", NULL, "Nh", PyWinObject_FromMSG(lpmsg), &wID);
}

