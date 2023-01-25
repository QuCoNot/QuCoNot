# Copyright 2022 Adam Glos

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages, setup

VERSION = "0.01"
DESCRIPTION = "QuCoNot is a Python library for all your MCT needs."

requirements = [
    "numpy",
    "qiskit",
]

info = {
    "name": "QuCoNot",
    "version": VERSION,
    "author": "Shraddha Aangiras, Adam Glos, Ankit Khandelwal, Handy Kurniawan, Özlem Salehi",
    "author_email": "adamglos92@gmail.com",
    "url": "https://github.com/QuCoNot/QuCoNot",
    "license": "Apache License 2.0",
    "packages": find_packages(where="."),
    "description": DESCRIPTION,
    "long_description": open("README.md").read(),
    "long_description_content_type": "text/markdown",
    "install_requires": requirements,
    "include_package_data": True,
    "project_urls": {
        "Bug Reports": "https://github.com/QuCoNot/QuCoNot/issues",
        "Source": "https://github.com/QuCoNot/QuCoNot/",
    },
}

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: POSIX",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Scientific/Engineering :: Physics",
]

setup(classifiers=classifiers, **(info))
