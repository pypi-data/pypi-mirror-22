// This file declares the IInternetProtocolSink Interface and Gateway for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyIInternetProtocolSink : public PyIUnknown
{
public:
	MAKE_PYCOM_CTOR(PyIInternetProtocolSink);
	static IInternetProtocolSink *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
	static PyObject *Switch(PyObject *self, PyObject *args);
	static PyObject *ReportProgress(PyObject *self, PyObject *args);
	static PyObject *ReportData(PyObject *self, PyObject *args);
	static PyObject *ReportResult(PyObject *self, PyObject *args);

protected:
	PyIInternetProtocolSink(IUnknown *pdisp);
	~PyIInternetProtocolSink();
};
// ---------------------------------------------------
//
// Gateway Declaration

class PyGInternetProtocolSink : public PyGatewayBase, public IInternetProtocolSink
{
protected:
	PyGInternetProtocolSink(PyObject *instance) : PyGatewayBase(instance) { ; }
	PYGATEWAY_MAKE_SUPPORT(PyGInternetProtocolSink, IInternetProtocolSink, IID_IInternetProtocolSink)



	// IInternetProtocolSink
	STDMETHOD(Switch)(
		PROTOCOLDATA __RPC_FAR * pProtocolData);

	STDMETHOD(ReportProgress)(
		ULONG ulStatusCode,
		LPCWSTR szStatusText);

	STDMETHOD(ReportData)(
		DWORD grfBSCF,
		ULONG ulProgress,
		ULONG ulProgressMax);

	STDMETHOD(ReportResult)(
		HRESULT hrResult,
		DWORD dwError,
		LPCWSTR szResult);

};
