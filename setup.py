"""Setup script for realpython-reader"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="markplates",
    version="1.0.0",
    description="Inject code snippets into your Markdown docs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jima80525/markplates",
    author="Jim Anderson",
    author_email="jima.coding@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["markplates"],
    include_package_data=False,
    install_requires=[
        "jinja2", "pytest", 
    ],
    entry_points={"console_scripts": ["markplates=markplates.__main__:main"]},
)
