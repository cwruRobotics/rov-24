"""setup.py for the keyboard module."""
import os
from glob import glob

from setuptools import setup

PACKAGE_NAME = "keyboard_driver"

setup(
    name=PACKAGE_NAME,
    version="1.0.0",
    packages=[PACKAGE_NAME],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + PACKAGE_NAME]),
        ("share/" + PACKAGE_NAME, ["package.xml"]),
        (os.path.join("share", PACKAGE_NAME, "launch"), glob("launch/*.py")),
    ],
    install_requires=["setuptools", "pynput"],
    zip_safe=True,
    maintainer="Seongmin Jung",
    maintainer_email="sxj754@case.edu",
    description="MATE ROV keyboard driver",
    license="Apache License 2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "keyboard_driver_node = keyboard_driver.keyboard_driver_node:main",
        ],
    },
)
