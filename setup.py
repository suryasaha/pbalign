from setuptools import setup, Extension, find_packages

import os
import sys

setup(
    name = 'pbalign',
    version='0.2.0',
    author='Pacific Biosciences',
    author_email='devnet@pacificbiosciences.com',
    license='LICENSE.txt',
    package_dir={'pbalign':'pbalign'},
    packages = find_packages(),
    zip_safe = False,
    install_requires=[
        'pbcore >= 0.8.5',
        ],
    entry_points={'console_scripts': [
        'pbalign=pbalign.pbalignrunner:main',
        'maskAlignedReads.py = pbalign.tools.mask_aligned_reads:main',
        'loadChemistry.py = pbalign.tools.loadChemistry:main',
        'extractUnmappedSubreads.py = pbalign.tools.extractUnmappedSubreads:main',
        'createChemistryHeader.py = pbalign.tools.createChemistryHeader:main'
        ]}
    )
