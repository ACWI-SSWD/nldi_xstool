#!/usr/bin/env python

"""The setup script."""
from os import path
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'requirements.txt')) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [line for line in requirements_file.read().splitlines()
                    if not line.startswith('#')]

# requirements = ['Click>=7.0',
#                 'pygeohydro==0.10.2',
#                 'git+https://github.com/cheginit/py3dep.git',
#                 'git+https://github.com/cheginit/pygeoogc.git',
#                 'git+https://github.com/cheginit/pygeoutils.git',
#                 'pynhd==0.10.1',
#                 'shapely',
#                 'dataretrieval',
#                 'folium',
#                 'lxml',
#                 'xarray',
#                 'scipy',
#                 'dask',
#                 'netcdf4',
#                 'bottleneck',
#                 'geopandas',
#                 'numba']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Richard McDonald",
    author_email='rmcd@usgs.gov',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Tool for extracting cross-sections",
    entry_points={
        'console_scripts': [
            'nldi_xstool=nldi_xstool.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nldi_xstool',
    name='nldi_xstool',
    packages=find_packages(include=['nldi_xstool', 'nldi_xstool.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rmcd-mscb/nldi_xstool',
    version='0.1.0',
    zip_safe=False,
)
