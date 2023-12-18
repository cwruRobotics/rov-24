"""setup.py for the gui module."""
import os
from glob import glob

from setuptools import setup

PACKAGE_NAME = 'gui'

setup(
    name=PACKAGE_NAME,
    version='1.1.0',
    packages=[PACKAGE_NAME, os.path.join(PACKAGE_NAME, 'widgets'),
              os.path.join(PACKAGE_NAME, 'event_nodes')],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + PACKAGE_NAME]),
        ('share/' + PACKAGE_NAME, ['package.xml']),
        # Include all launch files.
        (os.path.join('share', PACKAGE_NAME, 'launch'),
         glob('launch/*launch.[pxy][yma]*'))
    ],
    install_requires=['setuptools', 'pyqt6', 'pyqtdarktheme', 'opencv-python>=4.8.1',
                      'numpy>=1.26', 'pytest-qt', 'pytest-xvfb', 'flake8==4.0.1', 'mypy>=1.7'],
    zip_safe=True,
    maintainer='Benjamin Poulin',
    maintainer_email='bwp18@case.edu',
    description='MATE ROV GUI and related ROS nodes',
    license='Apache License 2.0',
    tests_require=['pytest', 'pytest-qt', 'pytest-xvfb'],
    entry_points={
        'console_scripts': ['run_pilot = gui.pilot_app:run_gui_pilot',
                            'run_operator = gui.operator_app:run_gui_operator'],
    },
)
