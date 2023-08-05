// This file declares the IDocHostUIHandler Interface and Gateway for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

class PyIDocHostUIHandler : public PyIUnknown
{
public:
	MAKE_PYCOM_CTOR(PyIDocHostUIHandler);
	static IDocHostUIHandler *GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
	static PyObject *ShowContextMenu(PyObject *self, PyObject *args);
	static PyObject *GetHostInfo(PyObject *self, PyObject *args);
	static PyObject *ShowUI(PyObject *self, PyObject *args);
	static PyObject *HideUI(PyObject *self, PyObject *args);
	static PyObject *UpdateUI(PyObject *self, PyObject *args);
	static PyObject *EnableModeless(PyObject *self, PyObject *args);
	static PyObject *OnDocWindowActivate(PyObject *self, PyObject *args);
	static PyObject *OnFrameWindowActivate(PyObject *self, PyObject *args);
	static PyObject *ResizeBorder(PyObject *self, PyObject *args);
	static PyObject *TranslateAccelerator(PyObject *self, PyObject *args);
	static PyObject *GetOptionKeyPath(PyObject *self, PyObject *args);
	static PyObject *GetDropTarget(PyObject *self, PyObject *args);
	static PyObject *GetExternal(PyObject *self, PyObject *args);
	static PyObject *TranslateUrl(PyObject *self, PyObject *args);
	static PyObject *FilterDataObject(PyObject *self, PyObject *args);

protected:
	PyIDocHostUIHandler(IUnknown *pdisp);
	~PyIDocHostUIHandler();
};
// ---------------------------------------------------
//
// Gateway Declaration

class PyGDocHostUIHandler : public PyGatewayBase, public IDocHostUIHandler
{
protected:
	PyGDocHostUIHandler(PyObject *instance) : PyGatewayBase(instance) { ; }
	PYGATEWAY_MAKE_SUPPORT2(PyGDocHostUIHandler, IDocHostUIHandler, IID_IDocHostUIHandler, PyGatewayBase)



	// IDocHostUIHandler
	STDMETHOD(ShowContextMenu)(
		DWORD dwID,
		POINT * ppt,
		IUnknown * pcmdtReserved,
		IDispatch * pdispReserved);

	STDMETHOD(GetHostInfo)(
		DOCHOSTUIINFO * pInfo);

	STDMETHOD(ShowUI)(
		DWORD dwID,
		IOleInPlaceActiveObject * pActiveObject,
		IOleCommandTarget * pCommandTarget,
		IOleInPlaceFrame * pFrame,
		IOleInPlaceUIWindow * pDoc);

	STDMETHOD(HideUI)(
		void);

	STDMETHOD(UpdateUI)(
		void);

	STDMETHOD(EnableModeless)(
		BOOL fEnable);

	STDMETHOD(OnDocWindowActivate)(
		BOOL fActivate);

	STDMETHOD(OnFrameWindowActivate)(
		BOOL fActivate);

	STDMETHOD(ResizeBorder)(
		LPCRECT prcBorder,
		IOleInPlaceUIWindow * pUIWindow,
		BOOL fRameWindow);

	STDMETHOD(TranslateAccelerator)(
		LPMSG lpMsg,
		const GUID * pguidCmdGroup,
		DWORD nCmdID);

	STDMETHOD(GetOptionKeyPath)(
		LPOLESTR * pchKey,
		DWORD dw);

	STDMETHOD(GetDropTarget)(
		IDropTarget * pDropTarget,
		IDropTarget ** ppDropTarget);

	STDMETHOD(GetExternal)(
		IDispatch ** ppDispatch);

	STDMETHOD(TranslateUrl)(
		DWORD dwTranslate,
		OLECHAR * pchURLIn,
		OLECHAR ** ppchURLOut);

	STDMETHOD(FilterDataObject)(
		IDataObject * pDO,
		IDataObject ** ppDORet);

};