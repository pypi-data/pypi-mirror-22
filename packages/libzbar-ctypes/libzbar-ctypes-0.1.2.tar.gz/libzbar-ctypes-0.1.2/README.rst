libzbar-ctypes
===========

This is libzbar python ctypes bindings, it should support python2 and python3.

I can not find a python3 version zbar library under raspberry pi, so i write this codes for it.
  
It should work under other platform only need replace the libzbar path.  

It only test under Raspbian (raspberry pi) now.


Usage
-----

- Install
    - install libzbar::
    
        sudo apt-get install zbar-tools
    
    - install libzbar_ctypes
        - python3::

            pip install libzbar-ctypes

        - python2::

            pip3 install libzbar-ctypes

- Example (on raspberry pi)  
    - install pillow  
        install Prerequisites packages. see http://pillow.readthedocs.org/en/latest/installation.html  
        download pillow source code (http://python-pillow.github.io/), and compile it.  
    
    - run the example script.

- test
    - test under ubuntu 15.04.
    - test on hardware firefly.
    - test on hardware rasyberry pi.

  
todo
----

Add all libzbar function bindings.

Contact
-------

by jf.  

zaazbb <zaazbb@163.com>
