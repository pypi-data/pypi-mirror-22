// This file implements the ICustomDestinationList Interface for Python.
// Generated by makegw.py

#include "shell_pch.h"

// Requires Windows 7 SDK to build
#if WINVER >= 0x0601

#include "PyICustomDestinationList.h"

// @doc - This file contains autoduck documentation
// ---------------------------------------------------
//
// Interface Implementation

PyICustomDestinationList::PyICustomDestinationList(IUnknown *pdisp):
	PyIUnknown(pdisp)
{
	ob_type = &type;
}

PyICustomDestinationList::~PyICustomDestinationList()
{
}

/* static */ ICustomDestinationList *PyICustomDestinationList::GetI(PyObject *self)
{
	return (ICustomDestinationList *)PyIUnknown::GetI(self);
}

// @pymethod |PyICustomDestinationList|SetAppID|Specifies the taskbar identifier for the jump list
// @comm Only needed if the calling app doesn't use the system-assigned default
PyObject *PyICustomDestinationList::SetAppID(PyObject *self, PyObject *args)
{
	ICustomDestinationList *pICDL = GetI(self);
	if ( pICDL == NULL )
		return NULL;
	TmpWCHAR AppID;
	PyObject *obAppID;
	// @pyparm str|AppID||The taskbar identifier of the application
	if ( !PyArg_ParseTuple(args, "O:SetAppID", &obAppID) )
		return NULL;
	if (!PyWinObject_AsWCHAR(obAppID, &AppID ))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pICDL->SetAppID(AppID );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pICDL, IID_ICustomDestinationList );
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod int, <o PyIObjectArray>|PyICustomDestinationList|BeginList|Clears the jump list and prepares it to be repopulated
// @rdesc Returns the number of slots and a collection of all destinations removed from the jump list
PyObject *PyICustomDestinationList::BeginList(PyObject *self, PyObject *args)
{
	ICustomDestinationList *pICDL = GetI(self);
	if ( pICDL == NULL )
		return NULL;
	UINT slots;
	REFIID riid = IID_IObjectArray;
	// @pyparm <o PyIID>|riid|IID_IObjectArray|The interface to return
	void *pv;
	if ( !PyArg_ParseTuple(args, "|O&:BeginList", PyWinObject_AsIID, &riid))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pICDL->BeginList(&slots, riid, &pv);
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pICDL, IID_ICustomDestinationList );
	return Py_BuildValue("kN", slots, PyCom_PyObjectFromIUnknown((IUnknown *)pv, riid, FALSE));
}

// @pymethod |PyICustomDestinationList|AppendCategory|Adds a custom category to the jump list
PyObject *PyICustomDestinationList::AppendCategory(PyObject *self, PyObject *args)
{
	ICustomDestinationList *pICDL = GetI(self);
	if ( pICDL == NULL )
		return NULL;
	
	TmpWCHAR Category;
	PyObject *obCategory, *obItems;
	IObjectArray *Items;
	// @pyparm str|Category||Display name of the category, can also be a dll and resource id for localization
	// @pyparm <o PyIObjectArray>|Items||Collection of IShellItem and/or IShellLink interfaces
	if ( !PyArg_ParseTuple(args, "OO:AppendCategory", &obCategory, &obItems))
		return NULL;
	if (!PyWinObject_AsWCHAR(obCategory, &Category, FALSE))
		return NULL;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obItems, IID_IObjectArray, (void **)&Items, FALSE))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pICDL->AppendCategory(Category, Items);
	Items->Release();
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pICDL, IID_ICustomDestinationList );
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod |PyICustomDestinationList|AppendKnownCategory|Adds one of the predefined categories to the custom list
PyObject *PyICustomDestinationList::AppendKnownCategory(PyObject *self, PyObject *args)
{
	ICustomDestinationList *pICDL = GetI(self);
	if ( pICDL == NULL )
		return NULL;
	KNOWNDESTCATEGORY category;
	// @pyparm int|Category||shellcon.KDC_RECENT or KDC_FREQUENT
	if ( !PyArg_ParseTuple(args, "i:AppendKnownCategory", &category) )
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pICDL->AppendKnownCategory( category );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pICDL, IID_ICustomDestinationList );
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod |PyICustomDestinationList|AddUserTasks|Sets the entries shown in the Tasks category
PyObject *PyICustomDestinationList::AddUserTasks(PyObject *self, PyObject *args)
{
	ICustomDestinationList *pICDL = GetI(self);
	if ( pICDL == NULL )
		return NULL;
	PyObject *obItems;
	IObjectArray *Items;
	// @pyparm <o PyIObjectArray>|Items||Collection of <o PyIShellItem> and/or <o PyIShellLink> interfaces
	if ( !PyArg_ParseTuple(args, "O:AddUserTasks", &obItems))
		return NULL;
	if (!PyCom_InterfaceFromPyInstanceOrObject(obItems, IID_IObjectArray, (void **)&Items, FALSE))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pICDL->AddUserTasks(Items);
	Items->Release();
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pICDL, IID_ICustomDestinationList );
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod |PyICustomDestinationList|CommitList|Finalizes changes.
PyObject *PyICustomDestinationList::CommitList(PyObject *self, PyObject *args)
{
	ICustomDestinationList *pICDL = GetI(self);
	if ( pICDL == NULL )
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pICDL->CommitList( );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pICDL, IID_ICustomDestinationList );
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod <o PyIObjectArray>|PyICustomDestinationList|GetRemovedDestinations|Returns all the items removed from the jump list
PyObject *PyICustomDestinationList::GetRemovedDestinations(PyObject *self, PyObject *args)
{
	ICustomDestinationList *pICDL = GetI(self);
	if ( pICDL == NULL )
		return NULL;
	// @pyparm <o PyIID>|riid|IID_IObjectArray|The interface to return
	REFIID riid = IID_IObjectArray;
	void *pv;
	if ( !PyArg_ParseTuple(args, "|O&:GetRemovedDestinations", PyWinObject_AsIID, &riid))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pICDL->GetRemovedDestinations( riid, &pv );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pICDL, IID_ICustomDestinationList );
	return PyCom_PyObjectFromIUnknown((IUnknown *)pv, riid, FALSE);
}

// @pymethod |PyICustomDestinationList|DeleteList|Removes any customization, leaving only the system-maintained Recent and Frequent lists
PyObject *PyICustomDestinationList::DeleteList(PyObject *self, PyObject *args)
{
	ICustomDestinationList *pICDL = GetI(self);
	if ( pICDL == NULL )
		return NULL;
	TmpWCHAR AppID;
	PyObject *obAppID = Py_None;
	// @pyparm str|AppID|None|The taskbar identifier of the application
	if ( !PyArg_ParseTuple(args, "|O:DeleteList", &obAppID))
		return NULL;
	if (!PyWinObject_AsWCHAR(obAppID, &AppID, TRUE))
		return NULL;

	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pICDL->DeleteList(AppID);
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pICDL, IID_ICustomDestinationList );
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod |PyICustomDestinationList|AbortList|Discards all changes
PyObject *PyICustomDestinationList::AbortList(PyObject *self, PyObject *args)
{
	ICustomDestinationList *pICDL = GetI(self);
	if ( pICDL == NULL )
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pICDL->AbortList( );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pICDL, IID_ICustomDestinationList );
	Py_INCREF(Py_None);
	return Py_None;
}

// @object PyICustomDestinationList|Interface used to customize an application's jump list
// @comm Requires Windows 7 or later
static struct PyMethodDef PyICustomDestinationList_methods[] =
{
	{ "SetAppID", PyICustomDestinationList::SetAppID, 1 }, // @pymeth SetAppID|Specifies the taskbar identifier for the jump list
	{ "BeginList", PyICustomDestinationList::BeginList, 1 }, // @pymeth BeginList|Clears the jump list and prepares it to be repopulated
	{ "AppendCategory", PyICustomDestinationList::AppendCategory, 1 }, // @pymeth AppendCategory|Adds a custom category to the jump list
	{ "AppendKnownCategory", PyICustomDestinationList::AppendKnownCategory, 1 }, // @pymeth AppendKnownCategory|Adds one of the predefined categories to the custom list
	{ "AddUserTasks", PyICustomDestinationList::AddUserTasks, 1 }, // @pymeth AddUserTasks|Sets the entries shown in the Tasks category
	{ "CommitList", PyICustomDestinationList::CommitList, METH_NOARGS }, // @pymeth CommitList|Finalizes changes
	{ "GetRemovedDestinations", PyICustomDestinationList::GetRemovedDestinations, 1 }, // @pymeth GetRemovedDestinations|Returns all the items removed from the jump list
	{ "DeleteList", PyICustomDestinationList::DeleteList, 1 }, // @pymeth DeleteList|Removes any customization, leaving only the system-maintained Recent and Frequent lists
	{ "AbortList", PyICustomDestinationList::AbortList, METH_NOARGS }, // @pymeth AbortList|Discards all changes
	{ NULL }
};

PyComTypeObject PyICustomDestinationList::type("PyICustomDestinationList",
		&PyIUnknown::type,
		sizeof(PyICustomDestinationList),
		PyICustomDestinationList_methods,
		GET_PYCOM_CTOR(PyICustomDestinationList));

#endif // WINVER
