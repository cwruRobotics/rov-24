"""setup.py for the utilities module."""
import os
from glob import glob

from setuptools import setup

PACKAGE_NAME = 'utilities'

print(glob('example/*'))

setup(
    name=PACKAGE_NAME,
    version='1.1.0',
    packages=[PACKAGE_NAME],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + PACKAGE_NAME]),
        ('share/' + PACKAGE_NAME, ['package.xml']),
        # Include all files.
        (os.path.join('share', PACKAGE_NAME, 'example'),
         glob('example/*', recursive=True))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Michael Carlstrom',
    maintainer_email='rmc170@case.edu',
    description='Various utilities',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['generate_package = utilities.generate_package:main'],
    },
)
