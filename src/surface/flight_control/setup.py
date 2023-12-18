import os
from glob import glob

from setuptools import setup

package_name = 'flight_control'

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
         glob('launch/*launch.[pxy][yma]*'))
    ],
    install_requires=['setuptools', 'flake8==4.0.1', 'mypy>=1.7', 'pynput'],
    zip_safe=True,
    maintainer='benjamin',
    maintainer_email='bwp18@case.edu',
    description='Mate ROV sub movement controllers',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'manual_control_node = flight_control.manual_control_node:main',
            'keyboard_control_node = flight_control.keyboard_control_node:main',
            'auto_docking_node = flight_control.auto_docking_node:main'
        ],
    },
)
