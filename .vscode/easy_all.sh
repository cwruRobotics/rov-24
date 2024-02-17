#!/bin/bash

# Done to suppress setup.py install deprecated warnings
# Can be removed once ROS redoes their python build system
PYTHONWARNINGS=ignore:::setuptools.command.install,ignore:::setuptools.command.easy_install,ignore:::pkg_resources
export PYTHONWARNINGS

# Install any missing dependencies
source "$(pwd)/.vscode/install_dependencies.sh"

colcon build --symlink-install
# shellcheck source=/dev/null
source install/setup.bash
