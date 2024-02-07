#!/bin/bash

# Update ROS dependencies
. /opt/ros/iron/setup.sh && rosdep update
sudo apt-get update -y

# Installs ROS dependencies
. /opt/ros/iron/setup.sh && rosdep install --from-paths src --ignore-src -r -y

# Deletes ROS build directories
rm -rf build install log

# Crazy one liner for install python dependencies
for d in src/pi/*/ src/surface/*/; do pip install -e "$d"; done
# Delete generated files
rm -rf $(find . | grep .egg-info)

# Install some random package that PyQt requires
sudo apt-get install libxcb-cursor0 -y