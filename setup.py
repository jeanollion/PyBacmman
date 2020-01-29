import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybacmman",
    version="0.0.1",
    author="Jean Ollion",
    author_email="jean.ollion@polytechnique.org",
    description="Utilities for analysis of data generated from bacmman software",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/jeanollion/PyBacmman",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=['py4j', 'pandas']
)
