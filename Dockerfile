#checkov:skip=CKV_DOCKER_3: being able to install things is good for testing
FROM osrf/ros:iron-desktop-full

# Specify no Healthcheck needed.
HEALTHCHECK NONE

# Install pip
# Install Video for Linux
# Install lsusb
# Install nano
RUN apt-get update -y \
 && apt-get install --no-install-recommends -y \
 python3-pip=22.0.2+dfsg-1ubuntu0.4 \
 v4l-utils=1.22.1-2build1 \
 usbutils=1:014-1build1 \
 nano=6.2-1 \
 && apt-get upgrade -y \
#  Clean for better performance
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Set Shell for calling shell scripts.
SHELL ["/bin/bash", "-c"]

# Done to suppress setup.py warnings
RUN echo "export PYTHONWARNINGS=ignore:::setuptools.command.install,ignore:::setuptools.command.easy_install,ignore:::pkg_resources" >> ~/.bashrc ;

WORKDIR /root/rov-24

COPY . .

# TODO for future nerd to do this via ENTRYPOINT which be better but, I could not get ENTRYPOINT to play with VsCODE.
# shellcheck source=/dev/null
RUN source /root/rov-24/.vscode/rov_setup.sh \
# Installs ROS and python dependencies
# shellcheck source=/dev/null
 && source /root/rov-24/.vscode/install_dependencies.sh \
# Builds package
# shellcheck source=/dev/null
 && source /opt/ros/iron/setup.bash \
 && PYTHONWARNINGS=ignore:::setuptools.command.install,ignore:::setuptools.command.easy_install,ignore:::pkg_resources; export PYTHONWARNINGS\
 && colcon build --symlink-install

# https://github.com/hadolint/hadolint/wiki/DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# Remove identity file generated by action/checkout
# Start by finding all files ending in config
# Then removes file paths without "git"
# Then removes the 'sshCommand' line from each file
RUN  find . -name "*config" | grep git | while read -r line; do sed -i "/sshCommand/d" "$line"; done
