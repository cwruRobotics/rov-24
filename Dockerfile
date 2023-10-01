FROM osrf/ros:humble-desktop-full

SHELL ["/bin/bash", "-c"] 

RUN source /opt/ros/humble/setup.sh \
    && rosdep update

RUN sudo apt-get update -y
RUN sudo apt-get install python3-pip -y

RUN echo "source /rov-24/install/setup.bash" >> ~/.bashrc ;
RUN echo "$export PYTHONWARNINGS=ignore:::setuptools.command.install,ignore:::setuptools.command.easy_install,ignore:::pkg_resources" >> ~/.bashrc ;

WORKDIR /rov-24

COPY . .

# Git submodule stuff
RUN git config --global --add url."https://github.com/".insteadOf "git@github.com:"
RUN git submodule update --init
RUN git config --global --add url."git@github.com:".insteadOf "https://github.com/"

# Installs ROS dependencies
RUN source /opt/ros/humble/setup.sh \
    && rosdep install --from-paths src --ignore-src -r -y

# Crazy one liner for install python dependencies
RUN for d in src/pi/*/ src/surface/*/; do pip install -e "$d"; done

RUN source /opt/ros/humble/setup.sh \
    && PYTHONWARNINGS=ignore:::setuptools.command.install,ignore:::setuptools.command.easy_install,ignore:::pkg_resources; export PYTHONWARNINGS\
    && colcon build --symlink-install