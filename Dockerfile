FROM osrf/ros:humble-desktop-full

RUN . /opt/ros/humble/setup.sh \
    && rosdep update

RUN sudo apt-get update -y

# Install missing libxcb-cursor0 xvfb for PyQt unit testing
# https://pytest-qt.readthedocs.io/en/latest/troubleshooting.html
RUN sudo apt-get install libxcb-cursor0 xvfb -y

# Install pip
RUN sudo apt-get install python3-pip -y

# Install Video for Linux
RUN sudo apt-get install v4l-utils -y

# Install lsusb
RUN sudo apt-get install usbutils -y

# Install nano
RUN sudo apt-get install nano -y

RUN sudo apt-get update -y
RUN sudo apt-get upgrade -y

# TODO for future nerd doing this via ENTRYPOINT would be better but, I could not get ENTRYPOINT to play with VsCODE.
RUN echo "source /root/rov-24/install/setup.bash" >> ~/.bashrc ;
RUN echo "$export PYTHONWARNINGS=ignore:::setuptools.command.install,ignore:::setuptools.command.easy_install,ignore:::pkg_resources" >> ~/.bashrc ;

WORKDIR /root/rov-24

COPY . .

# Installs ROS dependencies
RUN . /opt/ros/humble/setup.sh \
    && rosdep install --from-paths src --ignore-src -r -y

# Crazy one liner for install python dependencies
RUN for d in src/pi/*/ src/surface/*/; do sudo pip install -e "$d"; done

RUN . /opt/ros/humble/setup.sh \
    && PYTHONWARNINGS=ignore:::setuptools.command.install,ignore:::setuptools.command.easy_install,ignore:::pkg_resources; export PYTHONWARNINGS\
    && colcon build --symlink-install

# Remove identity file generated by action/checkout
# Start by finding all files ending in config
# Then removes file paths without "git"
# Then removes the 'sshCommand line from each file'
RUN  find . -name "*config" | grep git | while read -r line; do sed -i '/sshCommand/d' $line; done