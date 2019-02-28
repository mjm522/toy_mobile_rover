#! /usr/bin/env python

# Author: Michael J Mathew<mjm522@cs.bham.ac.uk>
# License: BSD 3 clause

from setuptools import setup, find_packages
VERSION = "0.0"

def setup_package():
    setup(
        name="tmr_world",
        version=VERSION,
        author="Michael J Mathew",
        author_email="mjm522@cs.bham.ac.uk",
        url="https://github.com/mjm522/toy_mobile_rover",
        description="Simulated Sensors",
        package_dir={'': 'src'},
        license="new BSD",
        classifiers=[
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Topic :: Software Development",
            "Topic :: Scientific/Engineering",
            "Operating System :: Linux",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.4",
        ],
        packages=find_packages(),
        requires=["numpy", "pygame"],
    )


if __name__ == "__main__":
    setup_package()
