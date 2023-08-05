// This file declares the IDebugExpressionCallBack Interface and Gateway for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyIDebugExpressionCallBack : public PyIUnknown
{
public:
	MAKE_PYCOM_CTOR_ERRORINFO(PyIDebugExpressionCallBack, IID_IDebugExpressionCallBack);
	static IDebugExpressionCallBack *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
	static PyObject *onComplete(PyObject *self, PyObject *args);

protected:
	PyIDebugExpressionCallBack(IUnknown *pdisp);
	~PyIDebugExpressionCallBack();
};
// ---------------------------------------------------
//
// Gateway Declaration

class PyGDebugExpressionCallBack : public PyGatewayBase, public IDebugExpressionCallBack
{
protected:
	PyGDebugExpressionCallBack(PyObject *instance) : PyGatewayBase(instance) { ; }
	PYGATEWAY_MAKE_SUPPORT(PyGDebugExpressionCallBack, IDebugExpressionCallBack, IID_IDebugExpressionCallBack)

	// IDebugExpressionCallBack
	STDMETHOD(onComplete)(
		void);

};
