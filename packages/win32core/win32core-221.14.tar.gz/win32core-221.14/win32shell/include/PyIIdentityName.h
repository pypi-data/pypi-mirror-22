// This file declares the IIdentityName Interface and Gateway for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyIIdentityName : public PyIRelatedItem
{
public:
	MAKE_PYCOM_CTOR(PyIIdentityName);
	static IIdentityName *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods

protected:
	PyIIdentityName(IUnknown *pdisp);
	~PyIIdentityName();
};
// ---------------------------------------------------
//
// Gateway Declaration

class PyGIdentityName : public PyGRelatedItem, public IIdentityName
{
protected:
	PyGIdentityName(PyObject *instance) : PyGRelatedItem(instance) { ; }
	PYGATEWAY_MAKE_SUPPORT2(PyGIdentityName, IIdentityName, IID_IIdentityName, PyGRelatedItem)

	// Only has IRelatedItem methods
	STDMETHOD(GetItemIDList)(PIDLIST_ABSOLUTE * ppidl)
		{return PyGRelatedItem::GetItemIDList(ppidl);}

	STDMETHOD(GetItem)(IShellItem ** ppsi)
		{return PyGRelatedItem::GetItem(ppsi);}
};
