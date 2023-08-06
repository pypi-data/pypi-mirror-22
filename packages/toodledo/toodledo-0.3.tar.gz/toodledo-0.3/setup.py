#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.rst") as f:
	long_description = f.read()

setup(name="toodledo",
	version="0.3",
	description="Python wrapper for the Toodledo v3 API which is documented at http://api.toodledo.com/3/",
	long_description=long_description,
	author="Rehan Khwaja",
	author_email="rehan@khwaja.name",
	url="https://github.com/rkhwaja/toodledo-python",
	packages=find_packages(),
	install_requires=["marshmallow", "requests", "requests_oauthlib"],
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3.5"
	],
	keywords="",
)
