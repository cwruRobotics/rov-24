#!/bin/bash

# Update ROS dependencies
# shellcheck source=/dev/null
. /opt/ros/iron/setup.sh && rosdep update
sudo apt-get update -y

# Installs ROS dependencies
# shellcheck source=/dev/null
. /opt/ros/iron/setup.sh && rosdep install --from-paths src --ignore-src -r -y

# Deletes ROS build directories
rm -rf build install log

# Install python dependencies
pip install .

# Install some random package that PyQt requires
sudo apt-get install libxcb-cursor0 -y

# Install the clean Shell script
curl -sS https://webi.sh/shfmt | sh
