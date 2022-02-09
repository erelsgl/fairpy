import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
print(f"\nHERE = {HERE.absolute()}\n")
README = (HERE / "README.md").read_text()
REQUIRES = (HERE / "requirements.txt").read_text().strip().split("\n")
REQUIRES = [lin.strip() for lin in REQUIRES]
print(f"\nREQUIRES = {REQUIRES}\n")


setuptools.setup(
    name="fairpy",
    # version is taken from setup.cfg, which takes it from fairpy.__init__.py
    packages=setuptools.find_packages(),
    install_requires=REQUIRES,
    author="Erel Segal-Halevi",
    author_email="erelsgl@gmail.com",
    description="Fair division algorithms in Python",
    keywords="fair division algorithms",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/erelsgl/fairpy",
    project_urls={
        "Documentation": "https://github.com/erelsgl/fairpy",
        "Bug Reports": "https://github.com/erelsgl/fairpy/issues",
        "Source Code": "https://github.com/erelsgl/fairpy",
    },
    python_requires=">=3.8",
    include_package_data=True,
    classifiers=[
        # see https://pypi.org/classifiers/
        "Development Status :: 3 - Alpha",
    ],
)

# Build:
#   Delete old folders: build, dist, *.egg_info, .venv_test.
#   Then run:
#        build
#   Or (old version):
#        python setup.py sdist bdist_wheel


# Publish to test PyPI:
#   twine upload --repository testpypi dist/*

# Publish to real PyPI:
#   twine upload --repository pypi dist/*
