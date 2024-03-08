<!-- Template From Here
https://github.com/leggedrobotics/ros_best_practices/blob/main/ros_package_template/README.md
-->

# Package Name

## Overview

This is a template: replace, remove, and add where required. Describe here what this package does and what it's meant for in a few sentences.

## Installation

Describe any dependencies not install by rosdep

## Usage

Describe the quickest way to run this software, for example:

Run the main node with

```bash
ros2 launch ros_package_template ros_package_template_launch.py
```

## Config files

Config file folder/set 1

* **config_file_1.yaml** Shortly explain the content of this config file

## Launch files

* **launch_file_1_launch.py:** shortly explain what is launched (e.g standard simulation, simulation with gdb,...)

  * **`argument_1`** Short description (e.g. as commented in launch file). Default: `default_value`.

## Nodes

### ros_package_template

Reads temperature measurements and computed the average.

#### Subscribed Topics

* **`/temperature`** ([sensor_msgs/Temperature])

    The temperature measurements from which the average is computed.

#### Published Topics

...

#### Services

* **`get_average`** ([std_srvs/Trigger])

    Returns information about the current average.

#### Parameters

* **`subscriber_topic`** (string, default: "/temperature")

    The name of the input topic.

* **`cache_size`** (int, default: 200, min: 0, max: 1000)

    The size of the cache.

### NODE_B_NAME

...

[std_srvs/Trigger]: http://docs.ros.org/api/std_srvs/html/srv/Trigger.html
[sensor_msgs/Temperature]: http://docs.ros.org/api/sensor_msgs/html/msg/Temperature.html
