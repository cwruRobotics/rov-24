#!/bin/bash

# Done to suppress setup.py install deprecated warnings
# Can be removed once ROS redoes their python build system
PYTHONWARNINGS=ignore:::setuptools.command.install,ignore:::setuptools.command.easy_install,ignore:::pkg_resources
export PYTHONWARNINGS

# Stolen from colcon build command in VsCode
colcon build --symlink-install
# shellcheck source=/dev/null
source install/setup.bash
