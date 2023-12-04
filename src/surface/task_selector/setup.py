"""setup.py for the task_selector module."""
import os
from glob import glob

from setuptools import setup

PACKAGE_NAME = 'task_selector'

setup(
    name=PACKAGE_NAME,
    version='1.0.0',
    packages=[PACKAGE_NAME],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + PACKAGE_NAME]),
        ('share/' + PACKAGE_NAME, ['package.xml']),
        # Include all launch files.
        (os.path.join('share', PACKAGE_NAME, 'launch'),
         glob('launch/*launch.[pxy][yma]*'))
    ],
    install_requires=['setuptools', 'flake8==4.0.1', 'mypy >= 1.7'],
    zip_safe=True,
    maintainer='ericy',
    maintainer_email='ery12@case.edu',
    description='Mate ROV task scheduler and task nodes',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'selector = task_selector.task_selector:main',
            'manual_control_node = task_selector.manual_control_node:main',
            'ex_request_client = task_selector.example_request_client:main',
            'ex_timed_task = task_selector.basic_task_timed_node:main',
            'ex_basic_task = task_selector.basic_task_node:main',
            'ex_morning_task = task_selector.is_morning_node:main',
        ],
    },
)
