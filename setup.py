"""Setup script for realpython-reader"""

import pathlib
from setuptools import setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

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
        "Programming Language :: Python :: 3.7",
    ],
    packages=["markplates"],
    include_package_data=False,
    install_requires=[
        "click", "jinja2", "pytest",
    ],
    entry_points={"console_scripts": ["markplates=markplates.__main__:main"]},
)
