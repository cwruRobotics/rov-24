from launch.actions import GroupAction
from launch.launch_description import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace


def generate_launch_description() -> LaunchDescription:
    keyboard_control_node: Node = Node(
        package='flight_control',
        executable='keyboard_control_node',
        remappings=[('/surface/mavros/rc/override', '/tether/mavros/rc/override')],
        emulate_tty=True,
        output='screen'
    )

    namespace_launch: GroupAction = GroupAction(
        actions=[
            PushRosNamespace("surface"),
            keyboard_control_node
        ]
    )

    return LaunchDescription([
        namespace_launch
    ])
