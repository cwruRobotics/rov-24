import os
from glob import glob

from setuptools import setup

package_name = 'rov_flir'

setup(
    name=package_name,
    version='1.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include all launch files.
        (os.path.join('share', package_name, 'launch'),
         glob('launch/*launch.[pxy][yma]*')),
        (os.path.join('share', package_name, 'config'),
         glob('config/*'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Michael Carlstrom',
    maintainer_email='rmc170@case.edu',
    description='Boilerplate for calling standard flir launch file.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={},
)
