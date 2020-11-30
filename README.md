# fairpy

An open-source library of [fair division algorithms](https://en.wikipedia.org/wiki/Fair_division) in Python.
To install, clone the repository and run the following in the main folder:

    python3 setup.py install
    
To test the installation, run:

    python3 demo.py
 
For each algorithm in file `x.py` there is a demo program `x_demo.py`. For example, try:

    python3 cake/cut_and_choose_demo.py
    python3 cake/last_diminisher_demo.py
    
For a complete list of algorithms and their implementation status, see the subfolders:

* [Cake-cutting algorithms](cake/README.md)  
* [Indivisible object allocation algorithms](indivisible/README.md) - in construction

     
![Tox result](https://github.com/erelsgl/fairpy/workflows/tox/badge.svg)

