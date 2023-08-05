// This file declares the IPersistFolder Interface and Gateway for Python.
// Generated by makegw.py
// ---------------------------------------------------
//
// Interface Declaration

// The shlwapi.h included with MSVC6 does not have this interface.
// A default Microsoft SDK does not provide an updated shlwapi.h file
// (even though the SDK on mhammond's machine does!).  Rather than
// try and figure out these header versions, just copy the interface
// definition here.
// #include "shlwapi.h"

// *** - start of shlwapi.h clone
enum {
    ASSOCF_INIT_NOREMAPCLSID           = 0x00000001,  //  do not remap clsids to progids
    ASSOCF_INIT_BYEXENAME              = 0x00000002,  //  executable is being passed in
    ASSOCF_OPEN_BYEXENAME              = 0x00000002,  //  executable is being passed in
    ASSOCF_INIT_DEFAULTTOSTAR          = 0x00000004,  //  treat "*" as the BaseClass
    ASSOCF_INIT_DEFAULTTOFOLDER        = 0x00000008,  //  treat "Folder" as the BaseClass
    ASSOCF_NOUSERSETTINGS              = 0x00000010,  //  dont use HKCU
    ASSOCF_NOTRUNCATE                  = 0x00000020,  //  dont truncate the return string
    ASSOCF_VERIFY                      = 0x00000040,  //  verify data is accurate (DISK HITS)
    ASSOCF_REMAPRUNDLL                 = 0x00000080,  //  actually gets info about rundlls target if applicable
    ASSOCF_NOFIXUPS                    = 0x00000100,  //  attempt to fix errors if found
    ASSOCF_IGNOREBASECLASS             = 0x00000200,  //  dont recurse into the baseclass
};
typedef DWORD ASSOCF;
#define LWSTDAPI          STDAPI
typedef enum {} ASSOCSTR;
typedef enum {} ASSOCKEY;
typedef enum {} ASSOCDATA;
typedef enum {} ASSOCENUM;
#undef INTERFACE
#define INTERFACE IQueryAssociations

DECLARE_INTERFACE_( IQueryAssociations, IUnknown )
{
    // IUnknown methods
    STDMETHOD (QueryInterface)(THIS_ REFIID riid, void **ppv) PURE;
    STDMETHOD_(ULONG, AddRef) ( THIS ) PURE;
    STDMETHOD_(ULONG, Release) ( THIS ) PURE;

    // IQueryAssociations methods
    STDMETHOD (Init)(THIS_ ASSOCF flags, LPCWSTR pszAssoc, HKEY hkProgid, HWND hwnd) PURE;
    STDMETHOD (GetString)(THIS_ ASSOCF flags, ASSOCSTR str, LPCWSTR pszExtra, LPWSTR pszOut, DWORD *pcchOut) PURE;
    STDMETHOD (GetKey)(THIS_ ASSOCF flags, ASSOCKEY key, LPCWSTR pszExtra, HKEY *phkeyOut) PURE;
    STDMETHOD (GetData)(THIS_ ASSOCF flags, ASSOCDATA data, LPCWSTR pszExtra, LPVOID pvOut, DWORD *pcbOut) PURE;
    STDMETHOD (GetEnum)(THIS_ ASSOCF flags, ASSOCENUM assocenum, LPCWSTR pszExtra, REFIID riid, LPVOID *ppvOut) PURE;
};

LWSTDAPI AssocCreate(CLSID clsid, REFIID riid, LPVOID *ppv);
// *** - end of shlwapi.h clone

class PyIQueryAssociations : public PyIUnknown
{
public:
	MAKE_PYCOM_CTOR(PyIQueryAssociations);
	static IQueryAssociations* GetI(PyObject *self);
	static PyComTypeObject type;

	// The Python methods
	static PyObject *Init(PyObject *self, PyObject *args);
	static PyObject *GetKey(PyObject *self, PyObject *args);
	static PyObject *GetString(PyObject *self, PyObject *args);

protected:
	PyIQueryAssociations(IUnknown *pdisp);
	~PyIQueryAssociations();
};
