"""Setup script for realpython-reader"""

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
NAME = "markplates"

# This call to setup() does all the work
setup(
    name=NAME,
    version="1.5.0",
    description="Inject code snippets into your Markdown docs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jima80525/markplates",
    author="Jim Anderson",
    author_email="jima.coding@gmail.com",
    python_requires=">=3.6.0",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=[NAME],
    include_package_data=False,
    install_requires=[
        "asttokens==2.0.4",
        "Click==7.1.2",
        "Jinja2==2.11.2",
        "pyperclip==1.8.0",
    ],
    entry_points={"console_scripts": ["markplates=markplates.__main__:main"]},
)
