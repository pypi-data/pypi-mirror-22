# The core of Pywin32

[![build status][2]][3] [![Codacy Badge][8]][9] [![codecov][10]][11]


This is the core of PyWin32. It contains all packages that are purely
Python Extensions (ie. not Executables) and that are possible to compile
with a default installation of MS Build Tools (ie. no MFC). This project
is needed because there are many projects that depend on this core functionality,
but the requirements for compiling executables and MFC has overcomplicated
the Pywin32 source code. The goal is to add this package as a dependency 
of Pywin32 and then have Pywin32 be the extra functionality.

## Directory Structure

Things have been refactored so that everything is much easier to understand.
Each folder is a python package or python extension. If it has a `module.yml` 
it's an extension. If it has an `__init__.py`, then it's a package. Extensions
are allowed to include header files from other extensions if they list the 
module name in the `modules` key of `module.yml`. 

[2]: https://ci.appveyor.com/api/projects/status/github/pywin32/pypiwin32?branch=master&svg=true
[3]: https://ci.appveyor.com/project/pywin32/pypiwin32
[8]: https://api.codacy.com/project/badge/Grade/48214aa9e87d4994a41061b155a94e45
[9]: https://www.codacy.com/app/pywin32/pypiwin32?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pywin32/pypiwin32&amp;utm_campaign=Badge_Grade
[10]: https://codecov.io/gh/pywin32/pypiwin32/branch/master/graph/badge.svg
[11]: https://codecov.io/gh/pywin32/pypiwin32
