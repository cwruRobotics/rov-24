# gui

## Overview

This package is for all the code related go the driver station gui. The gui is comprised of our custom widgets found in the gui/widgets folder. For connecting our gui with the rest of the ROS network we have implemented nodes which communicate between pyqt and ROS found in gui/event_nodes. Lastly we have the app.py which is the a custom super class which inherits from ROS Node and PyQT QWidget. Then operator_app.py and pilot_app.py inherit from App to make each custom gui.

## Installation

```bash
pip install pyqt6 pyqtdarktheme opencv-python opencv-python-headless
```

## Usage

Run the operator gui with

```bash
ros2 launch gui operator_launch.py
```

Run the pilot gui with

```bash
ros2 launch gui pilot_launch.py
```

## Launch files

* **operator_launch.py:** Launches the operator gui, ex. `ros2 launch gui operator_launch.py theme:=watermelon`

  * **`theme`** : Theme used by the gui; options are `dark`, `light`, `watermelon`. Default: `dark`.

* **pilot_launch.py:** Launches the pilot gui, ex. `ros2 launch gui pilot_launch.py theme:=watermelon gui:=debug`

  * **`theme`** : Theme used by the gui; options are `dark`, `light`, `watermelon`. Default: `dark`.

  * **`gui`** : Whether to use vertical or debug gui; options are `pilot`, `debug`. Default: `pilot`.

## Event Nodes

### GUIEventClient

Multithreaded client for sending service requests from the GUI.

### GUIEventPublisher

Publisher for sending messages from the GUI.

### GUIEventServer

Multithreaded server for processing server requests to update GUI.

### GUIEventSubscriber

Multithreaded subscriber for receiving messages to the GUI.

## Widgets

### Arm

Has two buttons for arming and disarming the pixhawk.

#### Services

* **`/mavros/cmd/arming`** ([mavros_msgs/srv/CommandBool])

    Sends a request to arm or disarm the pixhawk. Receives a confirmation about the success of the arm or disarm.

### Flood Warnng

Shows whether the robot is flooding or not on the GUI

#### Subscribed Topics

* **`/tether/flooding`** ([rov_msgs/msg/Flooding])

    A custom message for whether the robot is actively flooding

### Logger

Reads ROS logging information and displays it on the gui.

#### Subscribed Topics

* **`/rosout`** ([rcl_interfaces/msg/Log])

    The standard /rosout for communication information to the user.

### Seagrass

Has a surface seagrass grid and pool seagrass grid. In between is the video feed from the bottom of the rov.

#### Subscribed Topics

* **`/bottom_cam/image_raw`** ([sensor_msgs/msg/Image])

    The video feed from the bottom of the robot.

### Timer

A simple start and stop timer that counts down from 15 minutes.

### Video Widget

A widget to display video. There are two subclasses of the video widget: `PauseableVideoWidget` adds pausing the video stream and `SwitchableVideoWidget` enables toggling between video feeds.

#### Subscribed Topics

* **`/front_cam/image_raw`** ([sensor_msgs/msg/Image])

    The video feed from the front of the robot.

* **`/bottom_cam/image_raw`** ([sensor_msgs/msg/Image])

    The video feed from the bottom of the robot.

* **`/camera/color/image_raw`** ([sensor_msgs/msg/Image])

    The video feed from the intel realsense.

[rov_msgs/msg/Flooding]: ../../rov_msgs/msg/Flooding.msg
[mavros_msgs/srv/CommandBool]: https://github.com/mavlink/mavros/blob/ros2/mavros_msgs/srv/CommandBool.srv
[rcl_interfaces/msg/Log]: https://github.com/ros2/rcl_interfaces/blob/rolling/rcl_interfaces/msg/Log.msg
[sensor_msgs/msg/Image]: <http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Image.html>
