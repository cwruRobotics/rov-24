import os
from glob import glob

from setuptools import setup

PACKAGE_NAME = 'slam_main'

setup(
    name=PACKAGE_NAME,
    version='1.1.0',
    packages=[PACKAGE_NAME],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + PACKAGE_NAME]),
        ('share/' + PACKAGE_NAME, ['package.xml']),
        # Include all launch files.
        (os.path.join('share', PACKAGE_NAME, 'launch'),
         glob('launch/*launch.[pxy][yma]*'))
    ],
    install_requires=[],
    zip_safe=True,
    maintainer='Noah Mollserstuen',
    maintainer_email='nrm98@case.edu',
    description='Localization and mapping with a realsense depth camera',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={},
)