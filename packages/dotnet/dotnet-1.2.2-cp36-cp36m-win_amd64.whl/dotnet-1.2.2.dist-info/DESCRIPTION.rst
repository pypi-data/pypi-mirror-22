Allows seamless integration of .NET (e.g. C#) code with Python (CPython, Anaconda).

It runs as hybrid native code and CLR code. The CLR instance is created once
you import dotnet module into your Python code. Then you can load assemblies
and import namespaces and types directly into Python code, and use as Python
objects. This all runs within Python process, and no IPC is used to accomplish
this. Boost.Python has been used to write C++ layer, which glues Python and
Managed (.NET/CLR/C#) code.

