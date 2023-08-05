// This file implements the IKnownFolder Interface for Python.
// Generated by makegw.py

#include "shell_pch.h"
#include "PyIKnownFolder.h"

// @doc - This file contains autoduck documentation
// ---------------------------------------------------
//
// Interface Implementation

PyIKnownFolder::PyIKnownFolder(IUnknown *pdisp):
	PyIUnknown(pdisp)
{
	ob_type = &type;
}

PyIKnownFolder::~PyIKnownFolder()
{
}

/* static */ IKnownFolder *PyIKnownFolder::GetI(PyObject *self)
{
	return (IKnownFolder *)PyIUnknown::GetI(self);
}

// @pymethod <o PyIID>|PyIKnownFolder|GetId|Returns the id of the folder
PyObject *PyIKnownFolder::GetId(PyObject *self, PyObject *args)
{
	IKnownFolder *pIKF = GetI(self);
	if ( pIKF == NULL )
		return NULL;
	KNOWNFOLDERID kfid;
	if ( !PyArg_ParseTuple(args, ":GetId"))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIKF->GetId( &kfid );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIKF, IID_IKnownFolder );
	return PyWinObject_FromIID(kfid);
}

// @pymethod int|PyIKnownFolder|GetCategory|Returns the category for a folder (shellcon.KF_CATEGORY_*)
PyObject *PyIKnownFolder::GetCategory(PyObject *self, PyObject *args)
{
	IKnownFolder *pIKF = GetI(self);
	if ( pIKF == NULL )
		return NULL;
	KF_CATEGORY category;
	if ( !PyArg_ParseTuple(args, ":GetCategory"))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIKF->GetCategory(&category );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIKF, IID_IKnownFolder );
	return PyInt_FromLong(category);
}

// @pymethod <o PyIShellItem>|PyIKnownFolder|GetShellItem|Returns a shell interface for the folder
PyObject *PyIKnownFolder::GetShellItem(PyObject *self, PyObject *args)
{
	IKnownFolder *pIKF = GetI(self);
	if ( pIKF == NULL )
		return NULL;
	// @pyparm int|Flags|0|Combination of shellcon.KF_FLAG_* values
	// @pyparm <o PyIID>|riid|IID_IShellItem|The interface to return (IShellItem or IShellItem2)
	DWORD flags = 0;
	IID riid = IID_IShellItem;
	void *ret;
	if ( !PyArg_ParseTuple(args, "|kO&:GetShellItem", &flags, PyWinObject_AsIID, &riid))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIKF->GetShellItem(flags, riid, &ret);
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIKF, IID_IKnownFolder );
	return PyCom_PyObjectFromIUnknown((IUnknown *)ret, riid, FALSE);
}

// @pymethod str|PyIKnownFolder|GetPath|Returns the path to the folder
PyObject *PyIKnownFolder::GetPath(PyObject *self, PyObject *args)
{
	IKnownFolder *pIKF = GetI(self);
	if ( pIKF == NULL )
		return NULL;
	// @pyparm int|Flags|0|Combination of shellcon.KF_FLAG_* flags controlling how the path is returned
	DWORD flags=0;
	WCHAR *path;
	if ( !PyArg_ParseTuple(args, "|k:GetPath", &flags))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIKF->GetPath(flags, &path);
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIKF, IID_IKnownFolder );
	PyObject *ret = PyWinObject_FromWCHAR(path);
	CoTaskMemFree(path);
	return ret;
}

// @pymethod |PyIKnownFolder|SetPath|Changes the location of the folder
PyObject *PyIKnownFolder::SetPath(PyObject *self, PyObject *args)
{
	IKnownFolder *pIKF = GetI(self);
	if ( pIKF == NULL )
		return NULL;
	// @pyparm int|Flags||KF_FLAG_DONT_UNEXPAND, or 0
	// @pyparm str|Path||New path for known folder
	TmpWCHAR Path;
	PyObject *obPath;
	DWORD Flags;
	if ( !PyArg_ParseTuple(args, "kO:SetPath", &Flags, &obPath))
		return NULL;
	if (!PyWinObject_AsWCHAR(obPath, &Path))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIKF->SetPath(Flags, Path);
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIKF, IID_IKnownFolder );
	Py_INCREF(Py_None);
	return Py_None;
}

// @pymethod <o PyIDL>|PyIKnownFolder|GetIDList|Returns the folder's location as an item id list.
PyObject *PyIKnownFolder::GetIDList(PyObject *self, PyObject *args)
{
	IKnownFolder *pIKF = GetI(self);
	if ( pIKF == NULL )
		return NULL;
	// @pyparm int|Flags||Combination of shellcon.KF_FLAG_* values that affect how the operation is performed
	PIDLIST_ABSOLUTE pidl;
	DWORD Flags;
	if ( !PyArg_ParseTuple(args, "k:GetIDList", &Flags))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIKF->GetIDList(Flags, &pidl );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIKF, IID_IKnownFolder );
	return PyObject_FromPIDL(pidl, TRUE);
}

// @pymethod <o PyIID>|PyIKnownFolder|GetFolderType|Returns the type of the folder
// @rdesc Returns a folder type guid (shell.FOLDERTYPEID_*)
PyObject *PyIKnownFolder::GetFolderType(PyObject *self, PyObject *args)
{
	IKnownFolder *pIKF = GetI(self);
	if ( pIKF == NULL )
		return NULL;
	FOLDERTYPEID ftid;
	if ( !PyArg_ParseTuple(args, ":GetFolderType"))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIKF->GetFolderType( &ftid );
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIKF, IID_IKnownFolder );
	return PyWinObject_FromIID(ftid);
}

// @pymethod int|PyIKnownFolder|GetRedirectionCapabilities|Returns flags indicating how the folder can be redirected
// @rdesc Combination of shellcon.KF_REDIRECTION_CAPABILITIES_* flags
PyObject *PyIKnownFolder::GetRedirectionCapabilities(PyObject *self, PyObject *args)
{
	IKnownFolder *pIKF = GetI(self);
	if ( pIKF == NULL )
		return NULL;
	KF_REDIRECTION_CAPABILITIES Capabilities;
	if ( !PyArg_ParseTuple(args, ":GetRedirectionCapabilities"))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIKF->GetRedirectionCapabilities(&Capabilities );
	PY_INTERFACE_POSTCALL;

	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIKF, IID_IKnownFolder );
	return PyInt_FromLong(Capabilities);
}

// @pymethod dict|PyIKnownFolder|GetFolderDefinition|Retrieves detailed information about a known folder
// @rdesc Returns a dict containing info from a KNOWNFOLDER_DEFINITION struct
PyObject *PyIKnownFolder::GetFolderDefinition(PyObject *self, PyObject *args)
{
	IKnownFolder *pIKF = GetI(self);
	if ( pIKF == NULL )
		return NULL;
	KNOWNFOLDER_DEFINITION def;
	if ( !PyArg_ParseTuple(args, ":GetFolderDefinition"))
		return NULL;
	HRESULT hr;
	PY_INTERFACE_PRECALL;
	hr = pIKF->GetFolderDefinition(&def);
	PY_INTERFACE_POSTCALL;
	if ( FAILED(hr) )
		return PyCom_BuildPyException(hr, pIKF, IID_IKnownFolder );
	PyObject *ret = Py_BuildValue("{s:i, s:u, s:u, s:N, s:u, s:u, s:u, s:u, s:u, s:u, s:k, s:i, s:N}",
		"Category", def.category,
		"Name", def.pszName,
		"Description", def.pszDescription,
		"Parent", PyWinObject_FromIID(def.fidParent),
		"RelativePath",  def.pszRelativePath,
		"ParsingName", def.pszParsingName,
		"Tooltip", def.pszTooltip,
		"LocalizedName", def.pszLocalizedName,
		"Icon", def.pszIcon,
		"Security", def.pszSecurity,
		"Attributes", def.dwAttributes,
		"Flags", def.kfdFlags,
		"Type", PyWinObject_FromIID(def.ftidType));
	FreeKnownFolderDefinitionFields(&def);
	return ret;
}

// @object PyIKnownFolder|Interface representing a known folder that serves
// as a replacement for the numeric CSIDL definitions and API functions. 
// Requires Vista or later.
static struct PyMethodDef PyIKnownFolder_methods[] =
{
	{ "GetId", PyIKnownFolder::GetId, 1 }, // @pymeth GetId|Returns the id of the folder
	{ "GetCategory", PyIKnownFolder::GetCategory, 1 }, // @pymeth GetCategory|Returns the category for a folder (shellcon.KF_CATEGORY_*)
	{ "GetShellItem", PyIKnownFolder::GetShellItem, 1 }, // @pymeth GetShellItem|Returns a shell interface for the folder
	{ "GetPath", PyIKnownFolder::GetPath, 1 }, // @pymeth GetPath|Returns the path to the folder
	{ "SetPath", PyIKnownFolder::SetPath, 1 }, // @pymeth SetPath|Changes the location of the folder
	{ "GetIDList", PyIKnownFolder::GetIDList, 1 }, // @pymeth GetIDList|Returns the folder's location as an item id list
	{ "GetFolderType", PyIKnownFolder::GetFolderType, 1 }, // @pymeth GetFolderType|Returns the type of the folder
	{ "GetRedirectionCapabilities", PyIKnownFolder::GetRedirectionCapabilities, 1 }, // @pymeth GetRedirectionCapabilities|Returns flags indicating how the folder can be redirected
	{ "GetFolderDefinition", PyIKnownFolder::GetFolderDefinition, 1 }, // @pymeth GetFolderDefinition|Retrieves detailed information about a known folder
	{ NULL }
};

PyComTypeObject PyIKnownFolder::type("PyIKnownFolder",
		&PyIUnknown::type,
		sizeof(PyIKnownFolder),
		PyIKnownFolder_methods,
		GET_PYCOM_CTOR(PyIKnownFolder));
