// This file declares the IPersistStorage gateway for Python.
// Generated by makegw.py

class PyGPersistStorage : public PyGPersist, public IPersistStorage
{
protected:
	PyGPersistStorage(PyObject *instance) : PyGPersist(instance) { ; }
	PYGATEWAY_MAKE_SUPPORT2(PyGPersistStorage, IPersistStorage, IID_IPersistStorage, PyGPersist)

	// IPersist
	STDMETHOD(GetClassID)(CLSID FAR *pClassID) {return PyGPersist::GetClassID(pClassID);}

	// IPersistStorage
	STDMETHOD(IsDirty)(
		void);

	STDMETHOD(InitNew)(
		IStorage __RPC_FAR * pStg);

	STDMETHOD(Load)(
		IStorage __RPC_FAR * pStg);

	STDMETHOD(Save)(
		IStorage __RPC_FAR * pStgSave,
		BOOL fSameAsLoad);

	STDMETHOD(SaveCompleted)(
		IStorage __RPC_FAR * pStgNew);

	STDMETHOD(HandsOffStorage)(
		void);

};
