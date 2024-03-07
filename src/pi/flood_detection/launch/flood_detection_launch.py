from launch.launch_description import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """
    Generate LaunchDescription for flood_detector.

    Returns
    -------
    LaunchDescription
        Launches Flood Detection Node

    """
    # USB 3.0 front (fisheye)
    flood_detection: Node = Node(
        package='flood_detection',
        executable='flood_detector',
        emulate_tty=True,
        output='screen',
        remappings=[('/pi/ip_address', '/tether/ip_address')]
    )

    return LaunchDescription([
        flood_detection
    ])
