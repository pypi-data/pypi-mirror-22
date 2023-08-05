// This file automatically generates the SWIG library documentation
%doconly
%style latex_section="\\newpage \\section{:}"
%title "SWIG Library Reference",pre,sort,chop_left = 0,noinfo
/*
Version 1.1 
June, 1997

Copyright (C) 1996
Dave Beazley

(This file was automatically generated by SWIG)
*/
%style html_contents="<hr><h2>:</h2>"
%module swig_lib

%section " Introduction"
%text %{
This file describes all of the functions in the generic SWIG library.
The SWIG library is a collection of generally useful functions that
can be used to supplement an interface file.  These include functions
to manipulate arrays, functions from the C library, and interesting
modules.

This document is automatically generated by SWIG from the file 
"swig_lib/autodoc.i".   Some modules may supply additional documentation
for a particular target language.  To recreate the documentation for
a particular target language, simply run SWIG on the file 'autodoc.i'
with the appropriate target language option.
%}

#if defined(SWIGTCL)
%text %{
This document has been generated for Tcl.
%}
#elif defined(SWIGPERL)
%text %{
This document has been generated for Perl.
%}
#elif defined(SWIGPYTHON)
%text %{
This document has been generated for Python.
%}
#endif

%subsection "Call for contributions"
%text %{
My long-term goal is for the SWIG library to be a collection of useful
modules that can be used to quickly put together interesting programs.
To contribute new modules send e-mail to beazley@cs.utah.edu and I
will include them here.
%}

#define AUTODOC

%include array.i
%include math.i
%include timers.i
%include malloc.i
%include ctype.i
%include memory.i
%include exception.i
%include pointer.i
%include constraints.i
%include typemaps.i

#ifdef SWIGTCL
%section "Tcl Library Files",nosort
%text %{
The following library modules are available when using the Tcl
language module.
%}
%include "tcl/tclsh.i"
%include "tcl/wish.i"
%include "tcl/expect.i"
%include "tcl/expectk.i"
%include "tcl/blt.i"
%include "tcl/tix.i"
%include "tcl/ish.i"
%include "tcl/itclsh.i"
%include "tcl/iwish.i"
%include "tcl/itkwish.i"
#endif

#ifdef SWIGPYTHON
%section "Python Library Files",nosort
%text %{
The following modules are available when using the Python language
module.
%}
%include "python/embed.i"
%include "python/embed13.i"

#endif

#ifdef SWIGPERL
%section "Perl Library Files",nosort

%text %{
The following modules are available when using the Perl5 language
module.
%}

%include "perl5/perlmain.i"
#endif


