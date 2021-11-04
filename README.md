# fairpy

![Tox result](https://github.com/erelsgl/fairpy/workflows/tox/badge.svg)

An open-source library of [fair division algorithms](https://en.wikipedia.org/wiki/Fair_division) in Python.
To install:
    
    clone https://github.com/erelsgl/fairpy.git
    cd fairpy
    pip install -e .

Then add the parent of the cloned folder to the `PYTHONPATH` environment variable.
    
To test the installation, run the [demo program for item allocation](demo.py):

    python3 demo.py

Or the [demo program for cake-cutting](demo_cake.py):

    python3 demo_cake.py

For each algorithm in file `x.py` there is also a demo program `x_demo.py`. For example, try:

    python3 items/round_robin_demo.py
    python3 cake/last_diminisher_demo.py

For a partial list of algorithms and their implementation status, see the subfolders:

* [Cake-cutting algorithms](cake/README.md)  
* [Item allocation algorithms (divisible and indivisible)](items/README.md)


