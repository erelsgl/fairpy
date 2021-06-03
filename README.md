# fairpy

An open-source library of [fair division algorithms](https://en.wikipedia.org/wiki/Fair_division) in Python.
To install, clone the repository and run the following in the main folder:

    python3 setup.py install

Then add the cloned folder to the `PYTHONPATH` environment variable.
    
To test the installation, run

    python3 demo.py
    python3 demo_cake.py

or open the [demo notebook](demo.ipynb).

For each algorithm in file `x.py` there is a demo program `x_demo.py`. For example, try:

    python3 items/round_robin_demo.py
    python3 cake/last_diminisher_demo.py
    
For a partial list of algorithms and their implementation status, see the subfolders:

* [Cake-cutting algorithms](cake/README.md)  
* [Item allocation algorithms (divisible and indivisible)](items/README.md)

     
![Tox result](https://github.com/erelsgl/fairpy/workflows/tox/badge.svg)

