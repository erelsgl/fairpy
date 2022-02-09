"""
A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""


from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path
import warnings

here = path.abspath(path.dirname(__file__))
readme_path = path.join(here, "README.md")
requirements_path = path.join(here, "requirements.txt")

# Get the long description from the README file
with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

# Get the list of requirements from requirements.txt
try:
    with open(requirements_path, encoding="utf-8") as f:
        requirements = f.read().splitlines()
        requirements = [r for r in requirements if "git+" not in r]
except FileNotFoundError as err:
    warnings.warn(f"Requirements file {requirements_path} not found: {err}")
    # NOTE: The above code fails in GitHub actions:
    #   File "/tmp/pip-req-build-kwpxjwjf/setup.py", line 20, in <module>
    #     with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    #   File "/usr/lib/python3.6/codecs.py", line 897, in open
    #     file = builtins.open(filename, mode, buffering)
    # FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pip-req-build-kwpxjwjf/requirements.txt'
    requirements = [
        "numpy>=1.21.3",
        "cvxpy>=1.1.17",
        "scipy>=1.6.1",
        "networkx",
        "matplotlib",
    ]  # use default requirements


setup(
    name="fairpy",  # Required. Enables intallation with "pip install fairpy".
    version="1.0",  # Required
    description="Fair division algorithms in Python",  # Required. One line summary.
    long_description=long_description,  # Optional
    url="https://github.com/erelsgl/fairpy",  # Optional
    keywords="fair division algorithms",  # Optional
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # packages=['anytime'],  # Required
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    # py_modules=["agents","allocations","cut_and_choose","last_diminisher","partition_simplex"],
    packages=find_packages(),
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    python_requires=">=3.8",
    install_requires=requirements,  # Optional
    setup_requires=requirements,  # Optional
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={  # Optional
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
