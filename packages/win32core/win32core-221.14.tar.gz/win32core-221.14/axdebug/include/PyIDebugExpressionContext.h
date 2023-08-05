// This file declares the IDebugExpressionContext Interface and Gateway for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyIDebugExpressionContext : public PyIUnknown
{
public:
	MAKE_PYCOM_CTOR(PyIDebugExpressionContext);
	static IDebugExpressionContext *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
	static PyObject *ParseLanguageText(PyObject *self, PyObject *args);
	static PyObject *GetLanguageInfo(PyObject *self, PyObject *args);

protected:
	PyIDebugExpressionContext(IUnknown *pdisp);
	~PyIDebugExpressionContext();
};
// ---------------------------------------------------
//
// Gateway Declaration

class PyGDebugExpressionContext : public PyGatewayBase, public IDebugExpressionContext
{
protected:
	PyGDebugExpressionContext(PyObject *instance) : PyGatewayBase(instance) { ; }
	PYGATEWAY_MAKE_SUPPORT(PyGDebugExpressionContext, IDebugExpressionContext, IID_IDebugExpressionContext)

	// IDebugExpressionContext
	STDMETHOD(ParseLanguageText)(
		LPCOLESTR pstrCode,
		UINT nRadix,
		LPCOLESTR pstrDelimiter,
		DWORD dwFlags,
		IDebugExpression __RPC_FAR *__RPC_FAR * ppe);

	STDMETHOD(GetLanguageInfo)(
		BSTR __RPC_FAR * pbstrLanguageName,
		GUID __RPC_FAR * pLanguageID);

};