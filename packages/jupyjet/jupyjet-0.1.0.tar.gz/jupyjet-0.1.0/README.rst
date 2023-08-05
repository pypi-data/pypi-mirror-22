Jupyjet
=======

Jupyjet is a IPython notebook extension to facilitate:

-  `Literate programming <https://en.wikipedia.org/wiki/Literate_programming>`__
-  Separate a big notebook into several smaller notebooks / modules.

Practically speaking, for each notebook a python file is dynamically created: ie - it generate
python modules based of notebook content.

**Importante note: Jupyjet works only on unix based system for now.**

Usage
-----

Only 2 magics commands are exposed: ``%jet_init`` and ``%jet``

-  **jet\_init**: save all the content of the current cell and place it at the top of the file. It
   is supposed to contains imports / global variables. *NB: Only one init is allowed and it must be
   the last line of the cell.*

-  **jet** decl1 decl2 ...: save or update the declaration in the file. Classes, function and
   decorators are supported. The file content is updated everytime the magic runs.

Example
-------

**my\_super\_notebook.ipynb**

::

    import numpy as np
    pi = 3.14

    %jet_init

We declare here the header of the file

::

    def circle_perim(r):
        return 2 * pi * r

    def circle_area(r):
        return pi * r**2

    %jet circle_perm circle_area

And save them to the file

::

    print circle_perm(2.)
    print circle_area(2.2)

We can use the function normally but the declaration are also saved into a generated file like this:

**my\_super\_notebook.py**

::

    import numpy as np
    pi = 3.14


    # --- JET INIT END --- #



    def circle_perim(r):
        return 2 * pi * r


    def circle_area(r):
        return pi * r ** 2

So this python generated module can be called from other notebooks. *NB: comments are not saved in
the genrated files.*

Install
-------

Jupyjet is available on pip:

::

    pip install ********

Enable the extension
^^^^^^^^^^^^^^^^^^^^

Here is a small guide to activate the extension.

1. Create a jupyter profile
'''''''''''''''''''''''''''

``$ ipython profile create``

It will generate a default profile file at: ``~/.ipython/profile_default/ipython_config.py``.

2. Register Jupyjet as an extension (and other cool ones like `line-profiler <https://github.com/rkern/line_profiler>`__).
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

To do so add the following lines.

::

    c.TerminalIPythonApp.extensions = [
        'jupyjet',
        'line_profiler',
    ]
    c.InteractiveShellApp.extensions = [
        'jupyjet',
        'line_profiler',
    ]

3. Enjoy =)
'''''''''''

