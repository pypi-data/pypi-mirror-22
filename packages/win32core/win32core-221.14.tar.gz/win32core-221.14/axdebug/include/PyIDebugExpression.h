// This file declares the IDebugExpression Interface and Gateway for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyIDebugExpression : public PyIUnknown
{
public:
	MAKE_PYCOM_CTOR_ERRORINFO(PyIDebugExpression, IID_IDebugExpression);
	static IDebugExpression *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
	static PyObject *Start(PyObject *self, PyObject *args);
	static PyObject *Abort(PyObject *self, PyObject *args);
	static PyObject *QueryIsComplete(PyObject *self, PyObject *args);
	static PyObject *GetResultAsString(PyObject *self, PyObject *args);
	static PyObject *GetResultAsDebugProperty(PyObject *self, PyObject *args);

protected:
	PyIDebugExpression(IUnknown *pdisp);
	~PyIDebugExpression();
};
// ---------------------------------------------------
//
// Gateway Declaration

class PyGDebugExpression : public PyGatewayBase, public IDebugExpression
{
protected:
	PyGDebugExpression(PyObject *instance) : PyGatewayBase(instance) { ; }
	PYGATEWAY_MAKE_SUPPORT(PyGDebugExpression, IDebugExpression, IID_IDebugExpression)

	// IDebugExpression
	STDMETHOD(Start)(
		IDebugExpressionCallBack __RPC_FAR * pdecb);

	STDMETHOD(Abort)(
		void);

	STDMETHOD(QueryIsComplete)(
		void);

	STDMETHOD(GetResultAsString)(
		HRESULT __RPC_FAR * phrResult,
		BSTR __RPC_FAR * pbstrResult);

	STDMETHOD(GetResultAsDebugProperty)(
		HRESULT __RPC_FAR * phrResult,
		IDebugProperty __RPC_FAR * __RPC_FAR * pbstrResult);
};
