// This file declares the IDebugDocumentProvider Interface and Gateway for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyIDebugDocumentProvider : public PyIDebugDocumentInfo
{
public:
	MAKE_PYCOM_CTOR_ERRORINFO(PyIDebugDocumentProvider, IID_IDebugDocumentProvider);
	static IDebugDocumentProvider *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
	static PyObject *GetDocument(PyObject *self, PyObject *args);

protected:
	PyIDebugDocumentProvider(IUnknown *pdisp);
	~PyIDebugDocumentProvider();
};
// ---------------------------------------------------
//
// Gateway Declaration

class PyGDebugDocumentProvider : public PyGDebugDocumentInfo, public IDebugDocumentProvider
{
protected:
	PyGDebugDocumentProvider(PyObject *instance) : PyGDebugDocumentInfo(instance) { ; }
	PYGATEWAY_MAKE_SUPPORT2(PyGDebugDocumentProvider, IDebugDocumentProvider, IID_IDebugDocumentProvider, PyGDebugDocumentInfo)

	// IDebugDocumentInfo
	STDMETHOD(GetName)(  
		DOCUMENTNAMETYPE dnt,  
		BSTR *pbstrName);  
	STDMETHOD(GetDocumentClassId)(
		CLSID *pclsidDocument);

	// IDebugDocumentProvider
	STDMETHOD(GetDocument)(
		IDebugDocument __RPC_FAR *__RPC_FAR * ppssd);

};
