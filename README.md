python-shelltools
=================

Stuff for dealing with files (searching, copying, comparing etc) that I wish was built into Python. Still in its infancy, expect a lot of changes before it reaches something that resembles its "final" form.

What Will It Do
-------------------
* Find files
* copy files
* move files
* search for text in files
* get size of directories
* compare directories
* Advanced file copy
   *  pause, resume, survive network glitches, etc.

The idea is to have a way to do searches for specific types of files, and them perform some operation on them, all in a single line of code. At the terminal/command prompt, this can normally be done by typing a few simple commands. In python, this normally translates to importing os, glob, shutil, and possibly other modules, and then many times still needing to define your own custom function.

Some of this functionality exists in other python packages, and where it makes sense, I'd prefer to depend on those packages.

Some existing packages work great, but will not fit into the idea of this project. In those cases, functionality will be rewritten to fit this project.