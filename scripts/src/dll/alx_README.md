# ALX intgration

To run our system on ALX system, a wrapper file in C# call the python script.

You can compile this file in *.dll* or in *.exe* with visual studio 15 or later, or with VS15 developer console.

This file need two *.dll* from the IronPython installation of the target computer to run:
- *IronPython.dll*
- *Microsoft.Scripting.dll*

These file can normally be found on the path :
*C:\Program Files (x86)\IronPython 2.7*

Compile the wrapper in *.exe* :
```csc /r:IronPython.dll,Microsoft.Scripting.dll wrapper.cs```

Compile the wrapper in *.dll*

```csc /t:library /r:IronPython.dll,Microsoft.Scripting.dll /out:leica_wrapper.dll wrapper.cs```

Once *wrapper.cs* is compile, in *.dll*, place all the *.dll* file (*IronPython.dll Microsoft.Scripting.dll, leica_wrapper.dll*) in the ALX OS folder corresponding and the python script (*track.py,GeoCom.py*) into the path of the project to be runnable.
