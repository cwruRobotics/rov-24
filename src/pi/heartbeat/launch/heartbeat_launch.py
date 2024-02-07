from launch.launch_description import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    heartbeat_node = Node(
        package="heartbeat",
        executable="heartbeat_node",
        remappings=[("/pi/pi_heartbeat", "/tether/pi_heartbeat")],
        emulate_tty=True,
        output='screen'
    )

    return LaunchDescription([
        heartbeat_node
    ])
