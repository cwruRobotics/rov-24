"""setup.py for the example module."""

from setuptools import setup

PACKAGE_NAME = 'example'

setup(
    name=PACKAGE_NAME,
    version='1.1.0',
    packages=[PACKAGE_NAME],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + PACKAGE_NAME]),
        ('share/' + PACKAGE_NAME, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='TODO',
    maintainer_email='TODO@case.edu',
    description='TODO',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={},
)
